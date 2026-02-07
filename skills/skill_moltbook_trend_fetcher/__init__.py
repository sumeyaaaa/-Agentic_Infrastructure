"""
MoltBook Trend Fetcher Skill

Fetches trending topics from MoltBook agent social network with semantic filtering
and input sanitization.

Reference: skills/README.md - skill_moltbook_trend_fetcher
"""

from .interface import (
    MoltBookTrendFetcherInput,
    MoltBookTrendFetcherOutput,
    MoltBookTrendFetcherError,
    MoltBookTrendFetcherInterface,
)

__all__ = [
    "MoltBookTrendFetcherInput",
    "MoltBookTrendFetcherOutput",
    "MoltBookTrendFetcherError",
    "MoltBookTrendFetcherInterface",
]


