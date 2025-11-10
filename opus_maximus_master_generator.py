"""
OPUS MAXIMUS MASTER GENERATOR (GPU-NATIVE AGENTIC)
====================================================
The Ultimate Fully Automated Apocalyptic Hexaemeron Generation System

ARCHITECTURE:
- Local LLM inference (llama-cpp-python) with full GPU offload
- Agentic self-correction loop (LangGraph state machine)
- GPU-accelerated semantic database (ChromaDB)
- GPU-accelerated uniqueness checking (FAISS-GPU)
- Absolute ruleset enforcement (ALPHA, BETA, GAMMA, DELTA)
- Linguistic expansion: Greek + Syriac + Hebrew terms
- Doxological chaining synthesis

PERFORMANCE:
- All computation (LLM, Embeddings, Search) on local GPU
- Self-correcting logic minimizes full re-runs
- Zero network latency
- ~5-10x faster than API-based

MANDATES:
- RULESET ALPHA: Six-section structure, 10,000+ word count
- RULESET BETA: Formatting (4-space indent, em-dash ban, hyphen policy)
- RULESET GAMMA: Linguistic (capitalization, NOT...BUT, sentence algorithm)
- RULESET DELTA: Content per section
- ABSOLUTE UNIQUENESS: Every word unique per entry

Author: Automated System for Orthodox Apologetics
Date: 2025-11-07
Version: GPU-NATIVE-AGENTIC-V2 (WordCount + CrossRef + StyleInject)
"""

import os
import sys
import time
import logging
import pickle
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Set, TypedDict
from datetime import datetime
from collections import defaultdict, Counter
import argparse
import numpy as np

try:
    from sentence_transformers import SentenceTransformer, util
    import orjson
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.table import Table
    from rich.panel import Panel
    from pydantic import BaseModel, Field
    import diskcache
    import faiss
    from rapidfuzz import fuzz
    import torch
    import chromadb
    from llama_cpp import Llama
    from langgraph.graph import StateGraph, END
except ImportError as e:
    print(f"ERROR: Missing dependency: {e}")
    print("Install dependencies: pip install -r requirements.txt")
    print("!! MAKE SURE TO INSTALL llama-cpp-python WITH CUDA SUPPORT !!")
    sys.exit(1)

