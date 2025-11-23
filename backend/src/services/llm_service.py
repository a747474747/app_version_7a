"""
LLM Service Layer for Four-Engine System Architecture.

This module provides a high-level abstraction layer for LLM operations,
including connection testing, model management, and cost tracking.
"""

import asyncio
import logging
import time
from typing import Any, Dict, List, Optional, Union
from contextlib import asynccontextmanager
from dataclasses import dataclass, field

from .openrouter_client import (
    OpenRouterClient,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatMessage,
    MessageRole,
    OpenRouterError,
    OpenRouterRateLimitError,
    OpenRouterAuthError,
    OpenRouterServerError,
    OpenRouterClientError,
)
from config.settings import get_settings


logger = logging.getLogger(__name__)


class LLMServiceCostCalculator:
    """
    Calculator for LLM usage costs based on OpenRouter pricing.

    Provides cost estimation and tracking for different models.
    """

    # Default pricing per million tokens (as of 2024, subject to change)
    DEFAULT_PRICING = {
        # Anthropic models
        "anthropic/claude-3-haiku": {
            "prompt": 0.25,      # $0.25 per million prompt tokens
            "completion": 1.25,  # $1.25 per million completion tokens
        },
        "anthropic/claude-3-sonnet": {
            "prompt": 3.0,       # $3.00 per million prompt tokens
            "completion": 15.0,  # $15.00 per million completion tokens
        },
        "anthropic/claude-3-opus": {
            "prompt": 15.0,      # $15.00 per million prompt tokens
            "completion": 75.0,  # $75.00 per million completion tokens
        },
        # OpenAI models
        "openai/gpt-3.5-turbo": {
            "prompt": 0.5,
            "completion": 1.5,
        },
        "openai/gpt-4": {
            "prompt": 30.0,
            "completion": 60.0,
        },
        "openai/gpt-4-turbo": {
            "prompt": 10.0,
            "completion": 30.0,
        },
        # Default fallback
        "default": {
            "prompt": 1.0,
            "completion": 2.0,
        }
    }

    def __init__(self, custom_pricing: Optional[Dict[str, Dict[str, float]]] = None):
        """
        Initialize the cost calculator.

        Args:
            custom_pricing: Custom pricing overrides
        """
        self.pricing = self.DEFAULT_PRICING.copy()
        if custom_pricing:
            self.pricing.update(custom_pricing)

    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> CostBreakdown:
        """
        Calculate cost for a single request.

        Args:
            model: Model identifier
            prompt_tokens: Number of prompt tokens
            completion_tokens: Number of completion tokens

        Returns:
            Detailed cost breakdown
        """
        pricing = self.pricing.get(model, self.pricing["default"])

        prompt_cost = (prompt_tokens / 1_000_000) * pricing["prompt"]
        completion_cost = (completion_tokens / 1_000_000) * pricing["completion"]
        total_cost = prompt_cost + completion_cost
        total_tokens = prompt_tokens + completion_tokens

        return CostBreakdown(
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            prompt_cost_usd=round(prompt_cost, 6),
            completion_cost_usd=round(completion_cost, 6),
            total_cost_usd=round(total_cost, 6),
            pricing_info=pricing
        )

    def estimate_cost(
        self,
        model: str,
        estimated_prompt_tokens: int,
        estimated_completion_tokens: int
    ) -> CostBreakdown:
        """
        Estimate cost for a request before making it.

        Args:
            model: Model identifier
            estimated_prompt_tokens: Estimated prompt tokens
            estimated_completion_tokens: Estimated completion tokens

        Returns:
            Estimated cost breakdown
        """
        return self.calculate_cost(model, estimated_prompt_tokens, estimated_completion_tokens)

    def get_model_pricing(self, model: str) -> Dict[str, float]:
        """
        Get pricing information for a model.

        Args:
            model: Model identifier

        Returns:
            Pricing information
        """
        return self.pricing.get(model, self.pricing["default"])

    def update_pricing(self, model: str, prompt_price: float, completion_price: float) -> None:
        """
        Update pricing for a model.

        Args:
            model: Model identifier
            prompt_price: Price per million prompt tokens
            completion_price: Price per million completion tokens
        """
        self.pricing[model] = {
            "prompt": prompt_price,
            "completion": completion_price
        }


