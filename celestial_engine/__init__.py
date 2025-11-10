"""
Celestial Engine - Advanced Theological Entry Generation System

A comprehensive, production-grade system for generating CELESTIAL-tier
Orthodox Christian theological entries using local LLMs.

Features:
- Advanced preprocessing and topic analysis
- Multi-model orchestration
- Comprehensive validation system
- Iterative refinement to achieve quality targets
- Batch processing with parallel execution
- Full monitoring and logging
"""

__version__ = "2.0.0"
__author__ = "Celestial Engine Team"
__license__ = "MIT"

from .core.generator import CelestialGenerator
from .core.config import get_config
from .core.models import Entry, Section, ValidationResult, QualityTier
from .validation.validator import EntryValidator
from .preprocessing.topic_analyzer import TopicAnalyzer

__all__ = [
    "CelestialGenerator",
    "get_config",
    "Entry",
    "Section",
    "ValidationResult",
    "QualityTier",
    "EntryValidator",
    "TopicAnalyzer"
]
