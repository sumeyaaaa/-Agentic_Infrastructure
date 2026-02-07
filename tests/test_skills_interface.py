"""
Test Skills Interface

Tests that skill modules accept correct parameters according to their I/O contracts.

This test file follows TDD principles:
- Tests are written BEFORE implementation
- Tests SHOULD FAIL initially (defining the "empty slot" the AI must fill)
- Tests define the contract that implementation must satisfy

Reference: project.md Task 3.1
"""

import pytest
from uuid import UUID, uuid4
from decimal import Decimal
from typing import get_type_hints
import inspect

# Import skill interfaces
from skills.skill_moltbook_trend_fetcher.interface import (
    MoltBookTrendFetcherInterface,
    MoltBookTrendFetcherInput,
    MoltBookTrendFetcherOutput,
    MoltBookTrendFetcherError,
    MoltBookTrendFetcherParameters,
    MoltBookTrendFetcherContext,
)

from skills.skill_content_generator.interface import (
    ContentGeneratorInterface,
    ContentGeneratorInput,
    ContentGeneratorOutput,
    ContentGeneratorError,
    ContentGeneratorParameters,
    ContentGeneratorContext,
)

from skills.skill_wallet_manager.interface import (
    WalletManagerInterface,
    WalletManagerInput,
    WalletManagerOutput,
    WalletManagerError,
    WalletManagerParameters,
    WalletManagerContext,
)


class TestSkillImports:
    """Test that all skill modules can be imported correctly"""
    
    def test_moltbook_trend_fetcher_imports(self):
        """Test that MoltBook Trend Fetcher skill can be imported"""
        assert MoltBookTrendFetcherInterface is not None
        assert MoltBookTrendFetcherInput is not None
        assert MoltBookTrendFetcherOutput is not None
        assert MoltBookTrendFetcherError is not None
    
    def test_content_generator_imports(self):
        """Test that Content Generator skill can be imported"""
        assert ContentGeneratorInterface is not None
        assert ContentGeneratorInput is not None
        assert ContentGeneratorOutput is not None
        assert ContentGeneratorError is not None
    
    def test_wallet_manager_imports(self):
        """Test that Wallet Manager skill can be imported"""
        assert WalletManagerInterface is not None
        assert WalletManagerInput is not None
        assert WalletManagerOutput is not None
        assert WalletManagerError is not None


class TestSkillInterfaceStructure:
    """Test that skill interfaces have the required structure"""
    
    def test_moltbook_trend_fetcher_has_execute(self):
        """Test that MoltBook Trend Fetcher has execute method"""
        assert hasattr(MoltBookTrendFetcherInterface, 'execute')
        assert inspect.iscoroutinefunction(MoltBookTrendFetcherInterface.execute) or \
               inspect.ismethod(MoltBookTrendFetcherInterface.execute)
    
    def test_moltbook_trend_fetcher_has_validate_input(self):
        """Test that MoltBook Trend Fetcher has validate_input method"""
        assert hasattr(MoltBookTrendFetcherInterface, 'validate_input')
        assert inspect.ismethod(MoltBookTrendFetcherInterface.validate_input)
    
    def test_moltbook_trend_fetcher_has_sanitize(self):
        """Test that MoltBook Trend Fetcher has _sanitize_parameters method"""
        assert hasattr(MoltBookTrendFetcherInterface, '_sanitize_parameters')
        assert inspect.ismethod(MoltBookTrendFetcherInterface._sanitize_parameters)
    
    def test_content_generator_has_execute(self):
        """Test that Content Generator has execute method"""
        assert hasattr(ContentGeneratorInterface, 'execute')
        assert inspect.iscoroutinefunction(ContentGeneratorInterface.execute) or \
               inspect.ismethod(ContentGeneratorInterface.execute)
    
    def test_content_generator_has_validate_input(self):
        """Test that Content Generator has validate_input method"""
        assert hasattr(ContentGeneratorInterface, 'validate_input')
        assert inspect.ismethod(ContentGeneratorInterface.validate_input)
    
    def test_wallet_manager_has_execute(self):
        """Test that Wallet Manager has execute method"""
        assert hasattr(WalletManagerInterface, 'execute')
        assert inspect.iscoroutinefunction(WalletManagerInterface.execute) or \
               inspect.ismethod(WalletManagerInterface.execute)
    
    def test_wallet_manager_has_validate_input(self):
        """Test that Wallet Manager has validate_input method"""
        assert hasattr(WalletManagerInterface, 'validate_input')
        assert inspect.ismethod(WalletManagerInterface.validate_input)


