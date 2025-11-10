"""
Citation Validator - Validates authenticity of Patristic citations

Checks citations against verified database to prevent hallucination
"""

from typing import List, Tuple
import re


class CitationValidator:
    """Validates Patristic citations against verified database"""
    
    def __init__(self, citation_database):
        """
        Initialize with citation database
        
        Args:
            citation_database: CitationPreparer instance with verified works
        """
        self.database = citation_database
        
    def validate_citations(self, content: str) -> Tuple[int, int, List[str]]:
        """
        Validate all citations in content
        
        Args:
            content: Text content to validate
            
        Returns:
            Tuple of (verified_count, total_count, flagged_citations)
        """
        # Extract all citations
        citations = self._extract_citations(content)
        
        verified = 0
        flagged = []
        
        for father, work in citations:
            if self.database.verify_citation(father, work):
                verified += 1
            else:
                flagged.append(f"{father}: {work}")
        
        total = len(citations)
        return verified, total, flagged
    
    def _extract_citations(self, content: str) -> List[Tuple[str, str]]:
        """Extract (father, work) pairs from content"""
        citations = []
        
        # Pattern: St. [Name] in [Work]
        pattern = r'St\.\s+([\w\s]+?)\s+in\s+([^,\.]+)'
        matches = re.finditer(pattern, content)
        
        for match in matches:
            father = f"St. {match.group(1).strip()}"
            work = match.group(2).strip()
            citations.append((father, work))
        
        return citations
