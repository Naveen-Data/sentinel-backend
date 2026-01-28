"""
Sentinel Base Agent

This module defines the base class for all Sentinel agents.

Design principles:
- Agents propose, they do not execute
- All outputs are structured
- All executions are observable
- Single responsibility per agent
"""

from typing import Any, Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field

from app.logger import get_logger

logger = get_logger(__name__)


class AgentConfig(BaseModel):
    """
    Configuration for a Sentinel agent.
    
    Standardizes agent initialization across all agent types.
    """
    
    model: str = Field(
        default="gpt-4",
        description="LLM model to use for this agent",
    )
    
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Temperature for LLM responses",
    )
    
    verbose: bool = Field(
        default=True,
        description="Whether to log detailed agent execution",
    )
    
    max_iterations: int = Field(
        default=3,
        ge=1,
        description="Maximum iterations for agent reasoning",
    )


class ProposalOutput(BaseModel):
    """
    Structured output from an agent's analysis.
    
    All agents must return proposals in this format.
    """
    
    proposal_type: str = Field(
        ...,
        description="Type of proposal (create_task, send_email, etc.)",
    )
    
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Agent's confidence in this proposal (0.0 to 1.0)",
    )
    
    reasoning: str = Field(
        ...,
        description="Agent's explanation for this proposal",
    )
    
    proposed_action: dict = Field(
        ...,
        description="Structured action definition",
    )
    
    metadata: dict = Field(
        default_factory=dict,
        description="Additional proposal metadata",
    )


class BaseAgent(ABC):
    """
    Abstract base class for all Sentinel agents.
    
    All agents must:
    - Have a clear role and responsibility
    - Return structured proposals
    - Be observable
    - Not have side effects (except Executor, under constraints)
    """
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.logger = get_logger(self.__class__.__name__)
    
    @property
    @abstractmethod
    def role(self) -> str:
        """
        Agent's role definition.
        
        This should be a clear, one-sentence description.
        """
        pass
    
    @property
    @abstractmethod
    def goal(self) -> str:
        """
        Agent's goal.
        
        What is this agent trying to achieve?
        """
        pass
    
    @property
    @abstractmethod
    def backstory(self) -> str:
        """
        Agent's backstory and constraints.
        
        This provides context and boundaries for the agent's behavior.
        """
        pass
    
    @abstractmethod
    async def analyze(self, input_data: Any) -> ProposalOutput:
        """
        Primary analysis method.
        
        This is where the agent performs its reasoning and returns a proposal.
        
        Args:
            input_data: Input for the agent (structure varies by agent)
            
        Returns:
            ProposalOutput: Structured proposal with confidence
        """
        pass
    
    def log_execution(self, message: str, **kwargs) -> None:
        """
        Log agent execution with standard format.
        """
        self.logger.info(
            message,
            extra={
                "agent": self.__class__.__name__,
                **kwargs,
            },
        )
