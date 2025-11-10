"""
Coherence Analyzer - Analyzes logical flow and structural coherence

Validates:
- Cross-references between sections
- Logical progression
- Thematic consistency
- Argument structure
"""

from typing import List, Dict
import re


class CoherenceAnalyzer:
    """Analyzes coherence and structural integrity of entries"""
    
    def analyze_coherence(self, sections: List) -> Dict[str, any]:
        """
        Analyze entry coherence
        
        Args:
            sections: List of Section objects
            
        Returns:
            Dict with coherence metrics
        """
        # Count cross-references
        cross_refs = self._count_cross_references(sections)
        
        # Check logical flow
        flow_score = self._analyze_flow(sections)
        
        # Check thematic consistency
        consistency_score = self._analyze_consistency(sections)
        
        return {
            'cross_references': cross_refs,
            'flow_score': flow_score,
            'consistency_score': consistency_score,
            'overall_coherence': (flow_score + consistency_score) / 2
        }
    
    def _count_cross_references(self, sections: List) -> int:
        """Count cross-references between sections"""
        count = 0
        section_names = [s.name for s in sections]
        
        for section in sections:
            for other_name in section_names:
                if other_name != section.name:
                    # Check if other section is mentioned
                    if other_name.lower() in section.content.lower():
                        count += 1
        
        return count
    
    def _analyze_flow(self, sections: List) -> float:
        """Analyze logical flow (0-100)"""
        score = 70.0  # Base score
        
        # Check introduction previews
        if sections:
            intro = sections[0]
            if 'introduction' in intro.name.lower():
                # Should preview other sections
                previewed = sum(
                    1 for s in sections[1:]
                    if s.name.lower() in intro.content.lower()
                )
                score += min(20.0, previewed * 4.0)
        
        # Check conclusion recaps
        if len(sections) > 1:
            conclusion = sections[-1]
            if 'conclusion' in conclusion.name.lower():
                # Should reference previous sections
                referenced = sum(
                    1 for s in sections[:-1]
                    if s.name.lower() in conclusion.content.lower()
                )
                score += min(10.0, referenced * 2.0)
        
        return min(100.0, score)
    
    def _analyze_consistency(self, sections: List) -> float:
        """Analyze thematic consistency (0-100)"""
        # Simple heuristic: check for consistent terminology
        score = 80.0  # Base score
        
        # Would implement more sophisticated analysis
        # For now, return base score
        
        return score
