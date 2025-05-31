#!/usr/bin/env python3
"""
Test the explorer with sample data
"""
import csv
import webbrowser
import os
from pathlib import Path

def create_sample_data():
    """Create sample data in the format our benchmark produces"""
    sample_data = [
        {
            "pair_id": 1,
            "text1": "Birds can fly",
            "text2": "Birds cannot fly", 
            "kimera_contradiction": True,
            "kimera_confidence": 0.85,
            "kimera_reasoning": "Negation detected",
            "gpt4o_contradiction": True,
            "gpt4o_confidence": 0.90,
            "gpt4o_reasoning": "Clear contradiction",
            "agreement": True
        },
        {
            "pair_id": 2,
            "text1": "Snow is white",
            "text2": "Snow is black",
            "kimera_contradiction": False,
            "kimera_confidence": 0.65,
            "kimera_reasoning": "Color difference",
            "gpt4o_contradiction": True,
            "gpt4o_confidence": 0.95,
            "gpt4o_reasoning": "Opposite colors",
            "agreement": False
        },
        {
            "pair_id": 3,
            "text1": "The sky is blue",
            "text2": "The ocean is blue",
            "kimera_contradiction": False,
            "kimera_confidence": 0.75,
            "kimera_reasoning": "Similar color",
            "gpt4o_contradiction": False,
            "gpt4o_confidence": 0.80,
            "gpt4o_reasoning": "No contradiction",
            "agreement": True
        },
        {
            "pair_id": 4,
            "text1": "I like cats",
            "text2": "I don't like cats",
            "kimera_contradiction": True,
            "kimera_confidence": 0.90,
            "kimera_reasoning": "Negation penalty applied",
            "gpt4o_contradiction": True,
            "gpt4o_confidence": 0.95,
            "gpt4o_reasoning": "Direct contradiction",
            "agreement": True
        },
        {
            "pair_id": 5,
            "text1": "Water boils at 100°C",
            "text2": "Water boils at 50°C",
            "kimera_contradiction": False,
            "kimera_confidence": 0.60,
            "kimera_reasoning": "Similar structure",
            "gpt4o_contradiction": True,
            "gpt4o_confidence": 0.85,
            "gpt4o_reasoning": "Different temperatures",
            "agreement": False
        }
    ]
    
    # Write to CSV
    filename = "sample_benchmark_results.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        if sample_data:
            writer = csv.DictWriter(f, fieldnames=sample_data[0].keys())
            writer.writeheader()
            writer.writerows(sample_data)
    
    print(f"✓ Created {filename} with {len(sample_data)} sample pairs")
    return filename

def test_explorer():
    """Test the explorer with sample data"""
    print("🔍 Testing Kimera Explorer")
    print("=" * 30)
    
    # Create sample data
    sample_file = create_sample_data()
    
    # Check if explorer exists
    explorer_path = Path("tools/explorer.html")
    if not explorer_path.exists():
        print("❌ Explorer not found at tools/explorer.html")
        return
    
    print(f"✓ Explorer found at {explorer_path}")
    print(f"✓ Sample data created: {sample_file}")
    
    # Try to open in browser
    try:
        full_path = explorer_path.absolute()
        webbrowser.open(f"file://{full_path}")
        print("✓ Explorer opened in browser")
        
        print("\n📋 Instructions:")
        print("1. Click '📁 Load CSV' in the explorer")
        print(f"2. Select the file: {sample_file}")
        print("3. Check the 'Only disagreements' box to see conflicts")
        print("4. Add notes to interesting cases")
        print("5. Click '📤 Export Notes' to save your analysis")
        
        print("\n🎯 Expected Results:")
        print("- 5 total pairs loaded")
        print("- 2 disagreements when 'Only disagreements' is checked")
        print("- Debug info showing column mapping")
        print("- Green rows = agreement, Red rows = disagreement")
        
    except Exception as e:
        print(f"❌ Could not open browser: {e}")
        print(f"📂 Manually open: {explorer_path.absolute()}")

if __name__ == "__main__":
    test_explorer()