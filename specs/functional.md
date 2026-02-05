# Functional Specifications

## Autonomous Agent User Stories

### MoltBook Trend Fetcher Worker
**As a** MoltBook Trend Fetcher Worker  
**I need to** fetch trending topics from the 3 most relevant MoltBook submolts every 4 hours  
**So that** the Planner agent can identify content opportunities in the agent social network  

**Acceptance Criteria:**
1. ✅ Only uses `mcp-server-moltbook` for all API calls (no direct MoltBook API access)
2. ✅ Implements input sanitization against prompt injection attacks
3. ✅ Applies semantic filtering (SRS §4.1.1) with minimum relevance score of 0.75
4. ✅ Respects MoltBook rate limits (max 1 request per 5 minutes per submolt) **and** internal Orchestrator rate limits (10 requests/minute per agent)
5. ✅ Caches results in Redis with 1-hour TTL to prevent redundant calls
6. ✅ Includes agent persona tags for relevance filtering
7. ✅ Logs all fetches with MCP Sense telemetry for traceability

**Error Conditions:**
- MoltBook API timeout → Retry once after 30 seconds
- Rate limit exceeded → Exponential backoff with jitter
- Sanitization failure → Discard input and alert Judge agent