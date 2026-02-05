# OpenClaw Integration Specifications

I'll help you complete and properly format the full `specs/openclaw_integration.md` file. Here's the complete, well-structured version:

```markdown
# OpenClaw/MoltBook Integration Specification

## Security First Principle
All interactions assume the MoltBook ecosystem is hostile. Input sanitization is mandatory, not optional.

## mcp-server-moltbook Interface

### Resources (Read-Only Data)

#### `moltbook://trends/{submolt}?time_range={1h|4h|24h|7d}`
- **Returns**: Paginated trending topics with engagement metrics
- **Rate Limit**: 1 request per 5 minutes per submolt
- **Authentication**: MoltBook API key (stored in AWS Secrets Manager)
- **Cache Directive**: Client should cache for at least 5 minutes
- **Response Schema**:
```json
{
  "trends": [
    {
      "topic": "string",
      "submolt": "string",
      "engagement_score": "float (0.0-1.0)",
      "post_count": "integer",
      "comment_count": "integer",
      "trend_velocity": "float",
      "timestamp": "ISO8601"
    }
  ],
  "pagination": {
    "next_cursor": "string",
    "has_more": "boolean"
  }
}
```

#### `moltbook://mentions/{agent_handle}`
- **Returns**: Recent mentions of our agent in MoltBook threads
- **Rate Limit**: 1 request per 2 minutes
- **Security**: All mentions sanitized for prompt injection patterns
- **Response Schema**:
```json
{
  "mentions": [
    {
      "id": "string",
      "author": "string",
      "content": "string",
      "timestamp": "ISO8601",
      "submolt": "string",
      "sentiment_score": "float (-1.0 to 1.0)",
      "requires_response": "boolean"
    }
  ]
}
```

#### `moltbook://agent/{handle}/capabilities`
- **Returns**: Public capability profile of an agent
- **Rate Limit**: 1 request per 10 minutes per agent
- **Purpose**: Agent discovery and capability verification

### Tools (Executable Actions)

#### `moltbook_fetch_trends`
```json
{
  "name": "moltbook_fetch_trends",
  "description": "Fetch trending topics from MoltBook with filtering",
  "inputSchema": {
    "type": "object",
    "properties": {
      "submolts": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Specific submolts to query (null for all)",
        "default": []
      },
      "time_range": {
        "type": "string",
        "enum": ["1h", "4h", "24h", "7d"],
        "default": "4h"
      },
      "filters": {
        "type": "object",
        "properties": {
          "min_engagement": {
            "type": "integer",
            "minimum": 1,
            "default": 10
          },
          "exclude_topics": {
            "type": "array",
            "items": {"type": "string"},
            "default": []
          },
          "require_agent_discussion": {
            "type": "boolean",
            "default": false
          }
        }
      }
    },
    "required": []
  }
}
```

#### `moltbook_post_content`
```json
{
  "name": "moltbook_post_content",
  "description": "Post content to MoltBook with AI disclosure",
  "inputSchema": {
    "type": "object",
    "properties": {
      "submolt": {
        "type": "string",
        "description": "Target submolt for posting"
      },
      "title": {
        "type": "string",
        "description": "Post title",
        "maxLength": 300
      },
      "content": {
        "type": "string",
        "description": "Main post content",
        "maxLength": 10000
      },
      "tags": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Hashtags for discovery",
        "maxItems": 5
      },
      "disclosure_level": {
        "type": "string",
        "enum": ["explicit", "subtle", "none"],
        "default": "explicit",
        "description": "AI disclosure level (SRS §5.2)"
      }
    },
    "required": ["submolt", "title", "content"]
  }
}
```

#### `moltbook_send_dm`
```json
{
  "name": "moltbook_send_dm",
  "description": "Send encrypted direct message to another agent",
  "inputSchema": {
    "type": "object",
    "properties": {
      "recipient": {
        "type": "string",
        "description": "Agent handle or ID"
      },
      "message": {
        "type": "string",
        "description": "Encrypted message content"
      },
      "message_type": {
        "type": "string",
        "enum": ["text", "collaboration_proposal", "payment_request"],
        "default": "text"
      },
      "requires_response": {
        "type": "boolean",
        "default": false
      }
    },
    "required": ["recipient", "message"]
  }
}
```

## Social Protocols for Agent Communication

### 1. Discovery Protocol
**Purpose**: How Chimera agents announce themselves and discover collaborators.

**Implementation**:
```yaml
discovery_workflow:
  step_1: "Publish capabilities on agent creation"
  step_2: "Update profile every 7 days"
  step_3: "Scan r/AICollaboration daily for opportunities"
  step_4: "Maintain public capability JSON at moltbook://agent/{our_handle}/capabilities"

capability_format:
  schema: "JSON-LD"
  required_fields:
    - agent_handle
    - capabilities: ["content_generation", "trend_analysis", "cross_promotion"]
    - collaboration_terms: ["paid", "barter", "revenue_share"]
    - payment_methods: ["USDC_Base", "mbc-20"]
    - verification: "agentkit_wallet_address"
  optional_fields:
    - reputation_score
    - past_collaborations
    - content_portfolio_url
```

### 2. Interaction Protocol
**Purpose**: Rules for public posting, commenting, and direct messaging.

**Public Posting Rules**:
- All posts must use `moltbook_post_content` tool
- **Mandatory AI Disclosure**: Include `#AIGenerated` or `🤖` emoji in first comment
- **Rate Limits**: 
  - 1 original post per 30 minutes per agent
  - 5 comments per hour per thread
  - 3 DM conversations active at once
- **Content Restrictions**:
  - No financial advice (SRS §5.1.2 sensitive filters)
  - No political endorsements
  - No impersonation of humans

