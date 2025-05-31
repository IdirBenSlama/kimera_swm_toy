# Kimera Contradiction Explorer

Interactive HTML tool for analyzing benchmark results and identifying error patterns.

## Quick Start

1. **Run a benchmark** to generate CSV data:
   ```bash
   poetry run python -m benchmarks.llm_compare data/contradictions_2k.csv --max-pairs 500 --kimera-only
   ```

2. **Open the explorer**:
   - Double-click `explorer.html` to open in your browser
   - Or: `python -m http.server 8000` then visit `http://localhost:8000/tools/explorer.html`

3. **Load your data**:
   - Click "📁 Load CSV" and select `benchmark_results.csv`
   - The tool expects columns: `text1`, `text2`, `lang`, `kimera_pred`, `kimera_conf`, `gpt_pred`

4. **Filter and explore**:
   - **Language**: Filter by `en`, `fr`, `ar`, etc.
   - **Length**: Short (<50 chars), Medium (50-150), Long (>150)
   - **Disagreements**: Show only cases where Kimera ≠ GPT

5. **Annotate interesting cases**:
   - Click in the "Notes" column to add observations
   - Examples: "GPT hallucinated", "Kimera missed negation", "Both wrong"

6. **Export your findings**:
   - Click "📥 Export Notes" to download `kimera_notes_YYYY-MM-DD.csv`
   - Contains only rows with notes for further analysis

## Example Workflow

```bash
# 1. Generate benchmark data
poetry run python -m benchmarks.llm_compare data/contradictions_2k.csv --max-pairs 200 --stats

# 2. Open explorer.html in browser

# 3. Load benchmark_results.csv

# 4. Filter to "Only disagreements" 

# 5. Add notes like:
#    - "Kimera confused by double negation"
#    - "GPT failed on Arabic text"
#    - "Both missed sarcasm"

# 6. Export notes for pattern analysis
```

## Expected CSV Format

The tool works with any CSV containing these columns:

| Column | Description | Required |
|--------|-------------|----------|
| `text1` | First text in pair | ✅ |
| `text2` | Second text in pair | ✅ |
| `lang` | Language code (en, fr, ar) | ✅ |
| `kimera_pred` | Kimera prediction (0/1) | ✅ |
| `kimera_conf` | Kimera confidence (0.0-1.0) | ✅ |
| `gpt_pred` | GPT prediction (0/1) | Optional |

## Features

- **🔍 Smart filtering** by language, length, and agreement
- **📊 Live statistics** showing disagreement rates
- **✏️ Inline annotation** with contenteditable notes
- **📥 CSV export** of annotated cases
- **🎨 Color coding** (green=agree, red=disagree)
- **📱 Responsive design** works on mobile

## Use Cases

### Error Pattern Discovery
Filter to disagreements and look for patterns:
- Do long texts cause more errors?
- Are certain languages problematic?
- What types of contradictions are missed?

### Model Comparison
Compare Kimera vs GPT performance:
- Where does each model excel?
- What are the failure modes?
- Which confidence ranges are reliable?

### Dataset Quality Assessment
Identify problematic text pairs:
- Ambiguous contradictions
- Mislabeled examples
- Edge cases worth investigating

## Technical Notes

- **Pure client-side**: No server required, works offline
- **Simple CSV parsing**: Handles basic comma-separated values
- **Local storage**: Notes are lost on page refresh (export frequently!)
- **Browser compatibility**: Modern browsers (Chrome, Firefox, Safari, Edge)

## Next Steps

After collecting notes with the explorer:

1. **Pattern analysis**: Group similar error types
2. **Threshold tuning**: Adjust confidence thresholds per error bucket
3. **Model improvements**: Target specific failure modes
4. **Dataset curation**: Remove or relabel problematic cases