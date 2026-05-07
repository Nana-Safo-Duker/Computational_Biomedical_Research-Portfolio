"""
Comprehensive Exploratory Data Analysis (EDA)
Genomics Sequence Classification Dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

def extract_sequence_features(sequences):
    """Extract comprehensive features from DNA sequences"""
    from collections import Counter
    features = []
    
    for seq in sequences:
        seq = str(seq).upper()
        length = len(seq)
        
        # Basic composition
        gc_content = (seq.count('G') + seq.count('C')) / length if length > 0 else 0
        at_content = (seq.count('A') + seq.count('T')) / length if length > 0 else 0
        
        # Nucleotide frequencies
        a_freq = seq.count('A') / length if length > 0 else 0
        t_freq = seq.count('T') / length if length > 0 else 0
        g_freq = seq.count('G') / length if length > 0 else 0
        c_freq = seq.count('C') / length if length > 0 else 0
        
        # K-mer frequencies (2-mers and 3-mers)
        kmer_2 = {}
        kmer_3 = {}
        for i in range(len(seq) - 1):
            kmer2 = seq[i:i+2]
            kmer_2[kmer2] = kmer_2.get(kmer2, 0) + 1
        for i in range(len(seq) - 2):
            kmer3 = seq[i:i+3]
            kmer_3[kmer3] = kmer_3.get(kmer3, 0) + 1
        
        total_2mers = sum(kmer_2.values()) if kmer_2 else 1
        total_3mers = sum(kmer_3.values()) if kmer_3 else 1
        
        # Common k-mers
        aa_freq = kmer_2.get('AA', 0) / total_2mers
        at_freq = kmer_2.get('AT', 0) / total_2mers
        ag_freq = kmer_2.get('AG', 0) / total_2mers
        ac_freq = kmer_2.get('AC', 0) / total_2mers
        ta_freq = kmer_2.get('TA', 0) / total_2mers
        tt_freq = kmer_2.get('TT', 0) / total_2mers
        tg_freq = kmer_2.get('TG', 0) / total_2mers
        tc_freq = kmer_2.get('TC', 0) / total_2mers
        ga_freq = kmer_2.get('GA', 0) / total_2mers
        gt_freq = kmer_2.get('GT', 0) / total_2mers
        gg_freq = kmer_2.get('GG', 0) / total_2mers
        gc_freq = kmer_2.get('GC', 0) / total_2mers
        ca_freq = kmer_2.get('CA', 0) / total_2mers
        ct_freq = kmer_2.get('CT', 0) / total_2mers
        cg_freq = kmer_2.get('CG', 0) / total_2mers
        cc_freq = kmer_2.get('CC', 0) / total_2mers
        
        # Sequence complexity (Shannon entropy)
        counts = Counter(seq)
        entropy = -sum((count/len(seq)) * np.log2(count/len(seq)) 
                      for count in counts.values() if count > 0)
        
        # GC skew
        gc_skew = (g_freq - c_freq) / (g_freq + c_freq) if (g_freq + c_freq) > 0 else 0
        
        features.append({
            'length': length, 'gc_content': gc_content, 'at_content': at_content,
            'a_freq': a_freq, 't_freq': t_freq, 'g_freq': g_freq, 'c_freq': c_freq,
            'aa_freq': aa_freq, 'at_freq': at_freq, 'ag_freq': ag_freq, 'ac_freq': ac_freq,
            'ta_freq': ta_freq, 'tt_freq': tt_freq, 'tg_freq': tg_freq, 'tc_freq': tc_freq,
            'ga_freq': ga_freq, 'gt_freq': gt_freq, 'gg_freq': gg_freq, 'gc_freq': gc_freq,
            'ca_freq': ca_freq, 'ct_freq': ct_freq, 'cg_freq': cg_freq, 'cc_freq': cc_freq,
            'entropy': entropy, 'gc_skew': gc_skew
        })
    
    return pd.DataFrame(features)

def comprehensive_eda(df_features):
    """Perform comprehensive EDA"""
    
    print("=" * 80)
    print("COMPREHENSIVE EXPLORATORY DATA ANALYSIS")
    print("=" * 80)
    
    # 1. Data Overview
    print("\n1. DATA OVERVIEW")
    print("-" * 80)
    print(f"Dataset Shape: {df_features.shape}")
    print(f"\nColumn Names: {list(df_features.columns)}")
    print(f"\nData Types:\n{df_features.dtypes}")
    print(f"\nMissing Values:\n{df_features.isnull().sum()}")
    print(f"\nDuplicate Rows: {df_features.duplicated().sum()}")
    
    # 2. Target Variable Analysis
    print("\n2. TARGET VARIABLE ANALYSIS")
    print("-" * 80)
    label_counts = df_features['Labels'].value_counts().sort_index()
    print(f"Label Distribution:\n{label_counts}")
    print(f"\nLabel Proportions:\n{label_counts / len(df_features)}")
    print(f"\nClass Balance: {'Balanced' if abs(label_counts[0] - label_counts[1]) < 50 else 'Imbalanced'}")
    
    # 3. Feature Statistics
    print("\n3. FEATURE STATISTICS")
    print("-" * 80)
    numeric_cols = [col for col in df_features.columns if col not in ['Sequences', 'Labels']]
    print(f"\nSummary Statistics:\n{df_features[numeric_cols].describe()}")
    
    # 4. Correlation Analysis
    print("\n4. CORRELATION ANALYSIS")
    print("-" * 80)
    corr_matrix = df_features[numeric_cols].corr()
    print(f"\nTop Correlations:")
    corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j], 
                              corr_matrix.iloc[i, j]))
    corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    for pair in corr_pairs[:10]:
        print(f"  {pair[0]} - {pair[1]}: {pair[2]:.4f}")
    
    # 5. Feature Importance by Label
    print("\n5. FEATURE DIFFERENCES BY LABEL")
    print("-" * 80)
    for col in numeric_cols[:10]:  # Show top 10
        group_0 = df_features[df_features['Labels'] == 0][col]
        group_1 = df_features[df_features['Labels'] == 1][col]
        mean_diff = group_1.mean() - group_0.mean()
        t_stat, p_value = stats.ttest_ind(group_0, group_1)
        print(f"{col}: Mean difference={mean_diff:.4f}, p-value={p_value:.4f}")
    
    # 6. Outlier Analysis
    print("\n6. OUTLIER ANALYSIS")
    print("-" * 80)
    for col in numeric_cols[:10]:
        Q1 = df_features[col].quantile(0.25)
        Q3 = df_features[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df_features[(df_features[col] < Q1 - 1.5*IQR) | (df_features[col] > Q3 + 1.5*IQR)]
        print(f"{col}: {len(outliers)} outliers ({len(outliers)/len(df_features)*100:.2f}%)")
    
    print("\n" + "=" * 80)
    print("EDA COMPLETE")
    print("=" * 80)

def create_visualizations(df_features):
    """Create comprehensive visualizations"""
    numeric_cols = [col for col in df_features.columns if col not in ['Sequences', 'Labels']]
    
    # 1. Distribution plots
    fig, axes = plt.subplots(3, 3, figsize=(18, 15))
    axes = axes.ravel()
    for idx, col in enumerate(numeric_cols[:9]):
        ax = axes[idx]
        df_features[col].hist(bins=30, ax=ax, alpha=0.7, edgecolor='black')
        ax.set_title(f'Distribution of {col}', fontweight='bold')
        ax.set_xlabel(col)
        ax.set_ylabel('Frequency')
    plt.tight_layout()
    plt.savefig('../results/eda_distributions.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Correlation heatmap
    plt.figure(figsize=(14, 12))
    corr_matrix = df_features[numeric_cols].corr()
    sns.heatmap(corr_matrix, annot=False, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title('Correlation Heatmap - All Features', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('../results/eda_correlation.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Box plots by label
    fig, axes = plt.subplots(3, 3, figsize=(18, 15))
    axes = axes.ravel()
    for idx, col in enumerate(numeric_cols[:9]):
        ax = axes[idx]
        df_features.boxplot(column=col, by='Labels', ax=ax)
        ax.set_title(f'{col} by Label', fontweight='bold')
        ax.set_xlabel('Label')
        ax.get_figure().suptitle('')
    plt.tight_layout()
    plt.savefig('../results/eda_boxplots.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Visualizations saved to ../results/")

def main():
    # Load data
    df = pd.read_csv('../data/genomics_data.csv')
    print(f"Loading data... Shape: {df.shape}")
    
    # Extract features
    print("Extracting features...")
    feature_df = extract_sequence_features(df['Sequences'])
    df_features = pd.concat([df, feature_df], axis=1)
    
    # Perform EDA
    comprehensive_eda(df_features)
    
    # Create visualizations
    print("\nCreating visualizations...")
    create_visualizations(df_features)
    
    print("\nComprehensive EDA Complete!")

if __name__ == "__main__":
    main()