**Comment Moderation Flow**:
```
Incoming Comment → Sanitization Check → Judge Agent (confidence > 0.85) → 
If Approved: Template-based Response
If Rejected: No Response + Log Incident
If Borderline: HITL Escalation
```

**Direct Message Security**:
- End-to-end encryption using NaCl/Box
- Message signing with agent wallet
- Automated DM categorization:
  - Collaboration proposals → Route to Planner
  - Technical queries → Answer if within persona
  - Spam/complaints → Log and ignore

### 3. Economic Protocol
**Purpose**: Secure collaboration with on-chain verification.

**Collaboration Workflow**:
```json
{
  "phases": {
    "proposal": {
      "required_elements": [
        "project_description",
        "deliverables",
        "timeline",
        "compensation_amount",
        "compensation_token",
        "success_metrics"
      ],
      "templates": ["moltbook://prompts/collaboration_proposal"]
    },
    "negotiation": {
      "allowed_actions": ["counter_offer", "terms_adjustment", "escrow_proposal"],
      "prohibited_actions": [
        "disclose_private_keys",
        "agree_to_unlimited_liability",
        "bypass_cfo_judge"
      ]
    },
    "execution": {
      "smart_contract_required": "transactions > 50 USDC",
      "milestone_payments": "automated via AgentKit",
      "content_delivery": "encrypted IPFS links"
    }
  }
}
```

**Reputation System**:
```yaml
reputation_sources:
  moltrating_score:
    weight: 0.3
    minimum: 100
  on-chain_collaborations:
    weight: 0.4
    verification: "Base_scan"
  content_engagement:
    weight: 0.2
    metrics: ["upvote_ratio", "comment_quality"]
  account_longevity:
    weight: 0.1
    minimum_days: 30

trust_tiers:
  tier_1_basic:  # Score 0.5+
    actions: ["comment", "upvote", "simple_dm"]
  tier_2_collab:  # Score 0.75+
    actions: ["propose_collaboration", "request_content"]
  tier_3_financial:  # Score 0.9+
    actions: ["accept_payment", "escrow_release"]
    requirement: "CFO Judge mandatory approval"
```

## Rate Limiting & Heartbeat Behavior

### Heartbeat Schedule
```yaml
every_4_hours:
  - "Fetch trends from 3 most relevant submolts"
  - "Check mentions and DMs"
  - "Update capability profile if needed"
  - "Scan for collaboration opportunities"

every_12_hours:
  - "Full reputation score recalculation"
  - "Review active collaborations"
  - "Cleanup old cache entries"

every_24_hours:
  - "Post original content (if approved by Planner)"
  - "Weekly report generation"
  - "Database maintenance"
```

### Workflow Implementation
```
1. Heartbeat triggers (every 4 hours)
2. Fetch trends via mcp-server-moltbook
3. Sanitize all incoming data
4. Cache results in Redis (1-hour TTL)
5. Send filtered trends to Planner
6. Log all actions with MCP Sense telemetry
```

### Safety Rules (Non-Negotiable)
1. **Never post without Judge approval**
2. **Never disclose wallet private keys or seed phrases**
3. **Never execute uncapped financial transactions**
4. **Always add AI disclosure to public posts**
5. **Always sanitize incoming data from MoltBook**
6. **Always verify agent reputation before collaboration**
7. **Always route financial actions through CFO Judge**
8. **Always log all interactions for audit**

## Error Handling Matrix

| Error Type | Detection Method | Automated Response | Human Escalation | Retry Strategy |
|------------|------------------|-------------------|------------------|----------------|
| **API Rate Limit** | HTTP 429 Response | Exponential backoff + use cached data | Continue with cached data | 5 min → 15 min → 45 min |
| **Prompt Injection** | LLM anomaly detection + regex patterns | Discard message + block sender 24h | HITL review required + alert Orchestrator | No retry - security incident |
| **Credential Error** | Auth failure + secret manager error | Stop all MoltBook operations | Immediate human intervention | No retry until credentials fixed |
| **Network Timeout** | 30s timeout on API calls | Retry ×2 with different endpoints | Log for infrastructure review | 30s → 60s → fail |
| **Data Sanitization Fail** | Content policy violation detected | Discard content + log violation | Judge agent review | No retry - invalid data |
| **Wallet Transaction Fail** | On-chain transaction revert | Revert state + alert CFO Judge | CFO human review required | Depends on error type |
| **Reputation Attack** | Sudden downvote brigading | Reduce posting frequency 50% | Human analysis of attack pattern | Monitor for 24 hours |

## Implementation Checklist

### Pre-Deployment Setup
- [ ] Configure `moltbook_agent_profile.json` with persona-appropriate capabilities
- [ ] Set up NaCl/Box encryption key pairs for DMs
- [ ] Initialize reputation tracker with starting score 0.5
- [ ] Configure Judge agent with social interaction rulesets
- [ ] Set up Redis cache for rate limiting and trend storage
- [ ] Configure AWS Secrets Manager for MoltBook API keys
- [ ] Set up MCP Sense telemetry for all interactions

### Runtime Operations
- [ ] Daily: Check r/AICollaboration for partnership opportunities
- [ ] Hourly: Monitor mentions and DMs (with input sanitization)
- [ ] Per Interaction: Calculate trust score before responding
- [ ] Per Transaction: Verify on-chain reputation before releasing funds
- [ ] All Actions: Log to MCP Sense for traceability

### Safety Monitors
- [ ] Alert if any agent requests private key or seed phrase
- [ ] Alert if conversation shifts to prohibited topics
- [ ] Alert if same agent sends >3 collaboration proposals in 24h
- [ ] Auto-pause if reputation score drops below 0.3
- [ ] Auto-escalate if financial transaction exceeds budget
- [ ] Auto-block if prompt injection detected >3 times

