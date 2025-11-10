"""
Citation Preparer - Patristic citation database and preparation

Manages comprehensive database of verified Patristic citations including:
- Verified works by each Church Father
- Key quotations and passages
- Theological themes per work
- Citation formatting
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import json


@dataclass
class PatristicWork:
    """Information about a Patristic work"""
    title: str
    author: str
    alternate_titles: List[str]
    greek_latin_title: Optional[str]
    themes: List[str]
    key_passages: List[str]
    century: int
    verified: bool = True
    

@dataclass
class PreparedCitation:
    """A prepared citation ready for inclusion"""
    father: str
    work: str
    theme: str
    suggested_context: str
    citation_format: str
    theological_relevance: float
    

class CitationPreparer:
    """
    Prepares and validates Patristic citations
    Maintains database of verified works to prevent hallucination
    """
    
    def __init__(self):
        """Initialize citation database"""
        self.patristic_database = self._load_patristic_database()
        
    def prepare_citations(
        self,
        topic: str,
        suggested_fathers: List[str],
        themes: List[str],
        count: int = 20
    ) -> List[PreparedCitation]:
        """
        Prepare verified citations for a topic
        
        Args:
            topic: Theological topic
            suggested_fathers: List of relevant Church Fathers
            themes: Theological themes to address
            count: Number of citations to prepare
            
        Returns:
            List of prepared citations with verification
        """
        prepared = []
        
        for father in suggested_fathers:
            if father in self.patristic_database:
                works = self.patristic_database[father]
                
                # Find relevant works for this topic
                relevant_works = self._find_relevant_works(works, themes)
                
                for work in relevant_works[:min(3, len(relevant_works))]:
                    citation = self._create_citation(father, work, topic, themes)
                    if citation:
                        prepared.append(citation)
                        
                    if len(prepared) >= count:
                        return prepared
        
        return prepared
    
    def verify_citation(self, father: str, work_title: str) -> bool:
        """
        Verify if a citation is authentic
        
        Args:
            father: Church Father name
            work_title: Title of work
            
        Returns:
            True if verified, False otherwise
        """
        if father not in self.patristic_database:
            return False
        
        works = self.patristic_database[father]
        return any(
            work.title == work_title or work_title in work.alternate_titles
            for work in works
        )
    
    def get_works_by_father(self, father: str) -> List[PatristicWork]:
        """Get all verified works by a Church Father"""
        return self.patristic_database.get(father, [])
    
    def get_works_by_theme(self, theme: str) -> List[Tuple[str, PatristicWork]]:
        """Get all works addressing a specific theme"""
        results = []
        
        for father, works in self.patristic_database.items():
            for work in works:
                if theme.lower() in [t.lower() for t in work.themes]:
                    results.append((father, work))
        
        return results
    
    def _find_relevant_works(
        self,
        works: List[PatristicWork],
        themes: List[str]
    ) -> List[PatristicWork]:
        """Find works relevant to specified themes"""
        scored_works = []
        
        for work in works:
            # Score based on theme overlap
            score = sum(
                1 for theme in themes
                for work_theme in work.themes
                if theme.lower() in work_theme.lower()
            )
            if score > 0:
                scored_works.append((score, work))
        
        # Sort by relevance
        scored_works.sort(key=lambda x: x[0], reverse=True)
        
        return [work for score, work in scored_works]
    
    def _create_citation(
        self,
        father: str,
        work: PatristicWork,
        topic: str,
        themes: List[str]
    ) -> Optional[PreparedCitation]:
        """Create a prepared citation"""
        
        # Find most relevant theme
        theme = themes[0] if themes else "Orthodox theology"
        
        # Create citation format
        citation_format = f"{father}, in *{work.title}*"
        
        # Calculate theological relevance
        relevance = self._calculate_relevance(work, themes)
        
        # Generate suggested context
        context = self._generate_context(father, work, theme, topic)
        
        return PreparedCitation(
            father=father,
            work=work.title,
            theme=theme,
            suggested_context=context,
            citation_format=citation_format,
            theological_relevance=relevance
        )
    
    def _calculate_relevance(self, work: PatristicWork, themes: List[str]) -> float:
        """Calculate theological relevance score (0.0-1.0)"""
        if not themes:
            return 0.5
        
        overlap = sum(
            1 for theme in themes
            for work_theme in work.themes
            if theme.lower() in work_theme.lower()
        )
        
        return min(1.0, overlap / len(themes))
    
    def _generate_context(
        self,
        father: str,
        work: PatristicWork,
        theme: str,
        topic: str
    ) -> str:
        """Generate suggested context for citation"""
        return (
            f"{father} addresses {theme} in {work.title}, "
            f"providing patristic foundation for understanding {topic}"
        )
    
    def _load_patristic_database(self) -> Dict[str, List[PatristicWork]]:
        """Load comprehensive database of verified Patristic works"""
        
        database = {
            'St. Gregory of Nyssa': [
                PatristicWork(
                    title='On the Making of Man',
                    author='St. Gregory of Nyssa',
                    alternate_titles=['De Hominis Opificio'],
                    greek_latin_title='De hominis opificio',
                    themes=['Anthropology', 'Creation', 'Image of God', 'Soul', 'Body'],
                    key_passages=['On the dual nature of humanity', 'Image and likeness distinction'],
                    century=4
                ),
                PatristicWork(
                    title='The Life of Moses',
                    author='St. Gregory of Nyssa',
                    alternate_titles=['De Vita Moysis'],
                    greek_latin_title='De vita Moysis',
                    themes=['Theosis', 'Spiritual ascent', 'Apophatic theology', 'Mysticism'],
                    key_passages=['The darkness of unknowing', 'Perpetual progress'],
                    century=4
                ),
                PatristicWork(
                    title='Against Eunomius',
                    author='St. Gregory of Nyssa',
                    alternate_titles=['Contra Eunomium'],
                    greek_latin_title='Contra Eunomium',
                    themes=['Trinity', 'Divine nature', 'Theology proper', 'Heresy refutation'],
                    key_passages=['Divine simplicity', 'Trinitarian relations'],
                    century=4
                ),
                PatristicWork(
                    title='On the Soul and Resurrection',
                    author='St. Gregory of Nyssa',
                    alternate_titles=['De Anima et Resurrectione'],
                    greek_latin_title='De anima et resurrectione',
                    themes=['Eschatology', 'Soul', 'Resurrection', 'Immortality'],
                    key_passages=['Nature of the soul', 'Resurrection of the body'],
                    century=4
                ),
            ],
            
            'St. Maximus the Confessor': [
                PatristicWork(
                    title='Ambigua',
                    author='St. Maximus the Confessor',
                    alternate_titles=['Difficulties', 'Ambiguum'],
                    greek_latin_title='Ambigua',
                    themes=['Christology', 'Cosmology', 'Theosis', 'Logos', 'Creation'],
                    key_passages=['Logoi doctrine', 'Cosmic liturgy'],
                    century=7
                ),
                PatristicWork(
                    title='Chapters on Charity',
                    author='St. Maximus the Confessor',
                    alternate_titles=['Four Hundred Chapters on Love', 'Centuriae de charitate'],
                    greek_latin_title='Capita de caritate',
                    themes=['Love', 'Virtue', 'Spiritual life', 'Asceticism'],
                    key_passages=['Divine love', 'Passions and virtues'],
                    century=7
                ),
                PatristicWork(
                    title='Mystagogy',
                    author='St. Maximus the Confessor',
                    alternate_titles=['The Church\'s Mystagogy'],
                    greek_latin_title='Mystagogia',
                    themes=['Liturgy', 'Church', 'Sacraments', 'Symbolism'],
                    key_passages=['Liturgical symbolism', 'Church as image of cosmos'],
                    century=7
                ),
                PatristicWork(
                    title='Opuscula',
                    author='St. Maximus the Confessor',
                    alternate_titles=['Theological and Polemical Opuscula'],
                    greek_latin_title='Opuscula theologica et polemica',
                    themes=['Christology', 'Will of Christ', 'Monothelitism', 'Trinity'],
                    key_passages=['Two wills of Christ', 'Dyothelitism'],
                    century=7
                ),
            ],
            
            'St. Basil the Great': [
                PatristicWork(
                    title='On the Holy Spirit',
                    author='St. Basil the Great',
                    alternate_titles=['De Spiritu Sancto'],
                    greek_latin_title='De Spiritu Sancto',
                    themes=['Pneumatology', 'Trinity', 'Holy Spirit', 'Theology proper'],
                    key_passages=['Divinity of the Spirit', 'Trinitarian theology'],
                    century=4
                ),
                PatristicWork(
                    title='Hexaemeron',
                    author='St. Basil the Great',
                    alternate_titles=['The Six Days of Creation'],
                    greek_latin_title='Hexaemeron',
                    themes=['Creation', 'Cosmology', 'Nature', 'Science and faith'],
                    key_passages=['Days of creation', 'Divine wisdom in nature'],
                    century=4
                ),
                PatristicWork(
                    title='Against Eunomius',
                    author='St. Basil the Great',
                    alternate_titles=['Contra Eunomium'],
                    greek_latin_title='Adversus Eunomium',
                    themes=['Trinity', 'Divine nature', 'Heresy refutation'],
                    key_passages=['Divine simplicity', 'Son equal to Father'],
                    century=4
                ),
            ],
            
            'St. John Chrysostom': [
                PatristicWork(
                    title='Homilies on the Gospel of John',
                    author='St. John Chrysostom',
                    alternate_titles=['Homiliae in Joannem'],
                    greek_latin_title='In Johannem homiliae',
                    themes=['Christology', 'Scripture', 'Pastoral theology', 'Exegesis'],
                    key_passages=['Divinity of Christ', 'Incarnation'],
                    century=4
                ),
                PatristicWork(
                    title='On the Priesthood',
                    author='St. John Chrysostom',
                    alternate_titles=['De Sacerdotio'],
                    greek_latin_title='De sacerdotio',
                    themes=['Priesthood', 'Ministry', 'Church', 'Pastoral care'],
                    key_passages=['Dignity of priesthood', 'Pastoral responsibility'],
                    century=4
                ),
                PatristicWork(
                    title='Homilies on Matthew',
                    author='St. John Chrysostom',
                    alternate_titles=['Homiliae in Matthaeum'],
                    greek_latin_title='In Matthaeum homiliae',
                    themes=['Scripture', 'Ethics', 'Christian life', 'Exegesis'],
                    key_passages=['Sermon on the Mount', 'Christian virtue'],
                    century=4
                ),
            ],
            
            'St. Athanasius': [
                PatristicWork(
                    title='On the Incarnation',
                    author='St. Athanasius',
                    alternate_titles=['De Incarnatione'],
                    greek_latin_title='De incarnatione Verbi',
                    themes=['Christology', 'Incarnation', 'Soteriology', 'Theosis'],
                    key_passages=['God became man that man might become god', 'Salvation through Incarnation'],
                    century=4
                ),
                PatristicWork(
                    title='Against the Heathen',
                    author='St. Athanasius',
                    alternate_titles=['Contra Gentes'],
                    greek_latin_title='Oratio contra gentes',
                    themes=['Apologetics', 'Philosophy', 'Idolatry', 'Creation'],
                    key_passages=['Against paganism', 'True knowledge of God'],
                    century=4
                ),
                PatristicWork(
                    title='Letters to Serapion',
                    author='St. Athanasius',
                    alternate_titles=['Epistulae ad Serapionem'],
                    greek_latin_title='Epistolae ad Serapionem',
                    themes=['Pneumatology', 'Trinity', 'Holy Spirit'],
                    key_passages=['Divinity of the Holy Spirit', 'Trinitarian theology'],
                    century=4
                ),
            ],
            
            'St. Gregory Palamas': [
                PatristicWork(
                    title='Triads in Defense of the Holy Hesychasts',
                    author='St. Gregory Palamas',
                    alternate_titles=['The Triads'],
                    greek_latin_title='Triades',
                    themes=['Hesychasm', 'Divine energies', 'Essence-energies', 'Mysticism', 'Prayer'],
                    key_passages=['Essence-energies distinction', 'Uncreated light'],
                    century=14
                ),
                PatristicWork(
                    title='One Hundred and Fifty Chapters',
                    author='St. Gregory Palamas',
                    alternate_titles=['Physical, Theological, Moral, and Practical Chapters'],
                    greek_latin_title='Capita CL',
                    themes=['Theology', 'Philosophy', 'Asceticism', 'Divine energies'],
                    key_passages=['Natural contemplation', 'Theosis through energies'],
                    century=14
                ),
            ],
            
            'St. John of Damascus': [
                PatristicWork(
                    title='Exact Exposition of the Orthodox Faith',
                    author='St. John of Damascus',
                    alternate_titles=['De Fide Orthodoxa'],
                    greek_latin_title='Expositio fidei orthodoxae',
                    themes=['Systematic theology', 'Trinity', 'Christology', 'Anthropology'],
                    key_passages=['Systematic exposition', 'Orthodox doctrine'],
                    century=8
                ),
                PatristicWork(
                    title='On the Divine Images',
                    author='St. John of Damascus',
                    alternate_titles=['De Imaginibus'],
                    greek_latin_title='Orationes de imaginibus',
                    themes=['Iconography', 'Incarnation', 'Matter', 'Worship'],
                    key_passages=['Defense of icons', 'Incarnation and matter'],
                    century=8
                ),
            ],
        }
        
        return database
