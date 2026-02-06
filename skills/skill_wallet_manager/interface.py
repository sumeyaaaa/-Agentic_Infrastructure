"""
Wallet Manager Interface

Based on I/O contracts in skills/README.md
Specification References:
- Coinbase AgentKit: Non-custodial wallet operations (research/research.md)
- research/architecture_strategy.md: Section 2.2 (HITL Framework - CFO Judge)
- specs/_meta.md: Economic Agency First principle, Cost Constraints
"""

from typing import TypedDict, Optional, List, Literal
from decimal import Decimal
from uuid import UUID
from enum import Enum


# Input Contract Types
class TransferDetails(TypedDict, total=False):
    """Transfer operation details"""
    recipient_address: str  # Valid blockchain address format
    amount: Decimal  # Must be > 0, must respect budget_remaining
    token: Literal["USDC", "ETH", "BASE", "mbc-20"]  # Must be supported by Coinbase AgentKit
    memo: str  # Max 200 characters, sanitized


class TokenDeployment(TypedDict, total=False):
    """Token deployment details"""
    token_name: str  # Max 50 characters
    token_symbol: str  # Max 10 characters, uppercase
    initial_supply: int  # Must be > 0
    chain: Literal["base", "ethereum"]  # Must be supported by AgentKit


class WalletManagerParameters(TypedDict, total=False):
    """Parameters for wallet operations"""
    operation: Literal["get_balance", "transfer", "deploy_token", "get_transaction_status"]  # Required: true
    transfer_details: TransferDetails  # Required for transfer operation
    token_deployment: TokenDeployment  # Required for deploy_token operation
    transaction_id: Optional[str]  # Required for get_transaction_status, Valid blockchain transaction hash
    approval_threshold_usd: Decimal  # Default: 50.00 USD, can be overridden per agent


class WalletManagerContext(TypedDict, total=False):
    """Context for wallet operations"""
    agent_id: UUID  # Required: true
    campaign_id: Optional[UUID]  # Required: false
    budget_remaining: Decimal  # Required: true, Must be >= 0
    persona_constraints: Optional[List[str]]  # Required: false


class WalletManagerInput(TypedDict):
    """Input contract - must match skills/README.md exactly"""
    task_id: UUID  # From Planner
    parameters: WalletManagerParameters
    context: WalletManagerContext


# Output Contract Types
class Balance(TypedDict):
    """Wallet balance information"""
    usdc: Decimal
    eth: Decimal
    base: Decimal
    total_usd_equivalent: Decimal  # Calculated using current exchange rates


class Transaction(TypedDict, total=False):
    """Transaction information"""
    transaction_hash: str  # Valid hash format
    status: Literal["pending", "confirmed", "failed"]
    block_number: Optional[int]  # null if pending
    gas_used: Optional[int]  # null if pending
    gas_cost_usd: Decimal  # >= 0
    amount: Decimal
    token: str
    recipient: str
    timestamp: str  # ISO8601


class TokenDeploymentResult(TypedDict):
    """Token deployment result"""
    token_address: str
    token_name: str
    token_symbol: str
    deployment_cost_usd: Decimal


class WalletResultMetadata(TypedDict):
    """Metadata in result object"""
    wallet_address: str  # Base/Ethereum address format
    cfo_approval_required: bool  # true if transaction amount > approval_threshold_usd
    cfo_approval_status: Optional[Literal["pending", "approved", "rejected"]]  # null if approval not required
    budget_after_transaction: Decimal  # budget_remaining - transaction_cost
    audit_log_id: UUID  # Audit log entry ID for traceability


class WalletResult(TypedDict, total=False):
    """Result data structure"""
    operation: str  # Echo input
    balance: Balance  # For get_balance operation
    transaction: Transaction  # For transfer/get_transaction_status operations
    token_deployment: TokenDeploymentResult  # For deploy_token operation
    metadata: WalletResultMetadata


class SkillMetadata(TypedDict):
    """Top-level metadata"""
    execution_time_ms: int  # >= 0
    cost_incurred: Decimal  # Transaction cost + gas fees, >= 0, must not exceed budget_remaining
    confidence_score: float  # Range: 0.0-1.0, used by CFO Judge
    requires_validation: bool  # true if CFO Judge approval required


class SkillError(TypedDict):
    """Error structure"""
    code: str
    message: str  # Human-readable error
    recoverable: bool


class WalletManagerOutput(TypedDict):
    """Output contract - must match skills/README.md exactly"""
    task_id: UUID  # Echo input
    status: Literal["success", "pending_approval", "error"]
    result: Optional[WalletResult]
    metadata: SkillMetadata
    errors: List[SkillError]


# Error Codes
class WalletManagerError(Enum):
    """Error codes from skills/README.md Error Conditions"""
    BUDGET_EXCEEDED = "BUDGET_EXCEEDED"
    INSUFFICIENT_BALANCE = "INSUFFICIENT_BALANCE"
    INVALID_ADDRESS = "INVALID_ADDRESS"
    CFO_REJECTED = "CFO_REJECTED"
    TRANSACTION_FAILED = "TRANSACTION_FAILED"
    GAS_ESTIMATE_FAILED = "GAS_ESTIMATE_FAILED"


class WalletManagerInterface:
    """Interface definition - implementation will be added later
    
    This skill manages wallet operations with:
    - Non-custodial wallet support (Coinbase AgentKit)
    - CFO Judge approval for transactions > threshold
    - Budget controls and audit logging
    - Transaction validation and error handling
    """

    @classmethod
    async def execute(cls, input_data: WalletManagerInput) -> WalletManagerOutput:
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
            - Coinbase AgentKit: Non-custodial wallet operations
            - Architecture Strategy Section 2.2: CFO Judge approval
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
        - Required fields (task_id, operation, agent_id, budget_remaining)
        - Field types and constraints
        - Operation enum values
        - Transfer details (for transfer operation)
        - Token deployment (for deploy_token operation)
        - Transaction ID (for get_transaction_status operation)
        - Budget constraints (budget_remaining >= 0)
        - Approval threshold (should be >= 1.00 USD)
        
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
        Sanitize input parameters for security.
        
        Sanitizes:
        - Memo field (max 200 characters, no injection patterns)
        - Address format validation
        - Amount validation (must be > 0)
        
        Args:
            parameters: Input parameters to sanitize
            
        Returns:
            Sanitized parameters dictionary
            
        Reference:
            specs/technical.md: Input Sanitization Rules
        """
        # Implementation will sanitize according to specs
        raise NotImplementedError("Sanitization pending")

