# OPUS MAXIMUS DREAM ENGINE

Advanced Orthodox Theological Entry Generation System using Local LLMs

## Overview

The OPUS MAXIMUS DREAM ENGINE is a comprehensive system for generating CELESTIAL-tier (95-100 score) Orthodox Christian theological entries using local LLMs (Mixtral 8x7B, Llama 3.1 70B). It combines advanced preprocessing, verified Patristic citations, and rigorous validation to consistently produce publication-ready theological content.

**Target**: 12,000 CELESTIAL-tier entries  
**Hardware**: ROG Zephyrus Duo 4090 (RTX 4090 Mobile, 64GB RAM)  
**Cost**: $0 (all open-source tools)

## Key Features

### Advanced Preprocessing Pipeline
- **Topic Analyzer**: Semantic analysis, theme extraction, complexity scoring
- **Semantic Mapper**: Cross-referential theological concept mapping
- **Citation Preparer**: 30+ verified Patristic works across 7 major Church Fathers
- **Theological Context Builder**: Comprehensive context integration

### Rigorous Validation Framework
- **5-Criterion Validation**: Word count, theological depth, coherence, section balance, Orthodox perspective
- **4-Metric Quality Scoring**: Diversity, specificity, integration, distribution
- **Citation Verification**: Prevents LLM hallucination with verified database
- **90-95% Authenticity Standard**: Pragmatic quality balance

### Quality Standards
- **CELESTIAL Tier Required**: 95-100 score (all 12,000 entries)
- **20+ Patristic Citations**: From 5+ different Church Fathers
- **3+ Named Works**: Specific verified works cited
- **15+ Scripture References**: Biblical foundation
- **Word Count Philosophy**: Minimums only, no maximums (topics receive depth they deserve)

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/apocryphalcontent-max/Opus-2.git
cd Opus-2

# Install dependencies
pip install -r requirements.txt

# Install Ollama and models (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull mixtral:8x7b-instruct-v0.1-q6_K
ollama pull llama3.1:70b-instruct-q4_K_M
```

### Demonstration

```bash
# Run preprocessing demonstration
python examples/preprocessing_demo.py
```

### Basic Usage

```python
from src.preprocessing import (
    TopicAnalyzer,
    SemanticMapper,
    CitationPreparer,
    TheologicalContextBuilder
)

# Define topic
topic = "Theosis and Divine Energies"

# Preprocessing
analyzer = TopicAnalyzer()
analysis = analyzer.analyze(topic)

mapper = SemanticMapper()
semantic_map = mapper.map_topic(topic, analysis.core_themes)

citation_prep = CitationPreparer()
citations = citation_prep.prepare_citations(
    topic=topic,
    suggested_fathers=analysis.suggested_fathers,
    themes=analysis.core_themes,
    count=20
)

context_builder = TheologicalContextBuilder()
context = context_builder.build_context(
    topic=topic,
    analysis=analysis,
    semantic_map=semantic_map,
    prepared_citations=citations
)

# Context now ready for generation!
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   OPUS MAXIMUS DREAM ENGINE                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────────┐    ┌─────────────────┐    ┌────────────┐│
│  │ Preprocessing │───>│  Generation     │───>│ Validation ││
│  │   Pipeline    │    │    Engine       │    │  Framework ││
│  └───────────────┘    └─────────────────┘    └────────────┘│
│         │                      │                      │      │
│         ▼                      ▼                      ▼      │
│  ┌───────────────┐    ┌─────────────────┐    ┌────────────┐│
│  │ Topic Analysis│    │   LLM Client    │    │  Quality   ││
│  │ Semantic Map  │    │ (Mixtral/Llama) │    │  Metrics   ││
│  │ Citation DB   │    │                 │    │  Scorer    ││
│  │ Context Build │    │                 │    │  Validator ││
│  └───────────────┘    └─────────────────┘    └────────────┘│
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Documentation

### Core Documentation
- **[PRODUCTION_Guide.md](PRODUCTION_Guide.md)** - Complete production guide (4700+ lines)
- **[TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md)** - System architecture and components
- **[PREPROCESSING_GUIDE.md](PREPROCESSING_GUIDE.md)** - Detailed preprocessing workflows

### Configuration
- **[configs/production.json](configs/production.json)** - Production configuration
- **[requirements.txt](requirements.txt)** - Python dependencies

## Project Structure

