# ADR-0004: Judge-Centric HITL Safety Framework

## Status
Accepted

## Context

Project Chimera requires human oversight for high-risk operations, but cannot scale if humans review every action. The system must:
- Automatically approve low-risk actions
- Escalate high-risk actions to humans
- Provide humans with context and reasoning
- Maintain audit trails for compliance

Traditional approaches (human reviews all actions, or no human oversight) fail because:
- Reviewing all actions doesn't scale to thousands of agents
- No human oversight leads to safety risks (as seen in OpenClaw failures)

## Decision

Adopt a **Judge-Centric HITL Safety Framework** where:

1. **Judge Agent** validates all outputs before execution
2. **Escalation Criteria** trigger HITL review:
   - Low confidence scores (`confidence < 0.85`)
   - Sensitive topics detected
   - Budget thresholds exceeded
   - Sanitization flags raised
   - Financial transactions above threshold
3. **HITL Dashboard** provides human reviewers with:
   - Judge reasoning and confidence scores
   - Content preview and context
   - Approve/reject actions
4. **Management by Exception**: Humans only intervene when Judge escalates

**Key Principles**:
- Judge is the single decision point (no Worker can bypass)
- Escalation criteria are explicit and auditable
- HITL decisions are logged for compliance
- Default action is approval if no escalation criteria met

## Consequences

### Positive
- **Scalability**: Only ~1% of actions require human review (per `specs/_meta.md` §4)
- **Safety**: High-risk actions always reviewed by humans
- **Auditability**: All escalations and decisions logged
- **Efficiency**: Low-risk actions proceed automatically

### Negative
- **Latency**: HITL review adds delay (minutes to hours) for escalated items
- **False Positives**: Judge may escalate safe actions (requires tuning)
- **Human Bottleneck**: If escalation rate too high, humans become bottleneck

## Alternatives Considered

1. **Human Reviews All Actions**: Every action requires human approval
   - Rejected: Doesn't scale, defeats purpose of autonomous agents

2. **No Human Oversight**: Fully autonomous, no human review
   - Rejected: Safety risks (OpenClaw failures), regulatory compliance issues

3. **Threshold-Based Only**: Escalate based on single threshold (e.g., confidence < 0.8)
   - Rejected: Too simplistic, misses context-specific risks (e.g., financial transactions)

## References

- `research/architecture_strategy.md` §2.2 (HITL Framework)
- `specs/_meta.md` §2.2 (HITL Safety Layer)
- `specs/frontend.md` §1 (HITL Dashboard specifications)

