"""
Univariate, Bivariate, and Multivariate Analysis
Genomics Sequence Classification Dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def extract_sequence_features(sequences):
    """Extract features from DNA sequences"""
    features = []
    
    for seq in sequences:
        seq = str(seq).upper()
        
        # Basic features
        length = len(seq)
        gc_content = (seq.count('G') + seq.count('C')) / length if length > 0 else 0
        
        # Nucleotide frequencies
        a_freq = seq.count('A') / length if length > 0 else 0
        t_freq = seq.count('T') / length if length > 0 else 0
        g_freq = seq.count('G') / length if length > 0 else 0
        c_freq = seq.count('C') / length if length > 0 else 0
        
        # K-mer frequencies (2-mers)
        kmer_2 = {}
        for i in range(len(seq) - 1):
            kmer = seq[i:i+2]
            kmer_2[kmer] = kmer_2.get(kmer, 0) + 1
        
        # Normalize k-mer frequencies
        total_kmers = sum(kmer_2.values()) if kmer_2 else 1
        aa_freq = kmer_2.get('AA', 0) / total_kmers
        at_freq = kmer_2.get('AT', 0) / total_kmers
        ag_freq = kmer_2.get('AG', 0) / total_kmers
        ac_freq = kmer_2.get('AC', 0) / total_kmers
        
        # Sequence complexity (Shannon entropy)
        counts = Counter(seq)
        entropy = -sum((count/len(seq)) * np.log2(count/len(seq)) 
                      for count in counts.values() if count > 0)
        
        features.append({
            'length': length,
            'gc_content': gc_content,
            'a_freq': a_freq,
            't_freq': t_freq,
            'g_freq': g_freq,
            'c_freq': c_freq,
            'aa_freq': aa_freq,
            'at_freq': at_freq,
            'ag_freq': ag_freq,
            'ac_freq': ac_freq,
            'entropy': entropy
        })
    
    return pd.DataFrame(features)

def main():
    # Load data
    df = pd.read_csv('../data/genomics_data.csv')
    print(f"Dataset shape: {df.shape}")
    
    # Extract features
    feature_df = extract_sequence_features(df['Sequences'])
    df_features = pd.concat([df, feature_df], axis=1)
    
    numeric_cols = ['length', 'gc_content', 'a_freq', 't_freq', 'g_freq', 'c_freq', 'entropy']
    
    # Univariate Analysis
    print("\n=== UNIVARIATE ANALYSIS ===")
    for col in numeric_cols:
        print(f"\n{col.upper()}:")
        print(f"  Mean: {df_features[col].mean():.4f}")
        print(f"  Median: {df_features[col].median():.4f}")
        print(f"  Std Dev: {df_features[col].std():.4f}")
        print(f"  Skewness: {df_features[col].skew():.4f}")
    
    # Bivariate Analysis
    print("\n=== BIVARIATE ANALYSIS ===")
    correlation_matrix = df_features[numeric_cols].corr()
    print("\nTop Correlations:")
    corr_pairs = []
    for i in range(len(correlation_matrix.columns)):
        for j in range(i+1, len(correlation_matrix.columns)):
            corr_pairs.append((correlation_matrix.columns[i], 
                              correlation_matrix.columns[j], 
                              correlation_matrix.iloc[i, j]))
    corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    for pair in corr_pairs[:5]:
        print(f"  {pair[0]} - {pair[1]}: {pair[2]:.4f}")
    
    # Multivariate Analysis
    print("\n=== MULTIVARIATE ANALYSIS ===")
    X = df_features[numeric_cols].values
    y = df_features['Labels'].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    print(f"\nPCA Explained Variance: {sum(pca.explained_variance_ratio_):.2%}")
    
    # Feature Importance
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_scaled, y)
    feature_importance = pd.DataFrame({
        'feature': numeric_cols,
        'importance': rf.feature_importances_
    }).sort_values('importance', ascending=False)
    print("\nFeature Importance:")
    print(feature_importance)

if __name__ == "__main__":
    main()

