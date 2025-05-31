#!/usr/bin/env python3
"""Create a sample benchmark visualization for README."""

import matplotlib.pyplot as plt
import numpy as np

# Sample data for demonstration
methods = ['Kimera', 'GPT-4o-mini']
contradictions = [23, 19]
avg_times = [45.2, 1247.8]
avg_confidence = [0.847, 0.923]

# Agreement data
agreement_data = [35, 8, 7]  # Both agree, Kimera only, GPT-4o only
agreement_labels = ['Both Agree', 'Kimera Only', 'GPT-4o Only']

# Create the 4-panel visualization
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('Kimera vs GPT-4o Benchmark Comparison', fontsize=16, fontweight='bold')

# Panel 1: Contradictions detected
bars1 = ax1.bar(methods, contradictions, color=['#2E86AB', '#A23B72'])
ax1.set_title('Contradictions Detected')
ax1.set_ylabel('Count')
for i, v in enumerate(contradictions):
    ax1.text(i, v + 0.5, str(v), ha='center', va='bottom')

# Panel 2: Average time per pair (log scale)
bars2 = ax2.bar(methods, avg_times, color=['#2E86AB', '#A23B72'])
ax2.set_title('Average Time per Pair')
ax2.set_ylabel('Milliseconds')
ax2.set_yscale('log')
for i, v in enumerate(avg_times):
    ax2.text(i, v * 1.1, f'{v:.1f}ms', ha='center', va='bottom')

# Panel 3: Average confidence
bars3 = ax3.bar(methods, avg_confidence, color=['#2E86AB', '#A23B72'])
ax3.set_title('Average Confidence')
ax3.set_ylabel('Confidence Score')
ax3.set_ylim(0, 1)
for i, v in enumerate(avg_confidence):
    ax3.text(i, v + 0.02, f'{v:.3f}', ha='center', va='bottom')

# Panel 4: Agreement analysis (pie chart)
colors = ['#F18F01', '#2E86AB', '#A23B72']
ax4.pie(agreement_data, labels=agreement_labels, colors=colors, autopct='%1.1f%%')
ax4.set_title('Agreement Analysis')

plt.tight_layout()
plt.savefig('benchmark_summary_sample.png', dpi=300, bbox_inches='tight')
print("✓ Sample visualization saved as 'benchmark_summary_sample.png'")
print("  This shows what the benchmark system generates automatically.")