class LLMUsageTracker:
    """
    Advanced usage tracking with cost monitoring and limits.

    Tracks usage patterns, enforces limits, and provides detailed reporting.
    """

    def __init__(self, cost_calculator: LLMServiceCostCalculator):
        """
        Initialize the usage tracker.

        Args:
            cost_calculator: Cost calculator instance
        """
        self.cost_calculator = cost_calculator
        self.usage_history: List[Dict[str, Any]] = []
        self._lock = asyncio.Lock()

    async def record_request(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        response_time_ms: float,
        success: bool = True
    ) -> CostBreakdown:
        """
        Record a completed request and calculate costs.

        Args:
            model: Model used
            prompt_tokens: Prompt tokens used
            completion_tokens: Completion tokens used
            response_time_ms: Response time
            success: Whether request was successful

        Returns:
            Cost breakdown for the request
        """
        async with self._lock:
            cost_breakdown = self.cost_calculator.calculate_cost(
                model, prompt_tokens, completion_tokens
            )

            request_record = {
                "timestamp": time.time(),
                "model": model,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": cost_breakdown.total_tokens,
                "cost_usd": cost_breakdown.total_cost_usd,
                "response_time_ms": response_time_ms,
                "success": success,
            }

            self.usage_history.append(request_record)

            # Keep only last 1000 records to prevent memory issues
            if len(self.usage_history) > 1000:
                self.usage_history = self.usage_history[-1000:]

            return cost_breakdown

    async def get_usage_report(
        self,
        time_window_hours: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate a usage report.

        Args:
            time_window_hours: Hours to look back (None for all time)

        Returns:
            Usage report dictionary
        """
        async with self._lock:
            if time_window_hours:
                cutoff_time = time.time() - (time_window_hours * 3600)
                relevant_records = [
                    r for r in self.usage_history if r["timestamp"] >= cutoff_time
                ]
            else:
                relevant_records = self.usage_history

            if not relevant_records:
                return {
                    "total_requests": 0,
                    "successful_requests": 0,
                    "total_tokens": 0,
                    "total_cost_usd": 0.0,
                    "average_response_time_ms": 0.0,
                    "cost_by_model": {},
                    "usage_by_hour": [],
                }

            # Calculate aggregates
            total_requests = len(relevant_records)
            successful_requests = sum(1 for r in relevant_records if r["success"])
            total_tokens = sum(r["total_tokens"] for r in relevant_records)
            total_cost = sum(r["cost_usd"] for r in relevant_records)
            avg_response_time = sum(r["response_time_ms"] for r in relevant_records) / total_requests

            # Cost by model
            cost_by_model = {}
            for record in relevant_records:
                model = record["model"]
                cost_by_model[model] = cost_by_model.get(model, 0.0) + record["cost_usd"]

            # Usage by hour (last 24 hours if time window allows)
            usage_by_hour = []
            if time_window_hours and time_window_hours <= 24:
                hours = {}
                for record in relevant_records:
                    hour = int(record["timestamp"] // 3600)
                    if hour not in hours:
                        hours[hour] = {"requests": 0, "cost": 0.0, "tokens": 0}
                    hours[hour]["requests"] += 1
                    hours[hour]["cost"] += record["cost_usd"]
                    hours[hour]["tokens"] += record["total_tokens"]

                usage_by_hour = [
                    {"hour": hour, **data}
                    for hour, data in sorted(hours.items())
                ]

            return {
                "total_requests": total_requests,
                "successful_requests": successful_requests,
                "success_rate": successful_requests / total_requests if total_requests > 0 else 0.0,
                "total_tokens": total_tokens,
                "total_cost_usd": round(total_cost, 4),
                "average_response_time_ms": round(avg_response_time, 2),
                "cost_by_model": cost_by_model,
                "usage_by_hour": usage_by_hour,
                "time_window_hours": time_window_hours,
            }

    async def check_limits(self, metrics: LLMUsageMetrics) -> List[str]:
        """
        Check if usage limits are exceeded.

        Args:
            metrics: Current usage metrics

        Returns:
            List of limit violation messages
        """
        violations = []

        if (metrics.monthly_token_limit and
            metrics.current_month_tokens >= metrics.monthly_token_limit):
            violations.append(
                f"Monthly token limit exceeded: {metrics.current_month_tokens}/{metrics.monthly_token_limit}"
            )

        if (metrics.monthly_cost_limit_usd and
            metrics.current_month_cost >= metrics.monthly_cost_limit_usd):
            violations.append(
                f"Monthly cost limit exceeded: ${metrics.current_month_cost:.2f}/${metrics.monthly_cost_limit_usd:.2f}"
            )

        return violations


class LLMServiceMonitor:
    """
    Monitoring component for LLM service health and performance.

    Provides automated health checks, alerting, and performance tracking.
    """

    def __init__(self, service: 'LLMService', check_interval_seconds: int = 300):  # 5 minutes
        """
        Initialize the monitor.

        Args:
            service: LLM service instance to monitor
            check_interval_seconds: Interval between health checks
        """
        self.service = service
        self.check_interval = check_interval_seconds
        self._monitoring_task: Optional[asyncio.Task] = None
        self._alert_callbacks: List[callable] = []

    async def start_monitoring(self) -> None:
        """Start background monitoring."""
        if self._monitoring_task is None:
            self._monitoring_task = asyncio.create_task(self._monitor_loop())
            logger.info(f"Started LLM service monitoring with {self.check_interval}s interval")

    async def stop_monitoring(self) -> None:
        """Stop background monitoring."""
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass
            self._monitoring_task = None
            logger.info("Stopped LLM service monitoring")

    async def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        while True:
            try:
                await self._perform_health_check()
                await asyncio.sleep(self.check_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {str(e)}")
                await asyncio.sleep(self.check_interval)

    async def _perform_health_check(self) -> None:
        """Perform comprehensive health check."""
        try:
            # Test connection
            old_status = self.service.connection_status.is_connected
            await self.service.test_connection()

            # Update health metrics
            self._update_health_metrics()

            # Check for status changes and alert
            if old_status != self.service.connection_status.is_connected:
                await self._trigger_alerts(
                    "connection_status_change",
                    {
                        "old_status": old_status,
                        "new_status": self.service.connection_status.is_connected,
                        "error": self.service.connection_status.last_error,
                    }
                )

            # Check for degraded performance
            if self.service.connection_status.health_score < 0.8:
                await self._trigger_alerts(
                    "degraded_performance",
                    {
                        "health_score": self.service.connection_status.health_score,
                        "response_time": self.service.connection_status.response_time_ms,
                    }
                )

        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            await self._trigger_alerts("health_check_failed", {"error": str(e)})

    def _update_health_metrics(self) -> None:
        """Update health score and metrics based on recent performance."""
        # Calculate health score based on multiple factors
        connection_score = 1.0 if self.service.connection_status.is_connected else 0.0

        # Response time score (better if faster, target < 5000ms)
        response_time_score = max(0.0, min(1.0, 5000 / max(self.service.connection_status.response_time_ms or 5000, 100)))

        # Success rate score
        total_requests = self.service.usage_metrics.total_requests
        success_rate = (
            self.service.usage_metrics.successful_requests / max(total_requests, 1)
            if total_requests > 0 else 1.0
        )

        # Error rate penalty
        error_rate_penalty = min(0.5, self.service.usage_metrics.error_rate * 2)

        # Calculate overall health score
        health_score = (connection_score * 0.4 + response_time_score * 0.3 +
                       success_rate * 0.2 - error_rate_penalty * 0.1)
        health_score = max(0.0, min(1.0, health_score))

        self.service.connection_status.health_score = health_score

        # Update uptime percentage (simplified calculation)
        if self.service.connection_status.consecutive_failures == 0:
            self.service.usage_metrics.uptime_percentage = 100.0
        else:
            # Estimate based on recent failures
            estimated_uptime = max(0.0, 100.0 - (self.service.connection_status.consecutive_failures * 10))
            self.service.usage_metrics.uptime_percentage = estimated_uptime

    def add_alert_callback(self, callback: callable) -> None:
        """
        Add a callback function to be called when alerts are triggered.

        Args:
            callback: Function that takes (alert_type: str, data: dict)
        """
        self._alert_callbacks.append(callback)

    async def _trigger_alerts(self, alert_type: str, data: Dict[str, Any]) -> None:
        """Trigger alert callbacks."""
        for callback in self._alert_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(alert_type, data)
                else:
                    callback(alert_type, data)
            except Exception as e:
                logger.error(f"Error in alert callback: {str(e)}")


@dataclass
class LLMConnectionStatus:
    """Status information for LLM service connection."""
    is_connected: bool
    last_test_time: Optional[float] = None
    last_error: Optional[str] = None
    response_time_ms: Optional[float] = None
    models_available: List[str] = field(default_factory=list)
    consecutive_failures: int = 0
    last_success_time: Optional[float] = None
    health_score: float = 1.0  # 0.0 to 1.0, based on recent performance


@dataclass
class LLMUsageMetrics:
    """Usage metrics for LLM service."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_tokens_used: int = 0
    prompt_tokens_used: int = 0
    completion_tokens_used: int = 0
    total_cost_usd: float = 0.0
    average_response_time_ms: float = 0.0
    rate_limit_hits: int = 0
    last_request_time: Optional[float] = None
    error_rate: float = 0.0
    throughput_requests_per_minute: float = 0.0
    uptime_percentage: float = 100.0

    # Cost breakdown
    cost_by_model: Dict[str, float] = None
    tokens_by_model: Dict[str, int] = None

    # Usage limits and tracking
    monthly_token_limit: Optional[int] = None
    monthly_cost_limit_usd: Optional[float] = None
    current_month_tokens: int = 0
    current_month_cost: float = 0.0

    def __post_init__(self):
        if self.cost_by_model is None:
            self.cost_by_model = {}
        if self.tokens_by_model is None:
            self.tokens_by_model = {}


@dataclass
class CostBreakdown:
    """Detailed cost breakdown for a single request."""
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    prompt_cost_usd: float
    completion_cost_usd: float
    total_cost_usd: float
    pricing_info: Dict[str, Any]


class LLMServiceError(Exception):
    """Base exception for LLM service errors."""
    pass


class LLMConnectionError(LLMServiceError):
    """Exception raised when LLM service connection fails."""
    pass


class LLMModelNotAvailableError(LLMServiceError):
    """Exception raised when requested model is not available."""
    pass


class LLMService:
    """
    High-level LLM service abstraction layer.

    Provides connection management, model selection, cost tracking,
    and unified interface for LLM operations across the four-engine architecture.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://openrouter.ai/api/v1",
        default_model: Optional[str] = None,
        timeout: float = 60.0,
        max_retries: int = 3,
    ):
        """
        Initialize the LLM service.

        Args:
            api_key: OpenRouter API key (defaults to settings)
            base_url: OpenRouter API base URL
            default_model: Default model to use (defaults to settings)
            timeout: Request timeout in seconds
            max_retries: Maximum retries for failed requests
        """
        settings = get_settings()

        self.api_key = api_key or settings.llm.openrouter_api_key
        self.base_url = base_url
        self.default_model = default_model or settings.llm.default_model
        self.timeout = timeout
        self.max_retries = max_retries

        # Connection and metrics state
        self.connection_status = LLMConnectionStatus(is_connected=False)
        self.usage_metrics = LLMUsageMetrics()

        # Cost calculation and usage tracking
        self.cost_calculator = LLMServiceCostCalculator()
        self.usage_tracker = LLMUsageTracker(self.cost_calculator)

        # Monitoring
        self.monitor: Optional[LLMServiceMonitor] = None

        # Client instance (lazy initialization)
        self._client: Optional[OpenRouterClient] = None
        self._available_models: Optional[List[Dict[str, Any]]] = None

    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.cleanup()

    async def initialize(self) -> None:
        """Initialize the LLM service and test connection."""
        if self._client is None:
            self._client = OpenRouterClient(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=self.timeout,
                max_retries=self.max_retries,
            )

        # Initialize monitoring
        if self.monitor is None:
            self.monitor = LLMServiceMonitor(self)

        # Test connection and load models
        await self.test_connection()

    async def cleanup(self) -> None:
        """Clean up resources."""
        if self.monitor:
            await self.monitor.stop_monitoring()
        if self._client:
            await self._client._close_client()
            self._client = None

    async def test_connection(self) -> LLMConnectionStatus:
        """
        Test connection to LLM service.

        Returns:
            Connection status information
        """
        start_time = time.time()

        try:
            # Test with a simple request
            test_request = ChatCompletionRequest(
                model=self.default_model,
                messages=[ChatMessage(role=MessageRole.USER, content="Hello")],
                max_tokens=10,
                temperature=0.1,
            )

            response = await self._get_client().create_chat_completion(test_request)

            # Update connection status
            response_time = (time.time() - start_time) * 1000
            self.connection_status.is_connected = True
            self.connection_status.last_test_time = time.time()
            self.connection_status.last_success_time = time.time()
            self.connection_status.response_time_ms = response_time
            self.connection_status.consecutive_failures = 0
            self.connection_status.last_error = None

            # Load available models
            await self._load_available_models()

            logger.info(f"LLM service connection test successful. Response time: {response_time:.1f}ms")
            return self.connection_status

        except OpenRouterAuthError as e:
            error_msg = f"Authentication failed: {str(e)}"
            self.connection_status.is_connected = False
            self.connection_status.last_test_time = time.time()
            self.connection_status.last_error = error_msg
            self.connection_status.consecutive_failures += 1
            logger.error(error_msg)
            raise LLMConnectionError(error_msg) from e

        except OpenRouterError as e:
            error_msg = f"Connection test failed: {str(e)}"
            self.connection_status.is_connected = False
            self.connection_status.last_test_time = time.time()
            self.connection_status.last_error = error_msg
            self.connection_status.consecutive_failures += 1
            logger.error(error_msg)
            raise LLMConnectionError(error_msg) from e

    async def _load_available_models(self) -> None:
        """Load available models from OpenRouter."""
        try:
            models_response = await self._get_client().list_models()
            self._available_models = models_response.get("data", [])

            # Extract model IDs
            model_ids = [model.get("id", "") for model in self._available_models if model.get("id")]
            self.connection_status.models_available = model_ids

            logger.info(f"Loaded {len(model_ids)} available models")

        except OpenRouterError as e:
            logger.warning(f"Failed to load available models: {str(e)}")
            self._available_models = []

    def _get_client(self) -> OpenRouterClient:
        """Get the OpenRouter client instance."""
        if self._client is None:
            raise LLMServiceError("LLM service not initialized. Call initialize() first.")
        return self._client

    def is_model_available(self, model_id: str) -> bool:
        """
        Check if a model is available.

        Args:
            model_id: Model identifier to check

        Returns:
            True if model is available
        """
        return model_id in self.connection_status.models_available

    async def generate_completion(
        self,
        messages: List[Union[Dict[str, str], ChatMessage]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatCompletionResponse:
        """
        Generate a chat completion.

        Args:
            messages: List of messages (dict or ChatMessage)
            model: Model to use (defaults to default_model)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters

        Returns:
            Chat completion response

        Raises:
            LLMModelNotAvailableError: If requested model is not available
            LLMServiceError: If request fails
        """
        # Convert dict messages to ChatMessage objects
        chat_messages = []
        for msg in messages:
            if isinstance(msg, dict):
                chat_messages.append(ChatMessage(**msg))
            else:
                chat_messages.append(msg)

        # Validate model availability
        selected_model = model or self.default_model
        if not self.is_model_available(selected_model):
            logger.warning(f"Model {selected_model} not in available models list, proceeding anyway")

        # Create request
        request = ChatCompletionRequest(
            model=selected_model,
            messages=chat_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

        # Track request start
        start_time = time.time()
        self.usage_metrics.total_requests += 1

        try:
            response = await self._get_client().create_chat_completion(request)

            # Update metrics
            response_time = (time.time() - start_time) * 1000
            self.usage_metrics.successful_requests += 1
            self.usage_metrics.last_request_time = time.time()

            # Record detailed usage and costs
            cost_breakdown = await self.usage_tracker.record_request(
                model=selected_model,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                response_time_ms=response_time,
                success=True
            )

            # Update aggregate metrics
            self.usage_metrics.total_tokens_used += response.usage.total_tokens
            self.usage_metrics.prompt_tokens_used += response.usage.prompt_tokens
            self.usage_metrics.completion_tokens_used += response.usage.completion_tokens
            self.usage_metrics.total_cost_usd += cost_breakdown.total_cost_usd
            self.usage_metrics.current_month_tokens += response.usage.total_tokens
            self.usage_metrics.current_month_cost += cost_breakdown.total_cost_usd

            # Update cost by model
            self.usage_metrics.cost_by_model[selected_model] = (
                self.usage_metrics.cost_by_model.get(selected_model, 0.0) + cost_breakdown.total_cost_usd
            )
            self.usage_metrics.tokens_by_model[selected_model] = (
                self.usage_metrics.tokens_by_model.get(selected_model, 0) + response.usage.total_tokens
            )

            # Update rolling average response time
            if self.usage_metrics.average_response_time_ms == 0:
                self.usage_metrics.average_response_time_ms = response_time
            else:
                self.usage_metrics.average_response_time_ms = (
                    self.usage_metrics.average_response_time_ms * 0.9 + response_time * 0.1
                )

            # Update throughput (requests per minute, rolling average)
            time_since_last_request = (
                start_time - (self.usage_metrics.last_request_time or start_time)
            )
            if time_since_last_request > 0:
                current_throughput = 60 / time_since_last_request  # requests per minute
                if self.usage_metrics.throughput_requests_per_minute == 0:
                    self.usage_metrics.throughput_requests_per_minute = current_throughput
                else:
                    self.usage_metrics.throughput_requests_per_minute = (
                        self.usage_metrics.throughput_requests_per_minute * 0.9 + current_throughput * 0.1
                    )

            logger.debug(
                f"LLM completion successful. Tokens: {response.usage.total_tokens}, "
                f"Cost: ${cost_breakdown.total_cost_usd:.6f}, Time: {response_time:.1f}ms"
            )
            return response

        except OpenRouterRateLimitError as e:
            self.usage_metrics.rate_limit_hits += 1
            self.usage_metrics.failed_requests += 1
            self._update_error_rate()
            # Record failed request
            await self.usage_tracker.record_request(
                model=selected_model,
                prompt_tokens=0,
                completion_tokens=0,
                response_time_ms=(time.time() - start_time) * 1000,
                success=False
            )
            logger.warning(f"Rate limit hit: {str(e)}")
            raise LLMServiceError(f"Rate limit exceeded: {str(e)}") from e

        except OpenRouterError as e:
            self.usage_metrics.failed_requests += 1
            self._update_error_rate()
            # Record failed request
            await self.usage_tracker.record_request(
                model=selected_model,
                prompt_tokens=0,
                completion_tokens=0,
                response_time_ms=(time.time() - start_time) * 1000,
                success=False
            )
            logger.error(f"LLM request failed: {str(e)}")
            raise LLMServiceError(f"LLM request failed: {str(e)}") from e

    async def get_connection_status(self) -> LLMConnectionStatus:
        """
        Get current connection status.

        Returns:
            Connection status information
        """
        return self.connection_status

    async def get_usage_metrics(self) -> LLMUsageMetrics:
        """
        Get usage metrics.

        Returns:
            Usage metrics information
        """
        return self.usage_metrics

    async def get_available_models(self) -> List[Dict[str, Any]]:
        """
        Get list of available models.

        Returns:
            List of model information dictionaries
        """
        if self._available_models is None:
            await self._load_available_models()
        return self._available_models or []

    async def get_cost_estimate(
        self,
        model: str,
        estimated_prompt_tokens: int,
        estimated_completion_tokens: int
    ) -> CostBreakdown:
        """
        Get cost estimate for a potential request.

        Args:
            model: Model to use
            estimated_prompt_tokens: Estimated prompt tokens
            estimated_completion_tokens: Estimated completion tokens

        Returns:
            Cost estimate breakdown
        """
        return self.cost_calculator.estimate_cost(
            model, estimated_prompt_tokens, estimated_completion_tokens
        )

    async def get_usage_report(self, time_window_hours: Optional[int] = None) -> Dict[str, Any]:
        """
        Get detailed usage report.

        Args:
            time_window_hours: Hours to look back (None for all time)

        Returns:
            Usage report with costs and statistics
        """
        report = await self.usage_tracker.get_usage_report(time_window_hours)

        # Add current metrics
        report.update({
            "current_metrics": {
                "total_requests": self.usage_metrics.total_requests,
                "successful_requests": self.usage_metrics.successful_requests,
                "failed_requests": self.usage_metrics.failed_requests,
                "total_tokens_used": self.usage_metrics.total_tokens_used,
                "total_cost_usd": round(self.usage_metrics.total_cost_usd, 4),
                "error_rate": round(self.usage_metrics.error_rate, 4),
                "throughput_rpm": round(self.usage_metrics.throughput_requests_per_minute, 2),
                "uptime_percentage": round(self.usage_metrics.uptime_percentage, 2),
            },
            "limits": {
                "monthly_token_limit": self.usage_metrics.monthly_token_limit,
                "monthly_cost_limit_usd": self.usage_metrics.monthly_cost_limit_usd,
                "current_month_tokens": self.usage_metrics.current_month_tokens,
                "current_month_cost": round(self.usage_metrics.current_month_cost, 4),
            }
        })

        return report

    async def check_usage_limits(self) -> List[str]:
        """
        Check if any usage limits are exceeded.

        Returns:
            List of limit violation messages
        """
        return await self.usage_tracker.check_limits(self.usage_metrics)

    def set_usage_limits(
        self,
        monthly_token_limit: Optional[int] = None,
        monthly_cost_limit_usd: Optional[float] = None
    ) -> None:
        """
        Set usage limits.

        Args:
            monthly_token_limit: Maximum tokens per month
            monthly_cost_limit_usd: Maximum cost per month in USD
        """
        self.usage_metrics.monthly_token_limit = monthly_token_limit
        self.usage_metrics.monthly_cost_limit_usd = monthly_cost_limit_usd

    def update_model_pricing(
        self,
        model: str,
        prompt_price_per_million: float,
        completion_price_per_million: float
    ) -> None:
        """
        Update pricing for a specific model.

        Args:
            model: Model identifier
            prompt_price_per_million: Price per million prompt tokens
            completion_price_per_million: Price per million completion tokens
        """
        self.cost_calculator.update_pricing(model, prompt_price_per_million, completion_price_per_million)

    def _update_error_rate(self) -> None:
        """Update the error rate based on recent requests."""
        total = self.usage_metrics.total_requests
        if total > 0:
            self.usage_metrics.error_rate = self.usage_metrics.failed_requests / total

    async def start_monitoring(self, check_interval_seconds: int = 300) -> None:
        """
        Start background monitoring of the LLM service.

        Args:
            check_interval_seconds: Interval between health checks
        """
        if self.monitor is None:
            self.monitor = LLMServiceMonitor(self, check_interval_seconds)
        await self.monitor.start_monitoring()

    async def stop_monitoring(self) -> None:
        """Stop background monitoring."""
        if self.monitor:
            await self.monitor.stop_monitoring()

    def add_health_alert_callback(self, callback: callable) -> None:
        """
        Add a callback for health alerts.

        Args:
            callback: Function called with (alert_type: str, data: dict)
        """
        if self.monitor:
            self.monitor.add_alert_callback(callback)

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform comprehensive health check.

        Returns:
            Health check results
        """
        try:
            # Test connection if not recently tested
            if (self.connection_status.last_test_time is None or
                time.time() - self.connection_status.last_test_time > 300):  # 5 minutes
                await self.test_connection()

            return {
                "status": "healthy" if self.connection_status.is_connected else "unhealthy",
                "connection": {
                    "is_connected": self.connection_status.is_connected,
                    "last_test_time": self.connection_status.last_test_time,
                    "response_time_ms": self.connection_status.response_time_ms,
                    "models_available": len(self.connection_status.models_available),
                },
                "usage": {
                    "total_requests": self.usage_metrics.total_requests,
                    "success_rate": (
                        self.usage_metrics.successful_requests / max(self.usage_metrics.total_requests, 1)
                    ),
                    "rate_limit_hits": self.usage_metrics.rate_limit_hits,
                    "average_response_time_ms": self.usage_metrics.average_response_time_ms,
                },
                "timestamp": time.time(),
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": time.time(),
            }


# Global service instance
_llm_service_instance: Optional[LLMService] = None


async def get_llm_service() -> LLMService:
    """
    Get or create global LLM service instance.

    Returns:
        LLM service instance
    """
    global _llm_service_instance
    if _llm_service_instance is None:
        _llm_service_instance = LLMService()
        await _llm_service_instance.initialize()
    return _llm_service_instance


@asynccontextmanager
async def llm_service_context():
    """
    Context manager for LLM service usage.

    Usage:
        async with llm_service_context() as llm:
            response = await llm.generate_completion(...)
    """
    service = await get_llm_service()
    try:
        yield service
    finally:
        # Service cleanup is handled by the service itself
        pass
