"""
Content Generator Skill

Generates multimodal content (text, images, video) with character consistency
and cost controls.

Reference: skills/README.md - skill_content_generator
"""

from .interface import (
    ContentGeneratorInput,
    ContentGeneratorOutput,
    ContentGeneratorError,
    ContentGeneratorInterface,
)

__all__ = [
    "ContentGeneratorInput",
    "ContentGeneratorOutput",
    "ContentGeneratorError",
    "ContentGeneratorInterface",
]


