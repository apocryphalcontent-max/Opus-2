# Advanced Preprocessing Guide

## Overview

The preprocessing pipeline is the foundation of CELESTIAL-tier entry generation. This guide details every component and how to use them effectively.

## Why Preprocessing Matters

**Without preprocessing**, the LLM generates based on limited context:
- May hallucinate Church Father names or works
- May miss relevant theological connections
- May produce generic content lacking depth
- Citation distribution often poor

**With preprocessing**, the LLM receives rich context:
- Verified Church Fathers and works to cite
- Theological concept map showing relationships
- Historical development narrative
- Contemporary relevance framing
- Section-specific guidance
- Result: CELESTIAL-tier output (95-100 score)

## The Four Preprocessing Components

### 1. Topic Analyzer

**Purpose**: Deep semantic analysis of the theological topic

**What it does**:
1. Extracts core theological themes
2. Identifies primary theological domain
3. Suggests relevant Church Fathers
4. Recommends Scripture passages
5. Calculates topic complexity
6. Determines required depth level

**Example Usage**:

```python
from src.preprocessing import TopicAnalyzer

analyzer = TopicAnalyzer()
analysis = analyzer.analyze("Theosis and Quantum Entanglement")

print(f"Core themes: {analysis.core_themes}")
# Output: ['Theosis and Soteriology', 'Cosmology and Creation']

print(f"Domain: {analysis.theological_domain}")
# Output: 'soteriological'

print(f"Suggested fathers: {analysis.suggested_fathers}")
# Output: ['St. Maximus the Confessor', 'St. Gregory of Nyssa', ...]

print(f"Complexity: {analysis.complexity_score}")
# Output: 0.75 (advanced topic)
```

**How Complexity is Calculated**:
```python
complexity = 0.5  # Base
complexity += len(themes) * 0.05  # More themes = more complex
complexity += interdisciplinary_markers * 0.1  # "and", "synthesis", etc.
complexity += abstract_terms * 0.1  # "infinity", "mystery", etc.
# Range: 0.0 - 1.0
```

**Depth Levels**:
- **Foundational** (0.0-0.49): Basic topics, standard treatment
- **Intermediate** (0.50-0.74): Moderate complexity, expanded treatment
- **Advanced** (0.75-1.0): High complexity, comprehensive treatment

### 2. Semantic Mapper

**Purpose**: Creates cross-referential theological concept maps

**What it does**:
1. Identifies central concept and related concepts
2. Maps relationships (foundation, development, contrast, synthesis)
3. Identifies doctrinal layers (foundational → applied)
4. Finds Western theological contrasts
5. Maps liturgical connections

**Example Usage**:

```python
from src.preprocessing import SemanticMapper

mapper = SemanticMapper()
semantic_map = mapper.map_topic(
    "Theosis and Quantum Entanglement",
    analysis.core_themes
)

print(f"Central concept: {semantic_map.central_concept}")
# Output: 'Theosis'

print(f"Related concepts: {semantic_map.related_concepts}")
# Output: ['Trinity', 'Incarnation', 'Divine Energies']

print(f"Doctrinal layers: {semantic_map.doctrinal_layers}")
# Output: {
#     'foundational': ['Trinity', 'Incarnation'],
#     'essential': ['Divine Energies'],
#     'developmental': ['Hesychasm'],
#     'applied': ['Divine Liturgy', 'Eucharist']
# }

print(f"Western contrasts: {semantic_map.western_contrasts}")
# Output: [('Justification (forensic)', 'Orthodox emphasizes transformation...')]
```

**Relationship Types**:
- **FOUNDATION**: One doctrine foundational to another (e.g., Trinity → Theosis)
- **DEVELOPMENT**: Historical development path (e.g., Divine Energies → Hesychasm)
- **CONTRAST**: Dialectical opposition (e.g., Orthodox vs. Western views)
- **SYNTHESIS**: Synthetic integration of concepts
- **APPLICATION**: Practical application (e.g., Doctrine → Liturgy)

### 3. Citation Preparer