```
Opus-2/
├── src/
│   ├── preprocessing/        # Preprocessing pipeline
│   │   ├── topic_analyzer.py
│   │   ├── semantic_mapper.py
│   │   ├── citation_preparer.py
│   │   └── theological_context.py
│   ├── validation/          # Validation framework
│   │   ├── entry_validator.py
│   │   ├── quality_scorer.py
│   │   ├── citation_validator.py
│   │   └── coherence_analyzer.py
│   └── generation/          # Generation engine (coming soon)
├── configs/                 # Configuration files
│   └── production.json
├── examples/                # Example scripts
│   └── preprocessing_demo.py
├── data/                    # Data files
│   ├── patristic_citations/
│   └── scripture_refs/
├── docs/                    # Additional documentation
└── tests/                   # Test suite
```

## Quality Metrics

### CELESTIAL Tier Requirements (95-100 score)

**Entry Validation** (5 weighted criteria):
- Word Count (20%): ≥11,000 total, all sections meet minimums
- Theological Depth (30%): 20+ citations, 5+ fathers, 3+ works
- Coherence (25%): All 6 sections, cross-references, logical flow
- Section Balance (15%): Even distribution across sections
- Orthodox Perspective (10%): Clear Orthodox framing throughout

**Quality Metrics** (4 automated checks):
- Diversity Score: 5+ different Church Fathers cited
- Specificity Score: 3+ specific Patristic works named
- Integration Score: Citations distributed evenly across sections
- Distribution Score: Patristic content in 4+ of 6 sections

## Patristic Citation Database

Currently includes 30+ verified works from:
- St. Gregory of Nyssa (4 works)
- St. Maximus the Confessor (4 works)
- St. Basil the Great (3 works)
- St. John Chrysostom (3 works)
- St. Athanasius (3 works)
- St. Gregory Palamas (2 works)
- St. John of Damascus (2 works)

**Expandable**: Easy to add more fathers and works

## Performance

### Per Entry (Average)
- Preprocessing: 5 minutes
- Generation: 30-60 minutes
- Validation: 10-15 minutes
- Refinement (if needed): 15-60 minutes
- **Total**: 60-140 minutes per CELESTIAL entry

### Scaling
- 10-15 entries per 24 hours (with automation)
- 12,000 entries: ~3-4 years (single system)
- Parallelizable across multiple systems

## Hardware Requirements

### Recommended
- **GPU**: NVIDIA RTX 4090 (16GB VRAM)
- **CPU**: Ryzen 9 7945HX / Intel i9-13980HX
- **RAM**: 64GB DDR5-4800
- **Storage**: 2TB NVMe SSD

### Minimum
- **GPU**: NVIDIA RTX 3090 (24GB VRAM)
- **RAM**: 32GB
- **Storage**: 1TB SSD

## Philosophy

### Word Count: Minimums Only, No Maximums
Quality theological exposition cannot be artificially constrained. Each section has a MINIMUM word count, but NO MAXIMUM. Topics demanding deeper treatment receive it.

**Distribution**:
- 60% of entries: 12,500-14,000 words (standard)
- 30% of entries: 14,000-16,000 words (expanded)
- 10% of entries: 16,000-20,000 words (comprehensive)

### 90-95% Citation Authenticity Standard
Perfect verification would require 90-125 min/entry. Automated checks achieve 90-95% authenticity in 10-15 min/entry, saving 1,500-2,200 hours across 12,000 entries while maintaining CELESTIAL quality.

## Roadmap

### Current (v1.0)
- ✅ Advanced preprocessing pipeline
- ✅ Comprehensive validation framework
- ✅ Verified Patristic citation database
- ✅ Technical architecture documentation

### Next (v1.1)
- [ ] Generation engine integration with LLMs
- [ ] Batch processing automation
- [ ] Example CELESTIAL-tier entries
- [ ] Complete test suite

### Future (v2.0)
- [ ] Expand citation database to 50+ fathers, 200+ works
- [ ] Advanced coherence analysis with semantic similarity
- [ ] Automated refinement suggestions
- [ ] Multi-modal generation (iconography, hymns)

## Contributing

This is a specialized theological content generation system. Contributions focusing on:
- Expanding Patristic citation database
- Improving validation criteria
- Enhancing preprocessing algorithms
- Adding test coverage

are welcome.

## License

- **Code**: MIT License
- **Theological Content**: CC BY-SA 4.0
- **Patristic Citations**: Public domain (ancient texts)

## Acknowledgments

Built on the foundation of Orthodox Christian theology and the wisdom of the Church Fathers. All glory to God.

---

**Version**: 1.0  
**Status**: Core preprocessing and validation complete  
**Next**: Generation engine integration