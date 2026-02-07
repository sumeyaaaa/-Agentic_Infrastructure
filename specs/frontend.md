# Frontend Specifications

## Overview

This document defines the frontend interfaces for Project Chimera's human interaction layer. The system provides two primary dashboards:

1. **HITL Dashboard**: Human-in-the-Loop review queue for content requiring human approval
2. **Orchestrator Control Panel**: Fleet management and monitoring interface

**Reference Architecture**: `research/architecture_strategy.md` §2.2 (HITL), §4 (Implementation Roadmap)  
**Technical Stack**: FastAPI (backend) + React (frontend) - lightweight, production-ready stack

---

## 1. HITL Dashboard

### 1.1 Purpose

The HITL Dashboard enables human reviewers to:
- Review and approve/reject content flagged by the Judge agent
- Override automated decisions when needed
- View context and reasoning for escalations
- Track review history and audit trails

### 1.2 API Endpoints (FastAPI Backend)

#### `GET /api/hitl/queue`
**Purpose**: Fetch pending items requiring human review

**Query Parameters**:
- `status`: `pending|reviewed|all` (default: `pending`)
- `priority`: `high|medium|low` (optional filter)
- `agent_id`: UUID (optional filter by agent)
- `limit`: integer (default: 50, max: 200)
- `offset`: integer (default: 0)

**Response Schema**:
```json
{
  "items": [
    {
      "review_id": "uuid_v4",
      "task_id": "uuid_v4",
      "agent_id": "uuid_v4",
      "agent_handle": "string",
      "campaign_id": "uuid_v4",
      "escalation_reason": "LOW_CONFIDENCE|SENSITIVE_TOPIC|BUDGET_THRESHOLD|SANITIZATION_FLAG",
      "priority": "high|medium|low",
      "judge_confidence": 0.65,
      "requires_validation": true,
      "content_preview": {
        "type": "trend_fetch|content_generation|wallet_transaction",
        "data": {}
      },
      "judge_reasoning": "string",
      "created_at": "2026-02-04T14:30:00Z",
      "expires_at": "2026-02-04T15:30:00Z"
    }
  ],
  "total": 42,
  "page": 1,
  "page_size": 50
}
```

#### `POST /api/hitl/review/{review_id}/approve`
**Purpose**: Approve a pending review item

**Request Body**:
```json
{
  "reviewer_id": "uuid_v4",
  "notes": "string (optional)",
  "override_judge": false
}
```

**Response Schema**:
```json
{
  "review_id": "uuid_v4",
  "status": "approved",
  "approved_at": "2026-02-04T14:35:00Z",
  "reviewer_id": "uuid_v4",
  "next_action": {
    "type": "publish|execute|proceed",
    "task_id": "uuid_v4"
  }
}
```

#### `POST /api/hitl/review/{review_id}/reject`
**Purpose**: Reject a pending review item

**Request Body**:
```json
{
  "reviewer_id": "uuid_v4",
  "rejection_reason": "string (required)",
  "block_agent": false,
  "escalate_to_orchestrator": false
}
```

**Response Schema**:
```json
{
  "review_id": "uuid_v4",
  "status": "rejected",
  "rejected_at": "2026-02-04T14:35:00Z",
  "reviewer_id": "uuid_v4",
  "actions_taken": [
    "task_cancelled",
    "agent_notified"
  ]
}
```

#### `GET /api/hitl/review/{review_id}`
**Purpose**: Get full details of a review item

**Response Schema**:
```json
{
  "review_id": "uuid_v4",
  "task_id": "uuid_v4",
  "agent_id": "uuid_v4",
  "agent_handle": "string",
  "campaign_id": "uuid_v4",
  "escalation_reason": "LOW_CONFIDENCE",
  "priority": "high",
  "judge_confidence": 0.65,
  "content": {
    "type": "trend_fetch",
    "data": {
      "trends": [...],
      "relevance_scores": [...],
      "sanitization_status": "SUSPECT"
    }
  },
  "judge_reasoning": "Relevance score 0.72 below threshold 0.75, sanitization flag detected",
  "context": {
    "budget_remaining": 45.25,
    "persona_constraints": ["fashion", "genz"],
    "campaign_goals": ["engagement", "reach"]
  },
  "history": [
    {
      "event": "judge_escalated",
      "timestamp": "2026-02-04T14:30:00Z",
      "details": "string"
    }
  ],
  "created_at": "2026-02-04T14:30:00Z",
  "expires_at": "2026-02-04T15:30:00Z"
}
```

### 1.3 React Component Structure