**Purpose**: Manages verified Patristic citation database

**What it does**:
1. Provides database of verified works by each Church Father
2. Prepares citations relevant to topic and themes
3. Prevents LLM hallucination by providing only verified works
4. Formats citations correctly
5. Calculates theological relevance of each work

**Example Usage**:

```python
from src.preprocessing import CitationPreparer

citation_prep = CitationPreparer()

# Prepare 20 citations for topic
citations = citation_prep.prepare_citations(
    topic="Theosis and Quantum Entanglement",
    suggested_fathers=analysis.suggested_fathers,
    themes=analysis.core_themes,
    count=20
)

for citation in citations[:5]:
    print(f"{citation.father} - {citation.work}")
    print(f"  Theme: {citation.theme}")
    print(f"  Format: {citation.citation_format}")
    print(f"  Relevance: {citation.theological_relevance:.2f}")
    print()

# Output:
# St. Maximus the Confessor - Ambigua
#   Theme: Theosis and Soteriology
#   Format: St. Maximus the Confessor, in *Ambigua*
#   Relevance: 0.95
```

**Database Structure**:
Each Church Father has verified works:

```python
'St. Maximus the Confessor': [
    PatristicWork(
        title='Ambigua',
        author='St. Maximus the Confessor',
        alternate_titles=['Difficulties'],
        themes=['Christology', 'Cosmology', 'Theosis', 'Logos'],
        key_passages=['Logoi doctrine', 'Cosmic liturgy'],
        century=7,
        verified=True
    ),
    # More works...
]
```

**Verification**:
```python
# Check if citation is authentic
is_valid = citation_prep.verify_citation(
    father="St. Maximus the Confessor",
    work_title="Ambigua"
)
# Returns: True

is_valid = citation_prep.verify_citation(
    father="St. Maximus the Confessor",
    work_title="Fake Work Title"
)
# Returns: False
```

**Finding Works by Theme**:
```python
works = citation_prep.get_works_by_theme("Theosis")
for father, work in works:
    print(f"{father}: {work.title}")
# Output:
# St. Maximus the Confessor: Ambigua
# St. Gregory of Nyssa: The Life of Moses
# St. Athanasius: On the Incarnation
# ...
```

### 4. Theological Context Builder

**Purpose**: Integrates all preprocessing outputs into unified context

**What it does**:
1. Builds historical development narrative
2. Identifies contemporary relevance
3. Establishes scriptural foundation
4. Maps liturgical context
5. Formats Western contrasts
6. Generates section-specific guidance

**Example Usage**:

```python
from src.preprocessing import TheologicalContextBuilder

context_builder = TheologicalContextBuilder()
context = context_builder.build_context(
    topic="Theosis and Quantum Entanglement",
    analysis=analysis,
    semantic_map=semantic_map,
    prepared_citations=citations
)

print("Historical Development:")
print(context.historical_development)
# Output: Multi-paragraph narrative of how this theology developed

print("\nContemporary Relevance:")
print(context.contemporary_relevance)
# Output: How this topic addresses modern questions

print("\nGeneration Guidance for Introduction:")
print(context.generation_guidance['Introduction'])
# Output: "Introduce Theosis and Quantum Entanglement from Orthodox
#         perspective. Preview the 2 main themes: Theosis and Soteriology,
#         Cosmology and Creation. Establish contemporary relevance..."
```

**Section-Specific Guidance**:
The context builder generates detailed guidance for each of the 6 sections:

1. **Introduction**: How to open, what to preview, Orthodox framing
2. **The Patristic Mind**: Which fathers to engage, themes to emphasize
3. **Symphony of Clashes**: Dialectical tensions to explore
4. **Orthodox Affirmation**: Scripture to cite, doctrines to connect
5. **Synthesis**: How to integrate, practical applications
6. **Conclusion**: How to recap, mystery to acknowledge, doxology

## Complete Preprocessing Workflow

### Step-by-Step Example

