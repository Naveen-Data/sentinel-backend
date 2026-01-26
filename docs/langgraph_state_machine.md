# Sentinel — LangGraph State Machine

## 1. Purpose of This Document

This document defines the explicit state machine that governs all decision-making in Sentinel.

Sentinel is not event-driven and not chat-driven.  
Sentinel is state-driven.

Every meaningful behavior in Sentinel must be explainable as:

- A state
- A transition
- A cause
- An outcome

If something happens outside this model, it is a bug.

---

## 2. Why a State Machine Is Mandatory

Agentic systems fail when:

- Decisions happen implicitly
- Actions occur without checkpoints
- Humans are bypassed
- Failures are hidden

The LangGraph state machine ensures:

- Determinism
- Replayability
- Human authority
- Safe recovery

LangGraph is Sentinel’s control plane.

---

## 3. Core Design Principles

### 3.1 Explicit Over Implicit

Every step must be a named state.

### 3.2 No Hidden Transitions

State changes only occur via defined transitions.

### 3.3 Human-in-the-Loop Is a State

Human approval is not a callback — it is a first-class state.

### 3.4 Failure Is a State

Failures are modeled, not swallowed.

---

## 4. Canonical States (V1)

Sentinel defines the following canonical states:

```
OBSERVED
→ ANALYZED
→ PROPOSED
→ AWAITING_HUMAN
→ APPROVED | REJECTED
→ EXECUTED
→ COMPLETED | FAILED
```

Each state is described below.

---

## 5. State Definitions

### 5.1 OBSERVED

**Meaning:**  
Raw facts have been captured from reality.

**Entry Conditions:**

- New email
- Calendar change
- Health data update
- Manual trigger

**Allowed Actions:**

- Persist observations
- Schedule analysis

**Forbidden Actions:**

- Agent reasoning
- Proposal generation
- Execution

This state represents truth, not interpretation.

---

### 5.2 ANALYZED

**Meaning:**  
Agents are reasoning over observations.

**Agents Involved:**

- Inbox Agent
- Planner Agent
- Health Agent

**Allowed Actions:**

- Classification
- Context enrichment
- Risk assessment

**Outputs:**

- Structured analysis artifacts
- No proposals yet

This state answers:  
“What does this mean?”

---

### 5.3 PROPOSED

**Meaning:**  
Agents have generated explicit proposals.

**Agents Involved:**

- Inbox Agent
- Planner Agent
- Critic Agent

**Allowed Actions:**

- Proposal creation
- Confidence scoring
- Risk tagging

**Rules:**

- Multiple proposals may exist
- Proposals are immutable once stored

This state answers:  
“What could be done?”

---

### 5.4 AWAITING_HUMAN

**Meaning:**  
System is paused, waiting for human authority.

**Triggers:**

- Proposal marked `requires_human = true`
- Critic Agent flags risk

**Interfaces:**

- Web frontend
- Telegram bot

**Allowed Actions:**

- Display proposals
- Collect approval / rejection / modification

**Forbidden Actions:**

- Execution
- Auto-advancement

Time stops here until a human acts.

---

### 5.5 APPROVED

**Meaning:**  
Human has explicitly approved a proposal.

**Entry Conditions:**

- Approval decision recorded

**Allowed Actions:**

- Action preparation
- Execution scheduling

**Rules:**

- Approval is final
- Payload may be modified by human

This state grants permission, not execution.

---

### 5.6 REJECTED

**Meaning:**  
Human has rejected a proposal.

**Allowed Actions:**

- Log rejection
- Optionally loop back to PROPOSED with changes

**Terminal by Default:**  
Unless explicitly re-opened by human.

---

### 5.7 EXECUTED

**Meaning:**  
Executor Agent has attempted execution.

**Agent Involved:**

- Executor Agent only

**Allowed Actions:**

- Tool invocation
- Result capture

**Rules:**

- One execution per approval
- No retries unless explicitly instructed

Execution is mechanical, not cognitive.

---

### 5.8 COMPLETED

**Meaning:**  
Execution succeeded.

**Actions:**

- Final logging
- Observability flush
- State archival

This is a terminal success state.

---

### 5.9 FAILED

**Meaning:**  
Execution failed or graph encountered an unrecoverable error.

**Causes:**

- Tool failure
- Validation failure
- System error

**Allowed Actions:**

- Error logging
- Human notification
- Optional retry proposal

Failure is visible, not silent.

---

## 6. Allowed Transitions

| From State   | To State       | Trigger                |
|--------------|----------------|------------------------|
| OBSERVED     | ANALYZED       | Scheduler / Trigger    |
| ANALYZED     | PROPOSED       | Agent completion       |
| PROPOSED     | AWAITING_HUMAN | Human required         |
| PROPOSED     | APPROVED       | Auto-approval (optional) |
| AWAITING_HUMAN | APPROVED      | Human approval         |
| AWAITING_HUMAN | REJECTED      | Human rejection        |
| APPROVED     | EXECUTED       | Executor start         |
| EXECUTED     | COMPLETED      | Success                |
| EXECUTED     | FAILED         | Failure                |
| FAILED       | PROPOSED       | Retry requested        |

No other transitions are permitted.

---

## 7. Human-in-the-Loop as a Control State

Human input:

- Pauses the graph
- Resumes deterministically
- Overrides agent intent

Humans are not interrupts — they are state transitions.

---

## 8. Failure & Recovery Paths

Failures must result in one of:

- Human-visible failure
- Retry proposal
- Explicit abandonment

There is no automatic retry loop.

---

## 9. Observability Requirements

For every graph run:

- Each state entry is logged
- Each transition is timestamped
- Cause of transition is recorded
- Associated agent(s) are recorded
- Langfuse trace IDs are attached

If a transition is not observable, it is invalid.

---

## 10. Invariants (Must Always Hold)

- Execution never occurs without approval
- Human decisions are final
- States never skip
- Terminal states are explicit
- Graph runs are replayable

Violation of invariants indicates a system defect.

---

## 11. Guiding Question

For every new state or transition:

> “Can a human understand why Sentinel moved here?”

If not, the state machine is incomplete.
