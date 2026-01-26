# Sentinel — Vision & Intent


## 1. What Sentinel Is

Sentinel is a personal, agentic AI system designed to observe, reason, and propose actions across personal data sources, while keeping a human firmly in control of all meaningful decisions.

- Sentinel is **not a chatbot**.
- Sentinel is **not an automation script**.
- Sentinel is a **stateful decision system**.

Its primary purpose is to explore and learn agentic AI architectures in a safe, observable, and production-aligned way.

---

## 2. Core Philosophy

Sentinel is built on five non-negotiable principles:

### 2.1 Observation Before Action

Sentinel never acts immediately.  
It first observes reality, then reasons, then proposes.

### 2.2 Human-in-the-Loop by Design

Every impactful action must pass through explicit human approval, unless explicitly configured otherwise.

Human judgment is a first-class system component, not an afterthought.

### 2.3 Agentic, Not Autonomous

Sentinel uses multiple specialized agents that:

- Reason independently
- Collaborate through orchestration
- Are constrained by clear roles and boundaries

Agents propose, they do not execute.

### 2.4 State Over Chat

Sentinel is driven by explicit state machines, not free-form conversations.

Every decision has:

- A state
- A transition
- A reason
- An outcome

### 2.5 Full Observability

Every agent decision, graph transition, human override, and execution outcome is observable and traceable.

If Sentinel does something, it must be explainable.

---

## 3. Sentinel Is NOT

To avoid architectural drift, Sentinel explicitly rejects the following patterns:

- ❌ Fully autonomous AI
- ❌ Chat-only interfaces
- ❌ Hidden agent loops
- ❌ Implicit side effects
- ❌ Silent failures
- ❌ “Magic” behavior without audit trails

If Sentinel ever feels “mysterious,” the design has failed.

---

## 4. Learning Objectives

This project exists to deeply learn:

- Agent role design and boundaries
- Multi-agent collaboration patterns
- LangGraph-based orchestration
- Human-in-the-loop pause and resume mechanics
- Agent failure modes and recovery
- Cost control in agentic systems
- Observability using Langfuse
- Correctness-first system design

Sentinel prioritizes understanding over speed and clarity over cleverness.

---

## 5. Scope (Initial Versions)

### Included

- Personal email, calendar, and health observations
- Multiple specialized agents
- Central orchestration via state machine
- Human approval via Web UI and Telegram
- Persistent decision history
- Observability-first design

### Explicitly Excluded (for now)

- Multi-user support
- Full autonomy
- Voice interfaces
- Social media integrations
- Large-scale optimization

These may be explored later, but not at the cost of correctness.

---

## 6. Success Criteria

Sentinel is considered successful if:

- Agent decisions can be traced end-to-end
- Human overrides are respected and logged
- State transitions are explicit and reproducible
- Failures are understandable, not silent
- The system can be reasoned about without guesswork

If Sentinel helps the author understand agentic AI deeply, it has achieved its goal.

---

## 7. Guiding Question

Every design decision in this repository should answer:

> “Does this make Sentinel safer, more understandable, and more observable as an agentic system?”

If the answer is no, the change does not belong.