```python
from src.preprocessing import (
    TopicAnalyzer,
    SemanticMapper,
    CitationPreparer,
    TheologicalContextBuilder
)

# Define topic
topic = "The Divine Infinity and the Mathematical Continuum: An Orthodox Synthesis"

# Step 1: Analyze topic (5-10 seconds)
print("Step 1: Analyzing topic...")
analyzer = TopicAnalyzer()
analysis = analyzer.analyze(topic)

print(f"  ✓ Identified {len(analysis.core_themes)} core themes")
print(f"  ✓ Domain: {analysis.theological_domain}")
print(f"  ✓ Complexity: {analysis.complexity_score:.2f} ({analysis.estimated_depth_required})")
print(f"  ✓ Suggested {len(analysis.suggested_fathers)} Church Fathers")

# Step 2: Create semantic map (2-5 seconds)
print("\nStep 2: Creating semantic map...")
mapper = SemanticMapper()
semantic_map = mapper.map_topic(topic, analysis.core_themes)

print(f"  ✓ Central concept: {semantic_map.central_concept}")
print(f"  ✓ {len(semantic_map.related_concepts)} related concepts")
print(f"  ✓ {len(semantic_map.relations)} theological relations mapped")
print(f"  ✓ {len(semantic_map.western_contrasts)} Western contrasts identified")

# Step 3: Prepare citations (3-5 seconds)
print("\nStep 3: Preparing citations...")
citation_prep = CitationPreparer()
citations = citation_prep.prepare_citations(
    topic=topic,
    suggested_fathers=analysis.suggested_fathers,
    themes=analysis.core_themes,
    count=20
)

print(f"  ✓ Prepared {len(citations)} verified citations")
fathers_used = set(c.father for c in citations)
print(f"  ✓ From {len(fathers_used)} different Church Fathers")

# Step 4: Build theological context (5-10 seconds)
print("\nStep 4: Building theological context...")
context_builder = TheologicalContextBuilder()
context = context_builder.build_context(
    topic=topic,
    analysis=analysis,
    semantic_map=semantic_map,
    prepared_citations=citations
)

print(f"  ✓ Historical development narrative created")
print(f"  ✓ Contemporary relevance identified")
print(f"  ✓ Liturgical context mapped")
print(f"  ✓ Scriptural foundation established")
print(f"  ✓ Section-specific guidance generated for all 6 sections")

print("\n" + "="*60)
print("PREPROCESSING COMPLETE")
print("="*60)
print(f"\nTotal time: ~15-30 seconds")
print(f"Context ready for CELESTIAL-tier generation")

# The context object now contains everything needed for generation:
# - Comprehensive topic analysis
# - Semantic relationship map
# - 20 verified citations
# - Historical narrative
# - Contemporary framing
# - Liturgical connections
# - Scriptural foundation
# - Detailed guidance for each section
```

## Best Practices

### 1. Always Preprocess Before Generation

**Don't skip preprocessing**. The 15-30 seconds spent preprocessing saves hours of refinement by:
- Providing verified citations (prevents hallucination)
- Mapping theological connections (ensures coherence)
- Suggesting relevant sources (increases depth)
- Generating section guidance (improves structure)

### 2. Review Preprocessing Output

Before generation, review:
- Are suggested fathers appropriate for this topic?
- Do prepared citations cover all core themes?
- Is complexity assessment accurate?
- Does section guidance align with your vision?

### 3. Customize When Needed

The preprocessing system is flexible:

```python
# Add specific fathers
analysis.suggested_fathers.append("St. Specific Father")

# Add specific citations
custom_citation = PreparedCitation(
    father="St. Custom Father",
    work="Custom Work",
    theme="Custom Theme",
    suggested_context="...",
    citation_format="St. Custom Father, in *Custom Work*",
    theological_relevance=0.95
)
citations.append(custom_citation)

# Adjust section guidance
context.generation_guidance['Introduction'] = "Custom guidance for introduction..."
```

### 4. Expand Citation Database

Add new fathers and works:

