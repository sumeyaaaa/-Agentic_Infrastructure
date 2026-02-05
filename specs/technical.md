## API Contracts

### MoltBook Trend Fetcher API
**Endpoint**: `POST /api/workers/trend-fetcher/fetch`  
**Authentication**: Agent JWT token + MCP server signature  
**Rate Limits**: 
- **Orchestrator Layer**: 10 requests/minute per agent (internal safety limit)  
- **MoltBook API Layer**: 1 request per 5 minutes per submolt (external constraint, see `openclaw_integration.md`)  

#### Request Schema (contract)
```json
{
  "task_id": "uuid_v4",
  "worker_type": "moltbook_trend_fetcher",
  "parameters": {
    "submolts": ["string"] | null,
    "time_range": "1h|4h|24h|7d",
    "min_engagement": 50,
    "persona_tags": ["fashion", "genz", "tech"],
    "max_topics": 10
  },
  "context": {
    "agent_id": "uuid_v4",
    "campaign_id": "uuid_v4",
    "budget_remaining": 45.25
  }
}
```

#### Response Schema (example)
```json
{
  "task_id": "uuid_v4",
  "status": "success|partial|failed",
  "data": {
    "trends": [
      {
        "topic": "AI agent collaboration patterns",
        "submolt": "r/AgentTech",
        "engagement_score": 0.85,
        "post_count": 147,
        "comment_count": 892,
        "trend_velocity": 0.72,
        "timestamp": "2026-02-04T14:30:00Z",
        "relevance_score": 0.88,
        "topic_embedding": [0.12, -0.34, 0.56]
      }
    ],
    "metadata": {
      "fetched_at": "2026-02-04T14:35:00Z",
      "source": "moltbook",
      "cache_hit": false,
      "processing_time_ms": 450
    }
  },
  "errors": []
}
```

#### Field Constraints

- `relevance_score`:
  - Type: `float`
  - Range: `0.0 - 1.0`
  - **Filter**: Only trends with `relevance_score >= 0.75` MUST be returned to callers (see `functional.md` AC3).
- `topic_embedding`:
  - Vector produced by Weaviate using the configured embedding model.
  - Used for semantic similarity against agent persona embeddings.

#### Error Codes

```json
{
  "error_codes": {
    "RATE_LIMITED": "MoltBook API rate limit exceeded",
    "SANITIZATION_FAILED": "Input failed sanitization check",
    "NETWORK_TIMEOUT": "API call timed out after 30s",
    "AUTH_FAILED": "MoltBook API authentication failed",
    "CACHE_ERROR": "Redis cache operation failed",
    "EMBEDDING_ERROR": "Weaviate embedding generation failed"
  }
}
```

### Database Schema Extension
```sql
-- Add to PostgreSQL schema (for trend metadata)
CREATE TABLE agent_trends (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id),
    topic TEXT NOT NULL,
    submolt VARCHAR(255),
    engagement_score DECIMAL(3,2) CHECK (engagement_score >= 0 AND engagement_score <= 1),
    relevance_score DECIMAL(3,2) CHECK (relevance_score >= 0 AND relevance_score <= 1),
    raw_data JSONB, -- Full MoltBook response for audit
    fetched_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ DEFAULT NOW() + INTERVAL '1 hour',
    
    -- Multi-tenancy indexing
    INDEX idx_agent_trends_agent_id (agent_id),
    INDEX idx_agent_trends_fetched (fetched_at DESC),
    
    -- Constraint: One trend record per agent-topic combination per hour
    UNIQUE(agent_id, topic, date_trunc('hour', fetched_at))
);
```

### Redis Cache Pattern

For high-velocity access, Redis MUST be used as follows:

- **Key**: `trend_cache:{agent_id}:{submolt}:{time_range_hash}`  
- **Value**: JSON-serialized trends list  
- **TTL**: `3600` seconds (1 hour) – must match `functional.md` AC5 and `openclaw_integration.md` workflow.

### Input Sanitization Rules

All inputs and MoltBook content MUST be sanitized before processing:

1. **Token/Marker Stripping**: Reject or strip content containing LLM control tokens such as `{system}`, `{user}`, `{assistant}`, `</s>`, `<|im_start|>`, `<|im_end|>`.
2. **Length Limits**: Truncate or reject any single text field longer than 10,000 characters.
3. **Payload Detection**: Reject content containing:\n   - Base64-looking payloads (long contiguous base64 alphabet segments)\n   - Shell command patterns (`; rm -rf`, `&&`, `| bash`, etc.)\n   - SQL injection patterns (`UNION SELECT`, `DROP TABLE`, etc.).
4. **Failure Handling**: On sanitization failure, **discard the input**, DO NOT call MoltBook APIs, and **alert the Judge agent** (see `functional.md` error conditions).\n

### Semantic Filtering Algorithm

To implement semantic filtering (see `functional.md` AC3):

1. Generate an embedding for each trend topic using Weaviate (topic text only).\n2. Generate/maintain an embedding for the agent's SOUL.md persona description.\n3. Compute cosine similarity between `topic_embedding` and persona embedding → `relevance_score` in `[0.0, 1.0]`.\n4. Filter out any trends where `relevance_score < 0.75`.\n5. Persist `topic_embedding` and `relevance_score` to `agent_trends` for future queries and audits.\n

### Persona Tags vs Embeddings

- `persona_tags` (request parameter) are **human-readable categories** used for coarse filtering (e.g., only fetch trends tagged with `fashion` or `genz`).  
- `topic_embedding` + `relevance_score` are **semantic signals** used for fine-grained filtering based on persona similarity.  
- Both MUST be supported:\n  - First filter by `persona_tags` (if provided),\n  - Then apply the semantic relevance threshold (`relevance_score >= 0.75`).