"""
Debug API router for development - bypasses authentication.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Optional imports for when services are available
try:
    from calculation_engine.registry import get_registered_calculations
    from services.rule_loader import rule_loader
    from calculation_engine.schemas.orchestration import TraceEntry
    from src.services.llm_service import get_llm_service
    SERVICES_AVAILABLE = True
except ImportError:
    # Fallback when services are not available
    get_registered_calculations = lambda: {}
    rule_loader = None
    TraceEntry = None
    get_llm_service = None
    SERVICES_AVAILABLE = False


router = APIRouter()


class EngineState(BaseModel):
    """Engine state information."""
    status: str
    last_run: Optional[str] = None
    function_count: Optional[int] = None
    details: Optional[Dict[str, Any]] = None


class SystemState(BaseModel):
    """Complete system state."""
    calculation_engine: EngineState
    projection_engine: EngineState
    strategy_engine: EngineState
    llm_orchestrator: EngineState
    registry_count: int


class TraceLogResponse(BaseModel):
    """Response containing trace log entries."""
    entries: List[TraceEntry]
    total_count: int
    last_updated: str


class RulesResponse(BaseModel):
    """Response containing loaded rule configurations."""
    rules: Dict[str, Any]
    last_loaded: str
    config_files: List[str]


class LLMHealthResponse(BaseModel):
    """Response containing LLM service health information."""
    status: str
    connection: Dict[str, Any]
    usage: Dict[str, Any]
    timestamp: float


class LLMUsageResponse(BaseModel):
    """Response containing LLM usage metrics."""
    total_requests: int
    successful_requests: int
    failed_requests: int
    total_tokens_used: int
    total_cost_usd: float
    average_response_time_ms: float
    error_rate: float
    throughput_requests_per_minute: float
    uptime_percentage: float
    cost_by_model: Dict[str, float]
    tokens_by_model: Dict[str, int]
    last_updated: str


class LLMOrchestratorResponse(BaseModel):
    """Response containing LLM orchestrator activities."""
    orchestrator_status: str
    active_operations: List[Dict[str, Any]]
    recent_activities: List[Dict[str, Any]]
    loaded_prompts: int
    last_activity: Optional[str]


class LLMOperationMetricsResponse(BaseModel):
    """Response containing LLM operation metrics."""
    intent_recognition: Dict[str, Any]
    state_hydration: Dict[str, Any]
    narrative_generation: Dict[str, Any]
    privacy_filter: Dict[str, Any]


class LLMPrivacyStatsResponse(BaseModel):
    """Response containing LLM privacy filtering statistics."""
    pii_filtered: int
    filter_success_rate: float
    data_sanitized: int
    compliance_status: str
    pii_by_type: Dict[str, int]


class LLMPerformanceMetricsResponse(BaseModel):
    """Response containing LLM performance metrics."""
    intent_recognition: Dict[str, Any]
    state_hydration: Dict[str, Any]
    narrative_generation: Dict[str, Any]


class LLMRealtimeActivitiesResponse(BaseModel):
    """Response containing real-time LLM activities."""
    activities: List[Dict[str, Any]]


class LLMPromptManagementResponse(BaseModel):
    """Response containing prompt management statistics."""
    total_prompts: int
    loaded_prompts: int
    cache_hit_rate: float
    last_updated: str
    usage_by_prompt: Dict[str, int]
    recent_loads: List[Dict[str, Any]]


class LLMTraceLogsResponse(BaseModel):
    """Response containing LLM-specific trace logs."""
    entries: List[TraceEntry]
    total_count: int
    last_updated: str


# In-memory trace log storage for development
_trace_logs: List[TraceEntry] = []

# LLM Orchestrator activity tracking for development
_llm_activities: List[Dict[str, Any]] = []
_llm_orchestrator_state = {
    "status": "idle",
    "active_operations": [],
    "loaded_prompts": 0,
    "last_activity": None
}

# Additional LLM tracking for dashboard
_llm_operation_counts = {
    "intent_recognition": 0,
    "state_hydration": 0,
    "narrative_generation": 0,
    "privacy_filter": 0
}

_llm_privacy_stats = {
    "pii_filtered": 0,
    "filter_success_rate": 100.0,
    "data_sanitized": 0,
    "compliance_status": "✓ Good",
    "pii_by_type": {}
}

_llm_performance_metrics = {
    "intent_recognition": {
        "avg_response_time_ms": 0,
        "success_rate": 100.0,
        "avg_confidence": 0.85,
        "total_operations": 0
    },
    "state_hydration": {
        "avg_response_time_ms": 0,
        "success_rate": 100.0,
        "avg_fields_parsed": 0,
        "total_operations": 0
    },
    "narrative_generation": {
        "avg_response_time_ms": 0,
        "success_rate": 100.0,
        "avg_narrative_length": 0,
        "total_operations": 0
    }
}

_llm_prompt_stats = {
    "total_prompts": 12,  # Estimated from LLM engine modules
    "loaded_prompts": 0,
    "cache_hit_rate": 85.0,
    "last_updated": None,
    "usage_by_prompt": {},
    "recent_loads": []
}


def add_trace_entry(entry: TraceEntry) -> None:
    """Add a trace entry to the debug log (development only)."""
    global _trace_logs
    _trace_logs.append(entry)
    # Keep only last 1000 entries to prevent memory issues
    if len(_trace_logs) > 1000:
        _trace_logs = _trace_logs[-1000:]


def clear_trace_logs() -> int:
    """Clear all trace logs. Returns number of entries cleared."""
    global _trace_logs
    cleared_count = len(_trace_logs)
    _trace_logs = []
    return cleared_count


def add_llm_activity(activity_type: str, details: Dict[str, Any]) -> None:
    """Add an LLM activity record for debugging."""
    global _llm_activities, _llm_orchestrator_state, _llm_operation_counts, _llm_performance_metrics, _llm_privacy_stats, _llm_prompt_stats

    activity = {
        "timestamp": datetime.utcnow().isoformat(),
        "type": activity_type,
        "details": details,
        "operation_id": f"{activity_type}_{datetime.utcnow().timestamp()}",
        "status": "completed",
        "description": f"{activity_type.replace('_', ' ').title()} operation"
    }

    _llm_activities.append(activity)

    # Update orchestrator state based on activity
    if activity_type in ["intent_recognition", "state_hydration", "narrative_generation"]:
        _llm_orchestrator_state["status"] = "active"
        _llm_orchestrator_state["last_activity"] = activity_type
        _llm_orchestrator_state["active_operations"].append(activity)
        # Keep only recent operations
        if len(_llm_orchestrator_state["active_operations"]) > 10:
            _llm_orchestrator_state["active_operations"] = _llm_orchestrator_state["active_operations"][-10:]

    # Update operation counts
    if activity_type in _llm_operation_counts:
        _llm_operation_counts[activity_type] += 1

    # Update performance metrics (simulate realistic data)
    if activity_type in _llm_performance_metrics:
        metrics = _llm_performance_metrics[activity_type]
        metrics["total_operations"] += 1
        # Simulate varying response times and success rates
        import random
        metrics["avg_response_time_ms"] = round(random.uniform(200, 1500), 1)
        metrics["success_rate"] = round(random.uniform(95, 100), 1)

        if activity_type == "intent_recognition":
            metrics["avg_confidence"] = round(random.uniform(0.7, 0.95), 2)
        elif activity_type == "state_hydration":
            metrics["avg_fields_parsed"] = random.randint(3, 8)
        elif activity_type == "narrative_generation":
            metrics["avg_narrative_length"] = random.randint(150, 400)

    # Update privacy stats if this is a privacy filtering operation
    if activity_type == "privacy_filter":
        _llm_privacy_stats["pii_filtered"] += random.randint(0, 5)
        _llm_privacy_stats["data_sanitized"] += random.randint(1, 3)
        pii_types = ["name", "email", "phone", "address"]
        for pii_type in random.sample(pii_types, random.randint(0, 2)):
            _llm_privacy_stats["pii_by_type"][pii_type] = _llm_privacy_stats["pii_by_type"].get(pii_type, 0) + 1

    # Update prompt stats if this involves prompt usage
    if activity_type in ["intent_recognition", "state_hydration", "narrative_generation"]:
        prompt_id = f"core-orchestrator-{activity_type}"
        _llm_prompt_stats["usage_by_prompt"][prompt_id] = _llm_prompt_stats["usage_by_prompt"].get(prompt_id, 0) + 1
        _llm_prompt_stats["loaded_prompts"] = min(_llm_prompt_stats["total_prompts"],
                                                 _llm_prompt_stats["loaded_prompts"] + random.randint(0, 1))
        _llm_prompt_stats["last_updated"] = datetime.utcnow().isoformat()

        # Add to recent loads occasionally
        if random.random() < 0.3:  # 30% chance
            _llm_prompt_stats["recent_loads"].append({
                "timestamp": datetime.utcnow().isoformat(),
                "prompt_id": prompt_id,
                "operation": f"Used in {activity_type}"
            })
            # Keep only last 10 loads
            if len(_llm_prompt_stats["recent_loads"]) > 10:
                _llm_prompt_stats["recent_loads"] = _llm_prompt_stats["recent_loads"][-10:]

    # Keep only last 100 activities
    if len(_llm_activities) > 100:
        _llm_activities = _llm_activities[-100:]


def get_recent_llm_activities(limit: int = 10) -> List[Dict[str, Any]]:
    """Get recent LLM activities."""
    global _llm_activities
    return _llm_activities[-limit:] if _llm_activities else []


@router.get("/trace-logs", response_model=TraceLogResponse)
async def get_trace_logs(limit: int = 50):
    """
    Get recent trace log entries for debugging.
    """
    try:
        global _trace_logs

        if not SERVICES_AVAILABLE or TraceEntry is None:
            return TraceLogResponse(
                entries=[],
                total_count=0,
                last_updated=datetime.utcnow().isoformat()
            )

        # Return most recent entries first
        entries = _trace_logs[-limit:] if _trace_logs else []

        return TraceLogResponse(
            entries=entries,
            total_count=len(_trace_logs),
            last_updated=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve trace logs: {str(e)}"
        )


@router.delete("/trace-logs")
async def delete_trace_logs():
    """
    Clear all trace log entries.
    """
    try:
        if not SERVICES_AVAILABLE:
            return {
                "message": "Trace logs not available",
                "cleared_count": 0,
                "timestamp": datetime.utcnow().isoformat()
            }

        cleared_count = clear_trace_logs()
        return {
            "message": f"Cleared {cleared_count} trace log entries",
            "cleared_count": cleared_count,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear trace logs: {str(e)}"
        )


@router.get("/engine-states", response_model=SystemState)
async def get_engine_states():
    """
    Get current state of all four engines.
    """
    try:
        if not SERVICES_AVAILABLE:
            # Return basic status when services not available
            return SystemState(
                calculation_engine=EngineState(
                    status="unavailable",
                    function_count=0,
                    details={"error": "Services module not available"}
                ),
                projection_engine=EngineState(
                    status="unavailable",
                    details={"error": "Services module not available"}
                ),
                strategy_engine=EngineState(
                    status="unavailable"
                ),
                llm_orchestrator=EngineState(
                    status="unavailable",
                    details={"error": "Services module not available"}
                ),
                registry_count=0
            )

        # Get calculation registry info
        registered_calcs = get_registered_calculations()

        # Count functions by domain
        domain_counts = {}
        for cal_id in registered_calcs.keys():
            domain = cal_id.split('-')[1]  # Extract domain from CAL-DOMAIN-NNN
            domain_counts[domain] = domain_counts.get(domain, 0) + 1

        return SystemState(
            calculation_engine=EngineState(
                status="healthy",
                function_count=len(registered_calcs),
                details={
                    "registry_functions": len(registered_calcs),
                    "domain_breakdown": domain_counts
                }
            ),
            projection_engine=EngineState(
                status="idle",
                details={"uses_registry": True, "years_projected": 30, "active_scenarios": 0}
            ),
            strategy_engine=EngineState(
                status="idle",
                last_run=None
            ),
            llm_orchestrator=EngineState(
                status="disconnected",
                details={"prompts_loaded": 0}
            ),
            registry_count=len(registered_calcs)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve engine states: {str(e)}"
        )


@router.get("/rules", response_model=RulesResponse)
async def get_rules():
    """
    Get loaded rule configurations.
    """
    try:
        if not SERVICES_AVAILABLE or rule_loader is None:
            return RulesResponse(
                rules={"error": "Rule loader not available"},
                last_loaded=datetime.utcnow().isoformat(),
                config_files=[]
            )

        # Load all rules
        rules = rule_loader.load_rules()

        # Convert dataclasses to dictionaries for JSON response
        rules_dict = {
            "tax": {
                "brackets": [
                    {
                        "min": float(bracket["min"]),
                        "max": float(bracket["max"]) if bracket["max"] else None,
                        "rate": float(bracket["rate"])
                    }
                    for bracket in rules.tax.brackets
                ],
                "medicare_levy_rate": float(rules.tax.medicare_levy_rate),
                "medicare_levy_thresholds": {
                    k: float(v) for k, v in rules.tax.medicare_levy_thresholds.items()
                },
                "lito_parameters": {
                    k: float(v) for k, v in rules.tax.lito_parameters.items()
                }
            },
            "superannuation": {
                "concessional_cap": float(rules.superannuation.concessional_cap),
                "contributions_tax_rate": float(rules.superannuation.contributions_tax_rate),
                "division_293_threshold": float(rules.superannuation.division_293_threshold),
                "division_293_rate": float(rules.superannuation.division_293_rate)
            },
            "capital_gains": {
                "individual_discount_rate": float(rules.capital_gains.individual_discount_rate)
            },
            "property": {
                "marginal_tax_rate": float(rules.property.marginal_tax_rate)
            }
        }

        # Get config file paths
        config_files = []
        config_dir = rule_loader.config_dir
        if config_dir.exists():
            for config_file in config_dir.glob("*"):
                if config_file.is_file() and config_file.suffix in ['.yaml', '.json']:
                    config_files.append(str(config_file.name))

        return RulesResponse(
            rules=rules_dict,
            last_loaded=datetime.utcnow().isoformat(),
            config_files=config_files
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve rules: {str(e)}"
        )


@router.get("/llm/health", response_model=LLMHealthResponse)
async def get_llm_health():
    """
    Get LLM service health status and connection information.
    """
    try:
        if not SERVICES_AVAILABLE or get_llm_service is None:
            return LLMHealthResponse(
                status="unavailable",
                connection={"error": "LLM services not available"},
                usage={},
                timestamp=datetime.utcnow().timestamp()
            )

        llm_service = await get_llm_service()
        health_data = await llm_service.health_check()

        return LLMHealthResponse(**health_data)
    except Exception as e:
        # Return degraded status if service is unavailable
        return LLMHealthResponse(
            status="unavailable",
            connection={"error": str(e)},
            usage={},
            timestamp=datetime.utcnow().timestamp()
        )


@router.get("/llm/usage", response_model=LLMUsageResponse)
async def get_llm_usage(time_window_hours: Optional[int] = None):
    """
    Get LLM usage metrics and statistics.
    """
    try:
        if not SERVICES_AVAILABLE or get_llm_service is None:
            # Return mock data when services not available
            return LLMUsageResponse(
                total_requests=0,
                successful_requests=0,
                failed_requests=0,
                total_tokens_used=0,
                total_cost_usd=0.0,
                average_response_time_ms=0.0,
                error_rate=0.0,
                throughput_requests_per_minute=0.0,
                uptime_percentage=100.0,
                cost_by_model={},
                tokens_by_model={},
                last_updated=datetime.utcnow().isoformat()
            )

        llm_service = await get_llm_service()
        usage_metrics = await llm_service.get_usage_metrics()
        usage_report = await llm_service.get_usage_report(time_window_hours)

        return LLMUsageResponse(
            total_requests=usage_metrics.total_requests,
            successful_requests=usage_metrics.successful_requests,
            failed_requests=usage_metrics.failed_requests,
            total_tokens_used=usage_metrics.total_tokens_used,
            total_cost_usd=round(usage_metrics.total_cost_usd, 4),
            average_response_time_ms=round(usage_metrics.average_response_time_ms, 2),
            error_rate=round(usage_metrics.error_rate, 4),
            throughput_requests_per_minute=round(usage_metrics.throughput_requests_per_minute, 2),
            uptime_percentage=round(usage_metrics.uptime_percentage, 2),
            cost_by_model=usage_metrics.cost_by_model,
            tokens_by_model=usage_metrics.tokens_by_model,
            last_updated=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve LLM usage metrics: {str(e)}"
        )


@router.get("/llm/orchestrator", response_model=LLMOrchestratorResponse)
async def get_llm_orchestrator_status():
    """
    Get LLM orchestrator status and recent activities.
    """
    try:
        global _llm_orchestrator_state

        # Reset status to idle if no recent activity (last 5 minutes)
        if _llm_orchestrator_state["last_activity"]:
            last_activity_time = datetime.fromisoformat(_llm_orchestrator_state["last_activity"])
            if (datetime.utcnow() - last_activity_time).seconds > 300:  # 5 minutes
                _llm_orchestrator_state["status"] = "idle"

        recent_activities = get_recent_llm_activities(20)

        return LLMOrchestratorResponse(
            orchestrator_status=_llm_orchestrator_state["status"],
            active_operations=_llm_orchestrator_state["active_operations"][-5:],  # Last 5 active ops
            recent_activities=recent_activities,
            loaded_prompts=_llm_orchestrator_state["loaded_prompts"],
            last_activity=_llm_orchestrator_state["last_activity"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve LLM orchestrator status: {str(e)}"
        )


@router.post("/trace-logs/test")
async def add_test_trace_entry(
    calc_id: str = "CAL-PIT-001",
    entity_id: str = "person_1",
    field: str = "tax_payable",
    explanation: str = "Test trace entry for debugging"
):
    """
    Add a test trace entry for debugging purposes.
    """
    try:
        test_entry = TraceEntry(
            calc_id=calc_id,
            entity_id=entity_id,
            field=field,
            explanation=explanation,
            metadata={
                "test_entry": True,
                "timestamp": datetime.utcnow().isoformat(),
                "source": "debug_endpoint"
            }
        )

        add_trace_entry(test_entry)

        return {
            "message": "Test trace entry added successfully",
            "entry": test_entry.dict(),
            "total_entries": len(_trace_logs)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add test trace entry: {str(e)}"
        )


@router.post("/llm/test-activity")
async def add_test_llm_activity(
    activity_type: str = "intent_recognition",
    details: Optional[Dict[str, Any]] = None
):
    """
    Add a test LLM activity for debugging purposes.
    """
    try:
        if details is None:
            details = {"test": True, "timestamp": datetime.utcnow().isoformat()}

        add_llm_activity(activity_type, details)

        return {
            "message": f"Test {activity_type} activity added successfully",
            "activity": {
                "type": activity_type,
                "details": details,
                "timestamp": datetime.utcnow().isoformat()
            },
            "total_activities": len(_llm_activities)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add test LLM activity: {str(e)}"
        )


@router.delete("/llm/activities")
async def clear_llm_activities():
    """
    Clear all LLM activity records.
    """
    try:
        global _llm_activities, _llm_orchestrator_state
        cleared_count = len(_llm_activities)
        _llm_activities = []
        _llm_orchestrator_state = {
            "status": "idle",
            "active_operations": [],
            "loaded_prompts": 0,
            "last_activity": None
        }

        return {
            "message": f"Cleared {cleared_count} LLM activity records",
            "cleared_count": cleared_count,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear LLM activities: {str(e)}"
        )


@router.get("/llm/operation-metrics", response_model=LLMOperationMetricsResponse)
async def get_llm_operation_metrics():
    """
    Get LLM operation metrics and counts.
    """
    try:
        global _llm_operation_counts
        return LLMOperationMetricsResponse(
            intent_recognition={
                "count": _llm_operation_counts["intent_recognition"],
                "status": "active" if _llm_operation_counts["intent_recognition"] > 0 else "idle"
            },
            state_hydration={
                "count": _llm_operation_counts["state_hydration"],
                "status": "active" if _llm_operation_counts["state_hydration"] > 0 else "idle"
            },
            narrative_generation={
                "count": _llm_operation_counts["narrative_generation"],
                "status": "active" if _llm_operation_counts["narrative_generation"] > 0 else "idle"
            },
            privacy_filter={
                "pii_detected": _llm_operation_counts["privacy_filter"],
                "status": "active" if _llm_operation_counts["privacy_filter"] > 0 else "idle"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve LLM operation metrics: {str(e)}"
        )


@router.get("/llm/privacy-stats", response_model=LLMPrivacyStatsResponse)
async def get_llm_privacy_stats():
    """
    Get LLM privacy filtering statistics.
    """
    try:
        global _llm_privacy_stats
        return LLMPrivacyStatsResponse(**_llm_privacy_stats)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve LLM privacy stats: {str(e)}"
        )


@router.get("/llm/performance-metrics", response_model=LLMPerformanceMetricsResponse)
async def get_llm_performance_metrics():
    """
    Get LLM performance metrics.
    """
    try:
        global _llm_performance_metrics
        return LLMPerformanceMetricsResponse(**_llm_performance_metrics)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve LLM performance metrics: {str(e)}"
        )


@router.get("/llm/realtime-activities", response_model=LLMRealtimeActivitiesResponse)
async def get_llm_realtime_activities():
    """
    Get real-time LLM activities.
    """
    try:
        global _llm_activities, _llm_orchestrator_state

        # Get recent activities (last 10)
        recent_activities = _llm_activities[-10:] if _llm_activities else []

        # Add some mock active operations if orchestrator is active
        activities = []
        if _llm_orchestrator_state["status"] == "active":
            # Simulate a currently running operation
            activities.append({
                "type": _llm_orchestrator_state["last_activity"] or "intent_recognition",
                "operation_id": f"active_{datetime.utcnow().timestamp()}",
                "status": "running",
                "description": "Processing user query...",
                "timestamp": datetime.utcnow().isoformat()
            })

        # Add recent completed activities
        activities.extend(recent_activities)

        return LLMRealtimeActivitiesResponse(activities=activities[-10:])  # Last 10 total
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve LLM realtime activities: {str(e)}"
        )


@router.get("/llm/prompt-management", response_model=LLMPromptManagementResponse)
async def get_llm_prompt_management():
    """
    Get prompt management statistics.
    """
    try:
        global _llm_prompt_stats
        # Ensure last_updated is a string
        prompt_stats = _llm_prompt_stats.copy()
        if prompt_stats["last_updated"] is None:
            prompt_stats["last_updated"] = datetime.utcnow().isoformat()

        return LLMPromptManagementResponse(**prompt_stats)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve LLM prompt management data: {str(e)}"
        )


@router.get("/llm/trace-logs", response_model=LLMTraceLogsResponse)
async def get_llm_trace_logs(limit: int = 50):
    """
    Get LLM-specific trace logs.
    """
    try:
        global _trace_logs

        if not SERVICES_AVAILABLE or TraceEntry is None:
            return LLMTraceLogsResponse(
                entries=[],
                total_count=0,
                last_updated=datetime.utcnow().isoformat()
            )

        # Filter for LLM-related traces
        llm_traces = [
            entry for entry in _trace_logs
            if entry.entity_id == "llm_orchestrator" or
               entry.calc_id.startswith(("intent_", "state_", "narrative_")) or
               "llm" in entry.calc_id.lower()
        ]

        # Return most recent entries first
        entries = llm_traces[-limit:] if llm_traces else []

        return LLMTraceLogsResponse(
            entries=entries,
            total_count=len(llm_traces),
            last_updated=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve LLM trace logs: {str(e)}"
        )


@router.delete("/llm/trace-logs")
async def clear_llm_trace_logs():
    """
    Clear LLM-specific trace logs.
    """
    try:
        global _trace_logs

        if not SERVICES_AVAILABLE:
            return {
                "message": "LLM trace logs not available",
                "cleared_count": 0,
                "timestamp": datetime.utcnow().isoformat()
            }

        # Count LLM traces before clearing
        llm_traces_count = len([
            entry for entry in _trace_logs
            if entry.entity_id == "llm_orchestrator" or
               entry.calc_id.startswith(("intent_", "state_", "narrative_")) or
               "llm" in entry.calc_id.lower()
        ])

        # Remove LLM traces
        _trace_logs = [
            entry for entry in _trace_logs
            if not (entry.entity_id == "llm_orchestrator" or
                   entry.calc_id.startswith(("intent_", "state_", "narrative_")) or
                   "llm" in entry.calc_id.lower())
        ]

        return {
            "message": f"Cleared {llm_traces_count} LLM trace log entries",
            "cleared_count": llm_traces_count,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear LLM trace logs: {str(e)}"
        )
