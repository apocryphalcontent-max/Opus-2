"""
Quality Scorer - Advanced quality metrics and automated checks

Implements the 4-metric quality system:
- Diversity Score (Patristic citation breadth)
- Specificity Score (Named works)
- Integration Score (Natural flow)
- Distribution Score (Content across sections)
"""

from typing import Dict, List
from dataclasses import dataclass
import re


@dataclass
class QualityMetrics:
    """Quality metrics results"""
    diversity_score: float  # 0-100
    specificity_score: float  # 0-100
    integration_score: float  # 0-100
    distribution_score: float  # 0-100
    composite_score: float  # 0-100
    passed: bool
    details: Dict[str, any]
    

class QualityScorer:
    """
    Implements automated quality checks from PRODUCTION_Guide
    Accepts 90-95% citation authenticity as sufficient
    """
    
    # Thresholds
    DIVERSITY_THRESHOLD = 80.0  # 4+ different fathers
    SPECIFICITY_THRESHOLD = 70.0  # 2+ named works
    INTEGRATION_THRESHOLD = 70.0  # Acceptable distribution
    DISTRIBUTION_THRESHOLD = 85.0  # 4+ sections with Patristic content
    
    # Church Father patterns
    FATHER_PATTERNS = [
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
        r'St\.\s+Gregory\s+Nazianzen',
    ]
    
    # Work title patterns
    WORK_PATTERNS = [
        r'On\s+the\s+Making\s+of\s+Man|De\s+Hominis\s+Opificio',
        r'Ambigua|Difficulties',
        r'On\s+the\s+Holy\s+Spirit|De\s+Spiritu\s+Sancto',
        r'Homilies\s+on|Commentary\s+on',
        r'Against\s+the\s+Heathen|Contra\s+Gentes',
        r'Triads\s+in\s+Defense|Triads',
        r'Exact\s+Exposition\s+of\s+the\s+Orthodox\s+Faith',
        r'Ladder\s+of\s+Divine\s+Ascent',
        r'Life\s+of\s+Moses|De\s+Vita\s+Moysis',
        r'On\s+the\s+Incarnation|De\s+Incarnatione',
        r'Hexaemeron',
        r'Mystagogy',
        r'Chapters\s+on\s+Charity',
    ]
    
    def __init__(self):
        """Initialize quality scorer"""
        pass
    
    def calculate_quality_metrics(self, sections: List) -> QualityMetrics:
        """
        Calculate all quality metrics
        
        Args:
            sections: List of Section objects
            
        Returns:
            QualityMetrics with all scores
        """
        # Combine all content
        total_content = " ".join(s.content for s in sections)
        
        # Calculate individual scores
        diversity = self._calculate_diversity_score(total_content)
        specificity = self._calculate_specificity_score(total_content)
        integration = self._calculate_integration_score(sections)
        distribution = self._calculate_distribution_score(sections)
        
        # Calculate composite score (weighted)
        composite = (
            diversity * 0.30 +
            specificity * 0.25 +
            integration * 0.20 +
            distribution * 0.25
        )
        
        # Check if passed all thresholds
        passed = (
            diversity >= self.DIVERSITY_THRESHOLD and
            specificity >= self.SPECIFICITY_THRESHOLD and
            integration >= self.INTEGRATION_THRESHOLD and
            distribution >= self.DISTRIBUTION_THRESHOLD
        )
        
        # Collect details
        details = {
            'fathers_cited': self._count_fathers_cited(total_content),
            'works_cited': self._count_works_cited(total_content),
            'sections_with_patristic': self._count_sections_with_patristic(sections),
            'citation_distribution_variance': self._calculate_citation_variance(sections),
        }
        
        return QualityMetrics(
            diversity_score=diversity,
            specificity_score=specificity,
            integration_score=integration,
            distribution_score=distribution,
            composite_score=composite,
            passed=passed,
            details=details
        )
    
    def _calculate_diversity_score(self, content: str) -> float:
        """
        Calculate diversity score (citation breadth)
        Checks that 5+ different Church Fathers are cited
        """
        fathers_cited = set()
        
        for pattern in self.FATHER_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                fathers_cited.add(pattern)
        
        diversity_count = len(fathers_cited)
        
        if diversity_count >= 5:
            return 100.0
        elif diversity_count == 4:
            return 80.0
        elif diversity_count == 3:
            return 60.0
        else:
            return 40.0
    
    def _calculate_specificity_score(self, content: str) -> float:
        """
        Calculate specificity score (named works)
        Ensures 3+ specific Patristic works are named
        """
        works_cited = 0
        
        for pattern in self.WORK_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                works_cited += 1
        
        if works_cited >= 3:
            return 100.0
        elif works_cited == 2:
            return 70.0
        elif works_cited == 1:
            return 40.0
        else:
            return 20.0
    
    def _calculate_integration_score(self, sections: List) -> float:
        """
        Calculate integration score (natural flow)
        Verifies citations flow naturally, not isolated
        """
        section_citation_counts = []
        
        for section in sections:
            citation_count = sum(
                len(re.findall(pattern, section.content, re.IGNORECASE))
                for pattern in self.FATHER_PATTERNS
            )
            section_citation_counts.append(citation_count)
        
        if not section_citation_counts:
            return 50.0
        
        # Calculate variance
        mean_citations = sum(section_citation_counts) / len(section_citation_counts)
        if mean_citations == 0:
            return 50.0
        
        variance = sum(
            (x - mean_citations) ** 2
            for x in section_citation_counts
        ) / len(section_citation_counts)
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
    
    def _calculate_distribution_score(self, sections: List) -> float:
        """
        Calculate distribution score
        Confirms Patristic content appears across multiple sections
        """
        patristic_sections = 0
        
        for section in sections:
            # Check for Father citations
            has_father_citation = any(
                re.search(pattern, section.content, re.IGNORECASE)
                for pattern in self.FATHER_PATTERNS
            )
            
            # Check for Patristic terms
            has_patristic_terms = bool(
                re.search(
                    r'Patristic|Fathers|Church\s+Father',
                    section.content,
                    re.IGNORECASE
                )
            )
            
            if has_father_citation or has_patristic_terms:
                patristic_sections += 1
        
        # Expect Patristic content in at least 4 of 6 sections
        if patristic_sections >= 5:
            return 100.0
        elif patristic_sections == 4:
            return 85.0
        elif patristic_sections == 3:
            return 65.0
        else:
            return 40.0
    
    def _count_fathers_cited(self, content: str) -> int:
        """Count number of different fathers cited"""
        return sum(
            1 for pattern in self.FATHER_PATTERNS
            if re.search(pattern, content, re.IGNORECASE)
        )
    
    def _count_works_cited(self, content: str) -> int:
        """Count number of specific works cited"""
        return sum(
            1 for pattern in self.WORK_PATTERNS
            if re.search(pattern, content, re.IGNORECASE)
        )
    
    def _count_sections_with_patristic(self, sections: List) -> int:
        """Count sections with Patristic content"""
        count = 0
        for section in sections:
            has_content = any(
                re.search(pattern, section.content, re.IGNORECASE)
                for pattern in self.FATHER_PATTERNS
            ) or bool(re.search(r'Patristic|Fathers', section.content, re.IGNORECASE))
            
            if has_content:
                count += 1
        
        return count
    
    def _calculate_citation_variance(self, sections: List) -> float:
        """Calculate variance in citation distribution"""
        counts = []
        for section in sections:
            count = sum(
                len(re.findall(pattern, section.content, re.IGNORECASE))
                for pattern in self.FATHER_PATTERNS
            )
            counts.append(count)
        
        if not counts:
            return 0.0
        
        mean = sum(counts) / len(counts)
        if mean == 0:
            return 0.0
        
        variance = sum((x - mean) ** 2 for x in counts) / len(counts)
        return variance ** 0.5
