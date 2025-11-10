# Copilot Instructions for Opus-2

## Repository Overview

Opus-2 is a system for generating high-quality Orthodox Christian theological content, specifically focused on creating CELESTIAL-tier (95-100 score) entries on theological topics. The repository contains:

- **PRODUCTION_Guide.md**: Comprehensive production optimization guide for generating theological entries
- **README.md**: Basic repository information

## Purpose and Context

This repository is designed to facilitate the creation of 12,000 CELESTIAL-tier Orthodox Christian theological entries using Large Language Models (LLMs) running on optimized hardware (ROG Zephyrus Duo 4090). The system emphasizes:

1. **Orthodox Theological Perspective**: All content must reflect authentic Eastern Orthodox Christian theology
2. **Patristic Foundation**: Heavy reliance on Church Fathers and Patristic sources
3. **High Quality Standards**: CELESTIAL-tier (95-100 validation score) is the only acceptable output
4. **Word Count Requirements**: Minimum word counts per section with NO MAXIMUMS to allow proper theological exposition

## Key Theological Principles

When working with this repository, maintain awareness of Orthodox Christian distinctives:

- **Theosis (Deification)**: The transformation of believers into the likeness of God
- **Divine Energies**: The distinction between God's essence and energies
- **Patristic Authority**: Church Fathers are authoritative theological sources
- **Liturgical Grounding**: Theology connected to worship and lived experience
- **Apophatic Balance**: Maintaining mystery alongside affirmative theology

## Important Standards

### Content Standards
- All theological content must align with Orthodox Christian teaching
- Citations must be accurate and verifiable against Patristic sources
- Content should distinguish Orthodox perspectives from Western theological traditions
- Minimum 20+ Patristic references per entry
- Minimum 15+ Scripture references per entry

### Quality Tiers
- **CELESTIAL (95-100)**: Publication-ready, required for all entries
- **ADAMANTINE (90-94)**: Excellent but insufficient - requires refinement
- **PLATINUM (85-89)**: Good but below standard - requires refinement
- Lower tiers are rejected and regenerated

### Section Structure
Every entry must contain exactly 6 sections:
1. **Introduction** (minimum 1,750 words)
2. **The Patristic Mind** (minimum 2,250 words)
3. **Symphony of Clashes** (minimum 2,350 words)
4. **Orthodox Affirmation** (minimum 2,250 words)
5. **Synthesis** (minimum 1,900 words)
6. **Conclusion** (minimum 1,800 words)

## Validation Criteria

Entries are scored on 5 weighted criteria:
1. **Word Count (20%)**: Meets minimum requirements and targets
2. **Theological Depth (30%)**: Patristic citations, Scripture references, Orthodox terminology
3. **Coherence (25%)**: Logical flow, cross-references, structural integrity
4. **Section Balance (15%)**: Each section meets requirements
5. **Orthodox Perspective (10%)**: Clear Orthodox framing and distinctives

## Coding Conventions

When adding or modifying code in this repository:

- **Python**: Follow PEP 8 style guidelines
- **Documentation**: Maintain comprehensive comments for theological validation logic
- **Configuration**: Use JSON for configuration files
- **Error Handling**: Gracefully handle LLM generation failures and timeouts

## Working with the Production Guide

The `PRODUCTION_Guide.md` is extensive and detailed. When making changes:

- Preserve the hierarchical structure and detailed instructions
- Maintain theological accuracy in all examples
- Keep hardware optimization recommendations current
- Ensure consistency in validation scoring algorithms

## Important Considerations

1. **Theological Sensitivity**: This repository handles religious content. Maintain respect and accuracy.
2. **Citation Accuracy**: Patristic citations should be verifiable. The system accepts 90-95% authenticity as sufficient.
3. **No Maximum Word Counts**: Unlike traditional writing, sections have minimums but NO MAXIMUMS to allow proper theological treatment.
4. **Orthodox Perspective**: All content should be from an Eastern Orthodox Christian viewpoint.

## Testing and Validation

When implementing new features:

- Test against the 5-criterion validation system
- Verify theological terminology accuracy
- Ensure compatibility with Ollama LLM backend
- Validate against CELESTIAL-tier requirements

## Development Workflow

1. Understand the theological context before making changes
2. Preserve existing quality standards and requirements
3. Test changes against sample theological content
4. Maintain backward compatibility with existing entries
5. Document theological validation logic clearly

## Questions and Clarifications

When uncertain about theological matters or Orthodox Christian perspectives:
- Consult the PRODUCTION_Guide.md for standards and examples
- Maintain consistency with existing Patristic citation practices
- Default to conservative Orthodox theological positions
- Preserve the distinction between Orthodox and Western perspectives

## Additional Resources

- Church Fathers cited include: Gregory of Nyssa, Maximus the Confessor, Basil the Great, John Chrysostom, Athanasius, Gregory Palamas
- Scripture references should follow Orthodox canonical order
- Liturgical references should align with Orthodox Divine Liturgy practices
