# 🌟 Celestial Engine v2.0

**Advanced Theological Entry Generation System**

An entirely new, optimized generation engine for creating CELESTIAL-tier Orthodox Christian theological entries using local LLMs. Built from the ground up to maximize quality, efficiency, and automation.

## ✨ Features

### Core Capabilities
- **🎯 Advanced Preprocessing**: Intelligent topic analysis and resource suggestion
- **🧠 Multi-Model Orchestration**: Uses different models optimized for different sections
- **📊 Comprehensive Validation**: 5 weighted criteria + 4 quality metrics
- **🔄 Iterative Refinement**: Automatically improves entries until CELESTIAL tier achieved
- **⚡ Batch Processing**: Parallel generation of multiple entries with checkpointing
- **📈 Full Monitoring**: Real-time progress tracking and detailed statistics
- **🎨 Intelligent Prompting**: Context-aware prompts optimized for each section

### Quality Standards
- **Target**: CELESTIAL tier (95-100 score) for every entry
- **Validation Criteria**:
  - Word Count (20%): 11,000+ words, balanced sections
  - Theological Depth (30%): 20+ Patristic citations, 5+ unique Fathers
  - Coherence (25%): Logical flow, cross-references, narrative cohesion
  - Section Balance (15%): All sections meet minimums
  - Orthodox Perspective (10%): Clear framing, Western contrasts, liturgical connections

### Advanced Features
- **Preprocessing Analysis**: Keywords, complexity scoring, resource suggestions
- **Resource Database Integration**: Patristic works, Scripture, theological terms
- **Automated Refinement Strategies**: 5 distinct strategies for improvement
- **Checkpoint System**: Resume interrupted batch processing
- **JSON Metadata**: Full entry metadata for analysis
- **Progress Tracking**: Real-time monitoring of generation progress

## 🚀 Quick Start

### Prerequisites
- **Hardware**: ROG Zephyrus Duo 4090 (or equivalent with NVIDIA RTX 4090, 16GB VRAM, 64GB RAM)
- **OS**: Ubuntu 22.04 LTS (or Windows 11)
- **Software**: Python 3.10+, Ollama installed

### Installation

1. **Clone the repository**:
```bash
cd /path/to/Opus-2
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
# OR install the package
pip install -e .
```

3. **Install and configure Ollama**:
```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
sudo systemctl start ollama
sudo systemctl enable ollama

# Pull required models (this takes time - models are large!)
ollama pull mixtral:8x7b-instruct-v0.1-q6_K
ollama pull llama3.1:70b-instruct-q4_K_M
```

4. **Verify setup**:
```bash
python -m celestial_engine.cli.main verify
# OR if installed:
celestial verify
```

Expected output:
```
🔍 Verifying Celestial Engine setup...

✅ Ollama is running

📦 Model Status:
  ✅ primary: mixtral:8x7b-instruct-v0.1-q6_K
  ✅ advanced: llama3.1:70b-instruct-q4_K_M
  ✅ preprocessor: mixtral:8x7b-instruct-v0.1-q6_K
  ✅ validator: llama3.1:70b-instruct-q4_K_M

🎉 All systems ready!
```

### First Generation

Generate your first CELESTIAL-tier entry:

```bash
python -m celestial_engine.cli.main generate "The Divine Infinity and the Mathematical Continuum"
```

This will:
1. ✅ Analyze the topic and suggest resources (preprocessing)
2. ✅ Generate all 6 sections using optimized prompts
3. ✅ Validate against CELESTIAL standards
4. ✅ Refine iteratively until target achieved
5. ✅ Save entry as Markdown + JSON metadata

Expected time: 45-90 minutes depending on complexity

## 📚 Usage Guide

### Command-Line Interface

The Celestial Engine provides a comprehensive CLI:

#### Generate Single Entry
```bash
# Basic generation
celestial generate "Topic Here"

# With options
celestial generate "Topic Here" \
  --output custom_output.md \
  --skip-preprocessing \
  --max-refinements 3 \
  --save-json
```

#### Batch Generation
```bash
# Create topics file
cat > topics.txt << EOF
The Nature of Divine Simplicity
Theosis and Human Transformation
The Uncreated Energies of God
EOF

# Process batch
celestial batch topics.txt \
  --workers 3 \
  --output-dir data/entries \
  --checkpoint-interval 5
```

#### Validate Entry
```bash
celestial validate path/to/entry.md --verbose
```