class TestMoltBookTrendFetcherInputContract:
    """Test MoltBook Trend Fetcher input contract matches skills/README.md"""
    
    def test_input_contract_has_task_id(self):
        """Test that input contract requires task_id (UUID)"""
        # This test will pass - TypedDict enforces structure
        hints = get_type_hints(MoltBookTrendFetcherInput)
        assert 'task_id' in hints
        assert hints['task_id'] == UUID
    
    def test_input_contract_has_parameters(self):
        """Test that input contract has parameters field"""
        hints = get_type_hints(MoltBookTrendFetcherInput)
        assert 'parameters' in hints
        assert hints['parameters'] == MoltBookTrendFetcherParameters
    
    def test_input_contract_has_context(self):
        """Test that input contract has context field"""
        hints = get_type_hints(MoltBookTrendFetcherInput)
        assert 'context' in hints
        assert hints['context'] == MoltBookTrendFetcherContext
    
    def test_parameters_has_required_fields(self):
        """Test that parameters TypedDict has expected fields"""
        hints = get_type_hints(MoltBookTrendFetcherParameters)
        # These fields should exist (total=False means optional)
        expected_fields = ['submolts', 'time_range', 'min_engagement', 'persona_tags', 'max_topics']
        for field in expected_fields:
            assert field in hints, f"Missing field: {field}"
    
    def test_context_has_required_fields(self):
        """Test that context TypedDict has required fields"""
        hints = get_type_hints(MoltBookTrendFetcherContext)
        # agent_id and budget_remaining are required (not in total=False dict)
        assert 'agent_id' in hints
        assert 'budget_remaining' in hints


class TestContentGeneratorInputContract:
    """Test Content Generator input contract matches skills/README.md"""
    
    def test_input_contract_structure(self):
        """Test that input contract has required fields"""
        hints = get_type_hints(ContentGeneratorInput)
        assert 'task_id' in hints
        assert 'parameters' in hints
        assert 'context' in hints
    
    def test_parameters_has_content_type(self):
        """Test that parameters has content_type field"""
        hints = get_type_hints(ContentGeneratorParameters)
        assert 'content_type' in hints
    
    def test_parameters_has_topic(self):
        """Test that parameters has topic field"""
        hints = get_type_hints(ContentGeneratorParameters)
        assert 'topic' in hints


class TestWalletManagerInputContract:
    """Test Wallet Manager input contract matches skills/README.md"""
    
    def test_input_contract_structure(self):
        """Test that input contract has required fields"""
        hints = get_type_hints(WalletManagerInput)
        assert 'task_id' in hints
        assert 'parameters' in hints
        assert 'context' in hints
    
    def test_parameters_has_operation(self):
        """Test that parameters has operation field"""
        hints = get_type_hints(WalletManagerParameters)
        assert 'operation' in hints


