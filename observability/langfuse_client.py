"""
Sentinel Langfuse Integration

This module provides Langfuse client initialization and tracing utilities.

Design principles:
- Centralized client management
- Lazy initialization
- Context managers for traces
- No observability should block business logic
"""

from typing import Optional, Any
from contextlib import contextmanager
from uuid import UUID

from langfuse import Langfuse
from langfuse import observe

from app.config import get_settings
from app.logger import get_logger

logger = get_logger(__name__)

_langfuse_client: Optional[Langfuse] = None


def get_langfuse_client() -> Optional[Langfuse]:
    """
    Get or initialize the Langfuse client.
    
    Returns None if observability is disabled or not configured.
    This allows graceful degradation.
    """
    global _langfuse_client
    
    settings = get_settings()
    
    if not settings.enable_observability:
        logger.debug("Observability is disabled")
        return None
    
    if _langfuse_client is not None:
        return _langfuse_client
    
    # Initialize Langfuse
    if not settings.langfuse_public_key or not settings.langfuse_secret_key:
        logger.warning(
            "Langfuse credentials not configured; observability will be disabled"
        )
        return None
    
    try:
        _langfuse_client = Langfuse(
            public_key=settings.langfuse_public_key,
            secret_key=settings.langfuse_secret_key,
            host=settings.langfuse_host,
        )
        logger.info("Langfuse client initialized successfully")
        return _langfuse_client
    except Exception as e:
        logger.error(f"Failed to initialize Langfuse client: {e}")
        return None


@contextmanager
def trace_graph_run(
    graph_run_id: UUID,
    trigger_type: str,
    metadata: Optional[dict] = None,
):
    """
    Context manager for tracing a complete graph run.
    
    Usage:
        with trace_graph_run(graph_run_id, "scheduled") as trace:
            # Execute graph
            trace.update(output=final_state)
    """
    client = get_langfuse_client()
    
    if client is None:
        # Observability disabled, yield dummy object
        class DummyTrace:
            def update(self, **kwargs):
                pass
        
        yield DummyTrace()
        return
    
    trace = client.trace(
        id=str(graph_run_id),
        name="sentinel_graph_run",
        metadata={
            "trigger_type": trigger_type,
            **(metadata or {}),
        },
    )
    
    try:
        yield trace
    except Exception as e:
        trace.update(
            output={"error": str(e)},
            level="ERROR",
        )
        raise
    finally:
        # Flush to ensure data is sent
        client.flush()


@contextmanager
def trace_agent_execution(
    trace_id: str,
    agent_name: str,
    task_description: str,
    metadata: Optional[dict] = None,
):
    """
    Context manager for tracing an agent's execution.
    
    Usage:
        with trace_agent_execution(trace_id, "inbox_agent", "Analyze email") as span:
            result = agent.execute()
            span.update(output=result)
    """
    client = get_langfuse_client()
    
    if client is None:
        class DummySpan:
            def update(self, **kwargs):
                pass
        
        yield DummySpan()
        return
    
    span = client.span(
        trace_id=trace_id,
        name=agent_name,
        metadata={
            "task": task_description,
            **(metadata or {}),
        },
    )
    
    try:
        yield span
    except Exception as e:
        span.update(
            output={"error": str(e)},
            level="ERROR",
        )
        raise
    finally:
        span.end()
        client.flush()


def shutdown_langfuse() -> None:
    """
    Flush and shutdown Langfuse client.
    
    Should be called on application shutdown.
    """
    global _langfuse_client
    
    if _langfuse_client is not None:
        logger.info("Flushing Langfuse client")
        _langfuse_client.flush()
        _langfuse_client = None
