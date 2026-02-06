# Agent Skills Directory

## Overview

This directory contains the **Skills** that the Chimera agents will use at runtime. A "Skill" is a specific capability package (e.g., `skill_moltbook_trend_fetcher`, `skill_content_generator`, `skill_wallet_manager`).

## Important Distinction

- **Skills** (this directory): Runtime capabilities for agents (internal processing logic)
- **MCP Servers** (external): Infrastructure bridges (database connectors, platform APIs)

## Structure

Each skill should have:
- `README.md`: Description, Input/Output contracts (this file contains the contracts)
- `interface.py` (or equivalent): Function signatures (to be implemented in later tasks)
- Implementation (to be added in later tasks)

---

## Skill: skill_moltbook_trend_fetcher

### Purpose
Fetches trending topics from MoltBook agent social network, applies semantic filtering and input sanitization, and returns relevance-scored trends for the Planner agent to identify content opportunities.

### Architecture Context
- **Used by**: Trend Spotter Worker (Worker Pool, Architecture Strategy Section 2.1)
- **Architecture Reference**: Section 3 (Defensive MCP Integration Layer) from `research/architecture_strategy.md`
- **Specification Reference**: `specs/functional.md` user story "MoltBook Trend Fetcher Worker"
- **Safety Layer**: Judge agent validation required for trends with `relevance_score < 0.85` or sanitization flags; all MoltBook inputs sanitized before processing (OpenClaw prompt injection defense)

### Input Contract

**Schema:**
```json
{
  "task_id": "uuid_v4 (from Planner)",
  "parameters": {
    "submolts": ["string"] | null,
    "time_range": "1h|4h|24h|7d",
    "min_engagement": "integer",
    "persona_tags": ["string"],
    "max_topics": "integer"
  },
  "context": {
    "agent_id": "uuid_v4",
    "campaign_id": "uuid_v4",
    "budget_remaining": "decimal (USD)",
    "persona_constraints": ["string"]
  }
}
```

**Field Descriptions:**
- `parameters.submolts`: Specific MoltBook submolts to query (null = fetch from 3 most relevant per heartbeat schedule). Max 10 submolts per request. Default: null
- `parameters.time_range`: Time window for trending topics. Must match openclaw_integration.md resource URL enum. Default: "4h"
- `parameters.min_engagement`: Minimum engagement threshold (post_count + comment_count). Minimum: 1, Default: 50
- `parameters.persona_tags`: Human-readable categories for coarse filtering (e.g., ['fashion', 'genz', 'tech']). Optional, used for initial keyword-based filtering before semantic scoring. Default: []
- `parameters.max_topics`: Maximum number of trends to return. Minimum: 1, Maximum: 50, Default: 10
- `context.agent_id`: Agent requesting trends (for persona embedding lookup). Required: true
- `context.campaign_id`: Campaign context for trend relevance. Required: false
- `context.budget_remaining`: Remaining budget for API calls (cost control). Must be >= 0. Required: true
- `context.persona_constraints`: Additional persona constraints from SOUL.md. Required: false

### Output Contract

**Schema:**
```json
{
  "task_id": "uuid_v4 (echo input)",
  "status": "success|partial_failure|error",
  "result": {
    "trends": [
      {
        "topic": "string",
        "submolt": "string",
        "engagement_score": "float (0.0-1.0)",
        "post_count": "integer",
        "comment_count": "integer",
        "trend_velocity": "float",
        "timestamp": "ISO8601",
        "relevance_score": "float (0.75-1.0)",
        "topic_embedding": ["float"]
      }
    ],
    "metadata": {
      "fetched_at": "ISO8601",
      "source": "moltbook",
      "cache_hit": "boolean",
      "processing_time_ms": "integer",
      "moltbook_api_calls": "integer",
      "orchestrator_rate_window_requests": "integer",
      "sanitization_status": "OK|SUSPECT|REJECT",
      "persona_tags_used": ["string"]
    }
  },
  "metadata": {
    "execution_time_ms": "integer",
    "cost_incurred": "decimal (USD)",
    "confidence_score": "float (0.0-1.0)",
    "requires_validation": "boolean"
  },
  "errors": [
    {
      "code": "RATE_LIMITED|SANITIZATION_FAILED|NETWORK_TIMEOUT|AUTH_FAILED|CACHE_ERROR|EMBEDDING_ERROR",
      "message": "string (human-readable error)",
      "recoverable": "boolean"
    }
  ]
}
```

