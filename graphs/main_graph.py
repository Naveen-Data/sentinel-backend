"""
Sentinel Main LangGraph Definition

This module defines the primary state machine that orchestrates all Sentinel behavior.

The graph:
- Enforces state transitions
- Pauses for human approval
- Coordinates agents
- Handles failures

This is Sentinel's control plane.
"""

from typing import TypedDict, Annotated, Sequence
from uuid import UUID

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from graphs.states import SentinelState
from app.logger import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------
# Graph State Definition
# ---------------------------------------------------------------------

class SentinelGraphState(TypedDict):
    """
    State object that flows through the Sentinel graph.
    
    This represents all context needed for decision-making.
    """
    
    # Identifiers
    graph_run_id: str
    observation_id: str
    
    # Current state
    current_state: str
    
    # Data
    observation_data: dict
    proposals: list[dict]
    selected_proposal: dict | None
    human_decision: dict | None
    execution_result: dict | None
    
    # Metadata
    errors: list[str]
    metadata: dict


# ---------------------------------------------------------------------
# Node Functions (Stubs)
# ---------------------------------------------------------------------

async def observe_node(state: SentinelGraphState) -> SentinelGraphState:
    """
    Initial observation node.
    
    This node captures facts from reality.
    """
    logger.info("Executing: observe_node")
    
    state["current_state"] = SentinelState.OBSERVED.value
    
    # TODO: Implement actual observation logic
    
    return state


async def analyze_node(state: SentinelGraphState) -> SentinelGraphState:
    """
    Agent analysis node.
    
    This node runs agents to analyze observations.
    """
    logger.info("Executing: analyze_node")
    
    state["current_state"] = SentinelState.ANALYZED.value
    
    # TODO: Run Inbox Agent, Context Agent, etc.
    
    return state


async def propose_node(state: SentinelGraphState) -> SentinelGraphState:
    """
    Proposal generation node.
    
    This node consolidates agent proposals.
    """
    logger.info("Executing: propose_node")
    
    state["current_state"] = SentinelState.PROPOSED.value
    
    # TODO: Collect and rank proposals
    
    return state


async def await_human_node(state: SentinelGraphState) -> SentinelGraphState:
    """
    Human approval node.
    
    This node PAUSES execution and waits for human input.
    """
    logger.info("Executing: await_human_node")
    
    state["current_state"] = SentinelState.AWAITING_HUMAN.value
    
    # TODO: Send notification to Web UI and Telegram
    # TODO: Pause graph execution
    
    return state


async def execute_node(state: SentinelGraphState) -> SentinelGraphState:
    """
    Action execution node.
    
    This node executes approved actions via Executor Agent.
    """
    logger.info("Executing: execute_node")
    
    state["current_state"] = SentinelState.EXECUTED.value
    
    # TODO: Run Executor Agent
    
    return state


# ---------------------------------------------------------------------
# Graph Construction
# ---------------------------------------------------------------------

def create_sentinel_graph() -> StateGraph:
    """
    Create and configure the Sentinel state machine.
    
    Returns:
        Compiled StateGraph ready for execution
    """
    logger.info("Building Sentinel graph")
    
    # Create graph
    workflow = StateGraph(SentinelGraphState)
    
    # Add nodes
    workflow.add_node("observe", observe_node)
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("propose", propose_node)
    workflow.add_node("await_human", await_human_node)
    workflow.add_node("execute", execute_node)
    
    # Define edges (state transitions)
    workflow.set_entry_point("observe")
    workflow.add_edge("observe", "analyze")
    workflow.add_edge("analyze", "propose")
    workflow.add_edge("propose", "await_human")
    
    # Conditional edge from await_human (approved vs rejected)
    # TODO: Add conditional routing based on human decision
    workflow.add_edge("await_human", "execute")
    workflow.add_edge("execute", END)
    
    # Compile with memory (for pause/resume)
    memory = MemorySaver()
    graph = workflow.compile(checkpointer=memory)
    
    logger.info("Sentinel graph built successfully")
    
    return graph


# ---------------------------------------------------------------------
# Graph Execution
# ---------------------------------------------------------------------

async def run_sentinel_graph(
    graph_run_id: UUID,
    observation_id: UUID,
    observation_data: dict,
) -> dict:
    """
    Execute the Sentinel graph for an observation.
    
    Args:
        graph_run_id: Unique identifier for this run
        observation_id: Which observation triggered this
        observation_data: The observation content
        
    Returns:
        Final state after execution
    """
    logger.info(f"Starting Sentinel graph run: {graph_run_id}")
    
    graph = create_sentinel_graph()
    
    initial_state: SentinelGraphState = {
        "graph_run_id": str(graph_run_id),
        "observation_id": str(observation_id),
        "current_state": SentinelState.OBSERVED.value,
        "observation_data": observation_data,
        "proposals": [],
        "selected_proposal": None,
        "human_decision": None,
        "execution_result": None,
        "errors": [],
        "metadata": {},
    }
    
    # Execute graph
    final_state = await graph.ainvoke(
        initial_state,
        config={"configurable": {"thread_id": str(graph_run_id)}},
    )
    
    logger.info(f"Graph run completed: {graph_run_id}")
    
    return final_state
