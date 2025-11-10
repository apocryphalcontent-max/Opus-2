"""
Topic Analyzer - Advanced semantic analysis for theological topics

Provides deep analysis of theological topics to extract:
- Core theological themes
- Related Patristic sources
- Relevant Scripture passages
- Doctrinal connections
- Historical context
"""

import re
from typing import Dict, List, Set, Optional
from dataclasses import dataclass


@dataclass
class TopicAnalysis:
    """Results of topic analysis"""
    topic: str
    core_themes: List[str]
    theological_domain: str
    suggested_fathers: List[str]
    suggested_scriptures: List[str]
    related_doctrines: List[str]
    complexity_score: float
    estimated_depth_required: str  # 'foundational', 'intermediate', 'advanced'
    
    
class TopicAnalyzer:
    """
    Analyzes theological topics to extract semantic information
    and provide preprocessing guidance for generation
    """
    
    # Theological domain keywords
    DOMAIN_KEYWORDS = {
        'trinitarian': ['trinity', 'trinitarian', 'father', 'son', 'spirit', 'persons', 'hypostases'],
        'christological': ['christ', 'incarnation', 'hypostatic', 'christology', 'divine nature', 'human nature'],
        'soteriological': ['salvation', 'theosis', 'deification', 'redemption', 'sanctification'],
        'ecclesiological': ['church', 'ecclesiology', 'sacraments', 'liturgy', 'worship'],
        'eschatological': ['eschatology', 'resurrection', 'eternal', 'kingdom', 'judgment'],
        'anthropological': ['humanity', 'soul', 'body', 'image', 'likeness', 'personhood'],
        'cosmological': ['creation', 'cosmos', 'nature', 'universe', 'matter'],
        'epistemological': ['knowledge', 'revelation', 'apophatic', 'cataphatic', 'mystery'],
    }
    
    # Father specializations
    FATHER_SPECIALIZATIONS = {
        'trinitarian': ['St. Gregory of Nyssa', 'St. Basil the Great', 'St. Gregory Nazianzen'],
        'christological': ['St. Athanasius', 'St. Cyril of Alexandria', 'St. Maximus the Confessor'],
        'soteriological': ['St. Maximus the Confessor', 'St. Gregory of Nyssa', 'St. Athanasius'],
        'ecclesiological': ['St. John Chrysostom', 'St. Ignatius of Antioch', 'St. Cyprian of Carthage'],
        'eschatological': ['St. Gregory of Nyssa', 'St. Irenaeus of Lyons'],
        'anthropological': ['St. Gregory of Nyssa', 'St. Maximus the Confessor', 'St. John of Damascus'],
        'cosmological': ['St. Basil the Great', 'St. Maximus the Confessor', 'St. Gregory of Nyssa'],
        'epistemological': ['St. Gregory Palamas', 'St. Dionysius the Areopagite', 'St. Maximus the Confessor'],
    }
    
    def __init__(self):
        """Initialize the topic analyzer"""
        self.theological_terms = self._load_theological_terms()
        
    def analyze(self, topic: str) -> TopicAnalysis:
        """
        Perform comprehensive analysis of a theological topic
        
        Args:
            topic: The theological topic to analyze
            
        Returns:
            TopicAnalysis object with detailed analysis results
        """
        # Normalize topic
        topic_lower = topic.lower()
        
        # Extract core themes
        core_themes = self._extract_core_themes(topic_lower)
        
        # Identify theological domain
        theological_domain = self._identify_domain(topic_lower)
        
        # Suggest relevant Church Fathers
        suggested_fathers = self._suggest_fathers(theological_domain, topic_lower)
        
        # Suggest Scripture passages
        suggested_scriptures = self._suggest_scriptures(theological_domain, topic_lower)
        
        # Identify related doctrines
        related_doctrines = self._identify_related_doctrines(topic_lower)
        
        # Calculate complexity
        complexity_score = self._calculate_complexity(topic_lower, core_themes)
        
        # Determine depth required
        depth_required = self._determine_depth_required(complexity_score)
        
        return TopicAnalysis(
            topic=topic,
            core_themes=core_themes,
            theological_domain=theological_domain,
            suggested_fathers=suggested_fathers,
            suggested_scriptures=suggested_scriptures,
            related_doctrines=related_doctrines,
            complexity_score=complexity_score,
            estimated_depth_required=depth_required
        )
    
    def _extract_core_themes(self, topic: str) -> List[str]:
        """Extract core theological themes from topic"""
        themes = []
        
        # Check for major theological concepts
        if any(word in topic for word in ['trinity', 'trinitarian', 'three persons']):
            themes.append('Trinitarian theology')
        if any(word in topic for word in ['incarnation', 'christ', 'christology']):
            themes.append('Christology')
        if any(word in topic for word in ['theosis', 'deification', 'salvation']):
            themes.append('Theosis and Soteriology')
        if any(word in topic for word in ['essence', 'energies', 'divine energies']):
            themes.append('Essence-Energies distinction')
        if any(word in topic for word in ['church', 'sacrament', 'liturgy']):
            themes.append('Ecclesiology and Liturgical life')
        if any(word in topic for word in ['creation', 'cosmos', 'nature']):
            themes.append('Cosmology and Creation')
        if any(word in topic for word in ['knowledge', 'apophatic', 'mystery']):
            themes.append('Theological epistemology')
        if any(word in topic for word in ['icon', 'image', 'beauty']):
            themes.append('Iconography and aesthetics')
            
        return themes if themes else ['General Orthodox theology']
    
    def _identify_domain(self, topic: str) -> str:
        """Identify primary theological domain"""
        domain_scores = {}
        
        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in topic)
            if score > 0:
                domain_scores[domain] = score
        
        if domain_scores:
            return max(domain_scores.items(), key=lambda x: x[1])[0]
        return 'general'
    
    def _suggest_fathers(self, domain: str, topic: str) -> List[str]:
        """Suggest relevant Church Fathers based on domain"""
        fathers = set()
        
        # Domain-specific fathers
        if domain in self.FATHER_SPECIALIZATIONS:
            fathers.update(self.FATHER_SPECIALIZATIONS[domain])
        
        # Always include foundational fathers
        fathers.add('St. Maximus the Confessor')
        fathers.add('St. Gregory of Nyssa')
        
        # Topic-specific additions
        if 'palamas' in topic or 'hesychasm' in topic or 'energies' in topic:
            fathers.add('St. Gregory Palamas')
        if 'damascus' in topic or 'icon' in topic:
            fathers.add('St. John of Damascus')
        if 'liturgy' in topic or 'worship' in topic:
            fathers.add('St. John Chrysostom')
        if 'athanasius' in topic or 'arius' in topic:
            fathers.add('St. Athanasius')
            
        return sorted(list(fathers))
    
    def _suggest_scriptures(self, domain: str, topic: str) -> List[str]:
        """Suggest relevant Scripture passages"""
        scriptures = []
        
        # Domain-specific Scripture
        if domain == 'trinitarian':
            scriptures.extend(['John 1:1-14', 'Matthew 28:19', '2 Corinthians 13:14'])
        elif domain == 'christological':
            scriptures.extend(['John 1:1-14', 'Philippians 2:5-11', 'Colossians 1:15-20'])
        elif domain == 'soteriological':
            scriptures.extend(['2 Peter 1:4', 'Romans 8:29-30', 'Ephesians 2:8-10'])
        elif domain == 'ecclesiological':
            scriptures.extend(['1 Corinthians 12:12-27', 'Ephesians 4:1-16', 'Acts 2:42'])
        elif domain == 'cosmological':
            scriptures.extend(['Genesis 1:1-31', 'Colossians 1:16-17', 'Psalm 104'])
            
        # Topic-specific additions
        if 'theosis' in topic or 'deification' in topic:
            scriptures.append('2 Peter 1:4')
        if 'image' in topic or 'likeness' in topic:
            scriptures.append('Genesis 1:26-27')
        if 'resurrection' in topic:
            scriptures.append('1 Corinthians 15')
            
        return scriptures if scriptures else ['John 1:1-14', 'Romans 8:29-30']
    
    def _identify_related_doctrines(self, topic: str) -> List[str]:
        """Identify related Orthodox doctrines"""
        doctrines = []
        
        # Always related
        doctrines.append('Holy Trinity')
        doctrines.append('Incarnation')
        
        # Topic-specific
        if any(word in topic for word in ['salvation', 'theosis', 'deification']):
            doctrines.append('Theosis')
        if any(word in topic for word in ['church', 'sacrament']):
            doctrines.append('Ecclesiology')
        if any(word in topic for word in ['energies', 'essence']):
            doctrines.append('Essence-Energies distinction')
        if any(word in topic for word in ['icon', 'image']):
            doctrines.append('Veneration of icons')
            
        return doctrines
    
    def _calculate_complexity(self, topic: str, themes: List[str]) -> float:
        """Calculate topic complexity score (0.0-1.0)"""
        complexity = 0.5  # Base complexity
        
        # More themes = more complex
        complexity += len(themes) * 0.05
        
        # Interdisciplinary topics are more complex
        interdisciplinary_markers = ['and', 'in', 'through', 'synthesis']
        complexity += sum(0.1 for marker in interdisciplinary_markers if marker in topic)
        
        # Abstract concepts are more complex
        abstract_terms = ['infinity', 'eternity', 'mystery', 'paradox', 'unknowable']
        complexity += sum(0.1 for term in abstract_terms if term in topic)
        
        return min(1.0, complexity)
    
    def _determine_depth_required(self, complexity_score: float) -> str:
        """Determine required depth based on complexity"""
        if complexity_score >= 0.75:
            return 'advanced'
        elif complexity_score >= 0.5:
            return 'intermediate'
        else:
            return 'foundational'
    
    def _load_theological_terms(self) -> Set[str]:
        """Load comprehensive list of theological terms"""
        return {
            'theosis', 'deification', 'incarnation', 'trinity', 'trinitarian',
            'hypostasis', 'hypostatic', 'ousia', 'essence', 'energies',
            'apophatic', 'cataphatic', 'perichoresis', 'kenosis',
            'synergy', 'liturgy', 'sacrament', 'patristic',
            'soteriology', 'ecclesiology', 'christology', 'pneumatology',
            'eschatology', 'anthropology', 'cosmology'
        }