**Field Descriptions:**
- `status`: "success" = all trends fetched and filtered; "partial_failure" = some submolts failed; "error" = complete failure
- `result.trends[].topic`: Trending topic text (sanitized). Max 500 characters, no LLM control tokens
- `result.trends[].submolt`: Source submolt (e.g., 'r/AgentTech')
- `result.trends[].engagement_score`: Normalized engagement metric from MoltBook. Range: 0.0-1.0
- `result.trends[].relevance_score`: Semantic similarity to agent persona (cosine similarity). MUST be >= 0.75 (filtered per functional.md AC3). Range: 0.0-1.0
- `result.trends[].topic_embedding`: Weaviate-generated embedding vector. Vector length matches Weaviate model dimension
- `result.metadata.sanitization_status`: Overall sanitization result. "REJECT" = no trends returned, "SUSPECT" = Judge review required
- `metadata.requires_validation`: true if Judge review needed (sanitization SUSPECT or relevance_score < 0.85). true triggers Judge agent review before trends reach Planner
- `errors[].recoverable`: true if retry is possible (e.g., NETWORK_TIMEOUT), false for security errors

### Error Conditions

| Error Code | Trigger Condition | Automatic Response | Escalation Path |
|------------|------------------|-------------------|-----------------|
| `RATE_LIMITED` | MoltBook API returns HTTP 429 OR Orchestrator limit (10/min) exceeded | Exponential backoff with jitter (5min → 15min → 45min), use cached data if available | Continue with cached trends, log to MCP Sense |
| `SANITIZATION_FAILED` | Input contains prompt injection patterns, secret keywords, or malicious payloads | Discard input, DO NOT call MoltBook API, return empty trends array | Alert Judge agent immediately (functional.md error conditions) |
| `NETWORK_TIMEOUT` | MoltBook API call exceeds 30s timeout | Retry once after 30s, then fail | Log for infrastructure review |
| `AUTH_FAILED` | MoltBook API authentication error (AWS Secrets Manager issue) | Stop all MoltBook operations | Immediate human intervention required |
| `CACHE_ERROR` | Redis cache operation failed | Continue without cache, fetch fresh data | Log error, continue execution |
| `EMBEDDING_ERROR` | Weaviate embedding generation failed | Return trends without relevance_score (set to null), mark as requires_validation=true | Judge agent must manually review |

### Dependencies

**MCP Servers Required:**
- `mcp-server-moltbook`: Provides `moltbook_fetch_trends` tool (specs/openclaw_integration.md)
- `mcp-server-weaviate`: Provides embedding generation and semantic search (Architecture Strategy Section 2.3)

**Database Connections:**
- PostgreSQL: `agent_trends` table (specs/technical.md Database Schema Extension)
- Redis: Cache layer with key pattern `trend_cache:{agent_id}:{submolt}:{time_range_hash}` (TTL=3600s)

**External APIs:**
- MoltBook API: Rate limit 1 request per 5 minutes per submolt (specs/openclaw_integration.md)
- Orchestrator: Rate limit 10 requests/minute per agent (specs/technical.md)

### Example Usage

```python
# Worker calls this skill via Planner task
from skills.skill_moltbook_trend_fetcher import fetch_trends

request = {
    "task_id": "550e8400-e29b-41d4-a716-446655440000",
    "parameters": {
        "submolts": ["r/AgentTech", "r/AICollaboration"],
        "time_range": "4h",
        "min_engagement": 50,
        "persona_tags": ["tech", "ai"],
        "max_topics": 10
    },
    "context": {
        "agent_id": "agent-123",
        "campaign_id": "campaign-456",
        "budget_remaining": 45.25,
        "persona_constraints": ["technical", "professional"]
    }
}

result = fetch_trends(request)

# Result validation
assert result["status"] in ["success", "partial_failure", "error"]
assert all(trend["relevance_score"] >= 0.75 for trend in result["result"]["trends"])
assert result["metadata"]["requires_validation"] in [True, False]

# If requires_validation=True, send to Judge agent before Planner
if result["metadata"]["requires_validation"]:
    judge_result = judge_agent.review_trends(result["result"]["trends"])
```

