# Sentinel — Observability & Tracing (Langfuse)

---

## 1. Purpose of This Document

This document defines how Sentinel observes itself.

In Sentinel:

- Observability is not optional
- Logs are not enough
- Metrics alone are insufficient

Sentinel uses Langfuse to make agentic behavior:

- Explainable
- Measurable
- Debuggable
- Learnable

If a decision cannot be observed, it is considered unsafe.

---

## 2. Observability Philosophy

### 2.1 Sentinel Is a Decision System

Observability focuses on decisions, not just execution.

We must be able to answer:

- Why did Sentinel do this?
- Which agent proposed it?
- What alternatives existed?
- Who approved it?
- What did it cost?
- What happened after execution?

---

### 2.2 Traces Over Logs

Traditional logs answer:

> “What happened?”

Langfuse traces answer:

> “What happened, in what context, and why?”

Sentinel prioritizes traces, spans, and events over raw logs.

---

## 3. What Langfuse Observes in Sentinel

Langfuse is integrated across four critical dimensions:

1. Agent Reasoning
2. LangGraph Orchestration
3. Human-in-the-Loop Decisions
4. Action Execution

Each is described below.

---

## 4. Trace Model (Top-Level)

### 4.1 Trace = One Sentinel Decision Lifecycle

A Langfuse Trace represents:

- One LangGraph run
- One end-to-end decision lifecycle
- One or more agent proposals
- Zero or more human interactions
- Zero or one execution attempt

**Trace Identifiers:**

Each trace is associated with:

- `graph_run_id`
- `trigger_type` (scheduled, manual, api)
- `start_time`
- `end_time`
- `overall_status`

This trace is the unit of analysis.

---

## 5. Agent Observability

### 5.1 Agent Spans

Each agent execution is recorded as a Langfuse Span.

**Captured Attributes:**

- `agent_name`
- `agent_role`
- `input_summary` (sanitized)
- `prompt_template_id`
- `model_name`
- `token_count`
- `latency`
- `confidence_score`

### 5.2 Why This Matters

This allows analysis such as:

- Which agent is most expensive?
- Which agent is most often overridden?
- Does confidence correlate with approval?

Agent reasoning must never be opaque.

---

## 6. LangGraph Orchestration Observability

### 6.1 State Transition Events

Each state transition emits a Langfuse Event.

**Captured Attributes:**

- `graph_run_id`
- `from_state`
- `to_state`
- `cause` (agent / human / failure)
- `caused_by` (agent_name or channel)
- `timestamp`

### 6.2 Graph-Level Spans

Each LangGraph node execution is wrapped in a span:

- Node name
- Duration
- Outcome (success / failure / paused)

This enables:

- Bottleneck detection
- Stalled state detection
- Recovery analysis

---

## 7. Human-in-the-Loop Observability

Human actions are first-class observability events.

### 7.1 Decision Events

Each human decision emits an event with:

- `proposal_id`
- `decision` (approve / reject / modify)
- `channel` (frontend / telegram)
- `decision_latency`
- `prior_agent_confidence`

### 7.2 Learning Value

This enables analysis such as:

- Where do humans most often intervene?
- Which agents humans trust least?
- Does UI vs Telegram affect decision speed?

Human behavior is part of the system, not noise.

---

## 8. Execution Observability

### 8.1 Execution Spans

Executor Agent actions are captured as spans.

**Captured Attributes:**

- `action_type`
- `target_system` (gmail, calendar, etc.)
- `execution_duration`
- `result` (success / failure)
- `error_category` (if any)

### 8.2 Failure Visibility

Failures are:

- Visible
- Attributed
- Correlated with upstream reasoning

There are no silent execution failures.

---

## 9. Cost Observability (Critical)

Sentinel tracks LLM cost explicitly.

**Metrics Captured:**

- Tokens per agent
- Tokens per graph run
- Cost per proposal
- Cost per successful execution

This enables:

- Cost caps
- Budget alerts
- Model comparisons

Unobserved cost is considered a defect.

---

## 10. Correlation with Database Records

Langfuse traces are correlated with PostgreSQL records via:

- `trace_id`
- `span_id`

These IDs may be stored on:

- Proposal
- HumanDecision
- Action
- GraphRun

This enables joining:

> “What the system thought”  
> with  
> “What the system did”

---

## 11. Privacy & Data Minimization

Langfuse traces must:

- Avoid storing full email bodies
- Avoid storing sensitive health data
- Prefer summaries and hashes

Observability must not violate trust.

---

## 12. What Is NOT Tracked (Intentionally)

Sentinel does not track:

- Raw secrets
- OAuth tokens
- Full PII
- Human free-text beyond decisions

If something is sensitive and not required for learning, it is excluded.

---

## 13. Operational Use of Observability

Langfuse is used for:

- Debugging failures
- Evaluating agent quality
- Tuning prompts
- Understanding human trust
- Demonstrating agentic competence

It is not a vanity dashboard.

---

## 14. Failure Modes in Observability

If observability fails:

- Sentinel continues safely
- Execution does not proceed blindly
- Human is notified

Observability loss degrades capability, not safety.

---

## 15. Guiding Observability Question

For every new feature:

> “Can I explain this decision six months later using traces alone?”

If not, observability is insufficient.

