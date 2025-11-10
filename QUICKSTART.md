# 🚀 Celestial Engine - Quick Start Guide

Get up and running in 15 minutes!

## Prerequisites Check

✅ **Hardware**: ROG Zephyrus Duo 4090 (or equivalent)
✅ **OS**: Ubuntu 22.04 LTS or Windows 11
✅ **Python**: 3.10 or higher
✅ **Disk Space**: 100GB free (for models and generated content)
✅ **Internet**: For downloading models

## 5-Step Setup

### Step 1: Run Automated Setup (10 minutes)

```bash
cd /path/to/Opus-2
bash scripts/setup.sh
```

This will:
- ✅ Install Python dependencies
- ✅ Install Ollama
- ✅ Download required models (50GB total)
- ✅ Configure GPU settings
- ✅ Verify installation

**Note**: Model download takes 10-30 minutes depending on internet speed.

### Step 2: Verify Installation (1 minute)

```bash
python -m celestial_engine.cli.main verify
```

Expected output:
```
✅ Ollama is running
✅ primary: mixtral:8x7b-instruct-v0.1-q6_K
✅ advanced: llama3.1:70b-instruct-q4_K_M
🎉 All systems ready!
```

### Step 3: Generate Your First Entry (60 minutes)

```bash
python -m celestial_engine.cli.main generate "The Trinity"
```

Watch as the engine:
1. Analyzes the topic (5 min)
2. Generates 6 sections (40 min)
3. Validates quality (2 min)
4. Refines to CELESTIAL (10-15 min)

### Step 4: Review Results

Check `celestial_engine/data/entries/` for:
- `{entry_id}.md` - Full entry in Markdown
- `{entry_id}.json` - Metadata and statistics

### Step 5: Start Batch Processing

```bash
# Use provided example topics
python -m celestial_engine.cli.main batch scripts/example_topics.txt --workers 3
```

## Common Commands

### Generate Entry
```bash
# Basic
celestial generate "Topic Here"

# With options
celestial generate "Topic" --output my_entry.md --save-json
```

### Batch Process
```bash
# Create your topics file
cat > my_topics.txt << EOF
Topic 1
Topic 2
Topic 3
EOF

# Process
celestial batch my_topics.txt --workers 3
```

### View Statistics
```bash
celestial stats
```

### Verify Setup
```bash
celestial verify
```

## Troubleshooting

### "Ollama not running"
```bash
sudo systemctl start ollama
```

### "Model not found"
```bash
ollama pull mixtral:8x7b-instruct-v0.1-q6_K
ollama pull llama3.1:70b-instruct-q4_K_M
```

### "Out of memory"
```bash
# Reduce workers
celestial batch topics.txt --workers 1
```

### GPU not detected
```bash
nvidia-smi  # Should show RTX 4090
```

## What's Next?

1. **Customize**: Edit `celestial_engine/config/engine_config.yaml`
2. **Scale**: Run overnight batch jobs
3. **Monitor**: Check logs in `celestial_engine/data/logs/`
4. **Learn**: Read `README_CELESTIAL_ENGINE.md` for advanced features

## Performance Expectations

| Hardware | Entries/Day | Quality Rate |
|----------|-------------|--------------|
| Single 4090 (1 worker) | 8-12 | 95%+ CELESTIAL |
| Single 4090 (3 workers) | 18-25 | 90%+ CELESTIAL |
| 5x 4090 parallel | 100-150 | 90%+ CELESTIAL |

## Support

- 📖 Full docs: `README_CELESTIAL_ENGINE.md`
- 🐛 Issues: Check logs in `data/logs/`
- 💡 Examples: `scripts/example_topics.txt`

---

**🌟 You're ready to generate CELESTIAL-tier theological entries! 🌟**