---

## Skill: skill_content_generator

### Purpose
Generates multimodal content (text, images, video) that maintains character consistency with the agent's SOUL.md persona, enforces cost controls, and applies consistency locks to ensure brand alignment.

### Architecture Context
- **Used by**: Content Generator Worker (Worker Pool, Architecture Strategy Section 2.1, C3W1)
- **Architecture Reference**: Section 2.1 (Hierarchical Swarm) and Section 2.3 (Polyglot Persistence) from `research/architecture_strategy.md`
- **Specification Reference**: SRS §4.3.1 (character consistency locks), SRS §4.3.2 (tiered video generation strategy)
- **Safety Layer**: Judge agent validation required for all generated content (confidence scoring, persona alignment check); CFO Judge approval required if generation cost exceeds budget threshold

### Input Contract

**Schema:**
```json
{
  "task_id": "uuid_v4 (from Planner)",
  "parameters": {
    "content_type": "text|image|video|multimodal",
    "topic": "string",
    "platform": "twitter|instagram|tiktok|moltbook",
    "persona_guidance": {
      "soul_md_excerpt": "string",
      "tone": "professional|casual|humorous|educational",
      "character_consistency_lock": "boolean"
    },
    "multimodal_config": {
      "include_image": "boolean",
      "include_video": "boolean",
      "video_tier": "quick|standard|premium"
    },
    "cost_constraints": {
      "max_cost_usd": "decimal",
      "prefer_cache": "boolean"
    }
  },
  "context": {
    "agent_id": "uuid_v4",
    "campaign_id": "uuid_v4",
    "budget_remaining": "decimal (USD)",
    "persona_constraints": ["string"]
  }
}
```

**Field Descriptions:**
- `parameters.content_type`: Type of content to generate. Must be one of: text, image, video, multimodal. Required: true
- `parameters.topic`: Content topic/theme (from trend fetcher or campaign brief). Max 500 characters, sanitized (no prompt injection patterns). Required: true
- `parameters.platform`: Target platform (affects format and constraints). Must match platform capabilities. Required: true
- `parameters.persona_guidance.soul_md_excerpt`: Relevant excerpt from agent's SOUL.md persona. Max 2000 characters
- `parameters.persona_guidance.tone`: Content tone. Must align with SOUL.md
- `parameters.persona_guidance.character_consistency_lock`: Enable strict character consistency (SRS §4.3.1). Default: true
- `parameters.multimodal_config.include_image`: Generate accompanying image. Default: false
- `parameters.multimodal_config.include_video`: Generate accompanying video (tiered strategy per SRS §4.3.2). Default: false
- `parameters.multimodal_config.video_tier`: Video generation quality tier (cost vs. quality tradeoff). quick = low cost, standard = balanced, premium = high quality. Default: "standard"
- `parameters.cost_constraints.max_cost_usd`: Maximum cost for this generation. Must be <= budget_remaining. Required: true
- `parameters.cost_constraints.prefer_cache`: Use cached assets when possible. Default: true
- `context.agent_id`: Agent generating content (for SOUL.md lookup and consistency). Required: true
- `context.budget_remaining`: Remaining budget for content generation. Must be >= 0. Required: true

### Output Contract

**Schema:**
```json
{
  "task_id": "uuid_v4 (echo input)",
  "status": "success|partial_failure|error",
  "result": {
    "content_id": "uuid_v4",
    "text_content": "string",
    "image_assets": [
      {
        "asset_id": "uuid_v4",
        "url": "string (S3/GCS object storage)",
        "generation_model": "string",
        "cost_usd": "decimal",
        "consistency_score": "float (0.0-1.0)"
      }
    ],
    "video_assets": [
      {
        "asset_id": "uuid_v4",
        "url": "string (S3/GCS object storage)",
        "tier": "quick|standard|premium",
        "duration_seconds": "integer",
        "cost_usd": "decimal",
        "consistency_score": "float (0.0-1.0)"
      }
    ],
    "metadata": {
      "generated_at": "ISO8601",
      "platform": "string",
      "persona_alignment_score": "float (0.0-1.0)",
      "character_consistency_applied": "boolean",
      "total_cost_usd": "decimal"
    }
  },
  "metadata": {
    "execution_time_ms": "integer",
    "cost_incurred": "decimal (USD)",
    "confidence_score": "float (0.0-1.0)",
    "requires_validation": "boolean"
  },
  "errors": [
    {
      "code": "BUDGET_EXCEEDED|CONSISTENCY_FAILED|GENERATION_ERROR|PLATFORM_INCOMPATIBLE|COST_ESTIMATE_FAILED",
      "message": "string (human-readable error)",
      "recoverable": "boolean"
    }
  ]
}
```

