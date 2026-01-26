# Sentinel — Database Design (PostgreSQL)

---

## 1. Purpose of This Document

This document defines the conceptual database design for Sentinel.

The database is not merely storage — it is Sentinel’s persistent memory of reality, reasoning, decisions, and outcomes.

This design prioritizes:

- Correctness
- Traceability
- Replayability
- Observability
- Agentic learning

---

## 2. Core Database Philosophy

### 2.1 Database as Source of Truth

PostgreSQL is the single authoritative source for Sentinel’s state.

No agent, interface, or tool maintains private truth.

---

### 2.2 Append-First, Mutate Carefully

Sentinel prefers:

- Appending new records
- Recording transitions explicitly
- Avoiding destructive updates

History matters more than convenience.

---

### 2.3 Agent- and Graph-Aware

Every meaningful record must be attributable to:

- An agent
- A graph run
- A state transition

This enables deep inspection and learning.

---

## 3. Database Domains (High-Level)

Sentinel’s database is organized into seven conceptual domains:

1. Accounts & Sources
2. Observations
3. Proposals
4. Human Decisions
5. Actions & Execution
6. Orchestration (LangGraph)
7. Preferences & System Metadata

Each domain is described below.

---

## 4. Accounts & Sources

**Purpose:**  
Track external data sources (not users).

Sentinel is single-user, but multi-source.

### Entity: Account

**Represents:**  
An external system connection.

**Conceptual Fields:**

- `account_id`
- `account_type` (gmail, calendar, health)
- `label` (personal, work, etc.)
- `external_identifier`
- `status` (active, revoked)
- `created_at`

**Notes:**

- No user table exists
- Accounts only describe data origin

---

## 5. Observations (Facts from Reality)

**Purpose:**  
Store raw facts observed from external systems.

Observations are immutable.

### Entity: Observation

**Conceptual Fields:**

- `observation_id`
- `account_id`
- `observation_type` (email, calendar_event, health_metric)
- `external_reference` (e.g., Gmail message ID)
- `observed_at`
- `raw_payload` (sanitized)
- `processed_flag`

**Key Rules:**

- Observations are never modified
- Reprocessing is allowed, mutation is not
- Observations precede all reasoning

---

## 6. Proposals (Agent Intent)

**Purpose:**  
Capture what agents want to do, not what happens.

This is the heart of Sentinel’s agentic design.

### Entity: Proposal

**Conceptual Fields:**

- `proposal_id`
- `observation_id`
- `agent_name`
- `proposal_type` (task, reminder, reschedule, delete, etc.)
- `proposed_payload` (structured JSON)
- `confidence_score`
- `risk_level` (low, medium, high)
- `requires_human` (boolean)
- `status` (pending, approved, rejected, expired)
- `created_at`

**Key Rules:**

- Proposals never execute themselves
- Proposals may expire
- Multiple proposals may stem from one observation

---

## 7. Human Decisions (Human-in-the-Loop)

**Purpose:**  
Record explicit human authority over agent intent.

### Entity: HumanDecision

**Conceptual Fields:**

- `decision_id`
- `proposal_id`
- `decision` (approve, reject, modify)
- `modified_payload` (optional)
- `channel` (frontend, telegram)
- `decision_latency`
- `decided_at`

**Key Rules:**

- Every impactful action must trace back to a decision
- Human decisions are final
- Decisions are immutable once recorded

---

## 8. Actions & Execution (Reality Changes)

**Purpose:**  
Track what actually happened in the real world.

### Entity: Action

**Conceptual Fields:**

- `action_id`
- `proposal_id`
- `executor_agent`
- `action_type`
- `final_payload`
- `execution_status` (success, failure, rollback)
- `execution_started_at`
- `execution_finished_at`
- `error_details` (optional)

**Key Rules:**

- Actions only occur after approval
- Failed actions are first-class events
- Retries are explicit, not implicit

---

## 9. Orchestration (LangGraph Persistence)

**Purpose:**  
Persist LangGraph execution context.

Graphs are stateful and must survive restarts.

### Entity: GraphRun

**Conceptual Fields:**

- `graph_run_id`
- `trigger_type` (scheduled, manual, api)
- `initial_state`
- `current_state`
- `status` (running, paused, completed, failed)
- `started_at`
- `finished_at`

### Entity: GraphStateTransition

**Conceptual Fields:**

- `transition_id`
- `graph_run_id`
- `from_state`
- `to_state`
- `cause` (agent, human, failure)
- `caused_by` (agent_name or channel)
- `transitioned_at`

**Key Rules:**

- All transitions are logged
- No implicit jumps between states

---

## 10. Preferences & System Metadata

**Purpose:**  
Store long-lived configuration, not observations.

### Entity: Preference

**Conceptual Fields:**

- `preference_key`
- `preference_value`
- `scope` (global, agent-specific)
- `updated_at`

**Rules:**

- Agents may read preferences
- Only humans modify preferences
- Preferences are versioned implicitly by time

---

## 11. Relationship Overview

```
Account
  └── Observation
        └── Proposal (by Agent)
              └── HumanDecision
                    └── Action (by Executor)

GraphRun
  └── GraphStateTransition
```

This chain guarantees:

- Explainability
- Auditability
- Replayability

---

## 12. Observability Correlation (Langfuse)

Each of the following entities may optionally store:

- `trace_id`
- `span_id`

This allows correlation between:

- Database state
- Agent reasoning
- Graph execution
- LLM cost and latency

---

## 13. Explicit Non-Goals (V1)

The database does not include:

- Vector embeddings
- Semantic memory
- Analytics aggregates
- Caches
- Derived summaries

These are computed, not stored.

---

## 14. Failure & Recovery Philosophy

Failures are:

- Stored
- Attributed
- Analyzable

Silent failure is considered data corruption.

---

## 15. Guiding Database Question

For every schema decision:

> “Can this explain why Sentinel behaved the way it did?”

If the answer is no, the schema is insufficient.
