# Sentinel — Architecture Decision Log (ADR)


## Purpose of This Document

This document records intentional architectural decisions made during the design of Sentinel.

Each entry captures:

- What decision was made
- Why it was made
- What alternatives were considered
- What trade-offs were accepted

This log exists to:

- Preserve design intent
- Prevent accidental regressions
- Enable future re-evaluation
- Demonstrate engineering maturity

If a major architectural choice is not documented here, it is considered accidental.

---

## ADR-001 — Sentinel Is a State-Driven System

**Status:** Accepted  
**Date:** Initial Design

### Decision

Sentinel is designed as an explicit state machine, not an event-driven or chat-driven system.

### Rationale

- Agentic systems fail when control flow is implicit
- State machines enable replay, debugging, and reasoning
- Human-in-the-loop must be modeled as a state, not a callback

### Alternatives Considered

- Event-driven pipelines
- Chat-based agent loops
- Implicit tool-triggered workflows

### Trade-offs

- More upfront design effort
- Slower initial iteration

### Consequences

- Strong correctness guarantees
- Clear mental model
- Easier long-term maintenance

---

## ADR-002 — Agents Propose, They Do Not Execute

**Status:** Accepted  
**Date:** Initial Design

### Decision

All agents in Sentinel may propose actions, but only the Executor Agent may execute — and only after approval.

### Rationale

- Prevents runaway automation
- Preserves human authority
- Makes agent mistakes visible and recoverable

### Alternatives Considered

- Autonomous agents
- Tool-calling agents
- Confidence-based auto-execution

### Trade-offs

- More human involvement
- Slightly slower workflows

### Consequences

- Safer agentic behavior
- Clear accountability chain
- Better learning outcomes

---

## ADR-003 — Human-in-the-Loop Is Mandatory

**Status:** Accepted  
**Date:** Initial Design

### Decision

Human approval is a first-class system state, not an optional override.

### Rationale

- Sentinel handles personal data
- Trust must be earned and preserved
- HITL is essential for learning agentic AI safely

### Alternatives Considered

- Silent automation
- Optional human review
- Post-hoc notifications

### Trade-offs

- Reduced autonomy
- Higher interaction cost

### Consequences

- Strong trust model
- Explicit decision records
- Safer evolution toward autonomy

---

## ADR-004 — LangGraph as the Orchestration Engine

**Status:** Accepted  
**Date:** Initial Design

### Decision

LangGraph is used as the control plane for Sentinel.

### Rationale

- Explicit state modeling
- Pause/resume semantics
- Graph-based recovery paths
- Clear separation from agent reasoning

### Alternatives Considered

- Custom orchestration logic
- Event queues
- Agent-driven loops

### Trade-offs

- Learning curve
- Additional abstraction

### Consequences

- Deterministic workflows
- Observable transitions
- Production-aligned architecture

---

## ADR-005 — CrewAI for Agent Reasoning

**Status:** Accepted  
**Date:** Initial Design

### Decision

CrewAI is used to define role-based cognitive agents.

### Rationale

- Explicit agent roles and goals
- Tool usage encapsulation
- Collaborative reasoning patterns

### Alternatives Considered

- Single monolithic agent
- Hand-rolled agent abstractions
- Chat-only LLM calls

### Trade-offs

- Slight framework overhead
- More structure required

### Consequences

- Clear agent boundaries
- Easier experimentation
- Better learning of agentic patterns

---

## ADR-006 — PostgreSQL as the Single Source of Truth

**Status:** Accepted  
**Date:** Initial Design

### Decision

PostgreSQL is used as Sentinel’s only authoritative database.

### Rationale

- Strong transactional guarantees
- Relational modeling of decision chains
- Replayability and auditability

### Alternatives Considered

- SQLite
- MongoDB
- Redis-first designs

### Trade-offs

- Slight operational overhead
- Schema discipline required

### Consequences

- Strong correctness guarantees
- Clear state ownership
- Easier observability correlation

---

## ADR-007 — Redis Is Not Used Initially

**Status:** Accepted  
**Date:** Initial Design

### Decision

Redis is deliberately excluded from the initial architecture.

### Rationale

- Sentinel is low-throughput and single-user
- Redis introduces secondary state
- Debuggability and learning suffer

### Alternatives Considered

- Redis for caching
- Redis for queues
- Redis for locks

### Trade-offs

- Potential future performance limits

### Consequences

- Simpler system
- Clearer failure modes
- Easier reasoning and replay

---

## ADR-008 — Observability via Langfuse Is Mandatory

**Status:** Accepted  
**Date:** Initial Design

### Decision

Langfuse is integrated as a first-class observability system.

### Rationale

- Agentic systems are opaque by default
- LLM cost must be visible
- Learning requires traceability

### Alternatives Considered

- Logs only
- Metrics only
- Custom tracing

### Trade-offs

- Additional integration effort
- Observability overhead

### Consequences

- Full explainability
- Cost control
- Strong learning signals

---

## ADR-009 — Frontend and Backend Are Separate Repositories

**Status:** Accepted  
**Date:** Initial Design

### Decision

Sentinel’s frontend and backend live in separate repositories.

### Rationale

- Independent deployment (Vercel + EC2)
- Clear separation of concerns
- Avoids accidental coupling

### Alternatives Considered

- Monorepo
- Backend-served frontend

### Trade-offs

- Slight coordination overhead
- API contracts must be maintained

### Consequences

- Cleaner architecture
- Production-aligned structure
- Easier long-term evolution

---

## ADR-010 — Sentinel Prioritizes Learning Over Optimization

**Status:** Accepted  
**Date:** Initial Design

### Decision

Sentinel intentionally prioritizes clarity, correctness, and learning over performance and automation.

### Rationale

- The primary goal is understanding agentic AI
- Premature optimization hides important lessons

### Alternatives Considered

- Fully autonomous agent system
- Performance-first architecture

### Trade-offs

- Slower workflows
- More explicit human involvement

### Consequences

- Deeper understanding
- Safer experimentation
- Strong architectural discipline

---

## How to Use This Document

- New architectural decisions must be added here
- Deprecated decisions must be updated, not deleted
- Rejected alternatives should be recorded
- This document evolves with Sentinel

---

## Guiding Question

For every change:

> “Would I be able to justify this decision to my future self?”

If not, it does not belong.
