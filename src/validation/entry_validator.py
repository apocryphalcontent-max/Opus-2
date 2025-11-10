"""
Entry Validator - Comprehensive validation of theological entries

Validates entries against all quality criteria:
- Word count requirements
- Theological depth
- Coherence and structure
- Section balance
- Orthodox perspective
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import re


class QualityTier(Enum):
    """Quality tier classification"""
    CELESTIAL = "CELESTIAL"  # 95-100
    ADAMANTINE = "ADAMANTINE"  # 90-94
    PLATINUM = "PLATINUM"  # 85-89
    GOLD = "GOLD"  # 80-84
    SILVER = "SILVER"  # 75-79
    BRONZE = "BRONZE"  # 70-74
    INSUFFICIENT = "INSUFFICIENT"  # <70
    

@dataclass
class SectionValidation:
    """Validation results for a single section"""
    name: str
    word_count: int
    min_required: int
    max_recommended: int
    target: int
    meets_minimum: bool
    score: float
    issues: List[str]
    

@dataclass
class ValidationResult:
    """Complete validation results"""
    overall_score: float
    quality_tier: QualityTier
    word_count_score: float
    theological_depth_score: float
    coherence_score: float
    section_balance_score: float
    orthodox_perspective_score: float
    section_validations: List[SectionValidation]
    issues: List[str]
    recommendations: List[str]
    passes_celestial: bool
    

@dataclass
class Entry:
    """Entry data structure"""
    topic: str
    sections: List['Section']
    total_word_count: int
    

@dataclass
class Section:
    """Section data structure"""
    name: str
    content: str
    word_count: int
    

class EntryValidator:
    """
    Comprehensive validator for Orthodox theological entries
    Implements all quality criteria from PRODUCTION_Guide
    """
    
    # Section requirements
    SECTION_REQUIREMENTS = {
        'Introduction': {'min': 1750, 'target': 1750, 'max': 2500},
        'The Patristic Mind': {'min': 2250, 'target': 2250, 'max': 3000},
        'Symphony of Clashes': {'min': 2350, 'target': 2350, 'max': 3200},
        'Orthodox Affirmation': {'min': 2250, 'target': 2250, 'max': 3000},
        'Synthesis': {'min': 1900, 'target': 1900, 'max': 2500},
        'Conclusion': {'min': 1800, 'target': 1800, 'max': 2400},
    }
    
    # Validation weights
    WEIGHTS = {
        'word_count': 0.20,
        'theological_depth': 0.30,
        'coherence': 0.25,
        'section_balance': 0.15,
        'orthodox_perspective': 0.10,
    }
    
    # Minimum requirements
    MIN_TOTAL_WORDS = 11000
    TARGET_TOTAL_WORDS = 12500
    MIN_PATRISTIC_CITATIONS = 20
    MIN_SCRIPTURE_REFERENCES = 15
    MIN_DIFFERENT_FATHERS = 5
    
    def __init__(self):
        """Initialize validator"""
        self.required_sections = list(self.SECTION_REQUIREMENTS.keys())
        
    def validate(self, entry: Entry) -> ValidationResult:
        """
        Perform comprehensive validation
        
        Args:
            entry: Entry to validate
            
        Returns:
            Complete ValidationResult
        """
        issues = []
        recommendations = []
        
        # Validate sections
        section_validations = self._validate_sections(entry.sections)
        
        # Calculate scores
        word_count_score = self._calculate_word_count_score(
            entry.total_word_count, section_validations
        )
        
        theological_depth_score = self._calculate_theological_depth_score(
            entry.sections
        )
        
        coherence_score = self._calculate_coherence_score(
            entry.sections
        )
        
        section_balance_score = self._calculate_section_balance_score(
            section_validations
        )
        
        orthodox_perspective_score = self._calculate_orthodox_perspective_score(
            entry.sections
        )
        
        # Calculate overall score
        overall_score = (
            word_count_score * self.WEIGHTS['word_count'] +
            theological_depth_score * self.WEIGHTS['theological_depth'] +
            coherence_score * self.WEIGHTS['coherence'] +
            section_balance_score * self.WEIGHTS['section_balance'] +
            orthodox_perspective_score * self.WEIGHTS['orthodox_perspective']
        )
        
        # Determine quality tier
        quality_tier = self._determine_quality_tier(overall_score)
        
        # Check if passes CELESTIAL
        passes_celestial = overall_score >= 95.0
        
        # Collect issues and recommendations
        self._collect_issues_and_recommendations(
            entry, section_validations, overall_score,
            issues, recommendations
        )
        
        return ValidationResult(
            overall_score=overall_score,
            quality_tier=quality_tier,
            word_count_score=word_count_score,
            theological_depth_score=theological_depth_score,
            coherence_score=coherence_score,
            section_balance_score=section_balance_score,
            orthodox_perspective_score=orthodox_perspective_score,
            section_validations=section_validations,
            issues=issues,
            recommendations=recommendations,
            passes_celestial=passes_celestial
        )
    
    def _validate_sections(self, sections: List[Section]) -> List[SectionValidation]:
        """Validate all sections"""
        validations = []
        
        for section in sections:
            if section.name in self.SECTION_REQUIREMENTS:
                req = self.SECTION_REQUIREMENTS[section.name]
                
                meets_minimum = section.word_count >= req['min']
                issues = []
                
                if not meets_minimum:
                    deficit = req['min'] - section.word_count
                    issues.append(f"Below minimum by {deficit} words")
                
                if section.word_count > req['max']:
                    excess = section.word_count - req['max']
                    issues.append(f"Exceeds recommended maximum by {excess} words")
                
                # Calculate section score
                score = self._score_section_word_count(
                    section.word_count, req['min'], req['target'], req['max']
                )
                
                validations.append(SectionValidation(
                    name=section.name,
                    word_count=section.word_count,
                    min_required=req['min'],
                    max_recommended=req['max'],
                    target=req['target'],
                    meets_minimum=meets_minimum,
                    score=score,
                    issues=issues
                ))
        
        return validations
    
    def _score_section_word_count(
        self, count: int, min_w: int, target: int, max_w: int
    ) -> float:
        """Score section word count (0-100)"""
        if min_w <= count <= max_w:
            # Within range - score based on proximity to target
            deviation = abs(count - target) / target
            return max(85.0, 100.0 - (deviation * 100))
        elif count < min_w:
            # Below minimum
            ratio = count / min_w
            return ratio * 85.0
        else:
            # Above maximum
            excess_ratio = (count - max_w) / max_w
            return max(50.0, 100.0 - (excess_ratio * 100))
    
    def _calculate_word_count_score(
        self, total: int, section_vals: List[SectionValidation]
    ) -> float:
        """Calculate word count score (0-100)"""
        if total < self.MIN_TOTAL_WORDS:
            # Below minimum
            ratio = total / self.MIN_TOTAL_WORDS
            return ratio * 85.0
        elif total <= 14000:
            # Within acceptable range
            deviation = abs(total - self.TARGET_TOTAL_WORDS) / self.TARGET_TOTAL_WORDS
            return max(85.0, 100.0 - (deviation * 100))
        else:
            # Significantly above target (still acceptable per philosophy)
            # Modest penalty for excessive length
            excess_ratio = (total - 14000) / 14000
            return max(80.0, 100.0 - (excess_ratio * 50))
    
    def _calculate_theological_depth_score(self, sections: List[Section]) -> float:
        """Calculate theological depth score (0-100)"""
        total_content = " ".join(s.content for s in sections)
        
        score = 40.0  # Base score
        
        # Count Patristic references
        patristic_terms = ['Patristic', 'patristic', 'Fathers', 'Father']
        patristic_count = sum(
            len(re.findall(rf'\b{term}\b', total_content))
            for term in patristic_terms
        )
        score += min(20.0, patristic_count * 1.0)
        
        # Count theological terms
        theological_terms = [
            'theosis', 'deification', 'incarnation', 'Incarnate',
            'Trinity', 'Trinitarian', 'divine energies', 'uncreated energies',
            'essence', 'hypostasis', 'sacrament', 'sacramental',
            'liturgy', 'liturgical'
        ]
        theological_count = sum(
            len(re.findall(rf'\b{term}\b', total_content, re.IGNORECASE))
            for term in theological_terms
        )
        score += min(15.0, theological_count * 0.3)
        
        # Count Church Father citations
        father_names = [
            'Gregory of Nyssa', 'Maximus the Confessor', 'Basil the Great',
            'John Chrysostom', 'Athanasius', 'Gregory Palamas',
            'John of Damascus', 'Ignatius', 'Irenaeus'
        ]
        fathers_cited = sum(
            1 for father in father_names
            if father in total_content
        )
        score += min(20.0, fathers_cited * 3.0)
        
        # Bonus for substantial sections
        patristic_section = next(
            (s for s in sections if s.name == 'The Patristic Mind'), None
        )
        if patristic_section and patristic_section.word_count >= 2000:
            score += 10.0
        
        orthodox_section = next(
            (s for s in sections if s.name == 'Orthodox Affirmation'), None
        )
        if orthodox_section and orthodox_section.word_count >= 2000:
            score += 10.0
        
        return min(100.0, score)
    
    def _calculate_coherence_score(self, sections: List[Section]) -> float:
        """Calculate coherence score (0-100)"""
        score = 0.0
        
        # Section presence (0-50 points)
        present = sum(1 for s in sections if s.name in self.required_sections)
        section_score = (present / len(self.required_sections)) * 50.0
        score += section_score
        
        # Content adequacy (0-50 points)
        content_score = 50.0
        for section in sections:
            if section.word_count < 500:
                content_score -= 10.0
            if section.word_count < 300:
                content_score -= 10.0
        score += max(0.0, content_score)
        
        # Cross-reference bonus (0-10 points)
        total_content = " ".join(s.content for s in sections)
        section_names = [s.name for s in sections]
        cross_refs = sum(
            1 for name in section_names
            if name.lower() in total_content.lower()
        )
        score += min(10.0, cross_refs * 2.0)
        
        return min(100.0, score)
    
    def _calculate_section_balance_score(
        self, validations: List[SectionValidation]
    ) -> float:
        """Calculate section balance score (0-100)"""
        if not validations:
            return 70.0
        
        scores = [v.score for v in validations]
        return sum(scores) / len(scores)
    
    def _calculate_orthodox_perspective_score(self, sections: List[Section]) -> float:
        """Calculate Orthodox perspective score (0-100)"""
        total_content = " ".join(s.content for s in sections)
        
        score = 70.0  # Base score
        
        # Primary indicators
        primary_terms = ['Orthodox', 'orthodox', 'Eastern Orthodox']
        primary_count = sum(
            len(re.findall(rf'\b{term}\b', total_content))
            for term in primary_terms
        )
        score += min(15.0, primary_count * 1.0)
        
        # Secondary indicators
        secondary_terms = ['Patristic', 'patristic', 'Fathers', 'tradition', 'Tradition']
        secondary_count = sum(
            len(re.findall(rf'\b{term}\b', total_content))
            for term in secondary_terms
        )
        score += min(10.0, secondary_count * 0.5)
        
        # Tertiary indicators
        tertiary_terms = ['theosis', 'divine energies', 'synergy']
        tertiary_count = sum(
            len(re.findall(rf'\b{term}\b', total_content, re.IGNORECASE))
            for term in tertiary_terms
        )
        score += min(5.0, tertiary_count * 1.0)
        
        return min(100.0, score)
    
    def _determine_quality_tier(self, score: float) -> QualityTier:
        """Determine quality tier from score"""
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
            return QualityTier.INSUFFICIENT
    
    def _collect_issues_and_recommendations(
        self,
        entry: Entry,
        section_vals: List[SectionValidation],
        overall_score: float,
        issues: List[str],
        recommendations: List[str]
    ):
        """Collect issues and recommendations"""
        
        # Check word count
        if entry.total_word_count < self.MIN_TOTAL_WORDS:
            issues.append(f"Total word count ({entry.total_word_count}) below minimum ({self.MIN_TOTAL_WORDS})")
            recommendations.append(f"Expand entry by {self.MIN_TOTAL_WORDS - entry.total_word_count} words")
        
        # Check section issues
        for val in section_vals:
            if val.issues:
                issues.extend([f"{val.name}: {issue}" for issue in val.issues])
                if not val.meets_minimum:
                    recommendations.append(f"Expand {val.name} to meet minimum {val.min_required} words")
        
        # Check for CELESTIAL
        if overall_score < 95:
            issues.append(f"Score {overall_score:.2f} below CELESTIAL threshold (95)")
            recommendations.append("Apply iterative refinement to reach CELESTIAL tier")
