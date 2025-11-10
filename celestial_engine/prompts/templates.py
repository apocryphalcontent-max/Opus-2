"""
Prompt templates for the Celestial Engine.
High-quality, optimized prompts for CELESTIAL-tier generation.
"""

from typing import Dict, List, Any, Optional
from ..core.models import PreprocessingResult


class PromptTemplates:
    """Collection of prompt templates for entry generation."""

    @staticmethod
    def introduction_prompt(
        topic: str,
        preprocessing: Optional[PreprocessingResult] = None,
        target_words: int = 1750
    ) -> str:
        """Generate prompt for Introduction section."""

        context = ""
        if preprocessing:
            context = f"""
**Suggested Resources:**
- Key Themes: {', '.join(preprocessing.theological_themes[:5])}
- Relevant Fathers: {', '.join(preprocessing.suggested_fathers[:3])}
- Scripture: {', '.join(preprocessing.suggested_scriptures[:3])}
"""

        return f"""You are a world-class Orthodox Christian theologian writing the **Introduction** section of a comprehensive theological entry on:

**Topic**: {topic}

**Your Task**: Write a CELESTIAL-tier introduction ({target_words} words) that:

1. **Establishes Significance**: Explain why this topic matters profoundly for Orthodox theology and spiritual life

2. **Orthodox Framing**: Provide explicit Orthodox framing from the outset
   - Use "Orthodox" or "Eastern Orthodox" 2-3 times
   - Distinguish from Western approaches where relevant

3. **Patristic Foundation**: Include 2-3 Patristic citations that establish the historical Orthodox engagement with this topic
   - Cite specific Church Fathers by name (e.g., "St. Gregory of Nyssa")
   - Reference specific works when possible

4. **Scriptural Grounding**: Reference 3-4 relevant Scripture passages that undergird this topic

5. **Preview Structure**: Briefly preview how this entry will unfold across its sections

6. **Theological Depth**: Use rich Orthodox theological vocabulary (theosis, energies, essence, hypostasis, etc.)

{context}

**Style Guidelines**:
- Write with scholarly rigor yet accessible prose
- Balance philosophical depth with pastoral warmth
- Demonstrate how this topic connects to lived Orthodox experience
- Avoid generic or superficial theological language
- Every sentence should carry theological weight

**Critical Requirements**:
- Target {target_words} words (minimum {int(target_words * 0.85)})
- 2-3 Patristic citations with names
- 3-4 Scripture references
- Clear Orthodox framing

Write the Introduction section now:"""

    @staticmethod
    def patristic_mind_prompt(
        topic: str,
        preprocessing: Optional[PreprocessingResult] = None,
        target_words: int = 2250
    ) -> str:
        """Generate prompt for The Patristic Mind section."""

        resources = ""
        if preprocessing:
            resources = f"""
**Suggested Resources:**
- Church Fathers: {', '.join(preprocessing.suggested_fathers[:8])}
- Works to Cite: {', '.join(preprocessing.suggested_works[:5])}
- Key Themes: {', '.join(preprocessing.theological_themes)}
"""

        return f"""You are a world-class Orthodox Christian theologian writing **The Patristic Mind** section of a comprehensive theological entry on:

**Topic**: {topic}

**Your Task**: Write a CELESTIAL-tier Patristic exposition ({target_words} words) that:

1. **Deep Patristic Engagement**: This is the heart of the entry's Patristic content
   - Cite 8-10 different Church Fathers throughout this section
   - Include at least 3-4 named specific works (e.g., "St. Maximus the Confessor, in his Ambigua...")
   - Draw from diverse periods and traditions (Cappadocian Fathers, Desert Fathers, Byzantine theologians, etc.)

2. **Theological Exposition**: Present the Patristic understanding of this topic with depth and nuance
   - Explore how different Fathers approached this topic
   - Show the development and consensus of Patristic thought
   - Highlight key insights and distinctive contributions

3. **Historical Context**: Provide historical context for Patristic engagement
   - When and why did Fathers address this topic?
   - What controversies or questions motivated their reflection?
   - How did their insights shape Orthodox theology?

4. **Theological Integration**: Show how Patristic insights integrate into a coherent vision
   - Demonstrate the "symphonic" quality of Patristic witness
   - Show agreements and complementary perspectives
   - Address any apparent tensions between Fathers

5. **Contemporary Relevance**: Connect ancient Patristic wisdom to contemporary questions

{resources}

**Critical Requirements**:
- Target {target_words} words (minimum {int(target_words * 0.9)})
- 8-10 different Church Fathers cited
- 3-4 specific works named
- Rich theological vocabulary
- Demonstrate breadth and depth of Patristic tradition

**Fathers to Consider Including** (cite 8-10):
- St. Maximus the Confessor
- St. Gregory of Nyssa
- St. Basil the Great
- St. John Chrysostom
- St. Athanasius
- St. Gregory Palamas
- St. John of Damascus
- St. Ignatius of Antioch
- St. Irenaeus of Lyons
- St. Cyril of Alexandria
- St. Isaac the Syrian
- St. Symeon the New Theologian

Write The Patristic Mind section now:"""

    @staticmethod
    def symphony_of_clashes_prompt(
        topic: str,
        preprocessing: Optional[PreprocessingResult] = None,
        target_words: int = 2350
    ) -> str:
        """Generate prompt for Symphony of Clashes section."""

        tensions = ""
        if preprocessing and preprocessing.potential_tensions:
            tensions = f"""
**Identified Tensions**:
{chr(10).join(f'- {t}' for t in preprocessing.potential_tensions)}
"""

        return f"""You are a world-class Orthodox Christian theologian writing the **Symphony of Clashes** section of a comprehensive theological entry on:

**Topic**: {topic}

**Your Task**: Write a CELESTIAL-tier dialectical exploration ({target_words} words) that:

1. **Identify Tensions**: Present 3-4 genuine theological tensions, paradoxes, or apparent contradictions related to this topic
   - These should be real tensions that require Orthodox synthesis
   - Not manufactured or trivial contradictions
   - Tensions that illuminate the depth of the topic

2. **Orthodox Synthesis**: Show how Orthodox theology holds these tensions in creative synthesis
   - Demonstrate the "both-and" rather than "either-or" approach
   - Show how apparent contradictions reveal deeper truth
   - Use Patristic wisdom to resolve or reframe tensions

3. **Patristic Grounding**: Ground your dialectical exploration in Patristic sources
   - Cite 3-4 Church Fathers who addressed these tensions
   - Show how Fathers navigated paradox and mystery
   - Demonstrate Orthodox comfort with apophatic theology

4. **Philosophical Sophistication**: Engage with philosophical dimensions
   - Use rigorous logical analysis
   - Address epistemological and metaphysical implications
   - Show the theological adequacy of Orthodox synthesis

5. **Practical Implications**: Connect theological synthesis to lived Orthodox experience
   - How does this synthesis shape prayer, liturgy, or spiritual life?
   - What difference does this make for Orthodox praxis?

{tensions}

**Critical Requirements**:
- Target {target_words} words (minimum {int(target_words * 0.9)})
- 3-4 genuine theological tensions explored
- Orthodox synthesis for each tension
- 3-4 Patristic citations grounding the synthesis
- Philosophical rigor combined with theological depth

**Example Tensions** (adapt to your topic):
- Transcendence vs. immanence
- Divine simplicity vs. real distinctions (essence/energies)
- Apophatic vs. cataphatic theology
- Divine sovereignty vs. human freedom
- Mysticism vs. rationality
- Particular vs. universal

Write the Symphony of Clashes section now:"""

    @staticmethod
    def orthodox_affirmation_prompt(
        topic: str,
        preprocessing: Optional[PreprocessingResult] = None,
        target_words: int = 2250
    ) -> str:
        """Generate prompt for Orthodox Affirmation section."""

        contrasts = ""
        if preprocessing and preprocessing.western_contrasts:
            contrasts = f"""
**Western Contrasts to Address**:
{chr(10).join(f'- {c}' for c in preprocessing.western_contrasts)}
"""

        return f"""You are a world-class Orthodox Christian theologian writing the **Orthodox Affirmation** section of a comprehensive theological entry on:

**Topic**: {topic}

**Your Task**: Write a CELESTIAL-tier Orthodox distinctives section ({target_words} words) that:

1. **Western Contrasts**: Identify 3-4 clear ways Orthodox theology differs from Western (Catholic/Protestant) approaches to this topic
   - Be specific and charitable in characterizing Western views
   - Show genuine theological differences, not caricatures
   - Explain why Orthodox theology takes a different path

2. **Orthodox Distinctives**: Articulate what is distinctively Orthodox about this topic
   - Essence-energies distinction
   - Apophatic theology
   - Palamite synthesis
   - Liturgical and sacramental integration
   - Theosis as framework

3. **Liturgical Connections**: Show how this topic connects to Orthodox liturgy and worship
   - How does the Divine Liturgy embody this theology?
   - What do hymns, prayers, or liturgical texts reveal?
   - How does liturgical practice shape understanding?

4. **Lived Experience**: Connect to lived Orthodox spiritual life
   - Monastic tradition and practice
   - Hesychasm and prayer
   - Sacramental life
   - Iconography and sacred art
   - Ascetical theology

5. **Patristic Grounding**: Ground Orthodox distinctives in Patristic sources (4-5 citations)
   - Show that these distinctives are not innovations but ancient tradition
   - Cite Fathers who articulated these perspectives

{contrasts}

**Critical Requirements**:
- Target {target_words} words (minimum {int(target_words * 0.9)})
- 3-4 Western contrasts explicitly addressed
- 4-5 Patristic citations
- 5+ references to liturgy, prayer, sacraments, or monastic tradition
- Clear Orthodox framing throughout

**Theological Distinctives to Highlight**:
- Essence-energies distinction (vs. Western simplicity)
- Apophaticism (vs. Western cataphatic emphasis)
- Theosis (vs. Western juridical salvation)
- Real synergy (vs. Western monergism or semi-Pelagianism)
- Uncreated grace (vs. created grace)
- Palamite synthesis (vs. Western scholasticism)

Write the Orthodox Affirmation section now:"""

    @staticmethod
    def synthesis_prompt(
        topic: str,
        previous_sections: Dict[str, str],
        preprocessing: Optional[PreprocessingResult] = None,
        target_words: int = 1900
    ) -> str:
        """Generate prompt for Synthesis section."""

        previous_content = "\n\n".join([
            f"**{name}**: {content[:500]}..." if len(content) > 500 else f"**{name}**: {content}"
            for name, content in previous_sections.items()
        ])

        return f"""You are a world-class Orthodox Christian theologian writing the **Synthesis** section of a comprehensive theological entry on:

**Topic**: {topic}

**Your Task**: Write a CELESTIAL-tier synthesis ({target_words} words) that:

1. **Integrate Previous Sections**: Bring together insights from all previous sections into a coherent whole
   - Reference earlier discussions explicitly
   - Show how Patristic wisdom, dialectical tensions, and Orthodox distinctives converge
   - Demonstrate the unity of Orthodox theological vision

2. **Theological Coherence**: Articulate the internal coherence of Orthodox theology on this topic
   - Show how all elements fit together logically and spiritually
   - Demonstrate that Orthodox theology is not arbitrary but deeply reasoned
   - Reveal the "symphonic" quality of Orthodox thought

3. **Practical Application**: Show how this theology translates into Orthodox life
   - What difference does this make for prayer?
   - How does this shape spiritual life?
   - What practical wisdom emerges?

4. **Forward-Looking**: Point toward deeper mysteries and further exploration
   - What questions remain open?
   - What depths have we only begun to plumb?
   - How does this topic connect to the broader Orthodox vision?

5. **Patristic Synthesis**: Ground your synthesis in 2-3 key Patristic insights
   - Show how the Fathers anticipated or articulated this synthesis
   - Let Patristic wisdom have the final theological word

**Previous Sections Summary**:
{previous_content}

**Critical Requirements**:
- Target {target_words} words (minimum {int(target_words * 0.9)})
- Explicit cross-references to previous sections
- 2-3 Patristic citations
- Demonstrate theological coherence
- Balance intellectual rigor with pastoral warmth

**Synthesis Strategy**:
1. Recap key insights from each section
2. Show how they interconnect and reinforce each other
3. Articulate the unified Orthodox vision
4. Apply to lived Orthodox experience
5. Point toward transcendent mystery

Write the Synthesis section now:"""

    @staticmethod
    def conclusion_prompt(
        topic: str,
        entry_summary: str,
        target_words: int = 1800
    ) -> str:
        """Generate prompt for Conclusion section."""

        return f"""You are a world-class Orthodox Christian theologian writing the **Conclusion** section of a comprehensive theological entry on:

**Topic**: {topic}

**Your Task**: Write a CELESTIAL-tier conclusion ({target_words} words) that:

1. **Summarize Key Insights**: Distill the most important theological insights from this entry
   - What have we learned about this topic?
   - What are the key takeaways?
   - What matters most?

2. **Final Patristic Word**: Let a Church Father have the concluding voice
   - Choose 1-2 powerful Patristic quotations that encapsulate the topic
   - Let Patristic wisdom close the theological exposition
   - Show the timeless relevance of Patristic thought

3. **Call to Orthodox Life**: Issue a call to embodied Orthodox living
   - How should this theology transform us?
   - What does this require of Orthodox Christians?
   - How do we live this truth?

4. **Theological Doxology**: End with doxological language
   - Point toward the glory of God
   - Express wonder and worship
   - Acknowledge the limits of human understanding before divine mystery

5. **Leave Reader Transformed**: The conclusion should leave the reader:
   - Deepened in Orthodox faith
   - Enriched in theological understanding
   - Inspired to greater holiness
   - Aware of both clarity and mystery

**Entry Summary**:
{entry_summary}

**Critical Requirements**:
- Target {target_words} words (minimum {int(target_words * 0.9)})
- 1-2 powerful Patristic quotations
- Call to Orthodox praxis
- Doxological conclusion
- Balance between closure and openness to mystery

**Conclusion Structure**:
1. Summarize journey through this topic (500-700 words)
2. Final Patristic wisdom (300-400 words)
3. Call to Orthodox life (400-500 words)
4. Doxological ending (200-300 words)

Write the Conclusion section now:"""

    @staticmethod
    def refinement_prompt(
        section_name: str,
        current_content: str,
        weaknesses: List[str],
        suggestions: List[str],
        target_words: int
    ) -> str:
        """Generate prompt for section refinement."""

        weaknesses_text = "\n".join(f"- {w}" for w in weaknesses)
        suggestions_text = "\n".join(f"- {s}" for s in suggestions)

        return f"""You are refining the **{section_name}** section to achieve CELESTIAL-tier quality (95-100 score).

**Current Content**:
{current_content}

**Identified Weaknesses**:
{weaknesses_text}

**Improvement Suggestions**:
{suggestions_text}

**Your Task**: Rewrite this section to address all weaknesses while maintaining its strengths.

**Requirements**:
- Target {target_words} words
- Address every weakness listed above
- Implement every suggestion
- Maintain theological depth and Orthodox perspective
- Improve Patristic citations if needed (add more, name specific works)
- Strengthen transitions and flow
- Enhance theological vocabulary and precision

**Rewrite the section now, incorporating all improvements**:"""
