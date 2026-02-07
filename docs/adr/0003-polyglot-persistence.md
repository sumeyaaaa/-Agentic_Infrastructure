# ADR-0003: Polyglot Persistence Strategy

## Status
Accepted

## Context

Project Chimera requires storing diverse data types:
- Structured relational data (agents, campaigns, transactions)
- High-velocity task queue and cache (Redis)
- Vector embeddings for semantic search (Weaviate)
- Large media files (videos, images)
- Time-series metrics and logs

Traditional single-database approaches (e.g., PostgreSQL for everything) fail because:
- Vector similarity search is inefficient in SQL databases
- Storing large media files in databases is a scaling anti-pattern
- High-velocity cache/queue requires in-memory data structures
- Different access patterns require different optimizations

## Decision

Adopt a **Polyglot Persistence Strategy** where each data type uses the optimal storage solution:

1. **PostgreSQL**: Structured relational data (agents, campaigns, transactions, audit logs)
2. **Redis**: Task queue, cache, session state, rate limiting counters
3. **Weaviate**: Vector embeddings for semantic similarity search
4. **Object Storage (S3/GCS)**: Large media files (videos, images, generated content)
5. **Time-Series DB (optional)**: Metrics and telemetry (if needed for advanced analytics)

**Key Principles**:
- Each data store optimized for its specific access pattern
- Data consistency handled at application layer (not database transactions)
- Multi-tenancy isolation enforced at application layer (not database level)

## Consequences

### Positive
- **Performance**: Each store optimized for its use case
- **Cost Efficiency**: Use cheaper storage for large files (object storage vs. database)
- **Scalability**: Scale each store independently based on load
- **Flexibility**: Swap implementations (e.g., Redis → Memcached, S3 → GCS)

### Negative
- **Complexity**: Multiple databases to manage, monitor, and backup
- **Data Consistency**: No cross-database transactions (must handle at app layer)
- **Operational Overhead**: More infrastructure to deploy and maintain

## Alternatives Considered

1. **PostgreSQL for Everything**: Use PostgreSQL with extensions (pgvector, JSONB)
   - Rejected: Inefficient for vector search, expensive for large media files

2. **MongoDB for Everything**: Use MongoDB as single NoSQL store
   - Rejected: No native vector search, inefficient for relational queries

3. **Single Cloud Database**: Use managed service (e.g., AWS RDS) for all data
   - Rejected: Cost-prohibitive for large media files, inefficient for vector search

## References

- `research/architecture_strategy.md` §2.4 (Polyglot Persistence)
- `specs/_meta.md` §2.3 (Polyglot Persistence Strategy)
- `specs/technical.md` (Database schema definitions)