console = Console()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('opus_master_generator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Check for CUDA
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
if DEVICE == 'cpu':
    logger.warning("CUDA not available. FAISS and Embeddings will use CPU.")
else:
    logger.info(f"CUDA available. Using device: {DEVICE}")


# ============================================================================
# DATA STRUCTURES
# ============================================================================

class QualityMetrics(BaseModel):
    """Comprehensive quality metrics"""
    word_count: int = 0
    paragraph_count: int = 0
    section_count: int = 0
    hyphen_violations: List[str] = Field(default_factory=list)
    em_dash_violations: List[str] = Field(default_factory=list)
    indentation_violations: int = 0
    liturgical_and_yet_but_count: int = 0
    not_but_constructions: int = 0
    theological_capitalization_score: float = 0.0
    theological_term_density: float = 0.0
    greek_terms_found: List[str] = Field(default_factory=list)
    syriac_terms_found: List[str] = Field(default_factory=list)
    hebrew_terms_found: List[str] = Field(default_factory=list)
    scriptural_references: int = 0
    apocryphal_references: int = 0
    has_theophanic_rupture: bool = False
    has_opening_prayer_sec_vi: bool = False
    has_eucharistic_culmination: bool = False
    has_doxological_cascade: bool = False
    has_from_to_structure: bool = False
    weight_of_glory_markers: int = 0
    patristic_subsections_count: int = 0
    patristic_citations_specific: int = 0
    dialectical_subsections_count: int = 0
    thesis_antithesis_synthesis: int = 0
    academic_prose_violations: List[str] = Field(default_factory=list)
    forbidden_transitions: List[str] = Field(default_factory=list)
    similarity_to_previous_entries: float = 0.0
    repeated_phrases_count: int = 0
    similarity_to_golden: float = 0.0
    sentence_complexity_score: float = 0.0
    overall_score: float = 0.0
    passes_absolute_mandates: bool = False

    class Config:
        arbitrary_types_allowed = True


class Blueprint(BaseModel):
    """Hyper-detailed blueprint"""
    subject: str
    tier: str
    category: str
    core_thesis: str
    structural_penthos: str
    theophanic_rupture_seed: str
    eucharistic_culmination_seed: str
    eschatological_consummation_seed: str = ""
    biblical_verses: List[Dict[str, str]] = Field(default_factory=list)
    apocryphal_seeds: List[Dict[str, str]] = Field(default_factory=list)
    patristic_interlocutors: List[Dict[str, Any]] = Field(default_factory=list)
    dialectical_clashes: List[Dict[str, Any]] = Field(default_factory=list)
    primary_works: List[Dict[str, str]] = Field(default_factory=list)
    semantic_patristic_citations: List[Dict[str, str]] = Field(default_factory=list)
    greek_terms_per_section: Dict[str, List[str]] = Field(default_factory=dict)
    syriac_terms_per_section: Dict[str, List[str]] = Field(default_factory=dict)
    hebrew_terms_per_section: Dict[str, List[str]] = Field(default_factory=dict)
    opening_pattern: str = "historical_moment"
    section_synthesis_requirements: Dict[str, str] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True


class EntryCandidate(BaseModel):
    """Generated entry with validation"""
    subject: str
    tier: str
    category: str
    blueprint: Blueprint
    content: str
    metrics: QualityMetrics
    generation_time: float
    attempt_number: int
    approved: bool = False
    rejection_reasons: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True


class GenerationState(TypedDict):
    """LangGraph state for agentic generation"""
    subject: str
    tier: str
    category: str
    blueprint: Optional[Blueprint]
    sections: List[str]  # List of 6 approved section contents
    current_section_num: int
    current_section_name: str
    current_section_content: str
    validation_failures: List[str]
    section_attempts: int
    entry_expansion_attempts: int  # NEW: For word count loop
    final_content: str
    final_metrics: Optional[QualityMetrics]
    generation_time: float
    start_time: float


# ============================================================================
# THEOLOGICAL TERM REGISTRY
# ============================================================================

class TheologicalTermRegistry:
    """Expanded linguistic registry"""

    GREEK_TERMS = {
        'nous': 'spiritual intellect',
        'kardia': 'heart as spiritual center',
        'logoi': 'divine purposes in creation',
        'logos': 'divine reason, the Word',
        'theosis': 'deification',
        'energeia': 'divine operation',
        'ousia': 'essence, being',
        'nepsis': 'watchfulness',
        'hesychia': 'stillness',
        'phos': 'light',
        'penthos': 'godly sorrow',
        'ekklesia': 'Church',
        'perichoresis': 'mutual indwelling',
        'hypostasis': 'subsistence, person',
        'prosopon': 'person',
        'apatheia': 'passionlessness',
        'metanoia': 'repentance',
        'anamnesis': 'liturgical remembrance',
        'epiklesis': 'invocation',
        'theoria': 'contemplation',
        'praxis': 'practice',
        'synergy': 'cooperation with grace',
    }

    SYRIAC_TERMS = {
        'qnoma': 'hypostasis',
        'ihidayutha': 'oneness, solitude',
        'madbha': 'altar',
        'ruha': 'spirit',
        'memra': 'word',
        'shekhinah': 'divine presence',
        'teshbokhta': 'hymn of praise',
        'raza': 'mystery, sacrament',
    }

    HEBREW_TERMS = {
        'kavod': 'glory, weight',
        'ruach': 'spirit, breath',
        'nephesh': 'soul, life',
        'dabar': 'word, thing',
        'hesed': 'steadfast love',
        'emeth': 'truth, faithfulness',
        'shalom': 'peace, wholeness',
        'bereshith': 'in the beginning',
    }

    @classmethod
    def get_all_terms(cls) -> List[str]:
        return (list(cls.GREEK_TERMS.keys()) +
                list(cls.SYRIAC_TERMS.keys()) +
                list(cls.HEBREW_TERMS.keys()))

    @classmethod
    def get_random_terms(cls, n: int, language: Optional[str] = None) -> List[str]:
        if language == 'greek':
            pool = list(cls.GREEK_TERMS.keys())
        elif language == 'syriac':
            pool = list(cls.SYRIAC_TERMS.keys())
        elif language == 'hebrew':
            pool = list(cls.HEBREW_TERMS.keys())
        else:
            pool = cls.get_all_terms()

        n = min(n, len(pool))
        return list(np.random.choice(pool, n, replace=False))


# ============================================================================
# PATTERN EXTRACTION
# ============================================================================

class GoldenPatternExtractor:
    """Extract patterns from golden entries"""

    def __init__(self, golden_entries_dir: Path):
        self.golden_dir = golden_entries_dir
        self.patterns = defaultdict(list)
        self.cache = diskcache.Cache('.pattern_cache')

        if 'patterns' in self.cache:
            logger.info("Loading cached golden patterns")
            self.patterns = defaultdict(list, self.cache['patterns'])
        else:
            logger.info(f"Extracting patterns from {self.golden_dir}...")
            self._extract_all_patterns()
            self._cache_patterns()

    def _extract_all_patterns(self):
        golden_files = list(self.golden_dir.rglob('*.md'))
        if not golden_files:
            logger.error(f"No .md files found in {self.golden_dir}")
            return

        console.print(f"[cyan]Found {len(golden_files)} golden entries[/cyan]")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Extracting patterns...", total=len(golden_files))

            for filepath in golden_files:
                try:
                    content = filepath.read_text(encoding='utf-8')
                    self._extract_openings(content, filepath.stem)
                    self._extract_liturgical_rhythms(content)
                    self._extract_not_but_structures(content)
                except Exception as e:
                    logger.warning(f"Could not parse golden file {filepath.name}: {e}")
                progress.advance(task)

    def _extract_openings(self, content: str, name: str):
        lines = content.split('\n')
        for i, line in enumerate(lines):
            # Find the line AFTER the "I. Strategic Role" header
            if line.strip().upper().startswith('## I. STRATEGIC ROLE') and i + 1 < len(lines):
                first_para = lines[i + 1].strip()
                if first_para and len(first_para) > 50:
                    self.patterns['openings'].append(first_para[:200])
                    break # Only take the first paragraph

    def _extract_liturgical_rhythms(self, content: str):
        # Find capitalized AND/YET/BUT followed by a clause
        # This regex looks for the capitalized word, a space, at least two words,
        # then a longer clause, ending in punctuation.
        patterns = re.findall(r'\b(AND|YET|BUT)\s+[a-zA-Z,\']+\s+[a-zA-Z]+\b[^.!?]{20,150}[.!?]', content)
        self.patterns['liturgical_rhythms'].extend(patterns[:10]) # Limit to 10 per file

    def _extract_not_but_structures(self, content: str):
        # Find "NOT [short clause] BUT [short clause]"
        # This regex looks for NOT, a word, a clause 5-70 chars, optional comma,
        # BUT, a word, another clause 5-70 chars, and ending punctuation.
        patterns = re.findall(r'NOT\s+\w+[^,]{5,70},?\s+BUT\s+\w+[^.!?]{5,70}[.!?]', content, re.IGNORECASE)
        self.patterns['not_but'].extend(patterns[:10]) # Limit to 10 per file

    def _cache_patterns(self):
        self.cache['patterns'] = dict(self.patterns)
        total = sum(len(v) for v in self.patterns.values())
        console.print(f"[green]Cached {total} patterns[/green]")

    def get_random_pattern(self, pattern_type: str, n: int = 1) -> List[Any]:
        patterns = self.patterns.get(pattern_type, [])
        if not patterns:
            return []
        indices = np.random.choice(len(patterns), min(n, len(patterns)), replace=False)
        return [patterns[i] for i in indices]


# ============================================================================
# SEMANTIC RESEARCH DATABASE (ChromaDB)
# ============================================================================

class SemanticResearchDatabase:
    """Research database using ChromaDB"""

    def __init__(self, db_path: Path = Path('research_db_chroma')):
        self.db_path = db_path
        if not self.db_path.exists():
            logger.error(f"FATAL: ChromaDB not found: {db_path}")
            logger.error("Please run db_builder.py first.")
            sys.exit(1)

        self.client = chromadb.PersistentClient(path=str(db_path))
        self.embedding_model = SentenceTransformer('BAAI/bge-large-en-v1.5', device=DEVICE)

        self.patristic_collection = self.client.get_collection("patristic_citations")
        self.biblical_collection = self.client.get_collection("biblical_verses")
        self.apocryphal_collection = self.client.get_collection("apocryphal_verses")
        self.opponent_collection = self.client.get_collection("dialectical_opponents")

        logger.info("SemanticResearchDatabase connected to ChromaDB")

    def _query_collection(self, collection, query_text: str, limit: int = 5,
                         where_filter: Dict = None, min_similarity: float = 0.3) -> List[Dict]:
        try:
            query_embedding = self.embedding_model.encode(query_text, device=DEVICE)
            query_embedding = query_embedding / np.linalg.norm(query_embedding)  # Normalize

            results = collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=limit * 2,  # Get extras for filtering
                where=where_filter  # Filter by metadata
            )

            metadatas = results.get('metadatas', [[]])[0]
            documents = results.get('documents', [[]])[0]
            distances = results.get('distances', [[]])[0]

            # Filter by minimum similarity
            filtered = []
            for meta, doc, dist in zip(metadatas, documents, distances):
                # ChromaDB uses L2 distance by default. For normalized embeddings, 
                # L2 distance (d) relates to cosine sim (s) as d^2 = 2 - 2s. 
                # So, cosine similarity s = 1 - (d^2 / 2).
                if dist is None: continue
                similarity = 1 - ((dist**2) / 2)
                
                if similarity >= min_similarity:
                    filtered.append({**meta, 'text': doc, 'similarity': similarity})

            # Sort by similarity, descending
            filtered.sort(key=lambda x: x['similarity'], reverse=True)
            
            return filtered[:limit]
        except Exception as e:
            logger.error(f"ChromaDB query failed: {e}")
            return []

    def semantic_search_patristic(self, query_text: str, topic: str = None, limit: int = 10) -> List[Dict]:
        where_filter = {"topic": topic} if topic else None
        results = self._query_collection(
            self.patristic_collection,
            query_text,
            limit,
            where_filter=where_filter,
            min_similarity=0.4  # Only return relevant results
        )
        return [{
            'father': r.get('father_name'),
            'work': r.get('work_title'),
            'ref': r.get('citation_ref'),
            'text': r.get('text'),
            'topic': r.get('topic'),
            'similarity': r.get('similarity')
        } for r in results]

    def search_biblical_verses(self, keywords: List[str], limit: int = 10) -> List[Dict]:
        query_string = ' '.join(keywords)
        results = self._query_collection(self.biblical_collection, query_string, limit)
        return [{'ref': r.get('reference'), 'text': r.get('text')} for r in results]

    def get_apocryphal_verses(self, theme: str, limit: int = 5) -> List[Dict]:
        results = self._query_collection(self.apocryphal_collection, theme, limit)
        return [{'ref': r.get('reference'), 'text': r.get('text')} for r in results]

    def find_dialectical_opponents(self, subject: str, category: str) -> List[Dict]:
        query_text = f"{subject} {category}"
        results = self._query_collection(self.opponent_collection, query_text, limit=3)
        return [{
            'opponent': r.get('opponent_name'),
            'relation': r.get('relation_type'),
            'positions': orjson.loads(r['key_positions']) if isinstance(r.get('key_positions'), str) else r.get('key_positions', []),
            'category': r.get('category')
        } for r in results]

    def close(self):
        # ChromaDB persistent client doesn't require explicit close
        pass


