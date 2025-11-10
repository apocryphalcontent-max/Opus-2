"""
Comprehensive validation system for entry quality assessment.
Implements the CELESTIAL-tier validation criteria.
"""

import re
import logging
from typing import Dict, List, Tuple, Any
from collections import Counter

from ..core.models import Entry, ValidationResult, QualityTier
from ..core.config import get_config

logger = logging.getLogger(__name__)


class EntryValidator:
    """Validates entries against CELESTIAL-tier standards."""

    def __init__(self):
        """Initialize validator."""
        self.config = get_config()

        # Load validation weights
        validation_config = self.config.get("validation.criteria", {})
        self.weights = {
            "word_count": validation_config.get("word_count", {}).get("weight", 0.20),
            "theological_depth": validation_config.get("theological_depth", {}).get("weight", 0.30),
            "coherence": validation_config.get("coherence", {}).get("weight", 0.25),
            "section_balance": validation_config.get("section_balance", {}).get("weight", 0.15),
            "orthodox_perspective": validation_config.get("orthodox_perspective", {}).get("weight", 0.10)
        }

        # Church Fathers patterns for detection
        self.father_patterns = [
            r'St\.\s+Gregory\s+of\s+Nyssa',
            r'St\.\s+Maximus\s+the\s+Confessor',
            r'St\.\s+Basil\s+the\s+Great',
            r'St\.\s+John\s+Chrysostom',
            r'St\.\s+Athanasius',
            r'St\.\s+Gregory\s+Palamas',
            r'St\.\s+John\s+of\s+Damascus',
            r'St\.\s+Ignatius',
            r'St\.\s+Irenaeus',
            r'St\.\s+Cyril\s+of\s+Alexandria',
            r'St\.\s+Isaac\s+the\s+Syrian',
            r'St\.\s+Symeon\s+the\s+New\s+Theologian',
            r'St\.\s+Gregory\s+the\s+Theologian',
            r'St\.\s+John\s+Cassian',
            r'St\.\s+Ephrem\s+the\s+Syrian'
        ]

        # Patristic works patterns
        self.work_patterns = [
            r'(On\s+the\s+Making\s+of\s+Man|De\s+Hominis\s+Opificio)',
            r'(Ambigua|Difficulty|Difficulties)',
            r'(On\s+the\s+Holy\s+Spirit|De\s+Spiritu\s+Sancto)',
            r'(Homilies\s+on\s+[A-Z]\w+)',
            r'(Against\s+the\s+Heathen|Contra\s+Gentes)',
            r'(Triads\s+in\s+Defense|Triads)',
            r'(Exact\s+Exposition\s+of\s+the\s+Orthodox\s+Faith)',
            r'(Ladder\s+of\s+Divine\s+Ascent)',
            r'(On\s+the\s+Incarnation)',
            r'(The\s+Life\s+of\s+Moses)',
            r'(Against\s+Eunomius)',
            r'(Mystagogy)',
            r'(Chapters\s+on\s+(Charity|Love|Knowledge))',
            r'(Commentary\s+on\s+[A-Z]\w+)'
        ]

    def validate(self, entry: Entry) -> ValidationResult:
        """
        Comprehensively validate an entry.

        Args:
            entry: Entry to validate

        Returns:
            ValidationResult with scores and feedback
        """
        logger.info(f"Validating entry: {entry.topic}")

        # Calculate individual criterion scores
        word_count_score = self._validate_word_count(entry)
        theological_depth_score = self._validate_theological_depth(entry)
        coherence_score = self._validate_coherence(entry)
        section_balance_score = self._validate_section_balance(entry)
        orthodox_perspective_score = self._validate_orthodox_perspective(entry)

        # Calculate quality metrics
        diversity_score = self._calculate_diversity_score(entry)
        specificity_score = self._calculate_specificity_score(entry)
        integration_score = self._calculate_integration_score(entry)
        distribution_score = self._calculate_distribution_score(entry)

        # Calculate overall score
        overall_score = (
            word_count_score * self.weights["word_count"] +
            theological_depth_score * self.weights["theological_depth"] +
            coherence_score * self.weights["coherence"] +
            section_balance_score * self.weights["section_balance"] +
            orthodox_perspective_score * self.weights["orthodox_perspective"]
        )

        # Determine tier
        tier = self._determine_tier(overall_score)

        # Check if passed
        passed = (
            tier == QualityTier.CELESTIAL and
            diversity_score >= 80 and
            specificity_score >= 70 and
            integration_score >= 70 and
            distribution_score >= 85
        )

        # Collect statistics
        stats = self._collect_statistics(entry)

        # Generate feedback
        strengths, weaknesses, suggestions = self._generate_feedback(
            entry,
            word_count_score,
            theological_depth_score,
            coherence_score,
            section_balance_score,
            orthodox_perspective_score,
            diversity_score,
            specificity_score,
            integration_score,
            distribution_score,
            stats
        )

        result = ValidationResult(
            overall_score=overall_score,
            tier=tier,
            passed=passed,
            word_count_score=word_count_score,
            theological_depth_score=theological_depth_score,
            coherence_score=coherence_score,
            section_balance_score=section_balance_score,
            orthodox_perspective_score=orthodox_perspective_score,
            diversity_score=diversity_score,
            specificity_score=specificity_score,
            integration_score=integration_score,
            distribution_score=distribution_score,
            strengths=strengths,
            weaknesses=weaknesses,
            suggestions=suggestions,
            total_words=stats["total_words"],
            patristic_citations=stats["patristic_citations"],
            scripture_references=stats["scripture_references"],
            unique_fathers=stats["unique_fathers"],
            named_works=stats["named_works"]
        )

        logger.info(f"Validation complete: {tier.value} ({overall_score:.1f}/100)")

        return result

    def _validate_word_count(self, entry: Entry) -> float:
        """Validate word count requirements."""
        total_words = entry.total_words
        min_words = self.config.get("entry.word_counts.total_min", 11000)

        score = 100.0

        # Check total word count
        if total_words < min_words:
            deficit = min_words - total_words
            penalty = min((deficit / min_words) * 100, 50)
            score -= penalty

        # Check individual sections
        for section in entry.sections:
            if section.word_count < section.min_words:
                section_deficit = section.min_words - section.word_count
                penalty = min((section_deficit / section.min_words) * 20, 15)
                score -= penalty

            if section.word_count < 500:
                score -= 50

        return max(score, 0.0)

    def _validate_theological_depth(self, entry: Entry) -> float:
        """Validate theological depth."""
        stats = self._collect_statistics(entry)

        score = 100.0

        # Patristic citations requirement (20+)
        if stats["patristic_citations"] < 20:
            deficit = 20 - stats["patristic_citations"]
            score -= deficit * 2.5

        # Scripture references requirement (15+)
        if stats["scripture_references"] < 15:
            deficit = 15 - stats["scripture_references"]
            score -= deficit * 2

        # Unique fathers requirement (5+)
        if stats["unique_fathers"] < 5:
            deficit = 5 - stats["unique_fathers"]
            score -= deficit * 5

        # Named works requirement (3+)
        if stats["named_works"] < 3:
            deficit = 3 - stats["named_works"]
            score -= deficit * 5

        # Orthodox terms requirement (15+)
        if stats["orthodox_terms"] < 15:
            deficit = 15 - stats["orthodox_terms"]
            score -= deficit * 1.5

        return max(score, 0.0)

    def _validate_coherence(self, entry: Entry) -> float:
        """Validate logical flow and coherence."""
        score = 100.0

        # Check for cross-references between sections
        cross_refs = self._count_cross_references(entry)
        if cross_refs < 5:
            score -= (5 - cross_refs) * 5

        # Check for transition quality (simplified heuristic)
        transition_score = self._assess_transitions(entry)
        score = (score + transition_score) / 2

        # Check for thematic consistency
        consistency_score = self._assess_thematic_consistency(entry)
        score = (score + consistency_score) / 2

        return max(score, 0.0)

    def _validate_section_balance(self, entry: Entry) -> float:
        """Validate section balance."""
        score = 100.0

        # Calculate variance in section lengths
        word_counts = [s.word_count for s in entry.sections]
        if not word_counts:
            return 0.0

        mean = sum(word_counts) / len(word_counts)
        variance = sum((x - mean) ** 2 for x in word_counts) / len(word_counts)
        std_dev = variance ** 0.5

        # Penalize high variance
        if std_dev > 500:
            penalty = min((std_dev - 500) / 50, 30)
            score -= penalty

        # Check for sections below minimum
        for section in entry.sections:
            if section.word_count < section.min_words:
                ratio = section.word_count / section.min_words
                penalty = (1 - ratio) * 30
                score -= penalty

        return max(score, 0.0)

    def _validate_orthodox_perspective(self, entry: Entry) -> float:
        """Validate Orthodox perspective and framing."""
        full_text = " ".join(s.content for s in entry.sections)

        score = 100.0

        # Check for Orthodox framing (10+ instances)
        orthodox_mentions = len(re.findall(r'\b(Orthodox|Eastern Orthodox)\b', full_text, re.IGNORECASE))
        if orthodox_mentions < 10:
            score -= (10 - orthodox_mentions) * 3

        # Check for Western contrasts (3+)
        western_patterns = [
            r'\b(Western|Catholic|Protestant|Latin)\s+(theology|tradition|understanding)',
            r'(in\s+contrast|differs\s+from|unlike)\s+(Western|Catholic|Protestant)',
            r'(Catholic|Protestant)\s+(view|understanding|doctrine)'
        ]
        western_contrasts = sum(len(re.findall(p, full_text, re.IGNORECASE)) for p in western_patterns)
        if western_contrasts < 3:
            score -= (3 - western_contrasts) * 5

        # Check for liturgical/lived experience references
        lived_patterns = [
            r'\b(liturgy|liturgical|prayer|praxis|sacrament|icon)\b',
            r'\b(monastery|monastic|hesychasm|ascetic)\b',
            r'\b(Divine\s+Liturgy|Eucharist|baptism)\b'
        ]
        lived_refs = sum(len(re.findall(p, full_text, re.IGNORECASE)) for p in lived_patterns)
        if lived_refs < 5:
            score -= (5 - lived_refs) * 4

        return max(score, 0.0)

    def _calculate_diversity_score(self, entry: Entry) -> float:
        """Calculate citation diversity (unique Church Fathers cited)."""
        full_text = " ".join(s.content for s in entry.sections)

        fathers_cited = set()
        for pattern in self.father_patterns:
            if re.search(pattern, full_text, re.IGNORECASE):
                fathers_cited.add(pattern)

        count = len(fathers_cited)

        if count >= 5:
            return 100.0
        elif count == 4:
            return 80.0
        elif count == 3:
            return 60.0
        else:
            return 40.0

    def _calculate_specificity_score(self, entry: Entry) -> float:
        """Calculate specificity (named Patristic works)."""
        full_text = " ".join(s.content for s in entry.sections)

        works_cited = 0
        for pattern in self.work_patterns:
            matches = re.findall(pattern, full_text, re.IGNORECASE)
            works_cited += len(matches)

        if works_cited >= 3:
            return 100.0
        elif works_cited == 2:
            return 70.0
        elif works_cited == 1:
            return 40.0
        else:
            return 20.0

    def _calculate_integration_score(self, entry: Entry) -> float:
        """Calculate citation integration (distribution across sections)."""
        section_citation_counts = []

        for section in entry.sections:
            citation_count = sum(
                len(re.findall(pattern, section.content, re.IGNORECASE))
                for pattern in self.father_patterns
            )
            section_citation_counts.append(citation_count)

        if not section_citation_counts or sum(section_citation_counts) == 0:
            return 0.0

        mean_citations = sum(section_citation_counts) / len(section_citation_counts)
        variance = sum((x - mean_citations) ** 2 for x in section_citation_counts) / len(section_citation_counts)
        std_dev = variance ** 0.5

        # Lower variance = better distribution
        if std_dev < 2:
            return 100.0
        elif std_dev < 4:
            return 85.0
        elif std_dev < 6:
            return 70.0
        else:
            return 50.0

    def _calculate_distribution_score(self, entry: Entry) -> float:
        """Calculate Patristic content distribution across sections."""
        patristic_sections = 0

        for section in entry.sections:
            has_father_citation = any(
                re.search(pattern, section.content, re.IGNORECASE)
                for pattern in self.father_patterns
            )
            has_patristic_terms = bool(
                re.search(r'(Patristic|Fathers|Church\s+Father)', section.content, re.IGNORECASE)
            )

            if has_father_citation or has_patristic_terms:
                patristic_sections += 1

        if patristic_sections >= 5:
            return 100.0
        elif patristic_sections == 4:
            return 85.0
        elif patristic_sections == 3:
            return 65.0
        else:
            return 40.0

    def _collect_statistics(self, entry: Entry) -> Dict[str, int]:
        """Collect entry statistics."""
        full_text = " ".join(s.content for s in entry.sections)

        # Count Patristic citations
        patristic_citations = sum(
            len(re.findall(pattern, full_text, re.IGNORECASE))
            for pattern in self.father_patterns
        )

        # Count unique fathers
        unique_fathers = sum(
            1 for pattern in self.father_patterns
            if re.search(pattern, full_text, re.IGNORECASE)
        )

        # Count named works
        named_works = sum(
            len(re.findall(pattern, full_text, re.IGNORECASE))
            for pattern in self.work_patterns
        )

        # Count Scripture references (simplified)
        scripture_pattern = r'\b(Gen\.|Exod\.|Matt\.|John|Rom\.|Cor\.|Gal\.|Eph\.|Phil\.|Col\.|Heb\.|James|Pet\.|Rev\.)\s+\d+'
        scripture_references = len(re.findall(scripture_pattern, full_text))

        # Count Orthodox theological terms
        orthodox_terms = len(re.findall(
            r'\b(theosis|energies|essence|hypostasis|ousia|physis|perichoresis|'
            r'apophatic|cataphatic|hesychasm|synergy|uncreated|nous|'
            r'deification|transfiguration|icon|liturgy)\b',
            full_text,
            re.IGNORECASE
        ))

        return {
            "total_words": entry.total_words,
            "patristic_citations": patristic_citations,
            "unique_fathers": unique_fathers,
            "named_works": named_works,
            "scripture_references": scripture_references,
            "orthodox_terms": orthodox_terms
        }

    def _count_cross_references(self, entry: Entry) -> int:
        """Count cross-references between sections."""
        # Look for phrases like "as discussed in", "as we saw", "building on", etc.
        cross_ref_patterns = [
            r'as\s+(discussed|mentioned|seen|noted|explored)\s+in',
            r'building\s+on',
            r'returning\s+to',
            r'as\s+we\s+(saw|discussed|noted)',
            r'earlier\s+discussion',
            r'previous\s+section'
        ]

        full_text = " ".join(s.content for s in entry.sections)
        count = sum(
            len(re.findall(pattern, full_text, re.IGNORECASE))
            for pattern in cross_ref_patterns
        )

        return count

    def _assess_transitions(self, entry: Entry) -> float:
        """Assess quality of transitions between sections (simplified)."""
        # This is a simplified heuristic
        # In a full implementation, this would use NLP or LLM analysis
        return 85.0  # Placeholder

    def _assess_thematic_consistency(self, entry: Entry) -> float:
        """Assess thematic consistency across entry (simplified)."""
        # This would ideally use semantic similarity analysis
        # For now, use a placeholder
        return 85.0  # Placeholder

    def _determine_tier(self, score: float) -> QualityTier:
        """Determine quality tier from score."""
        if score >= 95:
            return QualityTier.CELESTIAL
        elif score >= 90:
            return QualityTier.ADAMANTINE
        elif score >= 85:
            return QualityTier.PLATINUM
        elif score >= 80:
            return QualityTier.GOLD
        elif score >= 75:
            return QualityTier.SILVER
        elif score >= 70:
            return QualityTier.BRONZE
        else:
            return QualityTier.UNRANKED

    def _generate_feedback(
        self,
        entry: Entry,
        word_count_score: float,
        theological_depth_score: float,
        coherence_score: float,
        section_balance_score: float,
        orthodox_perspective_score: float,
        diversity_score: float,
        specificity_score: float,
        integration_score: float,
        distribution_score: float,
        stats: Dict[str, int]
    ) -> Tuple[List[str], List[str], List[str]]:
        """Generate detailed feedback."""
        strengths = []
        weaknesses = []
        suggestions = []

        # Word count feedback
        if word_count_score >= 95:
            strengths.append("Excellent word count distribution across sections")
        elif word_count_score < 80:
            weaknesses.append(f"Word count below target: {stats['total_words']} words")
            suggestions.append("Expand underdeveloped sections to meet minimum requirements")

        # Theological depth feedback
        if theological_depth_score >= 95:
            strengths.append("Outstanding theological depth and Patristic engagement")
        else:
            if stats["patristic_citations"] < 20:
                weaknesses.append(f"Insufficient Patristic citations: {stats['patristic_citations']}/20")
                suggestions.append("Add more direct quotations from Church Fathers")

            if stats["unique_fathers"] < 5:
                weaknesses.append(f"Limited diversity of Church Fathers: {stats['unique_fathers']}/5")
                suggestions.append("Include citations from a broader range of Patristic sources")

            if stats["named_works"] < 3:
                weaknesses.append(f"Few specific works cited: {stats['named_works']}/3")
                suggestions.append("Name specific Patristic works (e.g., 'St. Basil, On the Holy Spirit')")

        # Coherence feedback
        if coherence_score >= 85:
            strengths.append("Strong logical flow and internal coherence")
        else:
            weaknesses.append("Coherence could be improved")
            suggestions.append("Add more cross-references and transitions between sections")

        # Section balance feedback
        if section_balance_score >= 85:
            strengths.append("Well-balanced section distribution")
        else:
            weaknesses.append("Section lengths are unbalanced")
            suggestions.append("Redistribute content to achieve better section balance")

        # Orthodox perspective feedback
        if orthodox_perspective_score >= 85:
            strengths.append("Clear Orthodox framing and perspective throughout")
        else:
            weaknesses.append("Orthodox distinctives need strengthening")
            suggestions.append("Add more explicit Orthodox framing and Western contrasts")

        # Quality metrics feedback
        if diversity_score < 80:
            suggestions.append("Cite a more diverse range of Church Fathers (aim for 5+)")

        if specificity_score < 70:
            suggestions.append("Name specific Patristic works for greater scholarly precision")

        if integration_score < 70:
            suggestions.append("Distribute citations more evenly across all sections")

        if distribution_score < 85:
            suggestions.append("Ensure Patristic content appears in all major sections")

        return strengths, weaknesses, suggestions
