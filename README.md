# Project Chimera: Agentic Infrastructure Challenge

## Overview

Project Chimera is an **autonomous influencer system** that researches trends, generates content, and manages engagement without human intervention. This repository contains the **infrastructure, specifications, and governance framework** that enables AI agents to build and operate the system safely and reliably.

**Key Philosophy**: We are NOT building the influencer itself. We are building the **factory** and **safety net** that allows AI agents to build it.

## Project Status

### Task 1: The Strategist (Research & Foundation) - ✅ COMPLETE
- ✅ **Task 1.1**: Deep Research & Reading - Completed
- ✅ **Task 1.2**: Domain Architecture Strategy - Completed
- ✅ **Task 1.3**: Environment Setup - Completed (MCP Sense connected, pyproject.toml)

### Task 2: The Architect (Specification & Context Engineering) - ✅ COMPLETE
- ✅ **Task 2.1**: Master Specification - Completed
  - ✅ `specs/_meta.md` - Vision, constraints, principles
  - ✅ `specs/functional.md` - User stories
  - ✅ `specs/technical.md` - API contracts, database schemas
  - ✅ `specs/openclaw_integration.md` - OpenClaw/MoltBook protocols
- ✅ **Task 2.2**: Context Engineering - Completed
  - ✅ `.cursor/rules/agent.mdc` - IDE agent rules with Prime Directive
- ✅ **Task 2.3**: Tooling & Skills Strategy - Completed
  - ✅ `research/tooling_strategy.md` - Developer vs Runtime MCP strategy
  - ✅ `skills/README.md` - 3 critical skills with I/O contracts
  - ✅ `skills/*/interface.py` - Python interface files

### Task 3: The Governor (Infrastructure & Governance) - ✅ COMPLETE
- ✅ **Task 3.1**: Test-Driven Development - Completed
  - ✅ `tests/test_mcp_connection.py` - MCP configuration tests
  - ✅ `tests/test_moltbook_trend_fetcher.py` - Trend fetcher contract tests
  - ✅ `tests/test_skills_interface.py` - Skills interface validation tests
  - ✅ `tests/test_spec_alignment.py` - Spec alignment validation tests (26 tests)
  - ✅ `tests/test_dockerfile.py` - Dockerfile production readiness tests
- ✅ **Task 3.2**: Containerization & Automation - Completed
  - ✅ `Dockerfile` - Production-ready multi-stage container (builder, production, development)
  - ✅ `Makefile` - Standardized commands (setup, test, docker-test, lint, spec-check)
  - ✅ `scripts/spec_check.py` - Automated spec alignment verification
- ✅ **Task 3.3**: CI/CD & AI Governance - Completed
  - ✅ `.github/workflows/main.yml` - GitHub Actions pipeline
  - ✅ `.coderabbit.yaml` - AI review policy (spec alignment, security)

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
│   ├── test_mcp_connection.py
│   ├── test_moltbook_trend_fetcher.py
│   ├── test_skills_interface.py
│   ├── test_spec_alignment.py
│   └── test_dockerfile.py
├── scripts/              # Automation scripts
│   └── spec_check.py     # Spec alignment verification tool
├── .cursor/              # Cursor IDE configuration
│   ├── rules/            # Agent context rules
│   └── mcp.json          # MCP server configuration
├── .github/workflows/    # CI/CD pipelines
│   └── main.yml          # GitHub Actions workflow
├── Dockerfile            # Production-ready multi-stage container
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

# Run tests locally (will fail initially - TDD approach)
make test

# Run tests in Docker (Task 3.2 requirement)
make docker-test

# Verify code aligns with specs (Task 3.3)
make spec-check

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

### Spec Check Tool

The `make spec-check` command runs automated validation to ensure:
- All required spec files exist (`specs/_meta.md`, `functional.md`, `technical.md`, `openclaw_integration.md`)
- Skill interfaces reference specifications
- Tests reference specifications
- MCP-native principle is followed (no direct API calls)
- Security sanitization is present in critical skills
- TypedDict contracts are used for type safety
- Dockerfile and Makefile are properly configured

This enforces the **Spec-Driven Development (SDD)** principle throughout the codebase.

## Submission Requirements

### Day 1 (February 4) - ✅ Completed
- Research Summary (Google Drive link)
- Architectural Approach document

### Day 3 (February 6) - ✅ Ready for Submission
- ✅ Public GitHub Repository (this repo)
  - ✅ All required directories: `specs/`, `tests/`, `skills/`
  - ✅ All required files: `Dockerfile`, `Makefile`, `.github/workflows/`, `.cursor/rules/`
  - ✅ `.coderabbit.yaml` - AI review policy
- ⏳ **Remaining**: Loom Video (5 mins max) - To be recorded
  - Walk through Spec Structure and OpenClaw Integration Plan
  - Show Failing Tests running (TDD approach)
  - Demonstrate IDE Agent's Context (ask question, show rules-based response)
- ✅ MCP Telemetry: Tenx MCP Sense active and connected

## License

[To be determined]

## Contact

[To be added]

