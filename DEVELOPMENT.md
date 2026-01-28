# Sentinel Backend - Development Notes

## Current Status

The Sentinel backend foundation has been established with the following components:

### Completed Components

1. **Database Layer** (`/db`)
   - SQLAlchemy models for all 7 conceptual domains
   - Async session management
   - Alembic migration setup
   - Models: Accounts, Observations, Proposals, Decisions, Actions, GraphRuns, Preferences

2. **State Machine** (`/graphs`)
   - Canonical state definitions (SentinelState enum)
   - State transition logic with validation
   - LangGraph foundation with pause/resume support
   - State flow: OBSERVED → ANALYZED → PROPOSED → AWAITING_HUMAN → APPROVED/REJECTED → EXECUTED → COMPLETED/FAILED

3. **Observability** (`/observability`)
   - Langfuse client integration
   - Context managers for tracing
   - Graph run and agent execution tracing

4. **Agents** (`/agents`)
   - Base agent class with structured outputs
   - Inbox Agent (email analysis)
   - Planner Agent (scheduling)
   - Executor Agent (action execution)
   - All agents return ProposalOutput with confidence scores

5. **Tools** (`/tools`)
   - Gmail tool (read, send, archive emails)
   - Calendar tool (fetch, create, update events)
   - Health tool (fetch sleep, activity data)

6. **API Layer** (`/api`)
   - Proposals endpoint (list, get)
   - Graph runs endpoint (list, get)
   - Actions endpoint (get by proposal)
   - Decisions endpoint (create, get)
   - Full Pydantic schema validation

7. **HITL Mechanisms** (`/hitl`, `/telegram`)
   - Notification service for approval requests
   - Telegram bot foundation
   - Multi-channel notification support

8. **Scheduler** (`/scheduler`)
   - APScheduler integration
   - Scheduled email polling
   - Calendar and health data sync
   - Cron-based triggers

9. **Infrastructure**
   - FastAPI application with startup/shutdown hooks
   - Logging configuration
   - Authentication (bearer token)
   - Configuration management (Pydantic settings)
   - Environment variables

### 🚧 Next Steps (Implementation Required)

1. **Agent Integration**
   - Connect CrewAI framework to agents
   - Implement actual LLM calls
   - Add agent tools and task definitions

2. **LangGraph Implementation**
   - Complete graph node implementations
   - Add conditional routing
   - Implement pause/resume mechanics
   - Add error recovery paths

3. **Tool Implementations**
   - Google OAuth flow for Gmail/Calendar
   - Actual API integrations
   - Error handling and retries

4. **Database Migrations**
   - Create initial Alembic migration
   - Test migration up/down

5. **Telegram Bot**
   - Implement command handlers
   - Add inline buttons for approvals
   - Secure authentication

6. **Testing**
   - Unit tests for agents
   - Integration tests for API
   - State machine tests
   - End-to-end workflow tests

7. **Deployment**
   - Docker configuration
   - EC2 deployment scripts
   - Environment-specific configs

## Development Workflow

### Running Locally

```bash
# Activate venv
source venv/bin/activate

# Start PostgreSQL
# (using your preferred method)

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

### Creating Database Migrations

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "description"

# Review and edit migration file in db/migrations/versions/

# Apply migration
alembic upgrade head
```

### Code Quality

```bash
# Format code
black .

# Lint
ruff check .

# Type check
mypy .
```

## Architecture Reminders

- **Agents propose, they do not execute** - Only Executor Agent executes, after approval
- **State-driven, not event-driven** - All behavior flows through explicit states
- **Human approval is mandatory** - Every action must be approved
- **Single source of truth** - PostgreSQL only, no Redis
- **Observability is mandatory** - Everything must be traceable

## Key Files

- `app/config.py` - All configuration
- `db/models/` - Database schema
- `graphs/states.py` - State machine definitions
- `agents/base.py` - Agent base class
- `.github/copilot-instructions.md` - AI assistance guidelines

## Common Tasks

### Add a new database model

1. Create model in `db/models/your_model.py`
2. Import in `db/models/__init__.py`
3. Create migration: `alembic revision --autogenerate -m "add your_model"`
4. Review and apply: `alembic upgrade head`

### Add a new API endpoint

1. Create route in `api/your_router.py`
2. Add schemas in `api/schemas.py`
3. Register router in `app/main.py`

### Add a new agent

1. Create agent in `agents/your_agent/__init__.py`
2. Inherit from `BaseAgent`
3. Implement `role`, `goal`, `backstory`, `analyze()`
4. Wire into graph nodes

## Resources

- Documentation: `/docs`
- API Docs: http://localhost:8000/docs
- Langfuse: https://cloud.langfuse.com
- GitHub Copilot Instructions: `.github/copilot-instructions.md`