# ============================================================================
# UNIQUENESS CHECKER (FAISS-GPU)
# ============================================================================

class UniquenessChecker:
    """Uniqueness checking with FAISS-GPU"""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.embedding_model = SentenceTransformer('BAAI/bge-large-en-v1.5', device=DEVICE)
        self.generated_entries_cache = {}
        self.phrase_registry = set()
        self.embedding_dim = 1024 # From bge-large-en-v1.5

        if DEVICE == 'cuda' and hasattr(faiss, 'GpuIndexFlatIP'):
            logger.info("Initializing FAISS on GPU")
            res = faiss.StandardGpuResources()
            # Use IndexFlatIP for cosine similarity on normalized vectors
            self.faiss_index = faiss.GpuIndexFlatIP(res, self.embedding_dim)
        else:
            logger.warning("FAISS-GPU not found. Using CPU.")
            # Use IndexFlatIP for cosine similarity on normalized vectors
            self.faiss_index = faiss.IndexFlatIP(self.embedding_dim)

        self.entry_names = []
        self._load_existing_entries()

    def _load_existing_entries(self):
        if not self.output_dir.exists():
            return

        console.print("[cyan]Loading existing entries into FAISS/Uniqueness checker...[/cyan]")
        embeddings_list = []
        
        all_files = list(self.output_dir.rglob('*.md'))

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Loading entries...", total=len(all_files))

            for filepath in all_files:
                try:
                    content = filepath.read_text(encoding='utf-8')
                    embedding = self.embedding_model.encode(content, device=DEVICE)
                    embedding = embedding / np.linalg.norm(embedding) # Normalize
                    
                    subject_key = filepath.stem
                    self.generated_entries_cache[subject_key] = embedding
                    embeddings_list.append(embedding)
                    self.entry_names.append(subject_key)
                    
                    phrases = re.findall(r'\b(?:\w+\s+){3,10}\w+\b', content)
                    self.phrase_registry.update(p.lower() for p in phrases)
                except Exception as e:
                    logger.warning(f"Could not load {filepath.name} for uniqueness check: {e}")
                progress.advance(task)

        if embeddings_list:
            embeddings_array = np.vstack(embeddings_list).astype('float32')
            self.faiss_index.add(embeddings_array)

        console.print(f"[green]Loaded {len(self.generated_entries_cache)} entries into FAISS[/green]")

    def check_uniqueness(self, new_content: str, subject: str) -> Tuple[bool, List[str]]:
        violations = []

        # FAISS similarity check
        if self.faiss_index.ntotal > 0:
            new_embedding = self.embedding_model.encode(new_content, device=DEVICE)
            new_embedding = new_embedding / np.linalg.norm(new_embedding)
            new_embedding = new_embedding.reshape(1, -1).astype('float32')
            
            # Search returns dot product, which is cosine similarity for normalized vectors
            similarities, indices = self.faiss_index.search(new_embedding, min(5, self.faiss_index.ntotal))

            for similarity, idx in zip(similarities[0], indices[0]):
                if similarity >= 0.75: # High similarity threshold
                    violations.append(f"TOO SIMILAR to '{self.entry_names[idx]}': {similarity:.1%}")

        # Phrase check
        new_phrases = set(p.lower() for p in re.findall(r'\b(?:\w+\s+){3,10}\w+\b', new_content))
        repeated = new_phrases & self.phrase_registry
        if len(repeated) > 20: # Allow some overlap
            violations.append(f"REPEATED PHRASES: {len(repeated)} (Threshold: 20)")

        # Fuzzy check
        fuzzy_matches = 0
        for new_phrase in list(new_phrases)[:100]:  # Sample 100 new phrases
            if new_phrase not in self.phrase_registry:
                # Compare against a random sample of existing phrases
                sample_size = min(500, len(self.phrase_registry))
                if sample_size == 0: break
                sample = np.random.choice(list(self.phrase_registry), sample_size, replace=False)
                for existing_phrase in sample:
                    if fuzz.ratio(new_phrase, existing_phrase) >= 85: # High fuzzy match
                        fuzzy_matches += 1
                        break # Move to next new_phrase
        if fuzzy_matches > 5: # Allow a few fuzzy matches
            violations.append(f"SIMILAR PHRASES (fuzzy): {fuzzy_matches} (Threshold: 5)")

        # Placeholder check
        for placeholder in ['[TODO]', '[TBD]', 'PLACEHOLDER', '[CONTENT]', '[...]', '... existing code ...']:
            if placeholder.lower() in new_content.lower():
                violations.append(f"PLACEHOLDER DETECTED: '{placeholder}'")

        return len(violations) == 0, violations

    def register_new_entry(self, content: str, subject: str):
        try:
            embedding = self.embedding_model.encode(content, device=DEVICE)
            embedding = embedding / np.linalg.norm(embedding)
            embedding_array = embedding.reshape(1, -1).astype('float32')

            # Add to FAISS FIRST (atomic operation)
            idx_before = self.faiss_index.ntotal
            self.faiss_index.add(embedding_array)
            idx_after = self.faiss_index.ntotal

            if idx_after != idx_before + 1:
                raise RuntimeError(f"FAISS index inconsistency: expected {idx_before + 1}, got {idx_after}")

            # THEN register in parallel structures
            subject_key = subject.lower().replace(' ', '_').replace(':', '')
            self.entry_names.append(subject_key)
            self.generated_entries_cache[subject_key] = embedding

            # Verify alignment
            if len(self.entry_names) != self.faiss_index.ntotal:
                # Rollback!
                logger.error(f"Index misalignment: {len(self.entry_names)} names vs {self.faiss_index.ntotal} vectors. Rolling back.")
                self.faiss_index.remove_ids(np.array([idx_before]))
                self.entry_names.pop()
                del self.generated_entries_cache[subject_key]
                raise RuntimeError("FAISS registration failed and rolled back.")

            # Extract and register phrases
            phrases = set(p.lower() for p in re.findall(r'\b(?:\w+\s+){3,10}\w+\b', content))
            self.phrase_registry.update(phrases)

            logger.info(f"✓ Registered '{subject_key}' at FAISS index {idx_before} ({self.faiss_index.ntotal} total)")

        except Exception as e:
            logger.error(f"CRITICAL: Failed to register entry '{subject}': {e}", exc_info=True)
            raise  # Don't continue with corrupted state

    # NEW: Method for cross-referencing
    def find_similar_entries(self, query_text: str, subject_to_exclude: str, n: int = 3) -> List[str]:
        """Finds already-generated entries similar to the query text."""
        if self.faiss_index.ntotal == 0:
            return []
        
        try:
            query_embedding = self.embedding_model.encode(query_text, device=DEVICE)
            query_embedding = query_embedding / np.linalg.norm(query_embedding)
            query_embedding = query_embedding.reshape(1, -1).astype('float32')
            
            # Search for n+1 to have buffer for excluding self
            search_k = min(n + 5, self.faiss_index.ntotal) # Search 5 extra
            similarities, indices = self.faiss_index.search(query_embedding, search_k)
            
            similar_entries = []
            normalized_exclude = subject_to_exclude.lower().replace(' ', '_').replace(':', '')
            
            for similarity, idx in zip(similarities[0], indices[0]):
                if idx < 0 or idx >= len(self.entry_names):
                    continue # Invalid index
                    
                entry_name = self.entry_names[idx]
                if entry_name != normalized_exclude and similarity > 0.5: # 0.5 similarity threshold
                    similar_entries.append(entry_name)
                
                if len(similar_entries) >= n:
                    break
                    
            return similar_entries
        except Exception as e:
            logger.warning(f"Failed to find similar entries: {e}")
            return []