#### Show Statistics
```bash
celestial stats --entries-dir data/entries
```

#### Verify Setup
```bash
celestial verify
```

### Python API

Use Celestial Engine programmatically:

```python
from celestial_engine import CelestialGenerator, get_config

# Initialize
generator = CelestialGenerator()

# Generate entry
entry = generator.generate(
    topic="The Essence-Energies Distinction",
    skip_preprocessing=False,
    max_refinements=5
)

# Access results
print(f"Tier: {entry.validation_result.tier.value}")
print(f"Score: {entry.validation_result.overall_score:.1f}/100")
print(f"Words: {entry.total_words:,}")

# Save
entry.save(Path("output/"))
```

### Configuration

Edit `celestial_engine/config/engine_config.yaml` to customize:

- **LLM Settings**: Model names, parameters, timeouts
- **Entry Structure**: Section word counts, requirements
- **Validation Criteria**: Weights, thresholds
- **Refinement Strategies**: Triggers, priorities, actions
- **Batch Processing**: Workers, checkpoints, resource limits
- **Monitoring**: Log levels, metrics, alerts

## 🏗️ Architecture

```
celestial_engine/
├── core/
│   ├── models.py           # Data models (Entry, Section, ValidationResult)
│   ├── config.py           # Configuration management
│   ├── llm_interface.py    # Ollama API interface
│   └── generator.py        # Main generation orchestrator
├── preprocessing/
│   └── topic_analyzer.py   # Topic analysis and resource suggestion
├── prompts/
│   └── templates.py        # Intelligent prompt templates
├── validation/
│   └── validator.py        # Comprehensive validation system
├── refinement/
│   └── refiner.py          # Iterative refinement engine
├── batch/
│   └── processor.py        # Parallel batch processing
├── monitoring/
│   └── logger.py           # Logging and progress tracking
├── cli/
│   └── main.py             # Command-line interface
└── config/
    └── engine_config.yaml  # Main configuration
```

## 🎯 Generation Workflow

### Phase 1: Preprocessing (5 minutes)
- Extract keywords from topic
- Assess complexity (0-1 scale)
- Identify theological themes
- Suggest Church Fathers and works
- Suggest Scripture passages
- Identify potential tensions
- Generate structured outline

### Phase 2: Section Generation (30-60 minutes)
For each of 6 sections:
1. Select appropriate model (primary or advanced)
2. Generate context-aware prompt with preprocessing insights
3. Generate section content
4. Verify word count, expand if needed
5. Proceed to next section

**Sections:**
- Introduction (1,750 words)
- The Patristic Mind (2,250 words)
- Symphony of Clashes (2,350 words) [Advanced Model]
- Orthodox Affirmation (2,250 words)
- Synthesis (1,900 words) [Advanced Model]
- Conclusion (1,800 words)

### Phase 3: Validation (2 minutes)
- Calculate 5 criterion scores (word count, depth, coherence, balance, perspective)
- Calculate 4 quality metrics (diversity, specificity, integration, distribution)
- Determine overall score and tier
- Generate detailed feedback

### Phase 4: Refinement (15-60 minutes if needed)
If score < 95:
1. Identify applicable refinement strategies
2. Execute strategies in priority order:
   - Enhance theological depth
   - Expand sections
   - Improve coherence
   - Balance sections
   - Strengthen Orthodox perspective
3. Re-validate
4. Repeat until CELESTIAL or max iterations

### Phase 5: Completion
- Save Markdown entry
- Save JSON metadata
- Log statistics
- Report results

## 📊 Quality Metrics Explained

### Diversity Score (30% weight)
- **Measures**: Breadth of Patristic sources cited
- **Target**: 5+ unique Church Fathers
- **Threshold**: ≥ 80 (4+ Fathers)
- **Why**: Orthodox theology is consensus of Patristic witness, not individual opinions

### Specificity Score (25% weight)
- **Measures**: Named Patristic works cited
- **Target**: 3+ specific works
- **Threshold**: ≥ 70 (2+ works)
- **Why**: Demonstrates engagement with actual texts, enables verification

### Integration Score (20% weight)
- **Measures**: Distribution of citations across sections
- **Target**: Low variance (< 2 std dev)
- **Threshold**: ≥ 70
- **Why**: Patristic wisdom should illuminate all aspects, not be compartmentalized

