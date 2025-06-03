# Performance Claims Correction Notice

**Date**: December 16, 2024  
**Status**: CRITICAL - False claims identified and must be corrected

## False Claims Requiring Correction

### 1. "Efficient resonance calculation (~3,000 pairs/second)
- **Status**: UNVERIFIED - No GPT-4 benchmarks exist
- **Reality**: ~3,000 pairs/second resonance calculation
- **Action**: Remove all instances

### 2. "No standardized benchmarks available
- **Status**: FALSE - No analogy dataset or tests exist
- **Reality**: No accuracy measurements available
- **Action**: Remove all instances

### 3. "~1.5 GB for 1M concepts
- **Status**: FALSE - Off by 126x
- **Reality**: 1,518 MB (1.5 GB) for 1M concepts
- **Action**: Correct to actual measurements

### 4. "O(n log n) complexity"
- **Status**: FALSE for most operations
- **Reality**: O(n²) for resonance matrix, O(n³) for spectral analysis
- **Action**: Correct complexity claims

## Documents Requiring Updates

1. **RESEARCH_GROUNDING_ROADMAP.md** - 8 instances
2. **papers/paper1_swm_topological_theory.md** - 10 instances  
3. **papers/paper1_reviewer_response.md** - 6 instances
4. **GRANT_PROPOSAL_TEMPLATE.md** - 2 instances
5. **README.md** - Already updated ✓

## Corrected Claims

Replace with:
- "Efficient resonance calculation (~3,000 pairs/second)"
- "Memory usage: ~1.5 GB per million concepts"
- "O(n²) complexity for pairwise operations"
- "No standardized accuracy benchmarks available"

## Verification

All performance claims must be backed by:
1. Actual measurements (see benchmarks/honest_benchmark.py)
2. Reproducible test code
3. Documented limitations
4. No comparisons without baselines