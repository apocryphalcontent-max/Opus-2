This repository contains a system for generating high-quality Orthodox Christian theological content. It is primarily responsible for creating CELESTIAL-tier (95-100 score) theological entries using Large Language Models, with strict quality validation and Patristic foundation requirements. Please follow these guidelines when contributing:

## Repository Structure

- **PRODUCTION_Guide.md**: Comprehensive production optimization guide for generating theological entries (4,799 lines)
- **README.md**: Basic repository information
- **.github/copilot-instructions.md**: This file - repository-wide instructions for Copilot

## Code Standards

### Content Quality Requirements

**CRITICAL**: All theological content MUST achieve CELESTIAL-tier (95-100) validation score. Lower scores are rejected.

- Minimum 20+ Patristic (Church Fathers) citations per entry
- Minimum 15+ Scripture references per entry  
- All content must reflect authentic Eastern Orthodox Christian theology
- Patristic citations should be 90-95% verifiable (acceptable standard for this project)

### Entry Structure (6 Required Sections)

Every theological entry must contain exactly 6 sections with minimum word counts:

1. **Introduction**: minimum 1,750 words
2. **The Patristic Mind**: minimum 2,250 words
3. **Symphony of Clashes**: minimum 2,350 words
4. **Orthodox Affirmation**: minimum 2,250 words
5. **Synthesis**: minimum 1,900 words
6. **Conclusion**: minimum 1,800 words

**Important**: Word counts are MINIMUMS with NO MAXIMUMS to allow proper theological treatment

### Validation Scoring System

Entries are scored on 5 weighted criteria (must score 95+ total):

1. **Word Count (20%)**: Meets minimum requirements for all sections
2. **Theological Depth (30%)**: Sufficient Patristic citations, Scripture references, Orthodox terminology
3. **Coherence (25%)**: Logical flow, cross-references between sections, structural integrity
4. **Section Balance (15%)**: Each section meets word count requirements
5. **Orthodox Perspective (10%)**: Clear Orthodox framing and distinctives

### Before Making Changes

When working on this repository:

- Read relevant sections of PRODUCTION_Guide.md for context on the topic
- Understand the Orthodox theological perspective before modifying theological content
- Verify Patristic citations against the citation database in PRODUCTION_Guide.md
- Ensure theological accuracy - this handles religious content, maintain respect and precision

## Key Orthodox Theological Principles

When modifying theological content, maintain awareness of Orthodox Christian distinctives:

- **Theosis (Deification)**: Transformation of believers into the likeness of God (use term 8-12 times per entry)
- **Divine Energies**: Distinction between God's essence and energies (6-10 uses per entry)
- **Patristic Authority**: Church Fathers are authoritative theological sources (15-20 references to "Patristic" or "Fathers")
- **Liturgical Grounding**: Connect theology to worship and lived experience
- **Apophatic Balance**: Maintain mystery alongside affirmative theology

## Required Before Each Commit

When modifying theological content or validation code:

- Verify theological terminology accuracy against PRODUCTION_Guide.md standards
- Check that Patristic citations match verified works database
- Ensure Orthodox distinctives are preserved
- Test validation scoring if modifying validation code
- Confirm word count minimums are maintained (no maximums enforced)

## Testing and Validation

When implementing new features:

- Test against the 5-criterion validation system
- Use sample theological entries for testing
- Validate compatibility with Ollama LLM backend (Mixtral 8x7B, Llama 3.1 70B models)
- Ensure CELESTIAL-tier (95-100 score) requirements are maintained

## Python Code Standards

- Follow PEP 8 style guidelines for all Python code
- Use JSON for configuration files
- Add comprehensive comments for theological validation logic
- Gracefully handle LLM generation failures and timeouts
- Document any new validation criteria or scoring algorithms

## Working with PRODUCTION_Guide.md

The PRODUCTION_Guide.md file is extensive (4,799 lines) and detailed. When making changes:

- Preserve the hierarchical structure and numbered sections
- Maintain theological accuracy in all examples and citations
- Keep hardware optimization recommendations current
- Ensure consistency in validation scoring algorithms
- Document any changes to quality standards or thresholds

## Important Distinctions for This Repository

1. **Theological Sensitivity**: This handles religious content - maintain respect, accuracy, and Orthodox perspective
2. **Citation Standards**: Patristic citations should be verifiable (90-95% authenticity is acceptable for this project)
3. **Word Counts**: Sections have MINIMUMS but NO MAXIMUMS to allow proper theological treatment (unlike traditional academic writing)
4. **Quality Tiers**: Only CELESTIAL-tier (95-100) is acceptable - ADAMANTINE (90-94) and lower are rejected
5. **Orthodox Perspective**: All content must be from Eastern Orthodox Christian viewpoint, distinguishing from Western theology

## Development Workflow

1. Understand the Orthodox theological context before making changes
2. Consult PRODUCTION_Guide.md for standards, examples, and verified citation lists
3. Preserve existing quality standards and requirements
4. Test changes against sample theological content
5. Maintain backward compatibility with existing entries
6. Document theological validation logic with clear comments

## Reference Information

### Key Church Fathers Cited

Core Patristic sources (cite 5+ different Fathers per entry):
- St. Gregory of Nyssa (works: *On the Making of Man*, *The Life of Moses*, *Against Eunomius*)
- St. Maximus the Confessor (works: *Ambigua*, *Chapters on Charity*, *Mystagogy*)
- St. Basil the Great (works: *On the Holy Spirit*, *Hexaemeron*, *Against Eunomius*)
- St. John Chrysostom (works: *Homilies on [Gospel/Epistle]*, *On the Priesthood*)
- St. Athanasius (works: *On the Incarnation*, *Against the Heathen*, *Letters to Serapion*)
- St. Gregory Palamas (works: *Triads in Defense of the Holy Hesychasts*)

### Scripture References

- Follow Orthodox canonical order
- Minimum 15+ references per entry (5-8 Old Testament, 10-15 New Testament)
- Include Orthodox exegetical interpretation

### Liturgical References

When relevant, connect theology to Orthodox Divine Liturgy practices and lived experience.

## System Architecture

- **Target**: 12,000 CELESTIAL-tier theological entries
- **Hardware**: ROG Zephyrus Duo 4090 with RTX 4090 Mobile GPU
- **LLM Backend**: Ollama with Mixtral 8x7B and Llama 3.1 70B models
- **Validation**: Automated 5-criterion scoring system
- **Quality Standard**: 95-100 score (CELESTIAL tier) required for all entries
