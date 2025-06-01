"""
Kimera Web Interface
===================

A simple web interface for exploring Kimera's capabilities.
"""

from flask import Flask, render_template, request, jsonify
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from kimera.api import Kimera

app = Flask(__name__)
kimera = Kimera()

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/api/resonance', methods=['POST'])
def api_resonance():
    """API endpoint for resonance detection."""
    data = request.json
    text1 = data.get('text1', '')
    text2 = data.get('text2', '')
    
    if not text1 or not text2:
        return jsonify({'error': 'Both texts are required'}), 400
    
    try:
        result = kimera.find_resonance(text1, text2)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contradiction', methods=['POST'])
def api_contradiction():
    """API endpoint for contradiction detection."""
    data = request.json
    text1 = data.get('text1', '')
    text2 = data.get('text2', '')
    
    if not text1 or not text2:
        return jsonify({'error': 'Both texts are required'}), 400
    
    try:
        result = kimera.detect_contradiction(text1, text2)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patterns', methods=['POST'])
def api_patterns():
    """API endpoint for pattern extraction."""
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    
    try:
        patterns = kimera.extract_patterns(text)
        return jsonify({'patterns': patterns})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/insights', methods=['POST'])
def api_insights():
    """API endpoint for cross-domain insights."""
    data = request.json
    concept = data.get('concept', '')
    knowledge_base = data.get('knowledge_base', [])
    threshold = data.get('threshold', 0.5)
    
    if not concept or not knowledge_base:
        return jsonify({'error': 'Concept and knowledge base are required'}), 400
    
    try:
        insights = kimera.find_cross_domain_insights(concept, knowledge_base, threshold)
        return jsonify({'insights': insights})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = Path(__file__).parent / 'templates'
    templates_dir.mkdir(exist_ok=True)
    
    print("Starting Kimera Web Interface...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)