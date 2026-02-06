"""
Wallet Manager Skill

Manages non-custodial wallet operations for agentic commerce with CFO Judge
approval for transactions exceeding thresholds.

Reference: skills/README.md - skill_wallet_manager
"""

from .interface import (
    WalletManagerInput,
    WalletManagerOutput,
    WalletManagerError,
    WalletManagerInterface,
)

__all__ = [
    "WalletManagerInput",
    "WalletManagerOutput",
    "WalletManagerError",
    "WalletManagerInterface",
]

