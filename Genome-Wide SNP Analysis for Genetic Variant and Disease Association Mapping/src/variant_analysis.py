"""
Comprehensive Variant Analysis Script

This script performs comprehensive analysis of genetic variants including:
- Statistical summaries
- Visualization
- Disease association analysis

Author: Genetic Variants Analysis Project
Date: 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from variant_identification import VariantIdentifier, process_genomics_data
import os


def create_summary_statistics(results_df: pd.DataFrame) -> pd.DataFrame:
    """Create summary statistics for variant analysis."""
    summary = {
        'Metric': [
            'Total Sequences',
            'Sequences with SNPs',
            'Sequences with Indels',
            'Sequences with Structural Variants',
            'Average SNPs per Sequence',
            'Average Indels per Sequence',
            'Average Structural Variants per Sequence',
            'Max SNPs in a Sequence',
            'Max Indels in a Sequence',
            'Max Structural Variants in a Sequence'
        ],
        'Value': [
            len(results_df),
            (results_df['num_snps'] > 0).sum(),
            (results_df['num_indels'] > 0).sum(),
            (results_df['num_structural_variants'] > 0).sum(),
            results_df['num_snps'].mean(),
            results_df['num_indels'].mean(),
            results_df['num_structural_variants'].mean(),
            results_df['num_snps'].max(),
            results_df['num_indels'].max(),
            results_df['num_structural_variants'].max()
        ]
    }
    return pd.DataFrame(summary)


def analyze_disease_association(results_df: pd.DataFrame) -> pd.DataFrame:
    """Analyze association between variants and disease labels."""
    disease_assoc = results_df.groupby('label').agg({
        'num_snps': ['mean', 'std', 'median'],
        'num_indels': ['mean', 'std', 'median'],
        'num_structural_variants': ['mean', 'std', 'median'],
        'total_variants': ['mean', 'std', 'median']
    }).round(2)
    
    return disease_assoc


def create_visualizations(results_df: pd.DataFrame, output_dir: str = "results"):
    """Create visualization plots for variant analysis."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)
    
    # 1. Distribution of variant types
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # SNPs distribution
    axes[0, 0].hist(results_df['num_snps'], bins=30, edgecolor='black', alpha=0.7)
    axes[0, 0].set_title('Distribution of SNPs per Sequence', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Number of SNPs')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Indels distribution
    axes[0, 1].hist(results_df['num_indels'], bins=30, edgecolor='black', alpha=0.7, color='orange')
    axes[0, 1].set_title('Distribution of Indels per Sequence', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Number of Indels')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Structural variants distribution
    axes[1, 0].hist(results_df['num_structural_variants'], bins=30, edgecolor='black', alpha=0.7, color='green')
    axes[1, 0].set_title('Distribution of Structural Variants per Sequence', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Number of Structural Variants')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Total variants distribution
    axes[1, 1].hist(results_df['total_variants'], bins=30, edgecolor='black', alpha=0.7, color='red')
    axes[1, 1].set_title('Distribution of Total Variants per Sequence', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('Number of Total Variants')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/variant_distributions.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Disease association analysis
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Box plots for each variant type by label
    sns.boxplot(data=results_df, x='label', y='num_snps', ax=axes[0, 0])
    axes[0, 0].set_title('SNPs by Disease Label', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Disease Label (0=Control, 1=Disease)')
    axes[0, 0].set_ylabel('Number of SNPs')
    
    sns.boxplot(data=results_df, x='label', y='num_indels', ax=axes[0, 1], color='orange')
    axes[0, 1].set_title('Indels by Disease Label', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Disease Label (0=Control, 1=Disease)')
    axes[0, 1].set_ylabel('Number of Indels')
    
    sns.boxplot(data=results_df, x='label', y='num_structural_variants', ax=axes[1, 0], color='green')
    axes[1, 0].set_title('Structural Variants by Disease Label', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Disease Label (0=Control, 1=Disease)')
    axes[1, 0].set_ylabel('Number of Structural Variants')
    
    sns.boxplot(data=results_df, x='label', y='total_variants', ax=axes[1, 1], color='red')
    axes[1, 1].set_title('Total Variants by Disease Label', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('Disease Label (0=Control, 1=Disease)')
    axes[1, 1].set_ylabel('Number of Total Variants')
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/disease_association_analysis.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Correlation heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    correlation_cols = ['num_snps', 'num_indels', 'num_structural_variants', 'total_variants', 'label']
    corr_matrix = results_df[correlation_cols].corr()
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax)
    ax.set_title('Variant Type Correlation Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/correlation_heatmap.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Visualizations saved to {output_dir}/")


def main():
    """Main analysis pipeline."""
    print("=" * 60)
    print("Genetic Variant Analysis Pipeline")
    print("=" * 60)
    
    # Process data
    data_file = "data/genomics_data.csv"
    output_file = "results/variant_analysis_results.csv"
    
    print("\n1. Processing genomics data and identifying variants...")
    results_df = process_genomics_data(data_file, output_file)
    
    print("\n2. Generating summary statistics...")
    summary_stats = create_summary_statistics(results_df)
    print("\nSummary Statistics:")
    print(summary_stats.to_string(index=False))
    summary_stats.to_csv("results/summary_statistics.csv", index=False)
    
    print("\n3. Analyzing disease associations...")
    disease_assoc = analyze_disease_association(results_df)
    print("\nDisease Association Analysis:")
    print(disease_assoc)
    disease_assoc.to_csv("results/disease_association_analysis.csv")
    
    print("\n4. Creating visualizations...")
    create_visualizations(results_df, "results")
    
    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)
    print(f"\nResults saved to:")
    print(f"  - Variant analysis: {output_file}")
    print(f"  - Summary statistics: results/summary_statistics.csv")
    print(f"  - Disease association: results/disease_association_analysis.csv")
    print(f"  - Visualizations: results/*.png")


if __name__ == "__main__":
    main()

