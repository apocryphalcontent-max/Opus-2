"""
Theological Context Builder - Comprehensive context preparation

Builds rich theological context for generation including:
- Historical development
- Patristic consensus
- Contemporary applications
- Liturgical connections
- Scripture foundations
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from .topic_analyzer import TopicAnalysis
from .semantic_mapper import SemanticMap
from .citation_preparer import PreparedCitation


@dataclass
class TheologicalContext:
    """Complete theological context for entry generation"""
    topic: str
    analysis: TopicAnalysis
    semantic_map: SemanticMap
    prepared_citations: List[PreparedCitation]
    historical_development: str
    contemporary_relevance: str
    liturgical_context: str
    scriptural_foundation: str
    western_contrasts: List[str]
    generation_guidance: Dict[str, str]
    

class TheologicalContextBuilder:
    """
    Builds comprehensive theological context to guide
    high-quality entry generation
    """
    
    def __init__(self):
        """Initialize context builder"""
        self.historical_patterns = self._load_historical_patterns()
        
    def build_context(
        self,
        topic: str,
        analysis: TopicAnalysis,
        semantic_map: SemanticMap,
        prepared_citations: List[PreparedCitation]
    ) -> TheologicalContext:
        """
        Build complete theological context
        
        Args:
            topic: Theological topic
            analysis: Topic analysis results
            semantic_map: Semantic relationship map
            prepared_citations: Prepared Patristic citations
            
        Returns:
            Complete TheologicalContext for generation
        """
        # Build historical development narrative
        historical = self._build_historical_development(
            topic, analysis, semantic_map
        )
        
        # Identify contemporary relevance
        contemporary = self._identify_contemporary_relevance(
            topic, analysis
        )
        
        # Build liturgical context
        liturgical = self._build_liturgical_context(
            semantic_map.liturgical_connections
        )
        
        # Build scriptural foundation
        scriptural = self._build_scriptural_foundation(
            analysis.suggested_scriptures
        )
        
        # Format Western contrasts
        western = self._format_western_contrasts(
            semantic_map.western_contrasts
        )
        
        # Generate guidance for each section
        guidance = self._generate_section_guidance(
            topic, analysis, semantic_map
        )
        
        return TheologicalContext(
            topic=topic,
            analysis=analysis,
            semantic_map=semantic_map,
            prepared_citations=prepared_citations,
            historical_development=historical,
            contemporary_relevance=contemporary,
            liturgical_context=liturgical,
            scriptural_foundation=scriptural,
            western_contrasts=western,
            generation_guidance=guidance
        )
    
    def _build_historical_development(
        self,
        topic: str,
        analysis: TopicAnalysis,
        semantic_map: SemanticMap
    ) -> str:
        """Build narrative of historical development"""
        
        development = f"Historical Development of {topic}:\n\n"
        
        # Foundational layer
        if semantic_map.doctrinal_layers.get('foundational'):
            foundations = semantic_map.doctrinal_layers['foundational']
            development += f"Foundational doctrines: {', '.join(foundations)}\n"
            development += "These core teachings were established in the early centuries.\n\n"
        
        # Development through Church Fathers
        fathers = analysis.suggested_fathers
        if fathers:
            development += "Key Patristic developments:\n"
            for father in fathers[:5]:  # Top 5
                century = self._get_father_century(father)
                development += f"- {father} ({century} century)\n"
            development += "\n"
        
        # Contemporary synthesis
        development += "Modern Orthodox synthesis maintains patristic foundations "
        development += "while addressing contemporary questions.\n"
        
        return development
    
    def _identify_contemporary_relevance(
        self,
        topic: str,
        analysis: TopicAnalysis
    ) -> str:
        """Identify contemporary relevance of topic"""
        
        relevance = f"Contemporary Relevance of {topic}:\n\n"
        
        # Check for contemporary markers in topic
        topic_lower = topic.lower()
        
        if any(term in topic_lower for term in ['science', 'quantum', 'physics', 'mathematics']):
            relevance += "- Addresses relationship between Orthodox theology and modern science\n"
        
        if any(term in topic_lower for term in ['technology', 'digital', 'ai', 'artificial']):
            relevance += "- Engages with technological developments from Orthodox perspective\n"
        
        if any(term in topic_lower for term in ['ecology', 'environment', 'creation']):
            relevance += "- Provides Orthodox response to ecological concerns\n"
        
        if any(term in topic_lower for term in ['person', 'consciousness', 'mind']):
            relevance += "- Offers Orthodox anthropology for contemporary questions\n"
        
        # Always add general relevance
        relevance += "- Maintains living Patristic tradition in modern context\n"
        relevance += "- Addresses perennial theological questions with Orthodox wisdom\n"
        
        return relevance
    
    def _build_liturgical_context(
        self,
        connections: List[str]
    ) -> str:
        """Build liturgical context narrative"""
        
        if not connections:
            return "This topic connects to the Divine Liturgy and sacramental life of the Church.\n"
        
        context = "Liturgical Connections:\n\n"
        
        for connection in connections:
            if connection == 'Divine Liturgy':
                context += "- Central to the Divine Liturgy, the Church's primary worship\n"
            elif connection == 'Eucharist':
                context += "- Expressed in the Eucharistic celebration\n"
            elif connection == 'Baptism':
                context += "- Connected to Baptismal theology and practice\n"
            elif connection == 'Pascha':
                context += "- Celebrated especially during Pascha (Easter)\n"
            else:
                context += f"- Manifested in {connection}\n"
        
        context += "\nThe liturgical life embodies this theological truth.\n"
        
        return context
    
    def _build_scriptural_foundation(
        self,
        scriptures: List[str]
    ) -> str:
        """Build scriptural foundation narrative"""
        
        if not scriptures:
            return "Grounded in Scripture as interpreted by the Church Fathers.\n"
        
        foundation = "Scriptural Foundation:\n\n"
        foundation += "Key passages:\n"
        
        for scripture in scriptures[:8]:  # Limit to top 8
            foundation += f"- {scripture}\n"
        
        foundation += "\nThese passages, understood through Patristic exegesis, "
        foundation += "provide biblical foundation for this teaching.\n"
        
        return foundation
    
    def _format_western_contrasts(
        self,
        contrasts: List[tuple]
    ) -> List[str]:
        """Format Western theological contrasts"""
        
        formatted = []
        
        for western_view, explanation in contrasts:
            formatted.append(
                f"Unlike {western_view}, {explanation}"
            )
        
        if not formatted:
            # Add generic contrast
            formatted.append(
                "Orthodox theology maintains distinctions from Western scholastic approaches"
            )
        
        return formatted
    
    def _generate_section_guidance(
        self,
        topic: str,
        analysis: TopicAnalysis,
        semantic_map: SemanticMap
    ) -> Dict[str, str]:
        """Generate guidance for each entry section"""
        
        guidance = {}
        
        # Introduction
        guidance['Introduction'] = (
            f"Introduce {topic} from Orthodox perspective. "
            f"Preview the {len(analysis.core_themes)} main themes: {', '.join(analysis.core_themes)}. "
            f"Establish contemporary relevance and Orthodox framing."
        )
        
        # The Patristic Mind
        guidance['The Patristic Mind'] = (
            f"Engage deeply with these Church Fathers: {', '.join(analysis.suggested_fathers[:5])}. "
            f"Focus on {analysis.theological_domain} theology. "
            f"Cite specific works and provide quotations or paraphrases."
        )
        
        # Symphony of Clashes
        guidance['Symphony of Clashes'] = (
            f"Present dialectical tensions in {topic}. "
            f"Address philosophical and theological questions. "
            f"Show how Orthodox theology navigates apparent paradoxes."
        )
        
        # Orthodox Affirmation
        guidance['Orthodox Affirmation'] = (
            f"Clearly state Orthodox position on {topic}. "
            f"Ground in Scripture: {', '.join(analysis.suggested_scriptures[:5])}. "
            f"Show distinctions from Western theology. "
            f"Connect to core doctrines: {', '.join(analysis.related_doctrines)}."
        )
        
        # Synthesis
        guidance['Synthesis'] = (
            f"Integrate all threads into coherent Orthodox vision. "
            f"Show how {semantic_map.central_concept} relates to {', '.join(semantic_map.related_concepts[:3])}. "
            f"Provide practical applications for spiritual life."
        )
        
        # Conclusion
        guidance['Conclusion'] = (
            f"Recap the journey through {topic}. "
            f"Reaffirm Orthodox position with confidence and humility. "
            f"Acknowledge mystery while celebrating revealed truth. "
            f"End with doxological spirit."
        )
        
        return guidance
    
    def _get_father_century(self, father: str) -> str:
        """Get century in which Church Father lived"""
        centuries = {
            'St. Gregory of Nyssa': '4th',
            'St. Maximus the Confessor': '7th',
            'St. Basil the Great': '4th',
            'St. John Chrysostom': '4th-5th',
            'St. Athanasius': '4th',
            'St. Gregory Palamas': '14th',
            'St. John of Damascus': '8th',
            'St. Gregory Nazianzen': '4th',
            'St. Ignatius of Antioch': '1st-2nd',
            'St. Irenaeus of Lyons': '2nd',
            'St. Cyril of Alexandria': '5th',
        }
        return centuries.get(father, 'early')
    
    def _load_historical_patterns(self) -> Dict:
        """Load historical development patterns"""
        return {
            'trinitarian': 'Developed through 4th century Cappadocian synthesis',
            'christological': 'Clarified through Ecumenical Councils 4th-7th centuries',
            'hesychast': 'Synthesized by Gregory Palamas in 14th century',
        }