class TestSkillErrorCodes:
    """Test that error enums match skills/README.md"""
    
    def test_moltbook_trend_fetcher_error_codes(self):
        """Test that MoltBook Trend Fetcher has all required error codes"""
        expected_errors = [
            'RATE_LIMITED',
            'SANITIZATION_FAILED',
            'NETWORK_TIMEOUT',
            'AUTH_FAILED',
            'CACHE_ERROR',
            'EMBEDDING_ERROR',
        ]
        for error_code in expected_errors:
            assert hasattr(MoltBookTrendFetcherError, error_code), \
                f"Missing error code: {error_code}"
            assert getattr(MoltBookTrendFetcherError, error_code).value == error_code
    
    def test_content_generator_error_codes(self):
        """Test that Content Generator has all required error codes"""
        expected_errors = [
            'BUDGET_EXCEEDED',
            'CONSISTENCY_FAILED',
            'GENERATION_ERROR',
            'PLATFORM_INCOMPATIBLE',
            'COST_ESTIMATE_FAILED',
        ]
        for error_code in expected_errors:
            assert hasattr(ContentGeneratorError, error_code), \
                f"Missing error code: {error_code}"
            assert getattr(ContentGeneratorError, error_code).value == error_code
    
    def test_wallet_manager_error_codes(self):
        """Test that Wallet Manager has all required error codes"""
        expected_errors = [
            'BUDGET_EXCEEDED',
            'INSUFFICIENT_BALANCE',
            'INVALID_ADDRESS',
            'CFO_REJECTED',
            'TRANSACTION_FAILED',
            'GAS_ESTIMATE_FAILED',
        ]
        for error_code in expected_errors:
            assert hasattr(WalletManagerError, error_code), \
                f"Missing error code: {error_code}"
            assert getattr(WalletManagerError, error_code).value == error_code


class TestSkillExecutionContracts:
    """Test that execute methods raise NotImplementedError (TDD - should fail until implemented)"""
    
    @pytest.mark.asyncio
    async def test_moltbook_trend_fetcher_execute_not_implemented(self):
        """Test that execute raises NotImplementedError (expected to fail until implementation)"""
        input_data: MoltBookTrendFetcherInput = {
            'task_id': uuid4(),
            'parameters': {},
            'context': {
                'agent_id': uuid4(),
                'budget_remaining': Decimal('100.00'),
            }
        }
        with pytest.raises(NotImplementedError):
            await MoltBookTrendFetcherInterface.execute(input_data)
    
    @pytest.mark.asyncio
    async def test_content_generator_execute_not_implemented(self):
        """Test that execute raises NotImplementedError (expected to fail until implementation)"""
        input_data: ContentGeneratorInput = {
            'task_id': uuid4(),
            'parameters': {
                'content_type': 'text',
                'topic': 'test topic',
                'platform': 'twitter',
                'cost_constraints': {
                    'max_cost_usd': Decimal('10.00'),
                }
            },
            'context': {
                'agent_id': uuid4(),
                'budget_remaining': Decimal('100.00'),
            }
        }
        with pytest.raises(NotImplementedError):
            await ContentGeneratorInterface.execute(input_data)
    
    @pytest.mark.asyncio
    async def test_wallet_manager_execute_not_implemented(self):
        """Test that execute raises NotImplementedError (expected to fail until implementation)"""
        input_data: WalletManagerInput = {
            'task_id': uuid4(),
            'parameters': {
                'operation': 'get_balance',
            },
            'context': {
                'agent_id': uuid4(),
                'budget_remaining': Decimal('100.00'),
            }
        }
        with pytest.raises(NotImplementedError):
            await WalletManagerInterface.execute(input_data)


class TestSkillValidationContracts:
    """Test that validate_input methods raise NotImplementedError (TDD)"""
    
    def test_moltbook_trend_fetcher_validate_not_implemented(self):
        """Test that validate_input raises NotImplementedError"""
        with pytest.raises(NotImplementedError):
            MoltBookTrendFetcherInterface.validate_input({})
    
    def test_content_generator_validate_not_implemented(self):
        """Test that validate_input raises NotImplementedError"""
        with pytest.raises(NotImplementedError):
            ContentGeneratorInterface.validate_input({})
    
    def test_wallet_manager_validate_not_implemented(self):
        """Test that validate_input raises NotImplementedError"""
        with pytest.raises(NotImplementedError):
            WalletManagerInterface.validate_input({})


