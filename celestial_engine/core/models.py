"""
Core data models for the Celestial Engine.
Defines the structure of entries, sections, validation results, etc.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional, Any
from pathlib import Path
import json


class QualityTier(Enum):
    """Quality tier classifications for entries."""
    CELESTIAL = "CELESTIAL"
    ADAMANTINE = "ADAMANTINE"
    PLATINUM = "PLATINUM"
    GOLD = "GOLD"
    SILVER = "SILVER"
    BRONZE = "BRONZE"
    UNRANKED = "UNRANKED"


class SectionType(Enum):
    """Section types in an entry."""
    INTRODUCTION = "introduction"
    PATRISTIC_MIND = "patristic_mind"
    SYMPHONY_OF_CLASHES = "symphony_of_clashes"
    ORTHODOX_AFFIRMATION = "orthodox_affirmation"
    SYNTHESIS = "synthesis"
    CONCLUSION = "conclusion"


@dataclass
class Section:
    """Represents a single section of an entry."""
    name: str
    slug: str
    content: str = ""
    word_count: int = 0
    min_words: int = 1500
    target_words: int = 2000
    max_words: int = 2500
    model: str = "primary"
    requirements: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.content:
            self.word_count = len(self.content.split())

    def update_content(self, content: str):
        """Update section content and recalculate word count."""
        self.content = content
        self.word_count = len(content.split())

    def is_complete(self) -> bool:
        """Check if section meets minimum requirements."""
        return self.word_count >= self.min_words

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "slug": self.slug,
            "content": self.content,
            "word_count": self.word_count,
            "min_words": self.min_words,
            "target_words": self.target_words,
            "max_words": self.max_words,
            "model": self.model,
            "requirements": self.requirements,
            "metadata": self.metadata
        }


@dataclass
class ValidationResult:
    """Results from entry validation."""
    overall_score: float
    tier: QualityTier
    passed: bool

    # Individual criterion scores
    word_count_score: float
    theological_depth_score: float
    coherence_score: float
    section_balance_score: float
    orthodox_perspective_score: float

    # Quality metrics
    diversity_score: float
    specificity_score: float
    integration_score: float
    distribution_score: float

    # Detailed feedback
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)

    # Statistics
    total_words: int = 0
    patristic_citations: int = 0
    scripture_references: int = 0
    unique_fathers: int = 0
    named_works: int = 0

    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "overall_score": self.overall_score,
            "tier": self.tier.value,
            "passed": self.passed,
            "criteria_scores": {
                "word_count": self.word_count_score,
                "theological_depth": self.theological_depth_score,
                "coherence": self.coherence_score,
                "section_balance": self.section_balance_score,
                "orthodox_perspective": self.orthodox_perspective_score
            },
            "quality_metrics": {
                "diversity": self.diversity_score,
                "specificity": self.specificity_score,
                "integration": self.integration_score,
                "distribution": self.distribution_score
            },
            "feedback": {
                "strengths": self.strengths,
                "weaknesses": self.weaknesses,
                "suggestions": self.suggestions
            },
            "statistics": {
                "total_words": self.total_words,
                "patristic_citations": self.patristic_citations,
                "scripture_references": self.scripture_references,
                "unique_fathers": self.unique_fathers,
                "named_works": self.named_works
            },
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class Entry:
    """Represents a complete theological entry."""
    topic: str
    sections: List[Section] = field(default_factory=list)

    # Metadata
    entry_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    generation_time_seconds: float = 0
    refinement_iterations: int = 0

    # Validation
    validation_result: Optional[ValidationResult] = None

    # Configuration
    target_tier: QualityTier = QualityTier.CELESTIAL
    target_score: int = 95

    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def total_words(self) -> int:
        """Calculate total word count across all sections."""
        return sum(section.word_count for section in self.sections)

    @property
    def is_complete(self) -> bool:
        """Check if all sections are complete."""
        return all(section.is_complete() for section in self.sections)

    @property
    def is_celestial(self) -> bool:
        """Check if entry achieved CELESTIAL tier."""
        if not self.validation_result:
            return False
        return self.validation_result.tier == QualityTier.CELESTIAL

    def get_section(self, slug: str) -> Optional[Section]:
        """Get section by slug."""
        for section in self.sections:
            if section.slug == slug:
                return section
        return None

    def to_markdown(self) -> str:
        """Convert entry to markdown format."""
        lines = []

        # Header
        lines.append(f"# {self.topic}\n")

        # Metadata
        if self.validation_result:
            lines.append(f"**Quality Tier**: {self.validation_result.tier.value} ({self.validation_result.overall_score:.1f}/100)\n")
        lines.append(f"**Total Words**: {self.total_words:,}\n")
        lines.append(f"**Generated**: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n")
        if self.refinement_iterations > 0:
            lines.append(f"**Refinement Iterations**: {self.refinement_iterations}\n")
        lines.append("\n---\n")

        # Sections
        for section in self.sections:
            lines.append(f"\n## {section.name}\n")
            lines.append(f"\n{section.content}\n")

        # Footer
        lines.append("\n---\n")
        lines.append(f"\n*Generated by Celestial Engine v2.0*\n")

        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "topic": self.topic,
            "entry_id": self.entry_id,
            "sections": [s.to_dict() for s in self.sections],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "generation_time_seconds": self.generation_time_seconds,
            "refinement_iterations": self.refinement_iterations,
            "total_words": self.total_words,
            "validation_result": self.validation_result.to_dict() if self.validation_result else None,
            "target_tier": self.target_tier.value,
            "target_score": self.target_score,
            "metadata": self.metadata
        }

    def save(self, output_dir: Path):
        """Save entry to file."""
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save markdown
        md_path = output_dir / f"{self.entry_id}.md"
        md_path.write_text(self.to_markdown())

        # Save JSON metadata
        json_path = output_dir / f"{self.entry_id}.json"
        json_path.write_text(json.dumps(self.to_dict(), indent=2))

        return md_path, json_path


@dataclass
class PreprocessingResult:
    """Results from topic preprocessing."""
    topic: str
    keywords: List[str] = field(default_factory=list)
    complexity_score: float = 0.0
    estimated_word_count: int = 12500
    suggested_structure: Dict[str, Any] = field(default_factory=dict)

    # Resource suggestions
    suggested_fathers: List[str] = field(default_factory=list)
    suggested_works: List[str] = field(default_factory=list)
    suggested_scriptures: List[str] = field(default_factory=list)
    suggested_terms: List[str] = field(default_factory=list)

    # Analysis
    theological_themes: List[str] = field(default_factory=list)
    potential_tensions: List[str] = field(default_factory=list)
    western_contrasts: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "topic": self.topic,
            "keywords": self.keywords,
            "complexity_score": self.complexity_score,
            "estimated_word_count": self.estimated_word_count,
            "suggested_structure": self.suggested_structure,
            "resources": {
                "fathers": self.suggested_fathers,
                "works": self.suggested_works,
                "scriptures": self.suggested_scriptures,
                "terms": self.suggested_terms
            },
            "analysis": {
                "themes": self.theological_themes,
                "tensions": self.potential_tensions,
                "western_contrasts": self.western_contrasts
            }
        }


@dataclass
class RefinementTask:
    """Represents a refinement task for an entry."""
    strategy_name: str
    priority: int
    target_section: Optional[str] = None
    description: str = ""
    actions: List[str] = field(default_factory=list)
    estimated_time: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "strategy_name": self.strategy_name,
            "priority": self.priority,
            "target_section": self.target_section,
            "description": self.description,
            "actions": self.actions,
            "estimated_time": self.estimated_time
        }


@dataclass
class GenerationProgress:
    """Tracks generation progress for monitoring."""
    entry_id: str
    topic: str
    status: str  # "preprocessing", "generating", "validating", "refining", "complete", "failed"
    current_section: Optional[str] = None
    progress_percentage: float = 0.0

    start_time: datetime = field(default_factory=datetime.now)
    estimated_completion: Optional[datetime] = None

    sections_complete: int = 0
    total_sections: int = 6

    current_score: float = 0.0
    target_score: float = 95.0

    refinement_iteration: int = 0
    max_refinements: int = 5

    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "entry_id": self.entry_id,
            "topic": self.topic,
            "status": self.status,
            "current_section": self.current_section,
            "progress_percentage": self.progress_percentage,
            "start_time": self.start_time.isoformat(),
            "estimated_completion": self.estimated_completion.isoformat() if self.estimated_completion else None,
            "sections_complete": self.sections_complete,
            "total_sections": self.total_sections,
            "current_score": self.current_score,
            "target_score": self.target_score,
            "refinement_iteration": self.refinement_iteration,
            "max_refinements": self.max_refinements,
            "errors": self.errors,
            "warnings": self.warnings
        }
