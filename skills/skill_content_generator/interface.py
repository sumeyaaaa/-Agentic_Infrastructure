"""
Content Generator Interface

Based on I/O contracts in skills/README.md
Specification References:
- SRS §4.3.1: Character consistency locks
- SRS §4.3.2: Tiered video generation strategy
- research/architecture_strategy.md: Section 2.1 (Content Worker Pool)
- specs/_meta.md: Cost Constraints
"""

from typing import TypedDict, Optional, List, Literal
from decimal import Decimal
from uuid import UUID
from enum import Enum


# Input Contract Types
class PersonaGuidance(TypedDict, total=False):
    """Persona guidance for content generation"""
    soul_md_excerpt: str  # Max 2000 characters
    tone: Literal["professional", "casual", "humorous", "educational"]
    character_consistency_lock: bool  # Default: true (SRS §4.3.1)


class MultimodalConfig(TypedDict, total=False):
    """Multimodal content configuration"""
    include_image: bool  # Default: false
    include_video: bool  # Default: false
    video_tier: Literal["quick", "standard", "premium"]  # Default: "standard" (SRS §4.3.2)


class CostConstraints(TypedDict):
    """Cost constraints for generation"""
    max_cost_usd: Decimal  # Required: true, Must be <= budget_remaining
    prefer_cache: bool  # Default: true


class ContentGeneratorParameters(TypedDict):
    """Parameters for content generation"""
    content_type: Literal["text", "image", "video", "multimodal"]  # Required: true
    topic: str  # Required: true, Max 500 chars, sanitized
    platform: Literal["twitter", "instagram", "tiktok", "moltbook"]  # Required: true
    persona_guidance: PersonaGuidance
    multimodal_config: MultimodalConfig
    cost_constraints: CostConstraints


class ContentGeneratorContext(TypedDict, total=False):
    """Context for content generation"""
    agent_id: UUID  # Required: true
    campaign_id: Optional[UUID]  # Required: false
    budget_remaining: Decimal  # Required: true, Must be >= 0
    persona_constraints: Optional[List[str]]  # Required: false


class ContentGeneratorInput(TypedDict):
    """Input contract - must match skills/README.md exactly"""
    task_id: UUID  # From Planner
    parameters: ContentGeneratorParameters
    context: ContentGeneratorContext


# Output Contract Types
class ImageAsset(TypedDict):
    """Generated image asset"""
    asset_id: UUID
    url: str  # S3/GCS object storage URL
    generation_model: str  # e.g., 'ideogram-v1'
    cost_usd: Decimal
    consistency_score: float  # Range: 0.0-1.0 (SRS §4.3.1)


class VideoAsset(TypedDict):
    """Generated video asset"""
    asset_id: UUID
    url: str  # S3/GCS object storage URL
    tier: Literal["quick", "standard", "premium"]
    duration_seconds: int
    cost_usd: Decimal
    consistency_score: float  # Range: 0.0-1.0


class ContentResultMetadata(TypedDict):
    """Metadata in result object"""
    generated_at: str  # ISO8601
    platform: str
    persona_alignment_score: float  # Range: 0.0-1.0, used by Judge agent
    character_consistency_applied: bool
    total_cost_usd: Decimal  # Sum of all asset costs


class ContentResult(TypedDict):
    """Result data structure"""
    content_id: UUID
    text_content: str  # Platform-specific length limits, sanitized, persona-aligned
    image_assets: List[ImageAsset]
    video_assets: List[VideoAsset]
    metadata: ContentResultMetadata


class SkillMetadata(TypedDict):
    """Top-level metadata"""
    execution_time_ms: int  # >= 0
    cost_incurred: Decimal  # Must be <= max_cost_usd and <= budget_remaining
    confidence_score: float  # Range: 0.0-1.0, used by Judge agent
    requires_validation: bool  # true if Judge review needed


class SkillError(TypedDict):
    """Error structure"""
    code: str
    message: str  # Human-readable error
    recoverable: bool


class ContentGeneratorOutput(TypedDict):
    """Output contract - must match skills/README.md exactly"""
    task_id: UUID  # Echo input
    status: Literal["success", "partial_failure", "error"]
    result: Optional[ContentResult]
    metadata: SkillMetadata
    errors: List[SkillError]


# Error Codes
class ContentGeneratorError(Enum):
    """Error codes from skills/README.md Error Conditions"""
    BUDGET_EXCEEDED = "BUDGET_EXCEEDED"
    CONSISTENCY_FAILED = "CONSISTENCY_FAILED"
    GENERATION_ERROR = "GENERATION_ERROR"
    PLATFORM_INCOMPATIBLE = "PLATFORM_INCOMPATIBLE"
    COST_ESTIMATE_FAILED = "COST_ESTIMATE_FAILED"


class ContentGeneratorInterface:
    """Interface definition - implementation will be added later
    
    This skill generates multimodal content with:
    - Character consistency locks (SRS §4.3.1)
    - Tiered video generation strategy (SRS §4.3.2)
    - Cost controls and budget enforcement
    - Judge agent validation for quality and safety
    """

    @classmethod
    async def execute(cls, input_data: ContentGeneratorInput) -> ContentGeneratorOutput:
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
            - SRS §4.3.1: Character consistency locks
            - SRS §4.3.2: Tiered video generation
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
        - Required fields (task_id, content_type, topic, platform, agent_id, budget_remaining)
        - Field types and constraints
        - Content type enum values
        - Platform enum values
        - Budget constraints (budget_remaining >= 0, max_cost_usd <= budget_remaining)
        - Topic length (max 500 characters)
        
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
    def _sanitize_parameters(cls, parameters: dict) -> dict:
        """
        Sanitize input parameters for prompt injection.
        
        Applies same sanitization rules as MoltBook skill:
        - Token/Marker Stripping: Reject LLM control tokens
        - Length Limits: Max 10,000 characters per field
        - Payload Detection: Reject Base64, shell commands, SQL injection
        
        Args:
            parameters: Input parameters to sanitize (especially topic field)
            
        Returns:
            Sanitized parameters dictionary
            
        Reference:
            specs/technical.md: Input Sanitization Rules (lines 120-123)
        """
        # Implementation will sanitize according to specs
        raise NotImplementedError("Sanitization pending")

