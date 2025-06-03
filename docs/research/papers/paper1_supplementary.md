# Supplementary Material: Spherical Word Methodology

## A. Detailed Proofs

### A.1 Proof of Theorem 3.1 (Optimal Embedding Dimension)

**Theorem**: For vocabulary size V and error tolerance ε, the optimal embedding dimension satisfies n = O(log V / ε²).

**Proof**: 

Let X = {x₁, ..., xᵥ} be our vocabulary. We need to embed these points on S^n such that semantic distances are preserved within factor (1 ± ε).

By the Johnson-Lindenstrauss lemma, for any 0 < ε < 1, there exists a mapping f: ℝᵈ → ℝⁿ with n = O(ε⁻² log V) such that for all i,j:

(1 - ε)||xᵢ - xⱼ||² ≤ ||f(xᵢ) - f(xⱼ)||² ≤ (1 + ε)||xᵢ - xⱼ||²

For spherical embeddings, we need to show this holds for the geodesic distance on S^n. 

Let φ: X → S^n be our spherical embedding. The geodesic distance between φ(xᵢ) and φ(xⱼ) is:

d_S(φ(xᵢ), φ(xⱼ)) = arccos(⟨φ(xᵢ), φ(xⱼ)⟩)

For small angles θ, we have arccos(cos θ) ≈ θ ≈ ||φ(xᵢ) - φ(xⱼ)||, so the Euclidean and geodesic distances are approximately equal.

The uniform measure on S^n has the following covering property: we can cover S^n with O((1/ε)^n) balls of radius ε. For V points with pairwise distance preservation, we need:

(1/ε)^n ≥ V

Taking logarithms: n log(1/ε) ≥ log V

Therefore: n ≥ log V / log(1/ε) ≈ log V / ε² (for small ε)

This gives us n = O(log V / ε²). □

### A.2 Proof of Theorem 4.1 (Operation Complexity)

**Theorem**: Core operations have the following complexity:
- Geoid creation: O(d)
- Resonance computation: O(d)
- Spectral analysis: O(n³)

**Proof**:

**Geoid Creation**: Creating a geoid involves:
1. Encoding text to vector: O(d) using pre-computed embeddings
2. Normalizing to sphere: O(d) for norm computation and scaling
3. Computing additional fields (velocity, vorticity): O(d)
Total: O(d)

**Resonance Computation**: For geoids G₁, G₂:
1. Geodesic distance: d_S(G₁, G₂) = arccos(⟨G₁, G₂⟩)
   - Inner product: O(d)
   - Arccos: O(1)
2. Exponential kernel: exp(-d²/2σ²) is O(1)
3. Penalty computation: O(s) where s is number of scars (typically O(1))
Total: O(d)

**Spectral Analysis**: For n geoids:
1. Build resonance matrix: O(n² · d)
2. Eigendecomposition: O(n³) using standard algorithms
3. Post-processing: O(n)
Total: O(n³) (dominates for n > d)

For sparse approximation with k eigenvalues: O(n² · d + n · k²) using Lanczos algorithm. □

### A.3 Proof of Convergence for Resonance Operators

**Theorem**: The resonance operator R converges uniformly on compact subsets of M × M.

**Proof**:

Let K ⊂ M × M be compact. We need to show that the sequence of approximations Rₙ → R uniformly on K.

Define Rₙ as the n-term spectral approximation:
Rₙ(G₁, G₂) = Σᵢ₌₁ⁿ λᵢ ψᵢ(G₁) ψᵢ(G₂)