```
src/
  components/
    HITLDashboard/
      Dashboard.tsx          # Main dashboard container
      ReviewQueue.tsx        # List of pending items
      ReviewItem.tsx         # Individual review card
      ReviewDetail.tsx       # Full review modal/detail view
      ApproveButton.tsx      # Approval action
      RejectButton.tsx       # Rejection action
      FilterBar.tsx          # Status/priority filters
  hooks/
    useHITLQueue.ts          # React Query hook for queue data
    useReviewAction.ts       # Mutation hook for approve/reject
  services/
    hitlApi.ts              # Axios client for HITL endpoints
```

### 1.4 User Flows

**Flow 1: Review and Approve**
1. Reviewer opens HITL Dashboard
2. Sees list of pending items sorted by priority (high → medium → low)
3. Clicks on item to view full details
4. Reviews Judge reasoning, content preview, and context
5. Clicks "Approve" or "Reject"
6. If approved, task proceeds; if rejected, task is cancelled and agent notified

**Flow 2: Bulk Actions**
1. Reviewer selects multiple items (same escalation reason)
2. Clicks "Bulk Approve" or "Bulk Reject"
3. Confirms action
4. All selected items processed in batch

### 1.5 Authentication & Authorization

- **Authentication**: JWT tokens (same as agent authentication)
- **Authorization**: Role-based access control (RBAC)
  - `reviewer`: Can approve/reject items
  - `admin`: Can override Judge decisions, block agents
  - `auditor`: Read-only access to review history

---

## 2. Orchestrator Control Panel

### 2.1 Purpose

The Orchestrator Control Panel enables operators to:
- Monitor fleet health (agent status, queue depth, error rates)
- View campaign performance and ROI metrics
- Manually intervene (pause agents, adjust budgets, override policies)
- View audit logs and compliance reports

### 2.2 API Endpoints (FastAPI Backend)

#### `GET /api/orchestrator/fleet/status`
**Purpose**: Get overall fleet health metrics

**Response Schema**:
```json
{
  "fleet_summary": {
    "total_agents": 150,
    "active_agents": 142,
    "paused_agents": 5,
    "error_agents": 3,
    "queue_depth": 234,
    "avg_processing_time_ms": 450,
    "error_rate_24h": 0.02
  },
  "agents": [
    {
      "agent_id": "uuid_v4",
      "handle": "string",
      "status": "active|paused|error",
      "last_heartbeat": "2026-02-04T14:30:00Z",
      "tasks_completed_24h": 45,
      "tasks_failed_24h": 1,
      "budget_remaining": 125.50
    }
  ],
  "updated_at": "2026-02-04T14:35:00Z"
}
```

#### `GET /api/orchestrator/campaigns/{campaign_id}/metrics`
**Purpose**: Get campaign performance metrics

**Response Schema**:
```json
{
  "campaign_id": "uuid_v4",
  "name": "string",
  "status": "active|paused|completed",
  "metrics": {
    "roi": 2.45,
    "total_spent": 1250.00,
    "total_revenue": 3062.50,
    "engagement_rate": 0.085,
    "reach": 45000,
    "impressions": 125000
  },
  "agents": [
    {
      "agent_id": "uuid_v4",
      "handle": "string",
      "contribution": {
        "posts": 45,
        "engagement": 1250,
        "cost": 125.50
      }
    }
  ],
  "period": {
    "start": "2026-02-01T00:00:00Z",
    "end": "2026-02-04T23:59:59Z"
  }
}
```

#### `POST /api/orchestrator/agents/{agent_id}/pause`
**Purpose**: Pause an agent (manual intervention)

**Request Body**:
```json
{
  "reason": "string (required)",
  "operator_id": "uuid_v4"
}
```

**Response Schema**:
```json
{
  "agent_id": "uuid_v4",
  "status": "paused",
  "paused_at": "2026-02-04T14:35:00Z",
  "paused_by": "uuid_v4",
  "reason": "string"
}
```

#### `POST /api/orchestrator/agents/{agent_id}/resume`
**Purpose**: Resume a paused agent

**Response Schema**:
```json
{
  "agent_id": "uuid_v4",
  "status": "active",
  "resumed_at": "2026-02-04T14:35:00Z",
  "resumed_by": "uuid_v4"
}
```

#### `GET /api/orchestrator/audit/logs`
**Purpose**: Get audit logs for compliance

**Query Parameters**:
- `agent_id`: UUID (optional)
- `campaign_id`: UUID (optional)
- `event_type`: `approval|rejection|pause|resume|budget_override` (optional)
- `start_date`: ISO 8601 (required)
- `end_date`: ISO 8601 (required)
- `limit`: integer (default: 100, max: 1000)

**Response Schema**:
```json
{
  "logs": [
    {
      "log_id": "uuid_v4",
      "timestamp": "2026-02-04T14:30:00Z",
      "event_type": "approval",
      "actor_id": "uuid_v4",
      "actor_type": "human|agent|system",
      "target_id": "uuid_v4",
      "target_type": "agent|campaign|task",
      "action": "approved_review",
      "details": {},
      "ip_address": "string",
      "user_agent": "string"
    }
  ],
  "total": 1250,
  "page": 1,
  "page_size": 100
}
```

