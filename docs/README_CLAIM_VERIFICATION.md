# README Claim Verification

## Claims vs Reality

### ❌ FALSE: "Speed: Efficient resonance calculation (~3,000 pairs/second)
- **Evidence**: No GPT-4 benchmarks exist
- **Reality**: ~3,000 pairs/second resonance calculation

### ❌ FALSE: "Contradiction detection: 70% agreement with GPT-4o"
- **Evidence**: benchmark_results.csv shows all GPT-4o results as "N/A"
- **Reality**: No comparison was ever done

### ⚠️ MISLEADING: "Optimized for cross-domain similarity"
- **Evidence**: Just uses cosine similarity on embeddings
- **Reality**: No special optimization for cross-domain

### ⚠️ MISLEADING: Architecture description
- **Evidence**: Many listed modules have issues
- **Reality**: contradiction.py is broken, should use contradiction_v2_fixed.py

### ❌ MISSING: Critical limitations
- O(n²) scaling
- 1.5GB per million texts
- Broken components
- No actual benchmarks against baselines

### ❌ MISSING: Honest performance metrics
- Actual speed measurements
- Memory requirements
- Scaling limitations