**Field Descriptions:**
- `status`: "success" = all content generated; "partial_failure" = some assets failed; "error" = complete failure
- `result.text_content`: Generated text (caption, post body, etc.). Platform-specific length limits, sanitized, persona-aligned
- `result.image_assets[].consistency_score`: Character consistency score (SRS §4.3.1). Range: 0.0-1.0
- `result.metadata.persona_alignment_score`: Overall alignment with SOUL.md persona. Range: 0.0-1.0, used by Judge agent
- `result.metadata.total_cost_usd`: Total generation cost. Sum of all asset costs
- `metadata.requires_validation`: true if Judge review needed (confidence < 0.85 OR cost > threshold OR consistency_score < 0.8). true triggers Judge agent review before publishing

### Error Conditions

| Error Code | Trigger Condition | Automatic Response | Escalation Path |
|------------|------------------|-------------------|-----------------|
| `BUDGET_EXCEEDED` | Estimated cost > max_cost_usd OR > budget_remaining | Abort generation, return error | CFO Judge review if budget can be increased |
| `CONSISTENCY_FAILED` | Character consistency score < 0.8 (SRS §4.3.1) | Regenerate with stricter constraints, max 2 retries | Judge agent review if retries fail |
| `GENERATION_ERROR` | Image/video generation API failure | Retry once, then fail | Log for infrastructure review |
| `PLATFORM_INCOMPATIBLE` | Content format incompatible with platform | Return error, suggest alternative format | Planner agent adjusts strategy |
| `COST_ESTIMATE_FAILED` | Cannot estimate generation cost | Abort, return error | CFO Judge manual review required |

### Dependencies

**MCP Servers Required:**
- `mcp-server-ideogram`: Image generation (research/tooling_strategy.md)
- `mcp-server-weaviate`: Persona embedding lookup for consistency scoring
- `mcp-server-social`: Platform-specific formatting (future)

**Database Connections:**
- PostgreSQL: Content metadata, consistency scores
- Object Storage (S3/GCS): Generated media assets (Architecture Strategy Section 2.3)
- Redis: Cached assets and generation templates

**External APIs:**
- Image generation API: Rate limits per model provider
- Video generation API: Tiered pricing (quick/standard/premium per SRS §4.3.2)
- Orchestrator: Cost control enforcement

### Example Usage

```python
# Content Worker calls this skill
from skills.skill_content_generator import generate_content

request = {
    "task_id": "660e8400-e29b-41d4-a716-446655440001",
    "parameters": {
        "content_type": "multimodal",
        "topic": "AI agent collaboration patterns",
        "platform": "twitter",
        "persona_guidance": {
            "soul_md_excerpt": "Tech-savvy AI influencer focused on agent ecosystems...",
            "tone": "professional",
            "character_consistency_lock": True
        },
        "multimodal_config": {
            "include_image": True,
            "include_video": False,
            "video_tier": "standard"
        },
        "cost_constraints": {
            "max_cost_usd": 5.00,
            "prefer_cache": True
        }
    },
    "context": {
        "agent_id": "agent-123",
        "campaign_id": "campaign-456",
        "budget_remaining": 45.25
    }
}

result = generate_content(request)

# Judge agent validates before publishing
if result["metadata"]["requires_validation"]:
    judge_result = judge_agent.review_content(result["result"])
```

---

## Skill: skill_wallet_manager

### Purpose
Manages non-custodial wallet operations for agentic commerce, including balance checks, transfers, token deployment, and transaction validation, with mandatory CFO Judge approval for transactions exceeding thresholds.

### Architecture Context
- **Used by**: Commerce Worker (Worker Pool, Architecture Strategy Section 2.1, C3W3)
- **Architecture Reference**: Section 2.2 (HITL Framework - CFO Judge) and Implementation Roadmap Phase 2 from `research/architecture_strategy.md`
- **Specification Reference**: SRS Agentic Commerce via Coinbase AgentKit (research/research.md), specs/_meta.md Economic Agency First principle
- **Safety Layer**: CFO Judge mandatory approval for transactions >$50 USD equivalent; all transactions logged for audit; budget controls enforced per agent

