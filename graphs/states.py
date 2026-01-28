"""
Sentinel LangGraph States

This module defines all canonical states in Sentinel's state machine.

States represent:
- Where Sentinel is in its decision lifecycle
- What can happen next
- What has already happened

Every state must be explicitly defined here.
"""

import enum


class SentinelState(str, enum.Enum):
    """
    Canonical states in Sentinel's decision lifecycle.
    
    State flow:
    OBSERVED → ANALYZED → PROPOSED → AWAITING_HUMAN → APPROVED/REJECTED → EXECUTED → COMPLETED/FAILED
    
    Principles:
    - Explicit over implicit
    - No hidden transitions
    - Human-in-the-loop is a state
    - Failure is a state
    """
    
    # Initial States
    OBSERVED = "OBSERVED"
    
    # Processing States
    ANALYZED = "ANALYZED"
    PROPOSED = "PROPOSED"
    
    # Human-in-the-Loop States
    AWAITING_HUMAN = "AWAITING_HUMAN"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    
    # Execution States
    SCHEDULED = "SCHEDULED"
    EXECUTING = "EXECUTING"
    EXECUTED = "EXECUTED"
    
    # Terminal States
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    IGNORED = "IGNORED"


class AgentRole(str, enum.Enum):
    """
    Agent identities in Sentinel.
    
    Each agent has a single responsibility.
    """
    
    INBOX_AGENT = "inbox_agent"
    PLANNER_AGENT = "planner_agent"
    EXECUTOR_AGENT = "executor_agent"
    CONTEXT_AGENT = "context_agent"
    HEALTH_AGENT = "health_agent"
    CRITIC_AGENT = "critic_agent"


def get_allowed_transitions(from_state: SentinelState) -> list[SentinelState]:
    """
    Return allowed next states from a given state.
    
    This enforces the state machine invariants.
    """
    transitions = {
        SentinelState.OBSERVED: [SentinelState.ANALYZED, SentinelState.IGNORED],
        SentinelState.ANALYZED: [SentinelState.PROPOSED, SentinelState.IGNORED],
        SentinelState.PROPOSED: [SentinelState.AWAITING_HUMAN, SentinelState.SCHEDULED],
        SentinelState.AWAITING_HUMAN: [SentinelState.APPROVED, SentinelState.REJECTED],
        SentinelState.APPROVED: [SentinelState.SCHEDULED],
        SentinelState.REJECTED: [SentinelState.COMPLETED],
        SentinelState.SCHEDULED: [SentinelState.EXECUTING],
        SentinelState.EXECUTING: [SentinelState.EXECUTED, SentinelState.FAILED],
        SentinelState.EXECUTED: [SentinelState.COMPLETED],
        SentinelState.COMPLETED: [],  # Terminal
        SentinelState.FAILED: [],  # Terminal
        SentinelState.IGNORED: [],  # Terminal
    }
    
    return transitions.get(from_state, [])


def is_terminal_state(state: SentinelState) -> bool:
    """
    Check if a state is terminal (no further transitions).
    """
    terminal_states = {
        SentinelState.COMPLETED,
        SentinelState.FAILED,
        SentinelState.IGNORED,
    }
    
    return state in terminal_states
