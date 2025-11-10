"""
Semantic Mapper - Cross-referential theological mapping

Creates semantic maps of theological concepts showing:
- Interconnections between doctrines
- Historical development paths
- Patristic consensus areas
- Contemporary relevance
"""

from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from enum import Enum


class TheologicalRelationType(Enum):
    """Types of relationships between theological concepts"""
    FOUNDATION = "foundation"  # One concept foundational to another
    DEVELOPMENT = "development"  # Historical development relationship
    CONTRAST = "contrast"  # Dialectical opposition
    SYNTHESIS = "synthesis"  # Synthetic integration
    APPLICATION = "application"  # Practical application
    

@dataclass
class SemanticRelation:
    """Relationship between two theological concepts"""
    concept_from: str
    concept_to: str
    relation_type: TheologicalRelationType
    strength: float  # 0.0-1.0
    patristic_support: List[str]
    
    
@dataclass
class SemanticMap:
    """Complete semantic map of a theological topic"""
    central_concept: str
    related_concepts: List[str]
    relations: List[SemanticRelation]
    doctrinal_layers: Dict[str, List[str]]
    western_contrasts: List[Tuple[str, str]]
    liturgical_connections: List[str]
    

class SemanticMapper:
    """
    Creates comprehensive semantic maps of theological concepts
    showing interconnections and relationships
    """
    
    # Core Orthodox doctrinal relationships
    DOCTRINAL_FOUNDATIONS = {
        'Theosis': ['Trinity', 'Incarnation', 'Divine Energies'],
        'Incarnation': ['Trinity', 'Christology'],
        'Divine Energies': ['Trinity', 'Essence-Energies distinction'],
        'Sacramental life': ['Incarnation', 'Ecclesiology', 'Liturgical theology'],
        'Iconography': ['Incarnation', 'Christology', 'Theology of matter'],
        'Hesychasm': ['Divine Energies', 'Apophatic theology', 'Prayer'],
    }
    
    # Western contrasts
    WESTERN_CONTRASTS = {
        'Theosis': ('Justification (forensic)', 'Orthodox emphasizes transformation, West emphasizes legal status'),
        'Divine Energies': ('Created grace', 'Orthodox affirms uncreated energies, West posits created grace'),
        'Essence-Energies': ('Divine Simplicity (absolute)', 'Orthodox maintains real distinction, West absolute simplicity'),
        'Synergy': ('Sola gratia', 'Orthodox affirms cooperation, West emphasizes grace alone'),
        'Apophatic theology': ('Scholastic systematization', 'Orthodox maintains mystery, West systematizes'),
    }
    
    # Liturgical connections
    LITURGICAL_CONNECTIONS = {
        'Theosis': ['Divine Liturgy', 'Eucharist', 'Baptism', 'Chrismation'],
        'Incarnation': ['Nativity', 'Theophany', 'Transfiguration', 'Eucharist'],
        'Trinity': ['Divine Liturgy', 'Baptismal formula', 'Doxologies'],
        'Resurrection': ['Pascha', 'Divine Liturgy', 'Baptism'],
        'Pneumatology': ['Pentecost', 'Epiclesis', 'Chrismation'],
    }
    
    def __init__(self):
        """Initialize semantic mapper"""
        self.concept_graph = self._build_concept_graph()
        
    def map_topic(self, topic: str, core_themes: List[str]) -> SemanticMap:
        """
        Create comprehensive semantic map for a topic
        
        Args:
            topic: The theological topic
            core_themes: Core themes identified by TopicAnalyzer
            
        Returns:
            SemanticMap with complete relationship network
        """
        # Extract central concept
        central_concept = self._extract_central_concept(topic, core_themes)
        
        # Find related concepts
        related_concepts = self._find_related_concepts(central_concept)
        
        # Map relations
        relations = self._map_relations(central_concept, related_concepts)
        
        # Identify doctrinal layers
        doctrinal_layers = self._identify_doctrinal_layers(central_concept)
        
        # Find Western contrasts
        western_contrasts = self._find_western_contrasts(central_concept, related_concepts)
        
        # Map liturgical connections
        liturgical_connections = self._map_liturgical_connections(central_concept, related_concepts)
        
        return SemanticMap(
            central_concept=central_concept,
            related_concepts=related_concepts,
            relations=relations,
            doctrinal_layers=doctrinal_layers,
            western_contrasts=western_contrasts,
            liturgical_connections=liturgical_connections
        )
    
    def _extract_central_concept(self, topic: str, core_themes: List[str]) -> str:
        """Extract the central theological concept"""
        topic_lower = topic.lower()
        
        # Check for explicit doctrinal terms
        doctrinal_terms = [
            'theosis', 'deification', 'incarnation', 'trinity',
            'divine energies', 'essence', 'salvation', 'church',
            'sacrament', 'liturgy', 'icon', 'resurrection'
        ]
        
        for term in doctrinal_terms:
            if term in topic_lower:
                return term.title()
        
        # Use first core theme if available
        if core_themes:
            return core_themes[0]
        
        return topic
    
    def _find_related_concepts(self, central_concept: str) -> List[str]:
        """Find concepts related to central concept"""
        related = set()
        
        # Foundational relationships
        if central_concept in self.DOCTRINAL_FOUNDATIONS:
            related.update(self.DOCTRINAL_FOUNDATIONS[central_concept])
        
        # Reverse lookup - what concepts depend on this one
        for concept, foundations in self.DOCTRINAL_FOUNDATIONS.items():
            if central_concept in foundations:
                related.add(concept)
        
        # Always include core Orthodox doctrines
        related.update(['Trinity', 'Incarnation'])
        
        return sorted(list(related))
    
    def _map_relations(self, central: str, related: List[str]) -> List[SemanticRelation]:
        """Map relationships between concepts"""
        relations = []
        
        # Foundation relationships
        if central in self.DOCTRINAL_FOUNDATIONS:
            for foundation in self.DOCTRINAL_FOUNDATIONS[central]:
                if foundation in related:
                    relations.append(SemanticRelation(
                        concept_from=foundation,
                        concept_to=central,
                        relation_type=TheologicalRelationType.FOUNDATION,
                        strength=0.9,
                        patristic_support=self._get_patristic_support(foundation, central)
                    ))
        
        # Development relationships
        development_paths = {
            ('Trinity', 'Theosis'): 0.8,
            ('Incarnation', 'Iconography'): 0.9,
            ('Divine Energies', 'Hesychasm'): 0.85,
        }
        
        for (from_c, to_c), strength in development_paths.items():
            if from_c == central and to_c in related:
                relations.append(SemanticRelation(
                    concept_from=from_c,
                    concept_to=to_c,
                    relation_type=TheologicalRelationType.DEVELOPMENT,
                    strength=strength,
                    patristic_support=self._get_patristic_support(from_c, to_c)
                ))
        
        return relations
    
    def _identify_doctrinal_layers(self, central_concept: str) -> Dict[str, List[str]]:
        """Identify concentric layers of doctrinal context"""
        layers = {
            'foundational': ['Trinity', 'Incarnation'],
            'essential': [],
            'developmental': [],
            'applied': []
        }
        
        if central_concept in self.DOCTRINAL_FOUNDATIONS:
            layers['essential'] = self.DOCTRINAL_FOUNDATIONS[central_concept]
        
        # Find what develops from this concept
        for concept, foundations in self.DOCTRINAL_FOUNDATIONS.items():
            if central_concept in foundations:
                layers['developmental'].append(concept)
        
        # Liturgical applications
        if central_concept in self.LITURGICAL_CONNECTIONS:
            layers['applied'] = self.LITURGICAL_CONNECTIONS[central_concept]
        
        return layers
    
    def _find_western_contrasts(self, central: str, related: List[str]) -> List[Tuple[str, str]]:
        """Find relevant Western theological contrasts"""
        contrasts = []
        
        if central in self.WESTERN_CONTRASTS:
            western_view, explanation = self.WESTERN_CONTRASTS[central]
            contrasts.append((western_view, explanation))
        
        for concept in related:
            if concept in self.WESTERN_CONTRASTS:
                western_view, explanation = self.WESTERN_CONTRASTS[concept]
                contrasts.append((western_view, explanation))
        
        return contrasts
    
    def _map_liturgical_connections(self, central: str, related: List[str]) -> List[str]:
        """Map connections to liturgical life"""
        connections = set()
        
        if central in self.LITURGICAL_CONNECTIONS:
            connections.update(self.LITURGICAL_CONNECTIONS[central])
        
        for concept in related:
            if concept in self.LITURGICAL_CONNECTIONS:
                connections.update(self.LITURGICAL_CONNECTIONS[concept])
        
        # Always include Divine Liturgy as central
        connections.add('Divine Liturgy')
        
        return sorted(list(connections))
    
    def _get_patristic_support(self, from_concept: str, to_concept: str) -> List[str]:
        """Get Church Fathers who support this relationship"""
        # This would ideally query a database
        # For now, return relevant fathers
        support = ['St. Maximus the Confessor', 'St. Gregory of Nyssa']
        
        if 'Trinity' in [from_concept, to_concept]:
            support.append('St. Basil the Great')
        if 'Incarnation' in [from_concept, to_concept]:
            support.append('St. Athanasius')
        if 'Energies' in from_concept or 'Energies' in to_concept:
            support.append('St. Gregory Palamas')
            
        return support
    
    def _build_concept_graph(self) -> Dict:
        """Build complete concept relationship graph"""
        # This would be a comprehensive graph database
        # For now, return basic structure
        return {
            'concepts': list(self.DOCTRINAL_FOUNDATIONS.keys()),
            'relations': self.DOCTRINAL_FOUNDATIONS
        }