### Input Contract

**Schema:**
```json
{
  "task_id": "uuid_v4 (from Planner)",
  "parameters": {
    "operation": "get_balance|transfer|deploy_token|get_transaction_status",
    "transfer_details": {
      "recipient_address": "string (blockchain address)",
      "amount": "decimal",
      "token": "USDC|ETH|BASE|mbc-20",
      "memo": "string"
    },
    "token_deployment": {
      "token_name": "string",
      "token_symbol": "string",
      "initial_supply": "integer",
      "chain": "base|ethereum"
    },
    "transaction_id": "string",
    "approval_threshold_usd": "decimal"
  },
  "context": {
    "agent_id": "uuid_v4",
    "campaign_id": "uuid_v4",
    "budget_remaining": "decimal (USD)",
    "persona_constraints": ["string"]
  }
}
```

**Field Descriptions:**
- `parameters.operation`: Wallet operation to perform. Must be one of: get_balance, transfer, deploy_token, get_transaction_status. Required: true
- `parameters.transfer_details.recipient_address`: Recipient wallet address (Base/Ethereum). Valid blockchain address format. Required: false (only for transfer operation)
- `parameters.transfer_details.amount`: Transfer amount. Must be > 0, must respect budget_remaining. Required: false
- `parameters.transfer_details.token`: Token type for transfer. Must be supported by Coinbase AgentKit. Required: false
- `parameters.transfer_details.memo`: Transaction memo/note. Max 200 characters, sanitized. Required: false
- `parameters.token_deployment.token_name`: Name of token to deploy. Max 50 characters
- `parameters.token_deployment.token_symbol`: Token symbol. Max 10 characters, uppercase
- `parameters.token_deployment.initial_supply`: Initial token supply. Must be > 0
- `parameters.token_deployment.chain`: Blockchain for deployment. Must be supported by AgentKit
- `parameters.transaction_id`: Transaction hash for status lookup. Valid blockchain transaction hash. Required: false (only for get_transaction_status)
- `parameters.approval_threshold_usd`: CFO Judge approval threshold. Default: 50.00 USD, can be overridden per agent
- `context.agent_id`: Agent performing transaction (for wallet lookup and budget tracking). Required: true
- `context.budget_remaining`: Remaining budget for transactions. Must be >= 0, transaction amount must not exceed this. Required: true

### Output Contract

**Schema:**
```json
{
  "task_id": "uuid_v4 (echo input)",
  "status": "success|pending_approval|error",
  "result": {
    "operation": "string (echo input)",
    "balance": {
      "usdc": "decimal",
      "eth": "decimal",
      "base": "decimal",
      "total_usd_equivalent": "decimal"
    },
    "transaction": {
      "transaction_hash": "string",
      "status": "pending|confirmed|failed",
      "block_number": "integer",
      "gas_used": "integer",
      "gas_cost_usd": "decimal",
      "amount": "decimal",
      "token": "string",
      "recipient": "string",
      "timestamp": "ISO8601"
    },
    "token_deployment": {
      "token_address": "string",
      "token_name": "string",
      "token_symbol": "string",
      "deployment_cost_usd": "decimal"
    },
    "metadata": {
      "wallet_address": "string",
      "cfo_approval_required": "boolean",
      "cfo_approval_status": "pending|approved|rejected",
      "budget_after_transaction": "decimal (USD)",
      "audit_log_id": "uuid_v4"
    }
  },
  "metadata": {
    "execution_time_ms": "integer",
    "cost_incurred": "decimal (USD)",
    "confidence_score": "float (0.0-1.0)",
    "requires_validation": "boolean"
  },
  "errors": [
    {
      "code": "BUDGET_EXCEEDED|INSUFFICIENT_BALANCE|INVALID_ADDRESS|CFO_REJECTED|TRANSACTION_FAILED|GAS_ESTIMATE_FAILED",
      "message": "string (human-readable error)",
      "recoverable": "boolean"
    }
  ]
}
```

