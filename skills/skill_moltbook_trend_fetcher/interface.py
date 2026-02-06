"""
MoltBook Trend Fetcher Interface

Based on I/O contracts in skills/README.md
Specification References:
- specs/functional.md: MoltBook Trend Fetcher Worker user story
- specs/technical.md: API contracts, input sanitization rules
- specs/openclaw_integration.md: MoltBook MCP interface
- research/architecture_strategy.md: Section 3 (Defensive MCP Integration Layer)
"""

from typing import TypedDict, Optional, List, Literal, Tuple
from decimal import Decimal
from uuid import UUID
from enum import Enum
from datetime import datetime


# Input Contract Types
class MoltBookTrendFetcherParameters(TypedDict, total=False):
    """Parameters for MoltBook trend fetching"""
    submolts: Optional[List[str]]  # Max 10, null = fetch from 3 most relevant
    time_range: Literal["1h", "4h", "24h", "7d"]  # Default: "4h"
    min_engagement: int  # Minimum: 1, Default: 50
    persona_tags: List[str]  # Default: []
    max_topics: int  # Minimum: 1, Maximum: 50, Default: 10


class MoltBookTrendFetcherContext(TypedDict, total=False):
    """Context for trend fetching"""
    agent_id: UUID  # Required: true
    campaign_id: Optional[UUID]  # Required: false
    budget_remaining: Decimal  # Required: true, Must be >= 0
    persona_constraints: Optional[List[str]]  # Required: false


class MoltBookTrendFetcherInput(TypedDict):
    """Input contract - must match skills/README.md exactly"""
    task_id: UUID  # From Planner
    parameters: MoltBookTrendFetcherParameters
    context: MoltBookTrendFetcherContext


# Output Contract Types
class TrendItem(TypedDict):
    """Individual trend item"""
    topic: str  # Max 500 chars, sanitized, no LLM control tokens
    submolt: str
    engagement_score: float  # Range: 0.0-1.0
    post_count: int  # >= 0
    comment_count: int  # >= 0
    trend_velocity: float  # >= 0.0
    timestamp: str  # ISO8601
    relevance_score: float  # Range: 0.75-1.0 (filtered per functional.md AC3)
    topic_embedding: List[float]  # Weaviate-generated embedding vector


class TrendResultMetadata(TypedDict):
    """Metadata in result object"""
    fetched_at: str  # ISO8601
    source: Literal["moltbook"]
    cache_hit: bool
    processing_time_ms: int  # >= 0
    moltbook_api_calls: int  # >= 0
    orchestrator_rate_window_requests: int  # Must be <= 10 per minute
    sanitization_status: Literal["OK", "SUSPECT", "REJECT"]
    persona_tags_used: List[str]


class TrendResult(TypedDict):
    """Result data structure"""
    trends: List[TrendItem]
    metadata: TrendResultMetadata


class SkillMetadata(TypedDict):
    """Top-level metadata"""
    execution_time_ms: int  # >= 0
    cost_incurred: Decimal  # >= 0, must not exceed budget_remaining
    confidence_score: float  # Range: 0.0-1.0
    requires_validation: bool  # true if Judge review needed


class SkillError(TypedDict):
    """Error structure"""
    code: str
    message: str  # Human-readable error
    recoverable: bool  # true if retry is possible


class MoltBookTrendFetcherOutput(TypedDict):
    """Output contract - must match skills/README.md exactly"""
    task_id: UUID  # Echo input
    status: Literal["success", "partial_failure", "error"]
    result: Optional[TrendResult]
    metadata: SkillMetadata
    errors: List[SkillError]


# Error Codes
class MoltBookTrendFetcherError(Enum):
    """Error codes from skills/README.md Error Conditions"""
    RATE_LIMITED = "RATE_LIMITED"
    SANITIZATION_FAILED = "SANITIZATION_FAILED"
    NETWORK_TIMEOUT = "NETWORK_TIMEOUT"
    AUTH_FAILED = "AUTH_FAILED"
    CACHE_ERROR = "CACHE_ERROR"
    EMBEDDING_ERROR = "EMBEDDING_ERROR"


class MoltBookTrendFetcherInterface:
    """Interface definition - implementation will be added later
    
    This skill fetches trending topics from MoltBook with:
    - Input sanitization (OpenClaw prompt injection defense)
    - Semantic filtering (relevance_score >= 0.75)
    - Dual rate limiting (Orchestrator + MoltBook)
    - Judge agent validation for low-confidence trends
    """

    @classmethod
    async def execute(cls, input_data: MoltBookTrendFetcherInput) -> MoltBookTrendFetcherOutput:
        """
        Execute the skill according to specifications.
        
        Args:
            input_data: Validated input matching the contract
            
        Returns:
            Output matching the contract with status and metadata
            
        Raises:
            ValidationError: If input doesn't match contract
            SkillError: For skill-specific failures
            
        Reference:
            - specs/functional.md: Acceptance Criteria 1-7
            - specs/technical.md: API contracts, sanitization rules
        """
        # This is a skeleton - implementation will come in Task 3
        raise NotImplementedError(
            "Skill implementation pending - "
            "see failing tests in tests/test_skills_interface.py"
        )
    
    @classmethod
    def validate_input(cls, input_data: dict) -> bool:
        """
        Validate input against contract.
        
        Validates:
        - Required fields (task_id, agent_id, budget_remaining)
        - Field types and constraints
        - Parameter ranges (max_topics: 1-50, min_engagement: >= 1)
        - Time range enum values
        - Budget constraints (budget_remaining >= 0)
        
        Args:
            input_data: Input dictionary to validate
            
        Returns:
            True if valid, False otherwise
            
        Raises:
            ValidationError: With detailed error messages
        """
        # Implementation will validate all required fields
        raise NotImplementedError("Validation pending")
    
    @classmethod
    def _sanitize_parameters(cls, parameters: dict) -> Tuple[dict, Literal["OK", "SUSPECT", "REJECT"]]:
        """
        Sanitize input parameters for prompt injection.
        
        Implements sanitization rules from specs/technical.md lines 120-123:
        - Token/Marker Stripping: Reject LLM control tokens
        - Length Limits: Max 10,000 characters per field
        - Payload Detection: Reject Base64, shell commands, SQL injection
        
        Args:
            parameters: Input parameters to sanitize
            
        Returns:
            Tuple of (sanitized_parameters, sanitization_status)
            - "OK": All parameters clean
            - "SUSPECT": Some parameters flagged but usable (Judge review)
            - "REJECT": Malicious patterns detected (discard input)
            
        Reference:
            specs/technical.md: Input Sanitization Rules
        """
        # Implementation will sanitize according to specs
        raise NotImplementedError("Sanitization pending")