### 2.3 React Component Structure

```
src/
  components/
    OrchestratorPanel/
      Dashboard.tsx          # Main control panel
      FleetStatus.tsx         # Fleet health overview
      AgentList.tsx           # List of agents with status
      AgentCard.tsx           # Individual agent card
      CampaignMetrics.tsx     # Campaign performance charts
      AuditLogViewer.tsx      # Audit log table
      InterventionModal.tsx   # Pause/resume/override modal
  hooks/
    useFleetStatus.ts         # React Query hook for fleet data
    useCampaignMetrics.ts     # React Query hook for campaign data
    useAgentAction.ts         # Mutation hook for pause/resume
  services/
    orchestratorApi.ts        # Axios client for orchestrator endpoints
  charts/
    ROIMetric.tsx             # ROI visualization
    EngagementChart.tsx       # Engagement trends
    ErrorRateChart.tsx        # Error rate over time
```

### 2.4 User Flows

**Flow 1: Monitor Fleet Health**
1. Operator opens Orchestrator Control Panel
2. Views fleet summary (total agents, active, paused, error rates)
3. Clicks on agent to view detailed metrics
4. Identifies agent with high error rate
5. Clicks "Pause" to investigate

**Flow 2: Review Campaign Performance**
1. Operator navigates to Campaigns section
2. Selects campaign to view metrics
3. Reviews ROI, engagement, and cost breakdown
4. Adjusts budget or pauses underperforming agents

**Flow 3: Audit Trail Review**
1. Operator navigates to Audit Logs
2. Filters by date range, agent, or event type
3. Exports logs for compliance reporting

### 2.5 Real-time Updates

- **WebSocket Connection**: `/ws/orchestrator/updates`
- **Events**: `agent_status_change`, `task_completed`, `error_occurred`, `budget_threshold_reached`
- **Implementation**: FastAPI WebSocket endpoint + React `useWebSocket` hook

---

## 3. Shared Components & Infrastructure

### 3.1 Authentication Service

**Endpoint**: `POST /api/auth/login`

**Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```

**Response Schema**:
```json
{
  "access_token": "jwt_token",
  "refresh_token": "jwt_token",
  "user": {
    "user_id": "uuid_v4",
    "username": "string",
    "role": "reviewer|admin|auditor|operator",
    "permissions": ["approve_reviews", "pause_agents", "view_audit_logs"]
  }
}
```

### 3.2 State Management

- **React Query**: Server state management (API data, caching, refetching)
- **Zustand**: Client state management (UI state, filters, preferences)
- **React Context**: Authentication context (user, token, permissions)

### 3.3 Error Handling

- **API Errors**: Standardized error response format
  ```json
  {
    "error": {
      "code": "RATE_LIMITED|AUTH_FAILED|VALIDATION_ERROR",
      "message": "string",
      "details": {}
    }
  }
  ```
- **Frontend**: React Error Boundaries + toast notifications for user feedback

### 3.4 Responsive Design

- **Breakpoints**: Mobile (< 768px), Tablet (768px - 1024px), Desktop (> 1024px)
- **Framework**: Tailwind CSS for utility-first styling
- **Accessibility**: WCAG 2.1 AA compliance (keyboard navigation, screen reader support)

---

## 4. Implementation Notes

### 4.1 Technology Stack

- **Backend**: FastAPI (Python) - RESTful APIs + WebSocket support
- **Frontend**: React 18+ with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Query + Zustand
- **Build Tool**: Vite
- **Testing**: Jest + React Testing Library

### 4.2 Security Considerations

- **CORS**: Configured for production domain only
- **Rate Limiting**: API endpoints rate-limited per user role
- **Input Validation**: All API inputs validated using Pydantic models
- **XSS Protection**: React's built-in escaping + Content Security Policy headers

### 4.3 Deployment

- **Backend**: Docker container (FastAPI app)
- **Frontend**: Static build served via Nginx or CDN
- **Environment Variables**: Separate configs for dev/staging/production

---

## 5. Success Metrics

- **HITL Dashboard**:
  - Average review time < 2 minutes
  - Review queue backlog < 50 items
  - Approval/rejection rate tracked for audit

- **Orchestrator Control Panel**:
  - Real-time updates latency < 1 second
  - Dashboard load time < 2 seconds
  - 99.9% uptime for monitoring endpoints

---

**Reference**: `research/architecture_strategy.md` §2.2 (HITL), `specs/_meta.md` §4 (Success Metrics)  
**Next Steps**: Implement FastAPI backend endpoints, then React frontend components (Phase 2 of implementation roadmap)