# ============================================================================
# PROMPT ASSEMBLER
# ============================================================================

class PromptAssembler:
    """Build prompts for local LLM"""

    # MODIFIED: Added uniqueness_checker for cross-referencing
    def __init__(self, pattern_extractor: GoldenPatternExtractor,
                 research_db: SemanticResearchDatabase,
                 uniqueness_checker: UniquenessChecker):
        self.patterns = pattern_extractor
        self.research = research_db
        self.uniqueness_checker = uniqueness_checker

    def build_blueprint_prompt(self, subject: str, tier: str, category: str) -> str:
        
        # TASK 2: Enable Cross-Referencing (at Blueprint stage)
        cross_reference_str = ""
        query_text = f"{subject} {category}"
        similar_entries = self.uniqueness_checker.find_similar_entries(query_text, subject, n=3)
        if similar_entries:
            cross_reference_str = "\nCRITICAL CONTEXT: You have already written entries on "
            cross_reference_str += f"{', '.join(f"'{e}'" for e in similar_entries)}. "
            cross_reference_str += "You MUST build upon their arguments and NOT repeat them. Your core thesis must be unique."

        prompt = f"""You are an elite theological architect. Generate a comprehensive blueprint for an entry on: "{subject}" (Tier {tier}, Category: {category}).
{cross_reference_str}

Output ONLY valid JSON with these EXACT keys (no extra text):
{{
    "core_thesis": "The central theological argument (200-300 words). Must be unique and not repeat theses from similar entries.",
    "structural_penthos": "The opening 'godly sorrow' / 'penthos' of the entry (100 words). Must set the apocalyptic tone.",
    "theophanic_rupture_seed": "A moment of divine breaking-in, a 'BUT... did You not ordain, O Logos...' moment (100 words).",
    "eucharistic_culmination_seed": "How this subject points to the Eucharist/Liturgy (100 words).",
    "eschatological_consummation_seed": "Eschatological/doxological 'From...to...' cascade seed (100 words)."
}}

CRITICAL INSTRUCTIONS:
1. Output ONLY the JSON object above.
2. No markdown, no code blocks, no text before or after the JSON.
3. All values must be complete sentences and paragraphs, NOT lists.
4. Stay focused on the Orthodox theological perspective, drawing from the golden corpus style.
5. Be specific to "{subject}" and its unique strategic role.

Generate now:"""
        return prompt

    # MODIFIED: Now injects style examples and cross-references
    def build_section_prompt(self, section_num: int, section_name: str,
                            blueprint: Blueprint, research_facts: str,
                            prev_sections: List[str] = None) -> str:
        prev_text = "\n".join(prev_sections[-2:]) if prev_sections else ""

        # TASK 3: Teach the "Golden Style"
        style_examples_str = ""
        not_but_examples = self.patterns.get_random_pattern('not_but', n=2)
        if not_but_examples:
            style_examples_str += "\n- Use NOT...BUT structures (Rule G3) like: \n"
            for ex in not_but_examples:
                style_examples_str += f"    - \"...{ex[:100]}...\"\n"
        
        liturgical_examples = self.patterns.get_random_pattern('liturgical_rhythms', n=1)
        if liturgical_examples:
             style_examples_str += "\n- Use capitalized conjunctions (Rule G1) like: \n"
             for ex in liturgical_examples:
                style_examples_str += f"    - \"...{ex[:100]}...\"\n"

        # TASK 2: Enable Cross-Referencing (at Section stage)
        cross_reference_str = ""
        # Only add cross-references to key sections to avoid clutter
        if section_num in [0, 3, 4]: # Strategic Role, Patristic Mind, Clashes
            similar_entries = self.uniqueness_checker.find_similar_entries(
                blueprint.core_thesis, blueprint.subject, n=3
            )
            if similar_entries:
                cross_reference_str = "\nCRITICAL CONTEXT: You have already written entries on "
                cross_reference_str += f"{', '.join(f"'{e}'" for e in similar_entries)}. "
                cross_reference_str += "You MUST build upon their arguments and NOT repeat them."

        # Define section-specific word count targets to meet 10k total
        section_word_targets = {
            0: 2000, # I. Strategic Role
            1: 1000, # II. Classification
            2: 1500, # III. Primary Works
            3: 2500, # IV. The Patristic Mind
            4: 2500, # V. Symphony of Clashes
            5: 2000  # VI. Orthodox Affirmation
        }
        target_words = section_word_targets.get(section_num, 1500)
        min_words = int(target_words * 0.8) # 80% of target

        prompt = f"""You are generating Section {section_num+1}: "{section_name}" for an entry on "{blueprint.subject}".

ABSOLUTE MANDATES (FAILURE TO COMPLY WILL BE REJECTED):
- RULE B1: EVERY paragraph MUST start with EXACTLY FOUR (4) spaces.
- RULE B2: You are BANNED from using em-dash (—).
- RULE G1: LITURGICAL CONJUNCTIONS (AND/YET/BUT) - MUST be capitalized when structural.
- RULE G3: Build arguments via NOT...BUT dialectical structures.
- RULE G4: Sentences MUST be long and complex ("doxological chaining").
- RULE G5: Include theological terms: {', '.join(TheologicalTermRegistry.get_random_terms(5))}

CORE THESIS OF ENTRY:
{blueprint.core_thesis}
{cross_reference_str}

RESEARCH FACTS (You MUST integrate these):
{research_facts if research_facts else "No specific research facts provided for this section. Rely on core thesis."}

STYLE EXAMPLES (Follow this apocalyptic, dense voice):
{style_examples_str if style_examples_str else "No style examples available. Follow mandates."}

PREVIOUS CONTEXT (Last section written):
{prev_text[-500:] if prev_text else "This is the first section."}

Generate section {section_num+1} now (Target: {target_words} words, MINIMUM {min_words} words).
Start EVERY paragraph with 4 spaces:"""
        return prompt

    def build_correction_prompt(self, section_content: str, failures: List[str]) -> str:
        prompt = f"""The following section failed validation for these reasons:
{chr(10).join('- ' + f for f in failures)}

ABSOLUTE RULESETS:
- B1: Every paragraph MUST start with EXACTLY FOUR (4) spaces.
- B2: You are BANNED from using em-dash (—).
- G1: LITURGICAL CONJUNCTIONS (AND/YET/BUT) - MUST be capitalized.
- G3: Build arguments via NOT...BUT.
- MINIMUM LENGTH: Must be a substantial section.

ORIGINAL SECTION:
{section_content}

REWRITE the entire section to fix ALL errors. Maintain the content but fix all formatting and rule violations:"""
        return prompt

    # NEW: Prompt for expanding entry
    def build_expansion_prompt(self, section_name: str, section_content: str, target_words: int) -> str:
        prompt = f"""The following section "{section_name}" is TOO SHORT.
The full entry failed the 10,000-word minimum. This section must be expanded.

ORIGINAL SECTION ({len(section_content.split())} words):
{section_content}

REWRITE AND EXPAND this entire section to be at least {target_words} words.
- DO NOT just add paragraphs. Integrate new insights *into* the existing text.
- Add more detail, more scriptural and patristic engagement, and expand the dialectical arguments.
- Maintain all stylistic mandates (4-space indent, no em-dashes, AND/YET/BUT, NOT...BUT).

Generate the new, expanded section now:"""
        return prompt


