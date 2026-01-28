"""
Sentinel Observability Layer

This module integrates Langfuse for full observability of agentic behavior.

Langfuse tracks:
- Agent reasoning
- Graph orchestration
- Human decisions
- Action execution
- LLM costs

If something cannot be observed, it is unsafe.
"""

from observability.langfuse_client import get_langfuse_client, trace_graph_run, trace_agent_execution

__all__ = [
    "get_langfuse_client",
    "trace_graph_run",
    "trace_agent_execution",
]
