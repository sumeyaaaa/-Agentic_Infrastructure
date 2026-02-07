# ADR-0005: FastAPI + React for Frontend Stack

## Status
Accepted

## Context

Project Chimera requires frontend interfaces for:
- HITL Dashboard (human review queue)
- Orchestrator Control Panel (fleet management)

The frontend must be:
- Production-ready and maintainable
- Fast to develop and iterate
- Secure and performant
- Accessible and responsive

## Decision

Adopt **FastAPI (backend) + React (frontend)** as the frontend stack.

**Backend (FastAPI)**:
- Python ecosystem (consistent with Workers/Judge)
- Automatic API documentation (OpenAPI/Swagger)
- Built-in WebSocket support for real-time updates
- Type safety via Pydantic models
- High performance (async/await support)

**Frontend (React)**:
- Industry-standard, large ecosystem
- Component-based architecture (reusable UI components)
- Strong TypeScript support
- Rich ecosystem (React Query, Zustand, Tailwind CSS)
- Server-side rendering not required (dashboard is authenticated, not public)

## Consequences

### Positive
- **Rapid Development**: FastAPI auto-docs, React component libraries
- **Type Safety**: Pydantic models + TypeScript interfaces
- **Performance**: FastAPI async, React efficient rendering
- **Maintainability**: Large community, extensive documentation
- **Consistency**: Python backend matches Workers/Judge codebase

### Negative
- **Two Languages**: Python backend + TypeScript frontend (separate teams/deployment)
- **Bundle Size**: React apps can be large (mitigated by code splitting)
- **SEO Not Needed**: Not applicable for authenticated dashboards

## Alternatives Considered

1. **Django + Django Templates**: Full-stack Python
   - Rejected: Less flexible for complex UI interactions, slower development

2. **Next.js (Full-Stack)**: React + Node.js backend
   - Rejected: Adds Node.js to stack, prefer Python consistency

3. **FastAPI + Vue.js**: Alternative frontend framework
   - Rejected: React has larger ecosystem, more developers familiar

4. **Server-Side Rendered (SSR)**: Next.js or Django
   - Rejected: Not needed for authenticated dashboards, adds complexity

## References

- `specs/frontend.md` §4.1 (Technology Stack)
- `research/architecture_strategy.md` §4 (Implementation Roadmap - Phase 2)

