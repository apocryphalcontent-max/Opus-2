"""
Batch processing system for generating multiple entries.
Supports parallel processing and checkpointing.
"""

import logging
import time
import json
from pathlib import Path
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from datetime import datetime

from ..core.generator import CelestialGenerator
from ..core.config import get_config
from ..core.models import Entry

logger = logging.getLogger(__name__)


@dataclass
class BatchProgress:
    """Tracks batch processing progress."""
    total_topics: int
    completed: int = 0
    failed: int = 0
    in_progress: int = 0
    start_time: float = 0.0

    celestial_count: int = 0
    total_words: int = 0
    total_time: float = 0.0

    def to_dict(self):
        return asdict(self)


class BatchProcessor:
    """Processes multiple entry generations in batch."""

    def __init__(
        self,
        parallel_workers: int = 3,
        checkpoint_interval: int = 10
    ):
        """
        Initialize batch processor.

        Args:
            parallel_workers: Number of parallel workers
            checkpoint_interval: Save checkpoint every N entries
        """
        self.parallel_workers = parallel_workers
        self.checkpoint_interval = checkpoint_interval
        self.config = get_config()
        self.generator = CelestialGenerator()

    def process_batch(
        self,
        topics: List[str],
        output_dir: Optional[Path] = None
    ):
        """
        Process a batch of topics.

        Args:
            topics: List of topics to generate
            output_dir: Output directory (default: config.entries_dir)
        """
        output_dir = output_dir or self.config.entries_dir
        output_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Starting batch processing: {len(topics)} topics")
        logger.info(f"Parallel workers: {self.parallel_workers}")
        logger.info(f"Output directory: {output_dir}")

        progress = BatchProgress(
            total_topics=len(topics),
            start_time=time.time()
        )

        # Create checkpoint directory
        checkpoint_dir = self.config.checkpoints_dir
        checkpoint_dir.mkdir(parents=True, exist_ok=True)

        # Load previous checkpoint if exists
        checkpoint_file = checkpoint_dir / "batch_checkpoint.json"
        completed_topics = self._load_checkpoint(checkpoint_file)

        # Filter out completed topics
        remaining_topics = [t for t in topics if t not in completed_topics]
        progress.completed = len(completed_topics)

        logger.info(f"Resuming from checkpoint: {progress.completed} already completed")
        logger.info(f"Remaining topics: {len(remaining_topics)}")

        # Process topics
        if self.parallel_workers == 1:
            # Sequential processing
            self._process_sequential(
                remaining_topics,
                output_dir,
                progress,
                checkpoint_file,
                completed_topics
            )
        else:
            # Parallel processing
            self._process_parallel(
                remaining_topics,
                output_dir,
                progress,
                checkpoint_file,
                completed_topics
            )

        # Final report
        self._print_final_report(progress)

    def _process_sequential(
        self,
        topics: List[str],
        output_dir: Path,
        progress: BatchProgress,
        checkpoint_file: Path,
        completed_topics: set
    ):
        """Process topics sequentially."""
        for i, topic in enumerate(topics):
            try:
                logger.info(f"\n{'='*70}")
                logger.info(f"Processing {progress.completed + 1}/{progress.total_topics}: {topic}")
                logger.info(f"{'='*70}\n")

                entry = self.generator.generate(topic)

                # Save entry
                self._save_entry(entry, output_dir)

                # Update progress
                progress.completed += 1
                progress.total_words += entry.total_words
                progress.total_time += entry.generation_time_seconds

                if entry.validation_result and entry.validation_result.tier.value == "CELESTIAL":
                    progress.celestial_count += 1

                # Save checkpoint
                completed_topics.add(topic)
                if progress.completed % self.checkpoint_interval == 0:
                    self._save_checkpoint(checkpoint_file, completed_topics)
                    logger.info(f"📍 Checkpoint saved: {progress.completed} entries completed")

                # Progress update
                self._print_progress(progress)

            except Exception as e:
                logger.error(f"Failed to generate entry for '{topic}': {e}")
                progress.failed += 1

    def _process_parallel(
        self,
        topics: List[str],
        output_dir: Path,
        progress: BatchProgress,
        checkpoint_file: Path,
        completed_topics: set
    ):
        """Process topics in parallel."""
        with ThreadPoolExecutor(max_workers=self.parallel_workers) as executor:
            # Submit all tasks
            future_to_topic = {
                executor.submit(self._generate_entry_safe, topic): topic
                for topic in topics
            }

            # Process completed tasks
            for future in as_completed(future_to_topic):
                topic = future_to_topic[future]

                try:
                    entry = future.result()

                    if entry:
                        # Save entry
                        self._save_entry(entry, output_dir)

                        # Update progress
                        progress.completed += 1
                        progress.total_words += entry.total_words
                        progress.total_time += entry.generation_time_seconds

                        if entry.validation_result and entry.validation_result.tier.value == "CELESTIAL":
                            progress.celestial_count += 1

                        logger.info(f"✅ Completed: {topic}")
                    else:
                        progress.failed += 1
                        logger.error(f"❌ Failed: {topic}")

                    # Save checkpoint
                    completed_topics.add(topic)
                    if progress.completed % self.checkpoint_interval == 0:
                        self._save_checkpoint(checkpoint_file, completed_topics)
                        logger.info(f"📍 Checkpoint saved: {progress.completed} entries completed")

                    # Progress update
                    self._print_progress(progress)

                except Exception as e:
                    logger.error(f"Error processing {topic}: {e}")
                    progress.failed += 1

    def _generate_entry_safe(self, topic: str) -> Optional[Entry]:
        """Generate entry with error handling."""
        try:
            return self.generator.generate(topic)
        except Exception as e:
            logger.error(f"Generation failed for '{topic}': {e}")
            return None

    def _save_entry(self, entry: Entry, output_dir: Path):
        """Save entry to disk."""
        md_path = output_dir / f"{entry.entry_id}.md"
        json_path = output_dir / f"{entry.entry_id}.json"

        # Save markdown
        md_path.write_text(entry.to_markdown())

        # Save JSON metadata
        json_path.write_text(json.dumps(entry.to_dict(), indent=2))

        logger.info(f"💾 Saved: {md_path.name}")

    def _load_checkpoint(self, checkpoint_file: Path) -> set:
        """Load checkpoint of completed topics."""
        if checkpoint_file.exists():
            try:
                data = json.loads(checkpoint_file.read_text())
                return set(data.get("completed_topics", []))
            except Exception as e:
                logger.warning(f"Failed to load checkpoint: {e}")

        return set()

    def _save_checkpoint(self, checkpoint_file: Path, completed_topics: set):
        """Save checkpoint of completed topics."""
        try:
            data = {
                "completed_topics": list(completed_topics),
                "timestamp": datetime.now().isoformat()
            }
            checkpoint_file.write_text(json.dumps(data, indent=2))
        except Exception as e:
            logger.error(f"Failed to save checkpoint: {e}")

    def _print_progress(self, progress: BatchProgress):
        """Print progress update."""
        elapsed = time.time() - progress.start_time
        completed = progress.completed + progress.failed

        if completed > 0:
            avg_time = progress.total_time / progress.completed if progress.completed > 0 else 0
            celestial_rate = (progress.celestial_count / progress.completed * 100) if progress.completed > 0 else 0

            logger.info(f"\n📊 Progress: {completed}/{progress.total_topics} "
                       f"({completed/progress.total_topics*100:.1f}%)")
            logger.info(f"   ✅ Completed: {progress.completed}")
            logger.info(f"   ❌ Failed: {progress.failed}")
            logger.info(f"   🌟 CELESTIAL: {progress.celestial_count} ({celestial_rate:.1f}%)")
            logger.info(f"   ⏱️  Avg time: {avg_time:.1f}s per entry")
            logger.info(f"   📝 Avg words: {progress.total_words // progress.completed if progress.completed > 0 else 0:,}")

            # Estimate remaining time
            if avg_time > 0:
                remaining = progress.total_topics - completed
                est_time = remaining * avg_time
                logger.info(f"   ⏳ Est. remaining: {est_time/3600:.1f} hours")

    def _print_final_report(self, progress: BatchProgress):
        """Print final batch report."""
        elapsed = time.time() - progress.start_time

        logger.info(f"\n{'='*70}")
        logger.info("🎉 BATCH PROCESSING COMPLETE")
        logger.info(f"{'='*70}\n")

        logger.info(f"📊 Final Statistics:")
        logger.info(f"   Total topics: {progress.total_topics}")
        logger.info(f"   ✅ Completed: {progress.completed}")
        logger.info(f"   ❌ Failed: {progress.failed}")
        logger.info(f"   🌟 CELESTIAL tier: {progress.celestial_count} "
                   f"({progress.celestial_count/progress.completed*100 if progress.completed > 0 else 0:.1f}%)")

        logger.info(f"\n📝 Content Statistics:")
        logger.info(f"   Total words: {progress.total_words:,}")
        logger.info(f"   Avg words/entry: {progress.total_words // progress.completed if progress.completed > 0 else 0:,}")

        logger.info(f"\n⏱️  Time Statistics:")
        logger.info(f"   Total time: {elapsed/3600:.2f} hours")
        logger.info(f"   Avg time/entry: {progress.total_time / progress.completed if progress.completed > 0 else 0:.1f}s")
        logger.info(f"   Entries/hour: {progress.completed / (elapsed/3600) if elapsed > 0 else 0:.1f}")

        logger.info(f"\n{'='*70}\n")
