#!/bin/bash

# Quick test script to verify Celestial Engine works

echo "🧪 Celestial Engine Quick Test"
echo "==============================="
echo ""

echo "1️⃣  Verifying setup..."
python -m celestial_engine.cli.main verify
echo ""

echo "2️⃣  Generating test entry (this takes 45-90 minutes)..."
echo "   Topic: 'The Uncreated Light of Mount Tabor'"
echo ""

python -m celestial_engine.cli.main generate \
    "The Uncreated Light of Mount Tabor" \
    --output test_entry.md \
    --save-json

echo ""
echo "3️⃣  Displaying results..."
if [ -f "test_entry.md" ]; then
    echo "✅ Entry generated successfully!"
    echo ""
    echo "📊 Entry statistics:"
    wc -w test_entry.md | awk '{print "   Words: " $1}'
    echo ""
    echo "📄 First 50 lines:"
    head -n 50 test_entry.md
    echo ""
    echo "✨ Full entry saved to: test_entry.md"
    echo "📄 Metadata saved to: test_entry.json"
else
    echo "❌ Entry generation failed!"
    exit 1
fi

echo ""
echo "🎉 Test complete! Celestial Engine is working correctly."
