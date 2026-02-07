# ADR-0001: Hierarchical Swarm Architecture (Planner-Worker-Judge)

## Status
Accepted

## Context

Project Chimera requires a scalable architecture to manage thousands of autonomous AI agents. The system must:
- Decompose complex campaigns into executable tasks
- Execute tasks in parallel across specialized workers
- Validate outputs before any action affects the world
- Enable human oversight when needed

Traditional monolithic or flat agent architectures fail at scale due to:
- Lack of separation of concerns (planning vs. execution vs. validation)
- Inability to parallelize independent tasks
- No centralized governance or safety layer
- Difficulty managing complexity as agent count grows

## Decision

Adopt a **Hierarchical Swarm Architecture** with three distinct roles:

1. **Planner Agent**: Decomposes high-level campaigns into atomic tasks
2. **Worker Agents**: Execute specialized tasks (trend fetching, content generation, wallet operations)
3. **Judge Agent**: Validates all outputs before execution, routes to HITL when needed

**Key Principles**:
- Workers are stateless and ephemeral (scale horizontally)
- Judge is the single point of validation (no Worker can bypass)
- Planner-Worker-Judge communication via standardized JSON-RPC APIs
- All external interactions go through MCP servers (no direct API calls)

## Consequences

### Positive
- **Scalability**: Workers can scale independently based on queue depth
- **Safety**: Judge enforces all safety policies before execution
- **Parallelism**: Independent tasks execute simultaneously
- **Maintainability**: Clear separation of concerns, easier to test and debug
- **Governance**: Centralized validation enables consistent policy enforcement

### Negative
- **Latency**: Additional hop through Judge adds ~50-100ms per task
- **Complexity**: Three-tier architecture requires careful orchestration
- **Single Point of Failure**: Judge failure blocks all task execution (mitigated by redundancy)

## Alternatives Considered

1. **Flat Agent Architecture**: All agents equal, no hierarchy
   - Rejected: No centralized governance, difficult to enforce safety policies

2. **Two-Tier (Planner-Worker)**: No Judge layer
   - Rejected: Workers could execute unsafe actions without validation

3. **Monolithic Agent**: Single agent does everything
   - Rejected: Cannot scale, no parallelism, difficult to maintain

## References

- `research/architecture_strategy.md` §2.1 (Hierarchical Swarm)
- `specs/_meta.md` §2.1 (Core Architectural Constraints)
- `specs/technical.md` (API contracts for Planner-Worker-Judge communication)

