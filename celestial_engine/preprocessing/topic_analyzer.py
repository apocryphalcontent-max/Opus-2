"""
Topic analysis and preprocessing for the Celestial Engine.
Analyzes topics before generation to optimize structure and resources.
"""

import re
import logging
from typing import List, Dict, Any
from dataclasses import dataclass

from ..core.models import PreprocessingResult
from ..core.llm_interface import get_llm, ModelType
from ..core.config import get_config

logger = logging.getLogger(__name__)


class TopicAnalyzer:
    """Analyzes topics to extract insights and suggestions."""

    def __init__(self):
        """Initialize topic analyzer."""
        self.llm = get_llm()
        self.config = get_config()

    def analyze(self, topic: str) -> PreprocessingResult:
        """
        Analyze a topic comprehensively.

        Args:
            topic: The entry topic to analyze

        Returns:
            Preprocessing result with analysis and suggestions
        """
        logger.info(f"Analyzing topic: {topic}")

        result = PreprocessingResult(topic=topic)

        # Extract keywords
        result.keywords = self._extract_keywords(topic)

        # Assess complexity
        result.complexity_score = self._assess_complexity(topic)

        # Estimate word count based on complexity
        result.estimated_word_count = self._estimate_word_count(result.complexity_score)

        # Identify theological themes
        result.theological_themes = self._identify_themes(topic)

        # Suggest resources
        result.suggested_fathers = self._suggest_fathers(topic, result.theological_themes)
        result.suggested_works = self._suggest_works(topic, result.suggested_fathers)
        result.suggested_scriptures = self._suggest_scriptures(topic, result.theological_themes)
        result.suggested_terms = self._suggest_terms(topic)

        # Identify potential tensions
        result.potential_tensions = self._identify_tensions(topic)

        # Suggest Western contrasts
        result.western_contrasts = self._suggest_western_contrasts(topic)

        # Generate suggested structure
        result.suggested_structure = self._generate_structure(topic, result)

        logger.info(f"Topic analysis complete: complexity={result.complexity_score:.2f}, "
                   f"themes={len(result.theological_themes)}, fathers={len(result.suggested_fathers)}")

        return result

    def _extract_keywords(self, topic: str) -> List[str]:
        """Extract key theological terms from topic."""
        prompt = f"""Analyze this Orthodox theological topic and extract 5-10 key theological terms or concepts:

Topic: {topic}

List only the key terms, one per line, without explanations."""

        response = self.llm.generate_with_model_type(
            prompt=prompt,
            model_type=ModelType.PREPROCESSOR
        )

        if not response.success:
            logger.warning("Failed to extract keywords via LLM, using fallback")
            return self._fallback_keywords(topic)

        # Parse keywords from response
        keywords = [
            line.strip().strip('-').strip('•').strip()
            for line in response.text.strip().split('\n')
            if line.strip() and not line.strip().startswith('#')
        ]

        return keywords[:10]

    def _fallback_keywords(self, topic: str) -> List[str]:
        """Fallback keyword extraction using simple regex."""
        # Remove common words and extract capitalized terms
        words = topic.split()
        keywords = [w for w in words if w[0].isupper() and len(w) > 3]
        return keywords[:5]

    def _assess_complexity(self, topic: str) -> float:
        """
        Assess topic complexity on a 0-1 scale.

        Factors:
        - Length of topic
        - Number of concepts
        - Presence of specialized terms
        - Philosophical vs practical
        """
        score = 0.5  # Base score

        # Length factor
        words = topic.split()
        if len(words) > 10:
            score += 0.1
        elif len(words) < 5:
            score -= 0.1

        # Complexity indicators
        complex_terms = [
            'divine', 'essence', 'infinity', 'transcendent', 'immanent',
            'hypostasis', 'essence', 'energies', 'apophatic', 'cataphatic',
            'theosis', 'perichoresis', 'synthesis', 'dialectic', 'paradox'
        ]

        topic_lower = topic.lower()
        complex_count = sum(1 for term in complex_terms if term in topic_lower)
        score += min(complex_count * 0.05, 0.3)

        # Multiple concepts indicator
        connectors = ['and', 'or', 'versus', 'in', 'through', 'between']
        connector_count = sum(1 for conn in connectors if conn in topic_lower)
        score += min(connector_count * 0.05, 0.2)

        return min(max(score, 0.1), 1.0)

    def _estimate_word_count(self, complexity_score: float) -> int:
        """Estimate required word count based on complexity."""
        base_count = 12500

        if complexity_score > 0.8:
            return 16000
        elif complexity_score > 0.6:
            return 14000
        elif complexity_score < 0.3:
            return 11500
        else:
            return base_count

    def _identify_themes(self, topic: str) -> List[str]:
        """Identify major theological themes in the topic."""
        prompt = f"""Identify 3-5 major Orthodox theological themes that would be central to exploring this topic:

Topic: {topic}

List only the themes, one per line."""

        response = self.llm.generate_with_model_type(
            prompt=prompt,
            model_type=ModelType.PREPROCESSOR
        )

        if not response.success:
            return []

        themes = [
            line.strip().strip('-').strip('•').strip()
            for line in response.text.strip().split('\n')
            if line.strip() and not line.strip().startswith('#')
        ]

        return themes[:5]

    def _suggest_fathers(self, topic: str, themes: List[str]) -> List[str]:
        """Suggest Church Fathers most relevant to this topic."""
        prompt = f"""Which Church Fathers would be most relevant for exploring this Orthodox theological topic?

Topic: {topic}
Themes: {', '.join(themes)}

List 5-8 Church Fathers who wrote extensively on these themes. Use this format:
St. [Full Name]

One per line."""

        response = self.llm.generate_with_model_type(
            prompt=prompt,
            model_type=ModelType.PREPROCESSOR
        )

        if not response.success:
            return self._default_fathers()

        fathers = [
            line.strip()
            for line in response.text.strip().split('\n')
            if line.strip() and 'St.' in line
        ]

        return fathers[:8]

    def _default_fathers(self) -> List[str]:
        """Default set of Church Fathers for fallback."""
        return [
            "St. Maximus the Confessor",
            "St. Gregory of Nyssa",
            "St. Basil the Great",
            "St. John Chrysostom",
            "St. Athanasius"
        ]

    def _suggest_works(self, topic: str, fathers: List[str]) -> List[str]:
        """Suggest specific Patristic works for citation."""
        fathers_str = ', '.join(fathers[:5])

        prompt = f"""For this Orthodox theological topic and these Church Fathers, suggest 3-5 specific works that would be most relevant to cite:

Topic: {topic}
Church Fathers: {fathers_str}

Format: Author - Work Title
One per line."""

        response = self.llm.generate_with_model_type(
            prompt=prompt,
            model_type=ModelType.PREPROCESSOR
        )

        if not response.success:
            return []

        works = [
            line.strip().strip('-').strip('•').strip()
            for line in response.text.strip().split('\n')
            if line.strip() and ('-' in line or 'St.' in line)
        ]

        return works[:5]

    def _suggest_scriptures(self, topic: str, themes: List[str]) -> List[str]:
        """Suggest relevant Scripture passages."""
        prompt = f"""Suggest 5-8 key Scripture passages (books/chapters) most relevant to this Orthodox theological topic:

Topic: {topic}
Themes: {', '.join(themes)}

Use format: Book Chapter:Verse (e.g., John 1:1-14, Romans 8)
One per line."""

        response = self.llm.generate_with_model_type(
            prompt=prompt,
            model_type=ModelType.PREPROCESSOR
        )

        if not response.success:
            return []

        scriptures = [
            line.strip().strip('-').strip('•').strip()
            for line in response.text.strip().split('\n')
            if line.strip() and any(book in line for book in ['John', 'Matthew', 'Romans', 'Genesis', 'Psalm'])
        ]

        return scriptures[:8]

    def _suggest_terms(self, topic: str) -> List[str]:
        """Suggest important Orthodox theological terms."""
        prompt = f"""List 8-12 important Orthodox theological terms that should be used when writing about this topic:

Topic: {topic}

List technical terms like 'theosis', 'energies', 'hypostasis', etc.
One per line."""

        response = self.llm.generate_with_model_type(
            prompt=prompt,
            model_type=ModelType.PREPROCESSOR
        )

        if not response.success:
            return []

        terms = [
            line.strip().strip('-').strip('•').strip()
            for line in response.text.strip().split('\n')
            if line.strip() and len(line.strip()) < 50
        ]

        return terms[:12]

    def _identify_tensions(self, topic: str) -> List[str]:
        """Identify potential theological tensions or paradoxes."""
        prompt = f"""Identify 2-4 theological tensions, paradoxes, or apparent contradictions that this topic involves:

Topic: {topic}

These should be genuine tensions that Orthodox theology addresses and synthesizes.
One per line."""

        response = self.llm.generate_with_model_type(
            prompt=prompt,
            model_type=ModelType.PREPROCESSOR
        )

        if not response.success:
            return []

        tensions = [
            line.strip().strip('-').strip('•').strip()
            for line in response.text.strip().split('\n')
            if line.strip() and len(line.strip()) > 10
        ]

        return tensions[:4]

    def _suggest_western_contrasts(self, topic: str) -> List[str]:
        """Suggest contrasts with Western theology."""
        prompt = f"""Identify 3-4 key ways that Orthodox theology differs from Western (Catholic/Protestant) theology on this topic:

Topic: {topic}

Be specific about doctrinal or theological differences.
One per line."""

        response = self.llm.generate_with_model_type(
            prompt=prompt,
            model_type=ModelType.PREPROCESSOR
        )

        if not response.success:
            return []

        contrasts = [
            line.strip().strip('-').strip('•').strip()
            for line in response.text.strip().split('\n')
            if line.strip() and len(line.strip()) > 15
        ]

        return contrasts[:4]

    def _generate_structure(self, topic: str, result: PreprocessingResult) -> Dict[str, Any]:
        """Generate suggested structure for the entry."""
        section_configs = self.config.get_section_configs()

        structure = {
            "sections": []
        }

        for section_config in section_configs:
            section_info = {
                "name": section_config.name,
                "slug": section_config.slug,
                "target_words": section_config.target_words,
                "focus": self._get_section_focus(section_config.slug, topic, result)
            }
            structure["sections"].append(section_info)

        return structure

    def _get_section_focus(self, section_slug: str, topic: str, result: PreprocessingResult) -> str:
        """Get suggested focus for a specific section."""
        if section_slug == "introduction":
            return f"Introduce {topic} and establish its theological significance"

        elif section_slug == "patristic_mind":
            fathers_str = ', '.join(result.suggested_fathers[:3])
            return f"Deep exploration drawing from {fathers_str} and others"

        elif section_slug == "symphony_of_clashes":
            if result.potential_tensions:
                tension = result.potential_tensions[0]
                return f"Address tension: {tension}"
            return "Explore theological tensions and their Orthodox synthesis"

        elif section_slug == "orthodox_affirmation":
            if result.western_contrasts:
                contrast = result.western_contrasts[0]
                return f"Affirm Orthodox distinctiveness: {contrast}"
            return "Distinguish Orthodox perspective from Western approaches"

        elif section_slug == "synthesis":
            return f"Synthesize Patristic insights into coherent theological vision"

        elif section_slug == "conclusion":
            return f"Conclude with practical application and doxological reflection"

        return ""