```python
# In src/preprocessing/citation_preparer.py
database['St. New Father'] = [
    PatristicWork(
        title='New Work',
        author='St. New Father',
        alternate_titles=[],
        greek_latin_title='Original title',
        themes=['Theme1', 'Theme2'],
        key_passages=['Key passage'],
        century=5,
        verified=True
    )
]
```

## Advanced Techniques

### Custom Semantic Relations

Define custom relationships for specialized topics:

```python
# Add to semantic_mapper.py
CUSTOM_RELATIONS = {
    ('Custom Concept A', 'Custom Concept B'): {
        'type': TheologicalRelationType.DEVELOPMENT,
        'strength': 0.85,
        'patristic_support': ['St. Father1', 'St. Father2']
    }
}
```

### Dynamic Complexity Adjustment

Override complexity for known topics:

```python
TOPIC_COMPLEXITY_OVERRIDES = {
    'The Holy Trinity': 1.0,  # Always advanced
    'Christian Hope': 0.4,    # Foundational
    'Divine Infinity': 0.95   # Very advanced
}

if topic in TOPIC_COMPLEXITY_OVERRIDES:
    analysis.complexity_score = TOPIC_COMPLEXITY_OVERRIDES[topic]
```

### Contextual Citation Selection

Select citations based on section:

```python
def get_citations_for_section(section_name, all_citations):
    """Get most relevant citations for specific section"""
    if section_name == "The Patristic Mind":
        # Prioritize high-relevance citations
        return sorted(all_citations, key=lambda c: c.theological_relevance, reverse=True)[:8]
    elif section_name == "Orthodox Affirmation":
        # Prioritize doctrinal works
        return [c for c in all_citations if 'doctrine' in ' '.join(c.work.themes).lower()][:5]
    # ... etc
```

## Troubleshooting

### Issue: Not Enough Citations Prepared

**Problem**: Only 10 citations prepared, need 20

**Solution**: Expand suggested_fathers list
```python
analysis.suggested_fathers.extend([
    'St. Additional Father 1',
    'St. Additional Father 2'
])
citations = citation_prep.prepare_citations(..., count=20)
```

### Issue: Citations Not Relevant to Topic

**Problem**: Prepared citations don't match topic themes

**Solution**: Manually filter and add
```python
# Filter by relevance
relevant_citations = [c for c in citations if c.theological_relevance >= 0.7]

# Add topic-specific citations
topic_specific = citation_prep.get_works_by_theme("Specific Theme")
```

### Issue: Complexity Score Seems Wrong

**Problem**: Topic assessed as foundational, but it's advanced

**Solution**: Manually adjust
```python
analysis.complexity_score = 0.85  # Override to advanced
analysis.estimated_depth_required = 'advanced'
```

## Metrics and Validation

### Preprocessing Quality Metrics

Verify preprocessing completeness:

```python
def validate_preprocessing(context):
    """Ensure preprocessing is complete"""
    checks = {
        'fathers_suggested': len(context.analysis.suggested_fathers) >= 5,
        'citations_prepared': len(context.prepared_citations) >= 20,
        'themes_identified': len(context.analysis.core_themes) >= 1,
        'scriptures_suggested': len(context.analysis.suggested_scriptures) >= 5,
        'guidance_complete': len(context.generation_guidance) == 6,
        'semantic_map_complete': len(context.semantic_map.related_concepts) >= 2
    }
    
    all_passed = all(checks.values())
    
    if not all_passed:
        print("⚠ Preprocessing incomplete:")
        for check, passed in checks.items():
            if not passed:
                print(f"  ✗ {check}")
    else:
        print("✓ Preprocessing complete and validated")
    
    return all_passed
```

## Conclusion

Effective preprocessing is the key to CELESTIAL-tier entries. The 15-30 seconds spent preparing comprehensive theological context pays dividends in:
- Higher validation scores (95-100)
- Fewer refinement iterations
- Better citation distribution
- Stronger theological coherence
- Authentic Orthodox perspective

**Always preprocess. Always validate. Always refine to CELESTIAL.**

---

**Next**: See TECHNICAL_ARCHITECTURE.md for complete system overview
