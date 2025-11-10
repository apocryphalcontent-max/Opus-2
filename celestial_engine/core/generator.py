"""
Main entry generation engine for the Celestial Engine.
Orchestrates the complete generation workflow.
"""

import logging
import time
import uuid
from datetime import datetime
from typing import Optional, Dict

from .models import Entry, Section, PreprocessingResult, GenerationProgress
from .llm_interface import get_llm, ModelType
from .config import get_config
from ..preprocessing.topic_analyzer import TopicAnalyzer
from ..validation.validator import EntryValidator
from ..prompts.templates import PromptTemplates
from ..refinement.refiner import EntryRefiner

logger = logging.getLogger(__name__)


class CelestialGenerator:
    """Main generation engine for CELESTIAL-tier entries."""

    def __init__(self):
        """Initialize the generator."""
        self.llm = get_llm()
        self.config = get_config()
        self.analyzer = TopicAnalyzer()
        self.validator = EntryValidator()
        self.refiner = EntryRefiner()
        self.templates = PromptTemplates()

    def generate(
        self,
        topic: str,
        skip_preprocessing: bool = False,
        max_refinements: Optional[int] = None
    ) -> Entry:
        """
        Generate a complete CELESTIAL-tier entry.

        Args:
            topic: Topic to generate entry for
            skip_preprocessing: Skip preprocessing if True
            max_refinements: Maximum refinement iterations (default from config)

        Returns:
            Complete validated entry
        """
        logger.info(f"Starting generation for topic: {topic}")
        start_time = time.time()

        # Create entry
        entry = Entry(
            topic=topic,
            entry_id=self._generate_entry_id(topic)
        )

        # Initialize progress tracking
        progress = GenerationProgress(
            entry_id=entry.entry_id,
            topic=topic,
            status="preprocessing"
        )

        try:
            # Phase 1: Preprocessing
            preprocessing = None
            if not skip_preprocessing and self.config.preprocessing_enabled:
                logger.info("Phase 1: Preprocessing...")
                progress.status = "preprocessing"
                preprocessing = self.analyzer.analyze(topic)
                logger.info(f"Preprocessing complete: {len(preprocessing.suggested_fathers)} fathers suggested")

            # Phase 2: Section Generation
            logger.info("Phase 2: Generating sections...")
            progress.status = "generating"

            section_configs = self.config.get_section_configs()
            entry.sections = []

            for idx, section_config in enumerate(section_configs):
                progress.current_section = section_config.name
                progress.progress_percentage = (idx / len(section_configs)) * 50

                logger.info(f"Generating section {idx + 1}/{len(section_configs)}: {section_config.name}")

                section = self._generate_section(
                    section_config=section_config,
                    topic=topic,
                    preprocessing=preprocessing,
                    previous_sections={s.name: s.content for s in entry.sections}
                )

                entry.sections.append(section)
                progress.sections_complete = idx + 1

                logger.info(f"Section complete: {section.name} ({section.word_count} words)")

            # Phase 3: Validation
            logger.info("Phase 3: Validating entry...")
            progress.status = "validating"
            progress.progress_percentage = 60

            validation_result = self.validator.validate(entry)
            entry.validation_result = validation_result

            logger.info(f"Initial validation: {validation_result.tier.value} ({validation_result.overall_score:.1f}/100)")

            # Phase 4: Iterative Refinement
            if validation_result.overall_score < self.config.min_score:
                logger.info("Phase 4: Iterative refinement...")
                progress.status = "refining"

                max_iterations = max_refinements or self.config.refinement_max_iterations

                entry = self.refiner.refine_to_celestial(
                    entry=entry,
                    max_iterations=max_iterations,
                    progress=progress
                )

            # Phase 5: Complete
            progress.status = "complete"
            progress.progress_percentage = 100
            progress.current_score = entry.validation_result.overall_score

            generation_time = time.time() - start_time
            entry.generation_time_seconds = generation_time

            logger.info(f"Generation complete: {entry.validation_result.tier.value} "
                       f"({entry.validation_result.overall_score:.1f}/100) in {generation_time:.1f}s")

            return entry

        except Exception as e:
            progress.status = "failed"
            progress.errors.append(str(e))
            logger.error(f"Generation failed: {e}", exc_info=True)
            raise

    def _generate_section(
        self,
        section_config,
        topic: str,
        preprocessing: Optional[PreprocessingResult],
        previous_sections: Dict[str, str]
    ) -> Section:
        """Generate a single section."""

        # Create section
        section = Section(
            name=section_config.name,
            slug=section_config.slug,
            min_words=section_config.min_words,
            target_words=section_config.target_words,
            max_words=section_config.max_words,
            model=section_config.model,
            requirements=section_config.requirements
        )

        # Generate prompt based on section type
        prompt = self._get_section_prompt(
            section_config=section_config,
            topic=topic,
            preprocessing=preprocessing,
            previous_sections=previous_sections
        )

        # Determine model type
        model_type = self._get_model_type(section_config.model)

        # Generate content
        logger.debug(f"Generating {section.name} with {model_type.value} model")

        response = self.llm.generate_with_model_type(
            prompt=prompt,
            model_type=model_type
        )

        if not response.success:
            raise Exception(f"Failed to generate {section.name}: {response.error}")

        # Update section content
        section.update_content(response.text.strip())

        # Expand if too short
        if section.word_count < section.min_words:
            logger.warning(f"Section {section.name} below minimum ({section.word_count}/{section.min_words}), expanding...")
            section = self._expand_section(section, section_config, topic, model_type)

        return section

    def _get_section_prompt(
        self,
        section_config,
        topic: str,
        preprocessing: Optional[PreprocessingResult],
        previous_sections: Dict[str, str]
    ) -> str:
        """Get appropriate prompt for section."""

        if section_config.slug == "introduction":
            return self.templates.introduction_prompt(
                topic=topic,
                preprocessing=preprocessing,
                target_words=section_config.target_words
            )

        elif section_config.slug == "patristic_mind":
            return self.templates.patristic_mind_prompt(
                topic=topic,
                preprocessing=preprocessing,
                target_words=section_config.target_words
            )

        elif section_config.slug == "symphony_of_clashes":
            return self.templates.symphony_of_clashes_prompt(
                topic=topic,
                preprocessing=preprocessing,
                target_words=section_config.target_words
            )

        elif section_config.slug == "orthodox_affirmation":
            return self.templates.orthodox_affirmation_prompt(
                topic=topic,
                preprocessing=preprocessing,
                target_words=section_config.target_words
            )

        elif section_config.slug == "synthesis":
            return self.templates.synthesis_prompt(
                topic=topic,
                previous_sections=previous_sections,
                preprocessing=preprocessing,
                target_words=section_config.target_words
            )

        elif section_config.slug == "conclusion":
            entry_summary = self._create_entry_summary(previous_sections)
            return self.templates.conclusion_prompt(
                topic=topic,
                entry_summary=entry_summary,
                target_words=section_config.target_words
            )

        else:
            raise ValueError(f"Unknown section type: {section_config.slug}")

    def _get_model_type(self, model_name: str) -> ModelType:
        """Determine model type from configuration."""
        if model_name == "primary":
            return ModelType.PRIMARY
        elif model_name == "advanced":
            return ModelType.ADVANCED
        else:
            return ModelType.PRIMARY

    def _expand_section(self, section: Section, section_config, topic: str, model_type: ModelType) -> Section:
        """Expand a section that's below minimum word count."""

        deficit = section_config.min_words - section.word_count

        expand_prompt = f"""The following section needs to be expanded by approximately {deficit} words to meet the minimum requirement of {section_config.min_words} words.

**Section**: {section.name}
**Topic**: {topic}
**Current Content**:
{section.content}

**Task**: Expand this section by adding {deficit} more words of substantial content. Do not simply repeat what's already there. Add:
- Additional Patristic citations and quotations
- Deeper theological exposition
- More specific examples
- Further scriptural references
- Additional connections and implications

Write the FULL expanded section (including the original content plus expansions):"""

        response = self.llm.generate_with_model_type(
            prompt=expand_prompt,
            model_type=model_type
        )

        if response.success:
            section.update_content(response.text.strip())
            logger.info(f"Section expanded to {section.word_count} words")

        return section

    def _create_entry_summary(self, sections: Dict[str, str]) -> str:
        """Create a summary of previous sections for conclusion."""
        summary_parts = []

        for section_name, content in sections.items():
            # Extract first 200 words
            words = content.split()[:200]
            snippet = " ".join(words)
            summary_parts.append(f"**{section_name}**: {snippet}...")

        return "\n\n".join(summary_parts)

    def _generate_entry_id(self, topic: str) -> str:
        """Generate unique entry ID."""
        # Create slug from topic
        slug = topic.lower()
        slug = slug.replace(' ', '_')
        slug = ''.join(c for c in slug if c.isalnum() or c == '_')
        slug = slug[:50]

        # Add timestamp and UUID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]

        return f"{slug}_{timestamp}_{unique_id}"

    def quick_validate(self, entry: Entry) -> bool:
        """
        Quick validation check.

        Args:
            entry: Entry to validate

        Returns:
            True if entry passes quick checks
        """
        validation_result = self.validator.validate(entry)
        entry.validation_result = validation_result

        return validation_result.passed