**Field Descriptions:**
- `status`: "success" = operation completed; "pending_approval" = CFO Judge review required; "error" = operation failed
- `result.balance.total_usd_equivalent`: Total balance in USD. Calculated using current exchange rates
- `result.transaction.status`: Transaction status. "pending" = not yet confirmed, "confirmed" = on-chain, "failed" = reverted
- `result.transaction.block_number`: Block number when confirmed. null if pending
- `result.metadata.cfo_approval_required`: Whether CFO Judge approval was required. true if transaction amount > approval_threshold_usd
- `result.metadata.cfo_approval_status`: CFO Judge approval status. null if approval not required
- `result.metadata.budget_after_transaction`: Remaining budget after transaction. budget_remaining - transaction_cost
- `metadata.requires_validation`: true if CFO Judge approval required (transaction > threshold OR confidence < 0.9). true triggers CFO Judge review before transaction execution

### Error Conditions

| Error Code | Trigger Condition | Automatic Response | Escalation Path |
|------------|------------------|-------------------|-----------------|
| `BUDGET_EXCEEDED` | Transaction amount + gas > budget_remaining | Abort transaction, return error | CFO Judge review if budget can be increased |
| `INSUFFICIENT_BALANCE` | Wallet balance < transaction amount + gas | Abort transaction, return error | Planner agent adjusts strategy |
| `INVALID_ADDRESS` | Recipient address format invalid | Abort transaction, return error | No retry - invalid input |
| `CFO_REJECTED` | CFO Judge rejected transaction | Abort transaction, return error | Human CFO review required |
| `TRANSACTION_FAILED` | On-chain transaction reverted | Revert state, alert CFO Judge | CFO human review required |
| `GAS_ESTIMATE_FAILED` | Cannot estimate gas cost | Abort transaction, return error | CFO Judge manual review |

### Dependencies

**MCP Servers Required:**
- `mcp-server-coinbase`: Coinbase AgentKit integration (research/tooling_strategy.md)
  - Tools: `coinbase_get_balance`, `coinbase_transfer`, `coinbase_deploy_token`, `coinbase_get_transaction_status`

**Database Connections:**
- PostgreSQL: Transaction audit log, budget tracking (specs/_meta.md Cost Constraints)
- Blockchain: Base/Ethereum networks for transaction submission and verification

**External APIs:**
- Coinbase AgentKit: Non-custodial wallet operations (research/research.md)
- Blockchain RPC: Transaction status, gas estimation
- Exchange Rate API: USD equivalent calculations
- Orchestrator: Budget control enforcement

### Example Usage

```python
# Commerce Worker calls this skill
from skills.skill_wallet_manager import execute_wallet_operation

# Example 1: Get balance
request = {
    "task_id": "770e8400-e29b-41d4-a716-446655440002",
    "parameters": {
        "operation": "get_balance"
    },
    "context": {
        "agent_id": "agent-123",
        "budget_remaining": 100.00
    }
}
balance_result = execute_wallet_operation(request)

# Example 2: Transfer (requires CFO approval if >$50)
transfer_request = {
    "task_id": "880e8400-e29b-41d4-a716-446655440003",
    "parameters": {
        "operation": "transfer",
        "transfer_details": {
            "recipient_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
            "amount": 75.00,
            "token": "USDC",
            "memo": "Payment for collaboration"
        },
        "approval_threshold_usd": 50.00
    },
    "context": {
        "agent_id": "agent-123",
        "budget_remaining": 100.00
    }
}
transfer_result = execute_wallet_operation(transfer_request)

# If requires_validation=True, CFO Judge must approve
if transfer_result["metadata"]["requires_validation"]:
    cfo_result = cfo_judge.review_transaction(transfer_result)
    if cfo_result["approved"]:
        # Execute transaction
        final_result = execute_wallet_operation(transfer_request, cfo_approval=cfo_result)
```

---

## Status

✅ **COMPLETE** - Skill interfaces defined in Task 2.3  
These skill contracts are ready for implementation. Each skill:
- Has detailed Input/Output contracts traceable to specifications
- Includes error handling and escalation paths
- Defines dependencies (MCP servers, databases, APIs)
- Provides example usage code
- Enforces safety layers (Judge/CFO validation)

**Next Steps**: 
- Task 3.1: Create `tests/test_skills_interface.py` to validate these contracts
- Implementation: Build skill modules matching these interfaces