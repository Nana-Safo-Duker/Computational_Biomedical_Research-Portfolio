"""
Visualization script for regulatory element analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def visualize_regulatory_elements():
    """Create visualizations of regulatory element characteristics"""
    
    # Load data
    df = pd.read_csv('genomics_data.csv')
    
    # Separate regulatory and non-regulatory sequences
    regulatory = df[df['Labels'] == 1]['Sequences']
    non_regulatory = df[df['Labels'] == 0]['Sequences']
    
    # Calculate features
    def calculate_gc_content(seq):
        return (seq.count('G') + seq.count('C')) / len(seq) * 100
    
    def calculate_cpg_count(seq):
        return seq.count('CG')
    
    reg_gc = [calculate_gc_content(seq) for seq in regulatory]
    non_reg_gc = [calculate_gc_content(seq) for seq in non_regulatory]
    
    reg_cpg = [calculate_cpg_count(seq) for seq in regulatory]
    non_reg_cpg = [calculate_cpg_count(seq) for seq in non_regulatory]
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Regulatory Element Sequence Characteristics', fontsize=16, fontweight='bold')
    
    # 1. GC Content Distribution
    axes[0, 0].hist(reg_gc, bins=30, alpha=0.7, label='Regulatory (n=987)', color='#2ecc71', edgecolor='black')
    axes[0, 0].hist(non_reg_gc, bins=30, alpha=0.7, label='Non-regulatory (n=1013)', color='#e74c3c', edgecolor='black')
    axes[0, 0].set_xlabel('GC Content (%)', fontsize=12)
    axes[0, 0].set_ylabel('Frequency', fontsize=12)
    axes[0, 0].set_title('GC Content Distribution', fontsize=13, fontweight='bold')
    axes[0, 0].legend()
    axes[0, 0].grid(alpha=0.3)
    
    # 2. CpG Count Distribution
    axes[0, 1].hist(reg_cpg, bins=20, alpha=0.7, label='Regulatory', color='#2ecc71', edgecolor='black')
    axes[0, 1].hist(non_reg_cpg, bins=20, alpha=0.7, label='Non-regulatory', color='#e74c3c', edgecolor='black')
    axes[0, 1].set_xlabel('CpG Count', fontsize=12)
    axes[0, 1].set_ylabel('Frequency', fontsize=12)
    axes[0, 1].set_title('CpG Dinucleotide Count', fontsize=13, fontweight='bold')
    axes[0, 1].legend()
    axes[0, 1].grid(alpha=0.3)
    
    # 3. Box plot: GC Content
    data_gc = pd.DataFrame({
        'GC Content (%)': reg_gc + non_reg_gc,
        'Type': ['Regulatory'] * len(reg_gc) + ['Non-regulatory'] * len(non_reg_gc)
    })
    sns.boxplot(data=data_gc, x='Type', y='GC Content (%)', ax=axes[1, 0], palette=['#2ecc71', '#e74c3c'])
    axes[1, 0].set_title('GC Content Comparison', fontsize=13, fontweight='bold')
    axes[1, 0].grid(alpha=0.3, axis='y')
    
    # 4. Box plot: CpG Count
    data_cpg = pd.DataFrame({
        'CpG Count': reg_cpg + non_reg_cpg,
        'Type': ['Regulatory'] * len(reg_cpg) + ['Non-regulatory'] * len(non_reg_cpg)
    })
    sns.boxplot(data=data_cpg, x='Type', y='CpG Count', ax=axes[1, 1], palette=['#2ecc71', '#e74c3c'])
    axes[1, 1].set_title('CpG Count Comparison', fontsize=13, fontweight='bold')
    axes[1, 1].grid(alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('regulatory_elements_analysis.png', dpi=300, bbox_inches='tight')
    print("Visualization saved as 'regulatory_elements_analysis.png'")
    
    # Create motif presence comparison
    fig2, ax = plt.subplots(figsize=(12, 6))
    
    motifs_data = {
        'CTCF Site': (313, 83),
        'CAAT Box': (141, 170),
        'NF1 Site': (33, 43),
        'TATA Box': (26, 45),
        'AP1 Site': (13, 15),
        'GC Box': (11, 18),
        'SP1 Site': (6, 8),
        'CREB Site': (1, 0)
    }
    
    motifs = list(motifs_data.keys())
    reg_counts = [motifs_data[m][0] for m in motifs]
    non_reg_counts = [motifs_data[m][1] for m in motifs]
    
    x = np.arange(len(motifs))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, reg_counts, width, label='Regulatory', color='#2ecc71', edgecolor='black')
    bars2 = ax.bar(x + width/2, non_reg_counts, width, label='Non-regulatory', color='#e74c3c', edgecolor='black')
    
    ax.set_xlabel('Regulatory Motif', fontsize=12)
    ax.set_ylabel('Number of Sequences', fontsize=12)
    ax.set_title('Known Regulatory Motif Presence in Sequences', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(motifs, rotation=45, ha='right')
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('regulatory_motifs_comparison.png', dpi=300, bbox_inches='tight')
    print("Motif comparison saved as 'regulatory_motifs_comparison.png'")

if __name__ == "__main__":
    visualize_regulatory_elements()

