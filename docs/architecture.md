# Sentinel — System Architecture


## 1. Architectural Goal

Sentinel is designed as a stateful, agentic decision system with:

- Explicit control flow
- Human-in-the-loop enforcement
- Strong separation of concerns
- Full observability
- Correctness over autonomy

This document defines how Sentinel is structured, not how it is implemented.

---

## 2. High-Level Architecture

Sentinel follows a layered architecture where each layer has a single responsibility and clear boundaries.

```
┌─────────────────────────────┐
│        Human Interfaces     │
│  (Web UI + Telegram Bot)    │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│        API Gateway          │
│          (FastAPI)          │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│     Orchestration Layer     │
│        (LangGraph)          │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│      Agent Reasoning        │
│        (CrewAI Agents)      │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│      Deterministic Tools    │
│ (Email, Calendar, Health)   │
└──────────────┬──────────────┘
               │
┌──────────────▼──────────────┐
│     Reality & State Store   │
│        (PostgreSQL)         │
└─────────────────────────────┘
```

Observability via Langfuse spans all layers.

---

## 3. Core Architectural Principles

### 3.1 Single Source of Truth

PostgreSQL is the authoritative record for:

- Observations
- Proposals
- Human decisions
- Executed actions
- State transitions

No other system mutates reality directly.

---

### 3.2 Agents Propose, Systems Decide

CrewAI agents:

- Analyze inputs
- Generate proposals
- Assign confidence and risk

They do not execute actions.

LangGraph:

- Decides control flow
- Enforces approvals
- Manages retries and failures

---

### 3.3 Human-in-the-Loop Is Mandatory

All impactful actions pass through an explicit approval state unless explicitly configured otherwise.

Human input is:

- Logged
- Time-measured
- Correlated with agent confidence

---

### 3.4 Explicit State Machines

Sentinel is driven by state transitions, not implicit behavior.

Every workflow has:

- A known starting state
- Allowed transitions
- Terminal outcomes

This enables replay, debugging, and learning.

---

## 4. Layer-by-Layer Breakdown

### 4.1 Human Interface Layer

**Purpose:**  
Allow humans to inspect, approve, reject, or modify agent proposals.

**Components:**

- Web frontend (control plane)
- Telegram bot (fast approvals)

**Responsibilities:**

- Display proposals and reasoning
- Collect decisions
- Send commands to backend

**Non-Responsibilities:**

- No LLM calls
- No direct tool execution
- No business logic

---

### 4.2 API Gateway Layer (FastAPI)

**Purpose:**  
Act as the single ingress point into Sentinel.

**Responsibilities:**

- Authenticate requests
- Validate inputs
- Route commands into LangGraph
- Expose read-only system state

**Design Rule:**  
The API layer is intentionally thin.

---

### 4.3 Orchestration Layer (LangGraph)

**Purpose:**  
Control the lifecycle of decisions.

**Responsibilities:**

- Define workflow states
- Run agents in sequence or parallel
- Pause for human input
- Resume execution
- Handle failure paths

LangGraph is the control plane of Sentinel.

---

### 4.4 Agent Layer (CrewAI)

**Purpose:**  
Perform reasoning and analysis.

**Key Agents (Initial):**

- Inbox Agent
- Planner Agent
- Health Agent
- Critic Agent
- Executor Agent (constrained)

**Rules:**

- Agents do not share mutable state directly
- Agents communicate via structured outputs
- Agents never execute tools without approval

---

### 4.5 Tool Layer

**Purpose:**  
Bridge Sentinel to external systems deterministically.

**Examples:**

- Gmail adapter
- Calendar adapter
- Health data reader
- Notification sender

**Rules:**

- No reasoning
- No branching
- Deterministic inputs → outputs

---

### 4.6 Persistence Layer (PostgreSQL)

**Purpose:**  
Store facts, decisions, and outcomes.

**Stored Concepts:**

- Observations (what happened)
- Proposals (what agents want)
- Decisions (what humans chose)
- Actions (what was executed)
- Graph runs (how it flowed)

This enables replay, auditing, and learning.

---

### 4.7 Observability Layer (Langfuse)

**Purpose:**  
Make Sentinel explainable and debuggable.

**Tracked:**

- Agent prompts and outputs
- Token usage and cost
- Graph transitions
- Human overrides
- Execution success/failure

Observability is not optional.

---

## 5. Data Flow Summary

1. Reality produces observations
2. Observations are stored
3. Agents analyze observations
4. Proposals are generated
5. LangGraph evaluates next steps
6. Human approval is requested
7. Approved actions are executed
8. Outcomes are logged
9. Observability spans all steps

---

## 6. Failure Handling Philosophy

Failures are:

- Expected
- Explicit
- Logged
- Recoverable

Silent failure is considered a design defect.

---

## 7. Architectural Non-Goals

Sentinel does not aim to:

- Be real-time
- Be autonomous
- Be multi-tenant
- Be highly optimized initially

It aims to be understandable, safe, and observable.

---

## 8. Guiding Architectural Question

For every architectural change:

> “Does this preserve explicit control, state clarity, and human authority?”

If not, it does not belong in Sentinel.


