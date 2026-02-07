# ADR-0002: MCP-Native Integration for External Capabilities

## Status
Accepted

## Context

Project Chimera requires integration with multiple external systems:
- MoltBook/OpenClaw (agent social network)
- Social media platforms (Twitter, Instagram, TikTok)
- Coinbase AgentKit (blockchain transactions)
- Weaviate (vector database)
- Redis (caching, task queue)

Traditional direct API integration approaches suffer from:
- API volatility (social media APIs change frequently)
- Security risks (prompt injection, credential exposure)
- Lack of observability (difficult to monitor external calls)
- Vendor lock-in (tight coupling to specific API versions)

## Decision

Adopt **Model Context Protocol (MCP) as the universal bridge** for all external capabilities.

**Key Principles**:
- All external interactions MUST go through versioned MCP servers
- No direct API calls from Workers or other components
- MCP servers provide standardized, observable interfaces
- Each MCP server is independently versioned and deployable

**MCP Server Examples**:
- `mcp-server-moltbook`: MoltBook/OpenClaw integration
- `mcp-server-social`: Social media platform APIs
- `mcp-server-coinbase`: Coinbase AgentKit integration
- `mcp-server-weaviate`: Vector database operations

## Consequences

### Positive
- **Security**: Centralized input sanitization and rate limiting
- **Observability**: All external calls logged and monitored
- **Flexibility**: Swap MCP server implementations without changing Workers
- **Versioning**: Independent versioning of external integrations
- **Testing**: Mock MCP servers for unit/integration tests

### Negative
- **Additional Layer**: MCP server adds latency (~10-20ms per call)
- **Development Overhead**: Must build and maintain MCP servers
- **Complexity**: More components to deploy and monitor

## Alternatives Considered

1. **Direct API Calls**: Workers call external APIs directly
   - Rejected: Security risks, API volatility, difficult to monitor

2. **API Gateway Pattern**: Single gateway for all external calls
   - Rejected: Less flexible than MCP, harder to version independently

3. **SDK Wrappers**: Language-specific SDKs for each external service
   - Rejected: Tight coupling, difficult to standardize across services

## References

- `research/architecture_strategy.md` §2.3 (MCP as Universal Bridge)
- `specs/openclaw_integration.md` (MCP server specifications)
- `research/tooling_strategy.md` (MCP tooling strategy)

