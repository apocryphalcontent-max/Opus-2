"""
Command-line interface for the Celestial Engine.
Provides easy access to generation, validation, and batch processing.
"""

import click
import logging
import sys
from pathlib import Path
from typing import Optional

from ..core.config import get_config
from ..core.generator import CelestialGenerator
from ..core.llm_interface import get_llm
from ..validation.validator import EntryValidator
from ..batch.processor import BatchProcessor
from ..monitoring.logger import setup_logging


@click.group()
@click.option('--config', type=click.Path(exists=True), help='Path to configuration file')
@click.option('--log-level', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR']), default='INFO')
def cli(config, log_level):
    """Celestial Engine - Advanced theological entry generation system."""
    # Setup logging
    setup_logging(log_level)

    # Load config if provided
    if config:
        get_config(Path(config))


@cli.command()
@click.argument('topic')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--skip-preprocessing', is_flag=True, help='Skip preprocessing phase')
@click.option('--max-refinements', type=int, help='Maximum refinement iterations')
@click.option('--save-json', is_flag=True, help='Also save JSON metadata')
def generate(topic, output, skip_preprocessing, max_refinements, save_json):
    """Generate a single CELESTIAL-tier entry."""
    click.echo(f"🌟 Generating CELESTIAL-tier entry for: {topic}\n")

    try:
        generator = CelestialGenerator()
        entry = generator.generate(
            topic=topic,
            skip_preprocessing=skip_preprocessing,
            max_refinements=max_refinements
        )

        # Save entry
        config = get_config()
        if output:
            output_path = Path(output)
        else:
            output_path = config.entries_dir / f"{entry.entry_id}.md"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save markdown
        output_path.write_text(entry.to_markdown())
        click.echo(f"\n✅ Entry saved to: {output_path}")

        # Save JSON if requested
        if save_json:
            json_path = output_path.with_suffix('.json')
            import json
            json_path.write_text(json.dumps(entry.to_dict(), indent=2))
            click.echo(f"📄 Metadata saved to: {json_path}")

        # Display results
        validation = entry.validation_result
        click.echo(f"\n{'='*60}")
        click.echo(f"🌟 Quality Tier: {validation.tier.value}")
        click.echo(f"📊 Overall Score: {validation.overall_score:.1f}/100")
        click.echo(f"📝 Total Words: {entry.total_words:,}")
        click.echo(f"🔄 Refinement Iterations: {entry.refinement_iterations}")
        click.echo(f"⏱️  Generation Time: {entry.generation_time_seconds:.1f}s")
        click.echo(f"{'='*60}\n")

        if validation.tier.value == "CELESTIAL":
            click.echo("🎉 CELESTIAL tier achieved!")
        else:
            click.echo(f"⚠️  Warning: Entry did not reach CELESTIAL tier")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('entry_path', type=click.Path(exists=True))
@click.option('--verbose', '-v', is_flag=True, help='Show detailed feedback')
def validate(entry_path, verbose):
    """Validate an existing entry."""
    click.echo(f"📋 Validating entry: {entry_path}\n")

    try:
        # Load entry (simplified - would need full entry loading logic)
        from ..core.models import Entry
        entry_text = Path(entry_path).read_text()

        # Parse entry - simplified
        click.echo("⚠️  Note: Full entry parsing not yet implemented")
        click.echo("This command validates markdown files once parsing is implemented")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('topics_file', type=click.Path(exists=True))
@click.option('--workers', '-w', type=int, default=1, help='Number of parallel workers')
@click.option('--output-dir', '-o', type=click.Path(), help='Output directory')
@click.option('--checkpoint-interval', type=int, default=10, help='Checkpoint every N entries')
def batch(topics_file, workers, output_dir, checkpoint_interval):
    """Generate multiple entries from a topics file."""
    click.echo(f"🚀 Starting batch generation from: {topics_file}\n")

    try:
        # Load topics
        topics = Path(topics_file).read_text().strip().split('\n')
        topics = [t.strip() for t in topics if t.strip() and not t.startswith('#')]

        click.echo(f"📝 Loaded {len(topics)} topics")
        click.echo(f"⚙️  Workers: {workers}")
        click.echo(f"💾 Checkpoint interval: {checkpoint_interval}\n")

        # Setup batch processor
        processor = BatchProcessor(
            parallel_workers=workers,
            checkpoint_interval=checkpoint_interval
        )

        # Process topics
        processor.process_batch(
            topics=topics,
            output_dir=Path(output_dir) if output_dir else None
        )

        click.echo(f"\n✅ Batch processing complete!")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def verify():
    """Verify Ollama setup and model availability."""
    click.echo("🔍 Verifying Celestial Engine setup...\n")

    try:
        llm = get_llm()
        results = llm.verify_setup()

        # Ollama status
        if results["ollama_running"]:
            click.echo("✅ Ollama is running")
        else:
            click.echo("❌ Ollama is not running or not accessible")
            click.echo("   Start with: sudo systemctl start ollama")
            sys.exit(1)

        # Model availability
        click.echo("\n📦 Model Status:")
        for model_type, info in results["models_available"].items():
            status = "✅" if info["available"] else "❌"
            click.echo(f"  {status} {model_type}: {info['name']}")

        # Overall status
        if results["all_ready"]:
            click.echo("\n🎉 All systems ready!")
        else:
            click.echo("\n⚠️  Some models are missing. Download with:")
            for model_type, info in results["models_available"].items():
                if not info["available"]:
                    click.echo(f"  ollama pull {info['name']}")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--entries-dir', type=click.Path(), help='Entries directory to analyze')
def stats(entries_dir):
    """Show statistics about generated entries."""
    click.echo("📊 Entry Statistics\n")

    try:
        config = get_config()
        entries_path = Path(entries_dir) if entries_dir else config.entries_dir

        if not entries_path.exists():
            click.echo(f"❌ Directory not found: {entries_path}")
            sys.exit(1)

        # Count entries
        md_files = list(entries_path.glob("*.md"))
        json_files = list(entries_path.glob("*.json"))

        click.echo(f"📝 Total entries: {len(md_files)}")
        click.echo(f"📄 JSON metadata files: {len(json_files)}")

        # Analyze JSON files for detailed stats
        if json_files:
            import json

            tiers = {}
            total_words = 0
            total_time = 0

            for json_file in json_files:
                data = json.loads(json_file.read_text())
                tier = data.get("validation_result", {}).get("tier", "UNKNOWN")
                tiers[tier] = tiers.get(tier, 0) + 1
                total_words += data.get("total_words", 0)
                total_time += data.get("generation_time_seconds", 0)

            click.echo(f"\n🏆 Quality Distribution:")
            for tier, count in sorted(tiers.items(), reverse=True):
                percentage = (count / len(json_files)) * 100
                click.echo(f"  {tier}: {count} ({percentage:.1f}%)")

            click.echo(f"\n📊 Averages:")
            click.echo(f"  Words per entry: {total_words / len(json_files):,.0f}")
            click.echo(f"  Generation time: {total_time / len(json_files):.1f}s")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--port', type=int, default=8000, help='Server port')
def serve(port):
    """Start web interface (future feature)."""
    click.echo(f"🌐 Starting web interface on port {port}...")
    click.echo("⚠️  Web interface not yet implemented")
    click.echo("Use CLI commands for now")


if __name__ == '__main__':
    cli()