### Distribution Score (25% weight)
- **Measures**: Patristic content present across sections
- **Target**: 5-6 sections with Patristic content
- **Threshold**: ≥ 85 (4+ sections)
- **Why**: Entire entry should breathe Patristic air

## 🔧 Advanced Configuration

### Custom Model Configuration

Edit `config/engine_config.yaml`:

```yaml
llm:
  models:
    primary:
      name: "your-model-name"
      params:
        temperature: 0.7
        top_p: 0.9
        # ... other params
```

### Custom Section Structure

```yaml
entry:
  sections:
    - name: "Your Section"
      slug: "your_section"
      min_words: 2000
      target_words: 2500
      model: "primary"
      requirements:
        - "Your requirement 1"
        - "Your requirement 2"
```

### Custom Refinement Strategies

```yaml
refinement:
  strategies:
    - name: "your_strategy"
      priority: 1
      triggers:
        - "your_trigger_condition"
      actions:
        - "action_1"
        - "action_2"
```

## 📈 Performance Optimization

### Hardware Optimization

**GPU Settings**:
```bash
# Set persistence mode
sudo nvidia-smi -pm 1

# Set maximum power
sudo nvidia-smi -pl 175

# Lock clocks (optional)
sudo nvidia-smi -lgc 2040
sudo nvidia-smi -lmc 9001
```

**CPU Settings**:
```bash
# Set performance governor
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

### Generation Optimization

**Speed vs Quality Tradeoffs**:

1. **Fast (30-45 min/entry)**: Skip preprocessing, lower refinement iterations
```bash
celestial generate "Topic" --skip-preprocessing --max-refinements 2
```

2. **Balanced (45-75 min/entry)**: Default settings
```bash
celestial generate "Topic"
```

3. **Maximum Quality (75-120 min/entry)**: Extended refinement
```bash
celestial generate "Topic" --max-refinements 8
```

### Batch Optimization

**Parallel Workers**:
- 1 worker: 100% GPU utilization, sequential
- 3 workers: ~85% GPU utilization, 2.5x throughput
- 5 workers: ~70% GPU utilization, 3.5x throughput (high memory)

**Recommended**:
```bash
# For 64GB RAM: 3 workers
celestial batch topics.txt --workers 3

# For 32GB RAM: 1-2 workers
celestial batch topics.txt --workers 1
```

## 📊 Expected Results

### Single Entry Statistics
- **Generation Time**: 45-90 minutes
- **Total Words**: 12,500-16,000
- **Patristic Citations**: 20-30
- **Unique Fathers**: 5-10
- **Scripture References**: 15-25
- **Target Achievement**: 95-100% for CELESTIAL

### Batch Processing (3 workers)
- **Throughput**: 10-15 entries per 24 hours
- **CELESTIAL Rate**: 90-95%
- **12,000 entries**: 800-1,200 days

### Quality Distribution (Expected)
- CELESTIAL (95-100): 90-95%
- ADAMANTINE (90-94): 5-10%
- Lower tiers: <1%

## 🐛 Troubleshooting

### Ollama Connection Errors
```bash
# Check if Ollama is running
systemctl status ollama

# Restart Ollama
sudo systemctl restart ollama

# Check port
curl http://127.0.0.1:11434/api/tags
```

### Out of Memory Errors
```bash
# Reduce parallel workers
celestial batch topics.txt --workers 1

# Use lighter quantization
# Edit config to use q4_K_M instead of q6_K
```

### Low Scores
- Check preprocessing output (is topic well-analyzed?)
- Increase refinement iterations
- Review validation feedback
- Consider manual prompt tuning

### Slow Generation
- Check GPU temperature (should be < 85°C)
- Verify GPU clocks (use nvidia-smi)
- Check system load (top/htop)
- Reduce parallel workers if high memory usage

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Additional refinement strategies
- Enhanced preprocessing algorithms
- Alternative validation metrics
- Web interface
- Distributed generation across multiple GPUs
- Integration with citation databases

## 📄 License

MIT License - see LICENSE file

## 🙏 Acknowledgments

Built upon the foundation of the PRODUCTION_Guide.md system, with entirely new architecture optimized for quality, automation, and efficiency.

## 📧 Support

For issues or questions:
- Open an issue on GitHub
- Check troubleshooting section above
- Review logs in `data/logs/`

---

**🌟 Generate CELESTIAL-tier theological entries with unprecedented quality and efficiency 🌟**
