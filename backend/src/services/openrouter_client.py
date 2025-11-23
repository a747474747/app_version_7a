"""
OpenRouter LLM Client for Four-Engine System Architecture.

This module provides a robust client for interacting with OpenRouter's API,
including error handling, rate limiting, and response parsing.
"""

import asyncio
import json
import logging
import time
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

import httpx
from pydantic import BaseModel, Field, validator

from config.settings import get_settings
# Lazy import to avoid circular dependency
from calculation_engine.schemas.llm_tiers import LLMTier


class OpenRouterError(Exception):
    """Base exception for OpenRouter client errors."""

    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data or {}


class OpenRouterRateLimitError(OpenRouterError):
    """Exception raised when rate limit is exceeded."""
    pass


class OpenRouterAuthError(OpenRouterError):
    """Exception raised when authentication fails."""
    pass


class OpenRouterServerError(OpenRouterError):
    """Exception raised when OpenRouter returns a server error."""
    pass


class OpenRouterClientError(OpenRouterError):
    """Exception raised when client sends invalid request."""
    pass


class MessageRole(str, Enum):
    """OpenAI-style message roles."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(BaseModel):
    """A single message in a chat conversation."""
    role: MessageRole
    content: str

    @validator('content')
    def validate_content(cls, v):
        if not v or not v.strip():
            raise ValueError("Message content cannot be empty")
        return v.strip()


class ChatCompletionRequest(BaseModel):
    """Request model for chat completions."""
    model: str
    messages: List[ChatMessage] = Field(..., min_items=1)
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, gt=0)
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0)
    frequency_penalty: Optional[float] = Field(None, ge=-2.0, le=2.0)
    presence_penalty: Optional[float] = Field(None, ge=-2.0, le=2.0)
    stop: Optional[Union[str, List[str]]] = None
    stream: bool = False


class ChatCompletionChoice(BaseModel):
    """A single completion choice from OpenRouter."""
    index: int
    message: ChatMessage
    finish_reason: Optional[str] = None


class ChatCompletionUsage(BaseModel):
    """Token usage information."""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    """Response model for chat completions."""
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: ChatCompletionUsage


@dataclass
class RateLimitState:
    """Tracks rate limiting state."""
    requests_this_minute: int = 0
    requests_this_hour: int = 0
    minute_reset: float = 0.0
    hour_reset: float = 0.0
    last_request_time: float = 0.0


class OpenRouterClient:
    """
    Client for interacting with OpenRouter API.

    Implements rate limiting, error handling, and response validation.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://openrouter.ai/api/v1",
        timeout: float = 60.0,
        max_retries: int = 3,
        rate_limit_requests_per_minute: int = 50,
        rate_limit_requests_per_hour: int = 1000,
    ):
        """
        Initialize the OpenRouter client.

        Args:
            api_key: OpenRouter API key (defaults to settings)
            base_url: OpenRouter API base URL
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            rate_limit_requests_per_minute: Max requests per minute
            rate_limit_requests_per_hour: Max requests per hour
        """
        settings = get_settings()

        self.api_key = api_key or settings.llm.openrouter_api_key
        if not self.api_key:
            raise ValueError("OpenRouter API key is required")

        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries

        # Rate limiting configuration
        self.rate_limit_per_minute = rate_limit_requests_per_minute
        self.rate_limit_per_hour = rate_limit_requests_per_hour
        self.rate_limit_state = RateLimitState()

        # HTTP client
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        """Async context manager entry."""
        await self._ensure_client()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self._close_client()

    async def _ensure_client(self) -> None:
        """Ensure HTTP client is initialized."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/your-org/four-engine-architecture",
                    "X-Title": "Four-Engine System Architecture",
                }
            )

    async def _close_client(self) -> None:
        """Close HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def _check_rate_limit(self) -> None:
        """
        Check and enforce rate limits.

        Raises:
            OpenRouterRateLimitError: If rate limit is exceeded
        """
        now = time.time()

        # Reset counters if time windows have passed
        if now - self.rate_limit_state.minute_reset >= 60:
            self.rate_limit_state.requests_this_minute = 0
            self.rate_limit_state.minute_reset = now

        if now - self.rate_limit_state.hour_reset >= 3600:
            self.rate_limit_state.requests_this_hour = 0
            self.rate_limit_state.hour_reset = now

        # Check rate limits
        if self.rate_limit_state.requests_this_minute >= self.rate_limit_per_minute:
            raise OpenRouterRateLimitError(
                f"Rate limit exceeded: {self.rate_limit_per_minute} requests per minute",
                response_data={"retry_after": 60 - (now - self.rate_limit_state.minute_reset)}
            )

        if self.rate_limit_state.requests_this_hour >= self.rate_limit_per_hour:
            raise OpenRouterRateLimitError(
                f"Rate limit exceeded: {self.rate_limit_per_hour} requests per hour",
                response_data={"retry_after": 3600 - (now - self.rate_limit_state.hour_reset)}
            )

        # Update counters
        self.rate_limit_state.requests_this_minute += 1
        self.rate_limit_state.requests_this_hour += 1
        self.rate_limit_state.last_request_time = now

    def _handle_error_response(self, response: httpx.Response) -> None:
        """
        Handle error responses from OpenRouter API.

        Args:
            response: HTTP response object

        Raises:
            Appropriate OpenRouterError subclass
        """
        try:
            error_data = response.json()
        except json.JSONDecodeError:
            error_data = {"error": {"message": response.text}}

        error_message = error_data.get("error", {}).get("message", f"HTTP {response.status_code}")

        if response.status_code == 401:
            raise OpenRouterAuthError(f"Authentication failed: {error_message}", response.status_code, error_data)
        elif response.status_code == 429:
            raise OpenRouterRateLimitError(f"Rate limit exceeded: {error_message}", response.status_code, error_data)
        elif response.status_code >= 500:
            raise OpenRouterServerError(f"Server error: {error_message}", response.status_code, error_data)
        elif response.status_code >= 400:
            raise OpenRouterClientError(f"Client error: {error_message}", response.status_code, error_data)
        else:
            raise OpenRouterError(f"Unexpected error: {error_message}", response.status_code, error_data)

    async def create_chat_completion(
        self,
        request: ChatCompletionRequest
    ) -> ChatCompletionResponse:
        """
        Create a chat completion using OpenRouter.

        Args:
            request: Chat completion request

        Returns:
            Chat completion response

        Raises:
            OpenRouterError: If the request fails
        """
        await self._ensure_client()
        await self._check_rate_limit()

        request_data = request.dict(exclude_unset=True)

        for attempt in range(self.max_retries + 1):
            try:
                response = await self._client.post(
                    "/chat/completions",
                    json=request_data
                )

                if response.is_success:
                    response_data = response.json()
                    return ChatCompletionResponse(**response_data)
                else:
                    self._handle_error_response(response)

            except (httpx.TimeoutException, httpx.ConnectError) as e:
                if attempt == self.max_retries:
                    raise OpenRouterError(f"Request failed after {self.max_retries + 1} attempts: {str(e)}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

            except OpenRouterRateLimitError:
                # Don't retry rate limit errors
                raise

        # This should never be reached, but just in case
        raise OpenRouterError("Request failed after all retries")

    async def list_models(self) -> Dict[str, Any]:
        """
        List available models from OpenRouter.

        Returns:
            Dictionary containing model information
        """
        await self._ensure_client()
        await self._check_rate_limit()

        for attempt in range(self.max_retries + 1):
            try:
                response = await self._client.get("/models")

                if response.is_success:
                    return response.json()
                else:
                    self._handle_error_response(response)

            except (httpx.TimeoutException, httpx.ConnectError) as e:
                if attempt == self.max_retries:
                    raise OpenRouterError(f"Failed to list models after {self.max_retries + 1} attempts: {str(e)}")
                await asyncio.sleep(2 ** attempt)

        raise OpenRouterError("Failed to list models after all retries")

    async def get_rate_limit_status(self) -> Dict[str, Any]:
        """
        Get current rate limiting status.

        Returns:
            Dictionary with rate limit information
        """
        now = time.time()
        return {
            "requests_this_minute": self.rate_limit_state.requests_this_minute,
            "requests_this_hour": self.rate_limit_state.requests_this_hour,
            "minute_limit": self.rate_limit_per_minute,
            "hour_limit": self.rate_limit_per_hour,
            "seconds_until_minute_reset": max(0, 60 - (now - self.rate_limit_state.minute_reset)),
            "seconds_until_hour_reset": max(0, 3600 - (now - self.rate_limit_state.hour_reset)),
            "last_request_time": self.rate_limit_state.last_request_time,
        }

    async def select_model_for_tier(self, tier: LLMTier) -> str:
        """
        Select the best model ID for a given intelligence tier.

        Uses the Model Registry Service to dynamically select the optimal
        model based on cost, performance, and capability criteria.

        Args:
            tier: Intelligence tier (ROUTER, NARRATOR, or THINKER)

        Returns:
            OpenRouter model ID string

        Raises:
            OpenRouterError: If no suitable model is found for the tier
        """
        # Lazy import to avoid circular dependency
        from llm_engine import get_model_registry_service
        registry_service = get_model_registry_service()

        try:
            selection_result = await registry_service.select_model_for_tier(tier)
            if selection_result and selection_result.selected_model:
                return selection_result.selected_model.id
            else:
                raise OpenRouterError(f"No suitable model found for tier: {tier.value}")
        except Exception as e:
            # Fallback to hardcoded defaults if registry fails
            logger = logging.getLogger(__name__)
            logger.warning(f"Model registry selection failed for tier {tier.value}: {e}. Using fallback.")
            return self._get_fallback_model_for_tier(tier)

    def _get_fallback_model_for_tier(self, tier: LLMTier) -> str:
        """
        Get fallback model ID when registry selection fails.

        These are reasonable defaults based on current OpenRouter offerings.
        """
        fallbacks = {
            LLMTier.ROUTER: "anthropic/claude-3-haiku",  # Fast, cheap, good for classification
            LLMTier.NARRATOR: "anthropic/claude-3-sonnet",  # Good fluency and context
            LLMTier.THINKER: "anthropic/claude-3-opus",  # Best reasoning capabilities
        }
        return fallbacks.get(tier, "anthropic/claude-3-haiku")

    async def create_chat_completion_for_tier(
        self,
        tier: LLMTier,
        messages: List[ChatMessage],
        **kwargs
    ) -> ChatCompletionResponse:
        """
        Create a chat completion using the best model for the specified tier.

        This is a convenience method that automatically selects the optimal model
        for the intelligence tier before making the request.

        Args:
            tier: Intelligence tier to select model for
            messages: Chat messages for the completion
            **kwargs: Additional parameters for ChatCompletionRequest

        Returns:
            Chat completion response
        """
        model_id = await self.select_model_for_tier(tier)

        request = ChatCompletionRequest(
            model=model_id,
            messages=messages,
            **kwargs
        )

        return await self.create_chat_completion(request)
