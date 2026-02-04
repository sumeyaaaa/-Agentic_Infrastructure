# Project Chimera: Agentic Infrastructure Challenge

## Overview

Project Chimera is an **autonomous influencer system** that researches trends, generates content, and manages engagement without human intervention. This repository contains the **infrastructure, specifications, and governance framework** that enables AI agents to build and operate the system safely and reliably.

**Key Philosophy**: We are NOT building the influencer itself. We are building the **factory** and **safety net** that allows AI agents to build it.

## Project Status

- ✅ **Task 1.1**: Deep Research & Reading - Completed
- ✅ **Task 1.2**: Domain Architecture Strategy - Completed
- ✅ **Task 1.3**: Environment Setup - Completed
- 🚧 **Task 2**: Specification & Context Engineering - In Progress
- ⏳ **Task 3**: Infrastructure & Governance - Pending

## Repository Structure

```
.
├── research/              # Research notes and architecture strategy
│   ├── mcp_log.md        # Tenx MCP Sense connection log
│   ├── architecture_strategy.md  # Domain architecture decisions
│   └── notes_day1.md     # Research summary
├── specs/                # Master specifications (GitHub Spec Kit)
│   ├── _meta.md          # High-level vision and constraints
│   ├── functional.md     # User stories and functional requirements
│   ├── technical.md      # API contracts, database schemas
│   └── openclaw_integration.md  # OpenClaw/MoltBook protocols
├── skills/               # Agent Skills (runtime capabilities)
│   └── README.md         # Skills directory documentation
├── tests/                # Test-Driven Development tests
│   └── README.md         # Test documentation
├── .cursor/              # Cursor IDE configuration
│   ├── rules/            # Agent context rules
│   └── mcp.json          # MCP server configuration
├── .github/workflows/    # CI/CD pipelines
│   └── main.yml          # GitHub Actions workflow
├── Dockerfile            # Containerization
├── Makefile              # Standardized commands
├── pyproject.toml        # Python environment configuration
└── README.md            # This file
```

## Core Principles

### Spec-Driven Development (SDD)
- **No implementation code until specifications are ratified**
- Specs are the single source of truth for AI agents
- All code must align with `specs/` directory

### Traceability (MCP)
- **Tenx MCP Sense** is connected and logging all interactions
- This provides a "black box" flight recorder of development

### Skills vs. MCP Servers
- **Skills** (`skills/`): Runtime capabilities for agents (e.g., `skill_download_youtube`)
- **MCP Servers** (external): Infrastructure bridges (database connectors, platform APIs)

## Quick Start

### Prerequisites
- Python 3.10+
- Git
- Cursor IDE (with Tenx MCP Sense connected)

### Setup

```bash
# Install dependencies
make setup

# Run tests (will fail initially - TDD approach)
make test

# Run linters
make lint
```

## Architecture Overview

### Agent Pattern: Hierarchical Swarm
- **Planner Agent**: Strategy and task decomposition
- **Worker Agents**: Specialized execution (Trend Spotter, Content Generator, Publisher, etc.)
- **Judge Agent**: Quality control and safety (Content Judge, CFO Judge)

### Database: Hybrid Architecture
- **PostgreSQL**: Core entities (agents, campaigns, content, transactions)
- **Redis**: Caching and real-time data
- **Weaviate**: RAG memory and semantic search

### Human-in-the-Loop
- Content safety review (pre-publication)
- Budget approvals (CFO Judge)
- Persona consistency escalation
- Emergency stop capability

See `research/architecture_strategy.md` for detailed architecture documentation.

## Development Workflow

1. **Spec First**: Update `specs/` before writing code
2. **Test First**: Write failing tests in `tests/` (TDD)
3. **Implement**: Build features aligned with specs
4. **Verify**: Run `make test` and `make spec-check`

## Submission Requirements

### Day 1 (February 4) - ✅ Completed
- Research Summary (Google Drive link)
- Architectural Approach document

### Day 3 (February 6) - 🚧 In Progress
- Public GitHub Repository (this repo)
- Loom Video (5 mins max)
- MCP Telemetry verification

## License

[To be determined]

## Contact

[To be added]