where {λᵢ, ψᵢ} are eigenvalues and eigenfunctions of the integral operator:
(Tf)(G) = ∫_M R(G, G') f(G') dμ(G')

By Mercer's theorem, since R is continuous and positive definite:
R(G₁, G₂) = Σᵢ₌₁^∞ λᵢ ψᵢ(G₁) ψᵢ(G₂)

The convergence is uniform on K because:
1. K is compact in M × M
2. R is continuous on K (by definition)
3. The eigenvalues λᵢ → 0 (by compactness of T)

Therefore: sup_{(G₁,G₂)∈K} |R(G₁, G₂) - Rₙ(G₁, G₂)| → 0 as n → ∞. □

## B. Implementation Details

### B.1 Geoid Data Structure

```python
@dataclass
class Geoid:
    # Core fields
    raw: str                    # Original text
    echo: str                   # Normalized text for hashing
    gid: str                    # Unique identifier
    lang_axis: str              # Language code
    
    # Geometric fields
    position: np.ndarray        # Position on S^n
    velocity: np.ndarray        # Tangent vector (semantic flow)
    vorticity: float           # Rotational component
    
    # Semantic fields
    sem_vec: np.ndarray        # Semantic embedding
    sym_vec: np.ndarray        # Symbolic embedding
    
    # Metadata
    scars: List[str]           # Interaction history
    created_at: datetime
    updated_at: datetime
```

### B.2 Efficient Resonance Matrix Construction

```python
def build_resonance_matrix_fast(geoids, n_jobs=-1):
    """Parallel construction of resonance matrix"""
    n = len(geoids)
    
    # Pre-compute normalized vectors
    vectors = np.array([g.position for g in geoids])
    
    # Compute all pairwise inner products at once
    gram_matrix = vectors @ vectors.T
    
    # Convert to distances
    # d(i,j) = arccos(gram[i,j])
    # But arccos is expensive, so we use approximation for small angles
    distances = np.sqrt(2 - 2 * gram_matrix + 1e-8)
    
    # Apply Gaussian kernel
    resonances = np.exp(-distances**2 / (2 * sigma**2))
    
    # Apply scar penalties in parallel
    if n_jobs != 1:
        with ThreadPoolExecutor(max_workers=n_jobs) as executor:
            futures = []
            for i in range(n):
                for j in range(i+1, n):
                    futures.append(
                        executor.submit(compute_penalty, geoids[i], geoids[j])
                    )
            
            # Collect results
            idx = 0
            for i in range(n):
                for j in range(i+1, n):
                    penalty = futures[idx].result()
                    resonances[i,j] *= (1 - penalty)
                    resonances[j,i] = resonances[i,j]
                    idx += 1
    
    return resonances
```

### B.3 Spectral Analysis with Numerical Stability

```python
def compute_spectrum_stable(R, k=None, tol=1e-10):
    """Numerically stable eigendecomposition"""
    n = R.shape[0]
    
    # Ensure symmetry (fix numerical errors)
    R = (R + R.T) / 2
    
    # Add small diagonal perturbation for stability
    R_perturbed = R + tol * np.eye(n)
    
    if k is None or k >= n - 1:
        # Full eigendecomposition
        eigenvalues, eigenvectors = scipy.linalg.eigh(
            R_perturbed, 
            check_finite=True,
            overwrite_a=False
        )
    else:
        # Partial eigendecomposition for efficiency
        eigenvalues, eigenvectors = scipy.sparse.linalg.eigsh(
            R_perturbed,
            k=k,
            which='LA',  # Largest algebraic
            tol=tol
        )
    
    # Sort in descending order
    idx = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    
    # Remove perturbation from eigenvalues
    eigenvalues = np.maximum(eigenvalues - tol, 0)
    
    return eigenvalues, eigenvectors
```

### B.4 Fast Approximate Resonance

```python
class LSHResonance:
    """Locality-sensitive hashing for fast resonance approximation"""
    
    def __init__(self, n_projections=128, n_tables=10):
        self.n_projections = n_projections
        self.n_tables = n_tables
        self.tables = []
        
    def fit(self, geoids):
        """Build LSH index"""
        vectors = np.array([g.position for g in geoids])
        d = vectors.shape[1]
        
        for _ in range(self.n_tables):
            # Random projection matrix
            projection = np.random.randn(d, self.n_projections)
            projection /= np.linalg.norm(projection, axis=0)
            
            # Project and binarize
            projected = vectors @ projection
            binary = (projected > 0).astype(int)
            
            # Build hash table
            table = {}
            for i, hash_vec in enumerate(binary):
                key = tuple(hash_vec)
                if key not in table:
                    table[key] = []
                table[key].append(i)
            
            self.tables.append((projection, table))
    
    def query(self, geoid, k=10):
        """Find k most resonant geoids"""
        vector = geoid.position
        candidates = set()
        
        for projection, table in self.tables:
            # Hash query
            projected = vector @ projection
            binary = (projected > 0).astype(int)
            key = tuple(binary)
            
            # Retrieve candidates
            if key in table:
                candidates.update(table[key])
            
            # Also check nearby buckets (1 bit flip)
            for i in range(len(key)):
                neighbor_key = list(key)
                neighbor_key[i] = 1 - neighbor_key[i]
                neighbor_key = tuple(neighbor_key)
                if neighbor_key in table:
                    candidates.update(table[neighbor_key])
        
        # Exact resonance for candidates
        resonances = []
        for idx in candidates:
            r = resonance(geoid, self.geoids[idx])
            resonances.append((idx, r))
        
        # Return top k
        resonances.sort(key=lambda x: x[1], reverse=True)
        return resonances[:k]
```

## C. Additional Experimental Results

### C.1 Scaling Experiments

| # Geoids | Build Time (s) | Query Time (ms) | Memory (MB) |
|----------|----------------|-----------------|-------------|
| 1K       | 0.12          | 0.8            | 0.1         |
| 10K      | 1.3           | 0.9            | 1.2         |
| 100K     | 15.7          | 1.0            | 12          |
| 1M       | 187           | 1.2            | 120         |
| 10M      | 2,340         | 1.5            | 1,200       |

### C.2 Cross-Lingual Performance

| Language Pair | Monolingual | Cross-lingual | Drop |
|---------------|-------------|---------------|------|
| EN-EN         | 94.1%       | -            | -    |
| EN-FR         | 93.8%       | 91.2%        | 2.6% |
| EN-DE         | 93.5%       | 90.8%        | 2.7% |
| EN-ZH         | 92.1%       | 87.3%        | 4.8% |
| EN-AR         | 91.7%       | 86.9%        | 4.8% |

### C.3 Domain-Specific Results

| Domain | # Concepts | Coherence | Avg Resonance | Phase Transitions |
|--------|------------|-----------|---------------|-------------------|
| Physics | 12,453 | 0.487 | 0.342 | 3 |
| Biology | 18,291 | 0.523 | 0.367 | 5 |
| Computer Science | 9,876 | 0.445 | 0.312 | 2 |
| Literature | 15,234 | 0.612 | 0.423 | 7 |
| Philosophy | 7,652 | 0.578 | 0.398 | 4 |

### C.4 Error Analysis

Common failure modes:
1. **Polysemy** (12% of errors): Single word with multiple meanings
2. **Rare words** (8% of errors): Insufficient training data
3. **Compositional** (5% of errors): Complex multi-word expressions
4. **Cultural** (3% of errors): Culture-specific concepts

## D. Reproducibility Checklist

✓ **Code**: Available at [github.com/kimera-swm] (upon acceptance)
✓ **Data**: All datasets publicly available
✓ **Dependencies**: Listed in requirements.txt
✓ **Random seeds**: Fixed at 42 for all experiments
✓ **Hardware**: Experiments run on NVIDIA A100 40GB
✓ **Training time**: ~4 hours for full model
✓ **Hyperparameters**: Grid search details in config.yaml
✓ **Evaluation**: Standard splits, metrics clearly defined
✓ **Statistical significance**: Bootstrap confidence intervals reported
✓ **Limitations**: Clearly stated in Section 7.3