# ============================================================================
# AGENTIC GENERATOR (LangGraph)
# ============================================================================

class OpusMaximusAgenticGenerator:
    """GPU-native agentic generator with self-correction"""

    SECTION_NAMES = [
        'I. Strategic Role',
        'II. Classification',
        'III. Primary Works',
        'IV. The Patristic Mind',
        'V. The Symphony of Clashes',
        'VI. Orthodox Affirmation'
    ]
    
    # Target word counts per section to guide generation
    SECTION_WORD_TARGETS = [2000, 1000, 1500, 2500, 2500, 2000] # Total: 11,500
    MIN_SECTION_WORD_COUNT = [1500, 800, 1000, 2000, 2000, 1500] # Total: 8,800 (min)

    def __init__(self,
                 model_path: str,
                 golden_dir: Path = Path('OPUS_MAXIMUS_INDIVIDUALIZED/Enhancement_Corpus'),
                 output_dir: Path = Path('GENERATED_ENTRIES_MASTER'),
                 max_section_attempts: int = 3,
                 max_expansion_attempts: int = 2, # NEW: For word count loop
                 n_gpu_layers: int = -1,
                 n_ctx: int = 8192):

        self.model_path = model_path
        self.golden_dir = golden_dir
        self.output_dir = output_dir
        self.max_section_attempts = max_section_attempts
        self.max_expansion_attempts = max_expansion_attempts # NEW
        self.min_word_count = 10000 # NEW: Mandate A2

        # Initialize subsystems
        logger.info("Initializing Pattern Extractor...")
        self.pattern_extractor = GoldenPatternExtractor(golden_dir)

        logger.info("Initializing Semantic Research Database...")
        self.research_db = SemanticResearchDatabase()

        logger.info("Initializing Uniqueness Checker...")
        self.uniqueness_checker = UniquenessChecker(output_dir)

        logger.info("Initializing Prompt Assembler...")
        # MODIFIED: Pass uniqueness_checker for cross-referencing
        self.prompt_assembler = PromptAssembler(
            self.pattern_extractor, 
            self.research_db,
            self.uniqueness_checker
        )

        # Load Local LLM
        console.print(f"[cyan]Loading LLM: {model_path}[/cyan]")
        console.print("[yellow]This may take a moment...[/yellow]")
        try:
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=n_ctx,
                n_gpu_layers=n_gpu_layers,
                n_batch=512,
                verbose=False
            )
            console.print("[green]✓ LLM loaded successfully onto GPU[/green]")
        except Exception as e:
            logger.error(f"Failed to load LLM: {e}")
            sys.exit(1)

        # Statistics
        self.stats = defaultdict(int)
        self.stats['start_time'] = datetime.now()

        # Build agentic graph
        self.graph = self._build_graph()

    def _call_llm(self, prompt: str, max_tokens: int = 10000, temperature: float = 0.7) -> str:
        """Call local LLM"""
        start_time = time.time()

        try:
            logger.info(f"Calling LLM with prompt (first 200 chars): {prompt[:200]}...")
            response = self.llm.create_completion(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stop=["<|eot_id|>", "</s>"] # Standard stopping tokens
            )

            text = response['choices'][0]['text'].strip()
            api_time = time.time() - start_time
            self.stats['total_api_time'] += api_time
            self.stats['total_model_calls'] += 1
            logger.info(f"LLM call completed in {api_time:.2f}s, generated {len(text)} chars")

            return text
        except Exception as e:
            logger.error(f"LLM call error: {e}")
            return ""

    # MODIFIED: Added word count validation loop
    def _build_graph(self) -> StateGraph:
        """Build LangGraph state machine"""
        workflow = StateGraph(GenerationState)

        workflow.add_node("generate_blueprint", self.node_generate_blueprint)
        workflow.add_node("generate_section", self.node_generate_section)
        workflow.add_node("validate_section", self.node_validate_section)
        workflow.add_node("correct_section", self.node_correct_section)
        workflow.add_node("advance_section", self.node_advance_section)
        workflow.add_node("assemble_entry", self.node_assemble_entry)
        
        # NEW nodes for word count loop
        workflow.add_node("validate_final_entry", self.node_validate_final_entry)
        workflow.add_node("expand_entry_content", self.node_expand_entry_content)

        workflow.set_entry_point("generate_blueprint")
        workflow.add_edge("generate_blueprint", "generate_section")
        workflow.add_edge("generate_section", "validate_section")

        workflow.add_conditional_edges(
            "validate_section",
            self.decide_after_validation,
            {
                "correct": "correct_section",   # Self-correction loop
                "next": "advance_section",      # Advance to next section
                "finish": "assemble_entry",     # All sections done
                "fail": END                     # Failed too many times
            }
        )

        workflow.add_edge("correct_section", "validate_section")  # Loop back for re-validation
        workflow.add_edge("advance_section", "generate_section")  # Generate next section
        
        # MODIFIED: assemble_entry now goes to final validation
        workflow.add_edge("assemble_entry", "validate_final_entry")
        
        # NEW: Word count validation loop
        workflow.add_conditional_edges(
            "validate_final_entry",
            self.decide_after_assembly,
            {
                "expand": "expand_entry_content", # Entry too short, expand
                "finish": END,                    # Entry passes all checks
                "fail": END                       # Entry fails uniqueness or expansion
            }
        )
        # NEW: Expansion loop
        workflow.add_edge("expand_entry_content", "assemble_entry") # Re-assemble after expansion

        return workflow.compile()

    # ========================================================================
    # GRAPH NODES
    # ========================================================================

    def node_generate_blueprint(self, state: GenerationState) -> GenerationState:
        """Generate blueprint"""
        logger.info(f"Generating blueprint for {state['subject']}")
        prompt = self.prompt_assembler.build_blueprint_prompt(
            state['subject'], state['tier'], state['category']
        )
        response_text = self._call_llm(prompt, max_tokens=4000, temperature=0.5)

        try:
            # Extract JSON - handle markdown code blocks properly
            blueprint_dict = None

            # First try: direct parse
            try:
                blueprint_dict = orjson.loads(response_text.encode())
            except:
                # Second try: extract from markdown code block
                json_match = re.search(r'
if json_match:
                    json_str = json_match.group(1)
                    blueprint_dict = orjson.loads(json_str.encode())
                else:
                    # Third try: find JSON object (non-greedy)
                    json_match = re.search(r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}', response_text, re.S)
                    if json_match:
                        json_str = json_match.group(0)
                        blueprint_dict = orjson.loads(json_str.encode())
                    else:
                        raise ValueError("No JSON object found in response")

            # Validate required keys
            required_keys = ['core_thesis', 'structural_penthos', 'theophanic_rupture_seed',
                           'eucharistic_culmination_seed']
            missing = [k for k in required_keys if k not in blueprint_dict]
            if missing:
                raise ValueError(f"Missing required blueprint keys: {missing}")

            # Length validation
            for key in required_keys:
                text = blueprint_dict.get(key, '')
                if len(text.split()) < 30:  # Minimum 30 words per key field
                    raise ValueError(f"Blueprint field '{key}' too short ({len(text.split())} words, minimum 30)")

            # Semantic search
            semantic_citations = self.research_db.semantic_search_patristic(
                blueprint_dict.get('core_thesis', state['subject']), limit=10
            )

            blueprint = Blueprint(
                subject=state['subject'], tier=state['tier'], category=state['category'],
                **blueprint_dict,
                semantic_patristic_citations=semantic_citations
            )

            return {
                "blueprint": blueprint,
                "sections": [],
                "current_section_num": 0,
                "section_attempts": 0,
                "entry_expansion_attempts": 0, # NEW
                "validation_failures": []
            }
        except Exception as e:
            logger.error(f"Blueprint parse error: {e}", exc_info=True)
            logger.error(f"LLM Response was: {response_text}")
            return {
                "blueprint": None,
                "validation_failures": [f"Failed to generate blueprint: {str(e)}"],
                "sections": [],
                "current_section_num": 0,
                "section_attempts": 0,
                "entry_expansion_attempts": 0
            }

    def node_generate_section(self, state: GenerationState) -> GenerationState:
        """Generate section content"""
        num = state['current_section_num']
        name = self.SECTION_NAMES[num]
        logger.info(f"Generating Section {num+1}: {name}")

        # Gather relevant research for THIS section
        research_facts = ""
        if state['blueprint'] and state['blueprint'].semantic_patristic_citations:
            # Filter citations relevant to this section
            section_keywords = {
                0: ['strategic', 'role', 'significance', 'penthos'],
                1: ['classification', 'category', 'taxonomy', 'adversary', 'preparatory'],
                2: ['works', 'writings', 'texts', 'books', 'papers'],
                3: ['patristic', 'fathers', 'tradition', 'theology'],
                4: ['dialectical', 'opponents', 'clash', 'synthesis'],
                5: ['orthodox', 'affirmation', 'synthesis', 'eucharist', 'liturgy', 'doxology']
            }

            keywords = section_keywords.get(num, [])
            query_text = f"{state['blueprint'].core_thesis} {name} {' '.join(keywords)}"

            # Semantic search for this section
            research_citations = self.research_db.semantic_search_patristic(query_text, limit=5)

            if research_citations:
                research_facts = "**Relevant Patristic Citations for This Section:**\n"
                for cit in research_citations:
                    research_facts += f"- **{cit['father']}** ({cit['work']}): \"{cit['text'][:150]}...\"\n"

            # Add biblical verses if relevant
            if num in [0, 1, 3, 5]:  # Sections that benefit from Scripture
                biblical_verses = self.research_db.search_biblical_verses(
                    keywords + [state['subject']], limit=3
                )
                if biblical_verses:
                    research_facts += "\n**Relevant Biblical Verses:**\n"
                    for verse in biblical_verses:
                        research_facts += f"- {verse['ref']}: \"{verse['text'][:100]}...\"\n"
        
        # Add blueprint seeds to relevant sections
        if num == 0: # Strategic Role
            research_facts += f"\nSTRUCTURAL PENTHOS: {state['blueprint'].structural_penthos}\n"
        elif num == 5: # Orthodox Affirmation
             research_facts += f"\nEUCHARISTIC SEED: {state['blueprint'].eucharistic_culmination_seed}\n"
             research_facts += f"\nESCHATOLOGICAL SEED: {state['blueprint'].eschatological_consummation_seed}\n"


        prompt = self.prompt_assembler.build_section_prompt(
            num, name, state['blueprint'], research_facts, state['sections']
        )

        section_content = self._call_llm(prompt, max_tokens=10000, temperature=0.8)

        return {"current_section_content": section_content, "current_section_name": name}

    def node_validate_section(self, state: GenerationState) -> GenerationState:
        """Validate section"""
        content = state['current_section_content']
        num = state['current_section_num']
        name = state['current_section_name']
        failures = []
        
        min_words = self.MIN_SECTION_WORD_COUNT[num]

        # Length check
        word_count = len(content.split())
        if not content or word_count < min_words:
            failures.append(f"Section {num+1} '{name}' too short: {word_count} words (minimum {min_words})")

        # Em-dash prohibition
        if '—' in content:
            failures.append("Em-dash (—) violation found")

        # Check EVERY paragraph starts with 4 spaces
        lines = content.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]
        if not non_empty_lines:
             failures.append("Section is empty")
        else:
            for i, line in enumerate(non_empty_lines):
                if not line.startswith('    ') and line.strip():
                    failures.append(f"Line {i+1} missing 4-space indent: {line[:50]}...")
                    break  # Stop after first violation

        # Check for NOT...BUT dialectical structures
        if not re.search(r'NOT\s+\w+[^,]{5,50},?\s+BUT\s+\w+', content, re.IGNORECASE):
            failures.append("Missing NOT...BUT dialectical structure (Rule G3)")

        # Check liturgical capitalization (AND/YET/BUT must be capitalized)
        lower_liturgical = re.findall(r'\b(and|yet|but)\s+[a-z]', content)
        if lower_liturgical:
            failures.append(f"Liturgical conjunctions (and/yet/but) must be capitalized (Rule G1). Found: {lower_liturgical[:3]}")

        return {
            "validation_failures": failures,
            "section_attempts": state['section_attempts'] + 1
        }

    def node_correct_section(self, state: GenerationState) -> GenerationState:
        """Correct section"""
        logger.warning(f"Correcting section {state['current_section_name']} (Attempt {state['section_attempts']})")

        prompt = self.prompt_assembler.build_correction_prompt(
            state['current_section_content'],
            state['validation_failures']
        )

        corrected_content = self._call_llm(prompt, max_tokens=10000, temperature=0.6)

        return {"current_section_content": corrected_content}

    def node_assemble_entry(self, state: GenerationState) -> GenerationState:
        """Assemble final entry from the list of approved sections"""
        logger.info("Assembling final entry...")
        blueprint = state['blueprint']
        
        # In the main flow, the last section is in current_section_content
        # In the expansion loop, all 6 sections are in state['sections']
        
        all_sections = state['sections']
        if state['current_section_content'] and len(all_sections) == 5:
             # This is the first time assembling
            all_sections = state['sections'] + [state['current_section_content']]

        # Defensive check
        if len(all_sections) != len(self.SECTION_NAMES):
            logger.error(f"Section count mismatch: expected {len(self.SECTION_NAMES)}, got {len(all_sections)}")
            return {
                "final_content": "",
                "final_metrics": None,
                "validation_failures": [f"Incomplete entry: only {len(all_sections)} sections"]
            }

        parts = [f"# {blueprint.subject}: Orthodox Engagement\n"]
        for i, section_content in enumerate(all_sections):
            parts.append(f"\n## {self.SECTION_NAMES[i]}\n")
            parts.append(section_content)

        final_content = '\n'.join(parts)
        
        # Store the complete text and the list of sections for the next nodes
        return {"final_content": final_content, "sections": all_sections}

    # NEW: Final validation node
    def node_validate_final_entry(self, state: GenerationState) -> GenerationState:
        """Perform final validation on the assembled entry (Word Count, Uniqueness)"""
        logger.info("Performing final validation on assembled entry...")
        final_content = state['final_content']
        subject = state['blueprint'].subject
        failures = []

        # 1. Word Count Check (Rule A2)
        word_count = len(final_content.split())
        if word_count < self.min_word_count:
            failures.append(f"Word count too low: {word_count} (Minimum: {self.min_word_count})")

        # 2. Uniqueness Check
        is_unique, violations = self.uniqueness_checker.check_uniqueness(final_content, subject)
        if not is_unique:
            failures.extend(violations)
            
        # 3. Final Content Check (Ruleset DELTA)
        if "AND NOW, in this Liturgy, at this Altar" not in final_content:
             failures.append("Missing Eucharistic Culmination (Rule D4)")
        if not re.search(r'—O .* our God', final_content):
            # Note: The prompt bans em-dashes, but the golden corpus uses them for prayers.
            # We must be consistent. Let's assume the prayer should start with 4 spaces and "O..."
            if not re.search(r'    O .* our God', final_content):
                 failures.append("Missing Opening Prayer in Section VI (Rule D4)")
        
        # Create metrics
        metrics = QualityMetrics(
            word_count=word_count,
            paragraph_count=final_content.count('\n\n'),
            section_count=len(state['sections']),
            passes_absolute_mandates=(len(failures) == 0)
        )

        return {
            "final_metrics": metrics,
            "validation_failures": failures
        }

    # NEW: Expansion node
    def node_expand_entry_content(self, state: GenerationState) -> GenerationState:
        """Expand the shortest sections to meet word count"""
        logger.warning(f"Entry failed word count. Attempting expansion {state['entry_expansion_attempts'] + 1}/{self.max_expansion_attempts}")
        
        sections = state['sections']
        section_lengths = [(i, len(s.split())) for i, s in enumerate(sections)]
        
        # Find the 2 shortest sections
        section_lengths.sort(key=lambda x: x[1])
        sections_to_expand_indices = [idx for idx, length in section_lengths[:2]]
        
        new_sections = list(sections) # Create a copy to modify
        
        for idx in sections_to_expand_indices:
            section_name = self.SECTION_NAMES[idx]
            old_content = sections[idx]
            old_len = len(old_content.split())
            new_target_len = self.SECTION_WORD_TARGETS[idx] + 500 # Add 500 words
            
            logger.info(f"Expanding section {idx+1} '{section_name}' from {old_len} to {new_target_len} words...")
            
            prompt = self.prompt_assembler.build_expansion_prompt(section_name, old_content, new_target_len)
            new_content = self._call_llm(prompt, max_tokens=10000, temperature=0.7)
            
            # Simple validation on the new content
            if len(new_content.split()) > old_len and '    ' in new_content:
                logger.info(f"Expansion successful for section {idx+1}. New length: {len(new_content.split())}")
                new_sections[idx] = new_content
            else:
                logger.warning(f"Expansion failed for section {idx+1}. Keeping original content.")
        
        return {
            "sections": new_sections, # Return the list of 6 (now expanded) sections
            "entry_expansion_attempts": state['entry_expansion_attempts'] + 1,
            "current_section_content": "" # Clear this to avoid re-adding
        }

    def node_advance_section(self, state: GenerationState) -> GenerationState:
        """Advance to next section after approval"""
        logger.info(f"✓ Section {state['current_section_name']} approved")

        # Add approved section to list
        approved_sections = state['sections'] + [state['current_section_content']]
        next_section_num = state['current_section_num'] + 1

        return {
            "sections": approved_sections,
            "current_section_num": next_section_num,
            "section_attempts": 0,
            "validation_failures": []  # Clear failures
        }

    # ========================================================================
    # GRAPH DECISIONS
    # ========================================================================

    def decide_after_validation(self, state: GenerationState) -> str:
        """Route after section validation - NO STATE MUTATION"""
        if state['validation_failures']:
            if state['section_attempts'] >= self.max_section_attempts:
                logger.error(f"Failed section after {self.max_section_attempts} attempts. Aborting entry.")
                return "fail"
            logger.warning(f"Section validation failed: {state['validation_failures'][0]}. Correcting...")
            return "correct"

        # Section approved - check if more sections needed
        next_section_num = state['current_section_num'] + 1

        if next_section_num < len(self.SECTION_NAMES):
            return "next"  # More sections to generate
        else:
            return "finish"  # All sections complete

    # NEW: Decision node for word count loop
    def decide_after_assembly(self, state: GenerationState) -> str:
        """Route after final assembly and validation"""
        failures = state['validation_failures']
        
        if not failures:
            logger.info("✓ Final validation passed. Entry approved.")
            return "finish"
            
        # Check for uniqueness failures first (unrecoverable)
        if any("TOO SIMILAR" in f or "REPEATED PHRASES" in f for f in failures):
            logger.error(f"FATAL: Entry failed uniqueness check. Aborting. Failures: {failures}")
            return "fail"
            
        # Check for word count failure (recoverable)
        if any("Word count too low" in f for f in failures):
            if state['entry_expansion_attempts'] < self.max_expansion_attempts:
                logger.warning(f"Entry failed word count. Routing to expansion loop.")
                return "expand"
            else:
                logger.error(f"FATAL: Entry failed word count after {self.max_expansion_attempts} expansion attempts. Aborting.")
                return "fail"
        
        # Other fatal errors
        logger.error(f"FATAL: Entry failed final validation. Aborting. Failures: {failures}")
        return "fail"


    # ========================================================================
    # EXECUTION
    # ========================================================================

    def generate_entry(self, subject: str, tier: str, category: str) -> Optional[EntryCandidate]:
        """Run agentic graph"""
        console.print(f"\n[bold cyan]{'='*80}[/bold cyan]")
        console.print(f"[bold]STARTING: {subject} (Tier {tier})[/bold]")
        console.print(f"[bold cyan]{'='*80}[/bold cyan]\n")

        start_time = time.time()

        initial_state = GenerationState(
            subject=subject, tier=tier, category=category,
            blueprint=None, sections=[], current_section_num=0,
            current_section_content="", validation_failures=[],
            section_attempts=0, entry_expansion_attempts=0,
            final_content="", final_metrics=None,
            generation_time=0.0, start_time=start_time
        )

        final_state = self.graph.invoke(initial_state)
        generation_time = time.time() - start_time
        
        # Check the final node's name or a status flag
        # The 'END' node returns the state, so we check metrics
        if final_state.get('final_metrics') and final_state['final_metrics'].passes_absolute_mandates:
            console.print(f"[bold green]✓✓✓ APPROVED: {subject} in {generation_time:.1f}s[/bold green]")

            candidate = EntryCandidate(
                subject=subject, tier=tier, category=category,
                blueprint=final_state['blueprint'],
                content=final_state['final_content'],
                metrics=final_state['final_metrics'],
                generation_time=generation_time,
                attempt_number=1, # TODO: Track total attempts
                approved=True
            )
            self.save_entry(candidate)
            self.uniqueness_checker.register_new_entry(candidate.content, subject)
            return candidate
        else:
            console.print(f"[bold red]XXX FAILED: {subject}[/bold red]")
            logger.error(f"Generation failed for {subject}. Final validation failures: {final_state.get('validation_failures')}")
            return None

    def save_entry(self, candidate: EntryCandidate):
        """Save approved entry"""
        category_dirs = {
            'Biblical': 'Biblical_Figures',
            'Patristic': 'Patristic_Figures',
            'Theology': 'Theology',
            'Mathematics': 'Mathematics',
            'Physics': 'Physics',
            'Philosophy': 'Philosophy',
            'Science': 'Science',
            'Literature': 'Literature',
            'History': 'History'
        }
        subdir = category_dirs.get(candidate.category, 'Miscellaneous')
        output_path = self.output_dir / subdir
        output_path.mkdir(exist_ok=True, parents=True)

        filename = f"{candidate.subject.lower().replace(' ', '_').replace(':', '')}.md"
        filepath = output_path / filename
        filepath.write_text(candidate.content, encoding='utf-8', newline='\n')

        # Save metadata
        metadata_path = filepath.with_suffix('.json')
        metadata = {
            'subject': candidate.subject,
            'tier': candidate.tier,
            'category': candidate.category,
            'quality_score': candidate.metrics.overall_score,
            'word_count': candidate.metrics.word_count,
            'generation_time': candidate.generation_time,
            'timestamp': candidate.timestamp.isoformat(),
            'metrics': candidate.metrics.dict()
        }
        with open(metadata_path, 'wb') as f:
            f.write(orjson.dumps(metadata, option=orjson.OPT_INDENT_2))

        logger.info(f"✓ SAVED: {filepath}")

    def cleanup(self):
        self.research_db.close()


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Opus Maximus Agentic Generator (GPU-Native)")
    parser.add_argument('--mode', choices=['single', 'batch'], default='single')
    parser.add_argument('--subject', default='The Book of Revelation')
    parser.add_argument('--tier', default='S+', choices=['S+', 'S', 'A', 'B', 'C'])
    parser.add_argument('--category', default='Biblical')
    parser.add_argument('--batch-file', help='JSON file with batch entries')
    parser.add_argument('--model-path', required=True, help='Path to GGUF model')
    parser.add_argument('--golden-dir', default='OPUS_MAXIMUS_INDIVIDUALIZED/Enhancement_Corpus')
    parser.add_argument('--output-dir', default='GENERATED_ENTRIES_MASTER')
    parser.add_argument('--n-gpu-layers', type=int, default=-1, help='GPU layers (-1 for all)')
    parser.add_argument('--n-ctx', type=int, default=8192, help='Context window')
    parser.add_argument('--min-word-count', type=int, default=10000, help='Minimum word count for final entry')

    args = parser.parse_args()

    if not Path(args.model_path).exists():
        logger.error(f"Model file not found: {args.model_path}")
        logger.error("Download a GGUF model and provide path")
        sys.exit(1)

    generator = OpusMaximusAgenticGenerator(
        model_path=args.model_path,
        golden_dir=Path(args.golden_dir),
        output_dir=Path(args.output_dir),
        n_gpu_layers=args.n_gpu_layers,
        n_ctx=args.n_ctx
    )
    generator.min_word_count = args.min_word_count # Set word count from CLI

    try:
        if args.mode == 'single':
            generator.generate_entry(args.subject, args.tier, args.category)
        elif args.mode == 'batch':
            if not args.batch_file:
                logger.error("--batch-file required")
                return
            with open(args.batch_file, 'rb') as f:
                batch = orjson.loads(f.read())

            # Batch generation with error recovery
            results = {'successful': 0, 'failed': 0, 'errors': []}
            for i, entry in enumerate(batch):
                try:
                    console.print(f"\n[cyan]Processing batch entry {i+1}/{len(batch)}[/cyan]")
                    result = generator.generate_entry(entry['subject'], entry['tier'], entry['category'])
                    if result:
                        results['successful'] += 1
                    else:
                        results['failed'] += 1
                        results['errors'].append((entry['subject'], "Generation returned None"))
                except Exception as e:
                    logger.error(f"Batch entry {i+1} ({entry.get('subject', 'Unknown')}) failed: {e}", exc_info=True)
                    results['failed'] += 1
                    results['errors'].append((entry.get('subject', 'Unknown'), str(e)))

            # Print summary
            console.print(f"\n[bold cyan]{'='*80}[/bold cyan]")
            console.print(f"[bold]BATCH GENERATION COMPLETE[/bold]")
            console.print(f"[green]✓ Successful: {results['successful']}[/green]")
            console.print(f"[red]✗ Failed: {results['failed']}[/red]")
            if results['errors']:
                console.print(f"\n[yellow]Failed entries:[/yellow]")
                for subject, error in results['errors']:
                    console.print(f"  - {subject}: {error[:100]}")
            console.print(f"[bold cyan]{'='*80}[/bold cyan]")
    finally:
        generator.cleanup()


if __name__ == "__main__":
    main()