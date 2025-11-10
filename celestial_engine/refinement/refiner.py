"""
Iterative refinement system for achieving CELESTIAL-tier quality.
Automatically improves entries that don't meet target scores.
"""

import logging
import time
from typing import Optional, List

from ..core.models import Entry, ValidationResult, RefinementTask, GenerationProgress
from ..core.llm_interface import get_llm, ModelType
from ..core.config import get_config
from ..validation.validator import EntryValidator
from ..prompts.templates import PromptTemplates

logger = logging.getLogger(__name__)


class EntryRefiner:
    """Refines entries through iterative improvement."""

    def __init__(self):
        """Initialize refiner."""
        self.llm = get_llm()
        self.config = get_config()
        self.validator = EntryValidator()
        self.templates = PromptTemplates()

    def refine_to_celestial(
        self,
        entry: Entry,
        max_iterations: int = 5,
        progress: Optional[GenerationProgress] = None
    ) -> Entry:
        """
        Refine entry through iterative improvements until CELESTIAL tier achieved.

        Args:
            entry: Entry to refine
            max_iterations: Maximum refinement iterations
            progress: Optional progress tracker

        Returns:
            Refined entry
        """
        logger.info(f"Starting refinement for entry: {entry.topic}")

        iteration = 0
        best_score = entry.validation_result.overall_score if entry.validation_result else 0

        while iteration < max_iterations:
            iteration += 1
            entry.refinement_iterations = iteration

            if progress:
                progress.refinement_iteration = iteration
                progress.progress_percentage = 60 + (iteration / max_iterations) * 35

            logger.info(f"Refinement iteration {iteration}/{max_iterations}")

            # Validate current state
            validation = self.validator.validate(entry)
            entry.validation_result = validation

            if progress:
                progress.current_score = validation.overall_score

            logger.info(f"Current score: {validation.overall_score:.1f}/100 ({validation.tier.value})")

            # Check if target achieved
            if validation.tier.value == "CELESTIAL" and validation.overall_score >= self.config.min_score:
                logger.info(f"🌟 CELESTIAL tier achieved! Score: {validation.overall_score:.1f}/100")
                return entry

            # Track best score
            if validation.overall_score > best_score:
                best_score = validation.overall_score

            # Identify refinement tasks
            tasks = self._identify_refinement_tasks(entry, validation)

            if not tasks:
                logger.warning("No refinement tasks identified but target not met. Stopping.")
                break

            # Execute refinement tasks
            logger.info(f"Executing {len(tasks)} refinement task(s)")

            for task in tasks:
                try:
                    self._execute_refinement_task(entry, task)
                except Exception as e:
                    logger.error(f"Refinement task failed: {e}")
                    if progress:
                        progress.errors.append(f"Refinement task failed: {str(e)}")

        # Final validation
        final_validation = self.validator.validate(entry)
        entry.validation_result = final_validation

        if final_validation.tier.value != "CELESTIAL":
            logger.warning(f"Failed to achieve CELESTIAL tier after {max_iterations} iterations. "
                         f"Final score: {final_validation.overall_score:.1f}/100 ({final_validation.tier.value})")
        else:
            logger.info(f"🌟 CELESTIAL tier achieved after {iteration} iterations!")

        return entry

    def _identify_refinement_tasks(self, entry: Entry, validation: ValidationResult) -> List[RefinementTask]:
        """
        Identify refinement tasks based on validation results.

        Args:
            entry: Entry to refine
            validation: Current validation results

        Returns:
            List of refinement tasks to execute
        """
        tasks = []
        strategies = self.config.refinement_strategies

        for strategy in strategies:
            # Check if strategy triggers apply
            triggered = False

            for trigger in strategy.get("triggers", []):
                if self._check_trigger(trigger, validation):
                    triggered = True
                    break

            if triggered:
                task = RefinementTask(
                    strategy_name=strategy["name"],
                    priority=strategy["priority"],
                    description=f"Apply strategy: {strategy['name']}",
                    actions=strategy.get("actions", [])
                )
                tasks.append(task)

        # Sort by priority
        tasks.sort(key=lambda t: t.priority)

        return tasks

    def _check_trigger(self, trigger: str, validation: ValidationResult) -> bool:
        """Check if a refinement trigger condition is met."""

        # Parse trigger conditions
        if "theological_depth <" in trigger:
            threshold = float(trigger.split("<")[1].strip())
            return validation.theological_depth_score < threshold

        elif "patristic_citations <" in trigger:
            threshold = int(trigger.split("<")[1].strip())
            return validation.patristic_citations < threshold

        elif "word_count <" in trigger:
            return validation.word_count_score < 80

        elif "any_section <" in trigger:
            return validation.section_balance_score < 80

        elif "coherence <" in trigger:
            threshold = float(trigger.split("<")[1].strip())
            return validation.coherence_score < threshold

        elif "section_balance <" in trigger:
            threshold = float(trigger.split("<")[1].strip())
            return validation.section_balance_score < threshold

        elif "orthodox_perspective <" in trigger:
            threshold = float(trigger.split("<")[1].strip())
            return validation.orthodox_perspective_score < threshold

        return False

    def _execute_refinement_task(self, entry: Entry, task: RefinementTask):
        """Execute a refinement task."""

        logger.info(f"Executing refinement task: {task.strategy_name}")

        if task.strategy_name == "enhance_theological_depth":
            self._enhance_theological_depth(entry)

        elif task.strategy_name == "expand_sections":
            self._expand_sections(entry)

        elif task.strategy_name == "improve_coherence":
            self._improve_coherence(entry)

        elif task.strategy_name == "balance_sections":
            self._balance_sections(entry)

        elif task.strategy_name == "strengthen_orthodox_perspective":
            self._strengthen_orthodox_perspective(entry)

        else:
            logger.warning(f"Unknown refinement strategy: {task.strategy_name}")

    def _enhance_theological_depth(self, entry: Entry):
        """Enhance theological depth by adding citations and deepening exposition."""

        logger.info("Enhancing theological depth...")

        # Target sections that need more Patristic content
        sections_to_enhance = []

        for section in entry.sections:
            # Count current citations in section
            citation_count = section.content.count("St.")

            if citation_count < 3 and section.slug in ["introduction", "patristic_mind", "orthodox_affirmation"]:
                sections_to_enhance.append(section)

        for section in sections_to_enhance:
            logger.info(f"Enhancing {section.name}")

            enhancement_prompt = f"""Enhance the theological depth of this section by adding more Patristic citations and deeper exposition.

**Section**: {section.name}
**Current Content**:
{section.content}

**Task**: Rewrite this section with:
1. 3-5 additional Patristic citations (name the Church Fathers and their works)
2. Deeper theological exposition of key concepts
3. More precise theological vocabulary
4. Maintain current length (around {section.word_count} words)

Write the enhanced section:"""

            response = self.llm.generate_with_model_type(
                prompt=enhancement_prompt,
                model_type=ModelType.ADVANCED
            )

            if response.success:
                section.update_content(response.text.strip())
                logger.info(f"Enhanced {section.name}: {section.word_count} words")

    def _expand_sections(self, entry: Entry):
        """Expand sections that are below minimum word count."""

        logger.info("Expanding short sections...")

        for section in entry.sections:
            if section.word_count < section.min_words:
                deficit = section.min_words - section.word_count
                logger.info(f"Expanding {section.name} by {deficit} words")

                expansion_prompt = f"""This section is {deficit} words below the minimum requirement of {section.min_words} words.

**Section**: {section.name}
**Current Content** ({section.word_count} words):
{section.content}

**Task**: Expand this section to at least {section.min_words} words by:
1. Adding more Patristic citations and quotations
2. Deepening theological exposition
3. Adding more scriptural references
4. Providing additional examples or applications
5. Expanding on key concepts

Write the expanded section (minimum {section.min_words} words):"""

                response = self.llm.generate_with_model_type(
                    prompt=expansion_prompt,
                    model_type=ModelType.ADVANCED
                )

                if response.success:
                    section.update_content(response.text.strip())
                    logger.info(f"Expanded {section.name}: {section.word_count} words")

    def _improve_coherence(self, entry: Entry):
        """Improve coherence by adding transitions and cross-references."""

        logger.info("Improving coherence...")

        # Focus on transitions between sections
        for i in range(1, len(entry.sections)):
            current_section = entry.sections[i]
            previous_section = entry.sections[i - 1]

            coherence_prompt = f"""Improve the coherence of this section by adding better transitions and cross-references to previous content.

**Previous Section**: {previous_section.name}
Last paragraph: {previous_section.content.split(chr(10))[-1]}

**Current Section**: {current_section.name}
{current_section.content}

**Task**: Rewrite the current section to:
1. Add a smooth transition from the previous section
2. Include cross-references like "As we saw in...", "Building on..."
3. Strengthen the logical flow
4. Maintain current length

Write the improved section:"""

            response = self.llm.generate_with_model_type(
                prompt=coherence_prompt,
                model_type=ModelType.ADVANCED
            )

            if response.success:
                current_section.update_content(response.text.strip())
                logger.info(f"Improved coherence in {current_section.name}")

    def _balance_sections(self, entry: Entry):
        """Balance section lengths."""

        logger.info("Balancing section lengths...")

        # Find over-long and under-long sections
        for section in entry.sections:
            if section.word_count > section.max_words * 1.2:
                # Section is too long, condense
                logger.info(f"Condensing {section.name} from {section.word_count} to ~{section.target_words} words")

                condense_prompt = f"""This section is too long ({section.word_count} words). Condense it to approximately {section.target_words} words while maintaining all key content.

**Section**: {section.name}
**Current Content**:
{section.content}

**Task**: Condense to ~{section.target_words} words by:
1. Removing redundancy
2. Tightening prose
3. Combining similar points
4. Keeping all Patristic citations and key insights

Write the condensed section:"""

                response = self.llm.generate_with_model_type(
                    prompt=condense_prompt,
                    model_type=ModelType.ADVANCED
                )

                if response.success:
                    section.update_content(response.text.strip())
                    logger.info(f"Condensed {section.name}: {section.word_count} words")

    def _strengthen_orthodox_perspective(self, entry: Entry):
        """Strengthen Orthodox framing and distinctives."""

        logger.info("Strengthening Orthodox perspective...")

        # Focus on key sections
        sections_to_strengthen = [
            s for s in entry.sections
            if s.slug in ["introduction", "orthodox_affirmation", "conclusion"]
        ]

        for section in sections_to_strengthen:
            logger.info(f"Strengthening Orthodox perspective in {section.name}")

            strengthen_prompt = f"""Strengthen the Orthodox perspective in this section.

**Section**: {section.name}
**Current Content**:
{section.content}

**Task**: Rewrite to:
1. Add more explicit Orthodox framing (use "Orthodox" or "Eastern Orthodox" 3+ times)
2. Add 1-2 contrasts with Western (Catholic/Protestant) theology
3. Connect to Orthodox liturgical practice or lived experience
4. Ground distinctives in Patristic sources
5. Maintain current length

Write the strengthened section:"""

            response = self.llm.generate_with_model_type(
                prompt=strengthen_prompt,
                model_type=ModelType.ADVANCED
            )

            if response.success:
                section.update_content(response.text.strip())
                logger.info(f"Strengthened Orthodox perspective in {section.name}")
