# Sentinel — Agent Roles & Responsibilities


## 1. Purpose of This Document

This document defines the explicit roles, boundaries, and responsibilities of every agent in Sentinel.

In Sentinel:

- Agents are thinking units
- Agents are not autonomous actors
- Agents propose, they do not execute
- Agents are observable and accountable

If an agent’s behavior cannot be described clearly in this document, it should not exist.

---

## 2. Agent Design Principles

### 2.1 Single Responsibility

Each agent has one primary cognitive responsibility.

### 2.2 No Side Effects

Agents:

- Do not mutate global state
- Do not execute tools directly (except Executor, under constraints)
- Do not communicate implicitly

### 2.3 Structured Outputs

Every agent produces:

- A structured proposal or analysis
- A confidence estimate
- Optional reasoning metadata

### 2.4 Observability First

Every agent run must be:

- Traceable
- Measurable
- Replayable

Agents never act invisibly.

---

## 3. Core Agents (V1)

### 📩 3.1 Inbox Agent

**Role:**  
Email & Notification Intelligence Analyst

**Primary Responsibility:**  
Understand incoming communications and determine whether they require attention or action.

**Inputs:**

- Email observations
- Sender metadata
- Subject and body excerpts
- Historical context (read-only)

**Outputs:**

- Task proposals
- Reminder proposals
- Ignore classifications
- Confidence score per proposal

**Decisions This Agent CAN Make:**

- Is this actionable?
- Does this imply a task or reminder?
- Is this informational or noise?

**Decisions This Agent CANNOT Make:**

- When to schedule work
- Whether an action should be executed
- Whether something is deleted

**Failure Modes (Expected):**

- Over-classification (too many tasks)
- Under-classification (missed signals)

These failures are handled by:

- Planner Agent
- Human review

---

### 🗂️ 3.2 Planner Agent

**Role:**  
Task & Priority Strategist

**Primary Responsibility:**  
Determine what matters now, given limited time and capacity.

**Inputs:**

- Task proposals
- Existing tasks
- Calendar context
- Health-derived energy signals (read-only)

**Outputs:**

- Prioritized task lists
- Scheduling suggestions
- Escalation recommendations
- Confidence and urgency scores

**Decisions This Agent CAN Make:**

- Relative task importance
- Deadline risk detection
- Overload identification

**Decisions This Agent CANNOT Make:**

- Execute scheduling changes
- Override human preferences
- Delete or modify external data

**Failure Modes:**

- Over-prioritization
- Conservative scheduling

Handled by:

- Critic Agent
- Human approval

---

### 💤 3.3 Health Agent

**Role:**  
Energy & Capacity Estimator

**Primary Responsibility:**  
Estimate human capacity based on health signals.

**Inputs:**

- Sleep duration
- Sleep quality
- Recent activity (if available)

**Outputs:**

- Daily energy score
- Capacity constraints
- Scheduling modifiers

**Decisions This Agent CAN Make:**

- Energy level estimation
- Capacity warnings

**Decisions This Agent CANNOT Make:**

- Task prioritization
- Action approval
- Scheduling execution

**Failure Modes:**

- Noisy health data
- Overconfidence in estimates

Health data always acts as a soft constraint, never a hard rule.

---

### 🧑‍⚖️ 3.4 Critic Agent

**Role:**  
Decision Auditor & Skeptic

**Primary Responsibility:**  
Critically evaluate proposals made by other agents.

**Inputs:**

- Proposals from Inbox / Planner / Health agents
- Historical outcomes
- Confidence scores

**Outputs:**

- Approval flags
- Risk warnings
- Recommendation to defer to human

**Decisions This Agent CAN Make:**

- Flag inconsistencies
- Detect overconfidence
- Recommend human intervention

**Decisions This Agent CANNOT Make:**

- Approve execution
- Modify proposals directly
- Override humans

**Why This Agent Exists:**

The Critic Agent exists to:

- Reduce blind trust in LLMs
- Surface edge cases
- Teach self-evaluation in agent systems

This agent is essential for learning agentic AI.

---

### ⚙️ 3.5 Executor Agent

**Role:**  
Constrained Action Executor

**Primary Responsibility:**  
Execute explicitly approved actions safely and deterministically.

**Inputs:**

- Approved action payloads
- Execution instructions
- Tool references

**Outputs:**

- Execution result
- Success / failure status
- Error details (if any)

**Rules (Non-Negotiable):**

- Executor performs no reasoning
- Executor executes exactly one action
- Executor requires explicit approval
- Executor logs everything

**Decisions This Agent CANNOT Make:**

- Whether to execute
- How to interpret intent
- Whether to retry without instruction

The Executor Agent is intentionally “dumb.”

---

## 4. Agent Interaction Model

Agents do not call each other directly.

All coordination happens via:

- LangGraph orchestration
- Structured proposals
- Shared persistent state

This prevents:

- Hidden feedback loops
- Unbounded recursion
- Non-deterministic behavior

---

## 5. Human as an Agent (Conceptual)

Humans are treated as a special agent with:

- Ultimate authority
- Zero automation
- Explicit decision points

Human decisions are:

- Logged
- Measured
- Respected absolutely

---

## 6. Adding New Agents (Future Rule)

A new agent may only be added if:

1. Its responsibility cannot be fulfilled by an existing agent
2. Its inputs and outputs are clearly defined
3. Its failure modes are understood
4. It improves observability or safety

Otherwise, it does not belong.

---

## 7. Guiding Question for Agent Design

For every agent:

> “If this agent makes a mistake, will Sentinel fail safely and visibly?”

If the answer is no, the agent must be redesigned.


