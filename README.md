# Sentinel Backend

Personal agentic AI system with human-in-the-loop control.

## Overview

Sentinel is a state-driven, agentic AI system designed to observe, reason, and propose actions across personal data sources while keeping a human firmly in control.

**Sentinel is:**
- State-driven (not event-driven or chat-driven)
- Human-in-the-loop by design
- Fully observable and traceable
- A learning-focused project prioritizing clarity and correctness

## Architecture

- **LangGraph**: Orchestration and state machine control plane
- **CrewAI**: Multi-agent reasoning and collaboration
- **FastAPI**: API gateway layer
- **PostgreSQL**: Single source of truth database
- **Langfuse**: Observability and tracing

See `/docs` for detailed architectural documentation.

## Project Structure

```
sentinel-backend/
├── docs/              # Architectural documentation (source of truth)
├── app/               # FastAPI application
├── agents/            # CrewAI agent implementations
├── graphs/            # LangGraph state machine definitions
├── tools/             # Deterministic tools (email, calendar, health)
├── hitl/              # Human-in-the-loop approval systems
├── api/               # API routes and schemas
├── db/                # Database models, migrations, queries
├── observability/     # Langfuse integration and monitoring
├── scheduler/         # Background task scheduling
├── telegram/          # Telegram bot for approvals
└── infra/             # Infrastructure as code
```

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Virtual environment tool (venv or conda)

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd sentinel-backend
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database
```bash
# Create database
createdb sentinel

# Run migrations (once Alembic is set up)
alembic upgrade head
```

### Configuration

All configuration is done via environment variables (prefixed with `SENTINEL_`).

Key settings:
- `SENTINEL_DATABASE_URL`: PostgreSQL connection string
- `SENTINEL_API_AUTH_TOKEN`: Static bearer token for authentication
- `SENTINEL_LANGFUSE_PUBLIC_KEY`: Langfuse public key
- `SENTINEL_LANGFUSE_SECRET_KEY`: Langfuse secret key

See `app/config.py` for all available settings.

## Running

### Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production (TODO)

```bash
# Will be configured with proper ASGI server
```

## API Documentation

Once running, access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Code Style

- Type hints required for all function signatures
- Docstrings for all public functions and classes
- Use Pydantic models for structured data
- Follow the architectural principles in `/docs`

### Testing (TODO)

```bash
pytest
```

### Linting and Formatting

```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy .
```

## Core Principles

1. **State-Driven Architecture**: Explicit state machine using LangGraph
2. **Agents Propose, They Do Not Execute**: Only Executor Agent executes, after approval
3. **Human-in-the-Loop Is Mandatory**: Every impactful action requires human approval
4. **Single Source of Truth**: PostgreSQL is the only authoritative database
5. **Full Observability**: Everything is traceable via Langfuse

See `/docs/decisions_log.md` for architectural decision records.

## Documentation

- [Vision & Intent](docs/vision.md)
- [System Architecture](docs/architecture.md)
- [Agent Roles](docs/agent_roles.md)
- [Database Design](docs/database_design.md)
- [LangGraph State Machine](docs/langgraph_state_machine.md)
- [Observability](docs/observability_langfuse.md)
- [Architectural Decisions](docs/decisions_log.md)

## License

[License TBD]

## Contributing

This is a personal learning project. Contributions are not currently accepted.
