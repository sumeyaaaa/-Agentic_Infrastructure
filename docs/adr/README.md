# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records (ADRs) for Project Chimera. ADRs document important architectural decisions, their context, and consequences.

## What are ADRs?

ADRs are documents that capture important architectural decisions along with their context and consequences. They help:
- Document why certain decisions were made
- Provide context for future developers
- Enable informed decision-making when revisiting choices

## ADR Index

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [ADR-0001](./0001-hierarchical-swarm-architecture.md) | Hierarchical Swarm Architecture (Planner-Worker-Judge) | Accepted | 2026-02-07 |
| [ADR-0002](./0002-mcp-native-integration.md) | MCP-Native Integration for External Capabilities | Accepted | 2026-02-07 |
| [ADR-0003](./0003-polyglot-persistence.md) | Polyglot Persistence Strategy | Accepted | 2026-02-07 |
| [ADR-0004](./0004-hitl-judge-centric-safety.md) | Judge-Centric HITL Safety Framework | Accepted | 2026-02-07 |
| [ADR-0005](./0005-fastapi-react-frontend.md) | FastAPI + React for Frontend Stack | Accepted | 2026-02-07 |

## ADR Template

When creating a new ADR, use this template:

```markdown
# ADR-XXXX: [Title]

## Status
[Proposed | Accepted | Rejected | Deprecated | Superseded by ADR-YYYY]

## Context
[Describe the issue motivating this decision]

## Decision
[State the decision]

## Consequences
### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Drawback 1]
- [Drawback 2]

## Alternatives Considered
1. [Alternative 1]
   - Rejected: [Reason]

2. [Alternative 2]
   - Rejected: [Reason]

## References
- [Link to relevant docs]
```

## References

- [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- `research/architecture_strategy.md` (Overall architecture strategy)
- `specs/_meta.md` (Meta specification)

