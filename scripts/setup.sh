#!/bin/bash

# Celestial Engine Setup Script
# Automated setup for Ubuntu/Debian systems

set -e

echo "🌟 Celestial Engine Setup Script"
echo "=================================="
echo ""

# Check if running as root for some operations
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  Note: Some operations may require sudo password"
fi

echo "📦 Step 1: Installing Python dependencies..."
pip install -r requirements.txt
echo "✅ Python dependencies installed"
echo ""

echo "🔧 Step 2: Installing Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "Downloading and installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    echo "✅ Ollama installed"
else
    echo "✅ Ollama already installed"
fi
echo ""

echo "🚀 Step 3: Starting Ollama service..."
sudo systemctl start ollama
sudo systemctl enable ollama
sleep 2
echo "✅ Ollama service started"
echo ""

echo "📥 Step 4: Pulling required models (this will take a while)..."
echo "   This step downloads large model files (~50GB total)"
echo "   Primary model: mixtral:8x7b-instruct-v0.1-q6_K (~35GB)"
echo "   Advanced model: llama3.1:70b-instruct-q4_K_M (~40GB)"
echo ""

# Pull primary model
echo "Pulling primary model (mixtral 8x7b)..."
ollama pull mixtral:8x7b-instruct-v0.1-q6_K
echo "✅ Primary model downloaded"
echo ""

# Pull advanced model
echo "Pulling advanced model (llama3.1 70b)..."
ollama pull llama3.1:70b-instruct-q4_K_M
echo "✅ Advanced model downloaded"
echo ""

echo "📁 Step 5: Creating directories..."
mkdir -p celestial_engine/data/entries
mkdir -p celestial_engine/data/logs
mkdir -p celestial_engine/data/cache
mkdir -p celestial_engine/data/checkpoints
echo "✅ Directories created"
echo ""

echo "⚡ Step 6: Optimizing GPU settings (requires sudo)..."
sudo nvidia-smi -pm 1 2>/dev/null || echo "⚠️  Could not set GPU persistence mode"
sudo nvidia-smi -pl 175 2>/dev/null || echo "⚠️  Could not set GPU power limit"
echo "✅ GPU settings optimized"
echo ""

echo "🔍 Step 7: Verifying installation..."
python -m celestial_engine.cli.main verify
echo ""

echo "🎉 Setup Complete!"
echo ""
echo "Next steps:"
echo "  1. Test generation:"
echo "     python -m celestial_engine.cli.main generate \"The Trinity\""
echo ""
echo "  2. Start batch processing:"
echo "     python -m celestial_engine.cli.main batch topics.txt"
echo ""
echo "  3. Check stats:"
echo "     python -m celestial_engine.cli.main stats"
echo ""
echo "📖 See README_CELESTIAL_ENGINE.md for full documentation"
