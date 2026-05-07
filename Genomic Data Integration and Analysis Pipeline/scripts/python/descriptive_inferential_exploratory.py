"""
Descriptive, Inferential, and Exploratory Statistical Analysis
Genomics Sequence Classification Dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import chi2_contingency, mannwhitneyu, kruskal
import warnings
warnings.filterwarnings('ignore')

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def extract_sequence_features(sequences):
    """Extract features from DNA sequences"""
    from collections import Counter
    features = []
    
    for seq in sequences:
        seq = str(seq).upper()
        length = len(seq)
        gc_content = (seq.count('G') + seq.count('C')) / length if length > 0 else 0
        a_freq = seq.count('A') / length if length > 0 else 0
        t_freq = seq.count('T') / length if length > 0 else 0
        g_freq = seq.count('G') / length if length > 0 else 0
        c_freq = seq.count('C') / length if length > 0 else 0
        
        counts = Counter(seq)
        entropy = -sum((count/len(seq)) * np.log2(count/len(seq)) 
                      for count in counts.values() if count > 0)
        
        features.append({
            'length': length, 'gc_content': gc_content,
            'a_freq': a_freq, 't_freq': t_freq, 'g_freq': g_freq, 'c_freq': c_freq,
            'entropy': entropy
        })
    
    return pd.DataFrame(features)

def descriptive_statistics(df_features):
    """Perform descriptive statistical analysis"""
    print("=" * 70)
    print("DESCRIPTIVE STATISTICAL ANALYSIS")
    print("=" * 70)
    
    numeric_cols = ['length', 'gc_content', 'a_freq', 't_freq', 'g_freq', 'c_freq', 'entropy']
    
    # Summary statistics
    print("\n1. SUMMARY STATISTICS")
    print("-" * 70)
    desc_stats = df_features[numeric_cols].describe()
    print(desc_stats)
    
    # Additional descriptive measures
    print("\n2. ADDITIONAL DESCRIPTIVE MEASURES")
    print("-" * 70)
    for col in numeric_cols:
        print(f"\n{col.upper()}:")
        print(f"  Mean: {df_features[col].mean():.4f}")
        print(f"  Median: {df_features[col].median():.4f}")
        print(f"  Mode: {df_features[col].mode().values[0] if len(df_features[col].mode()) > 0 else 'N/A'}")
        print(f"  Std Dev: {df_features[col].std():.4f}")
        print(f"  Variance: {df_features[col].var():.4f}")
        print(f"  Range: {df_features[col].max() - df_features[col].min():.4f}")
        print(f"  IQR: {df_features[col].quantile(0.75) - df_features[col].quantile(0.25):.4f}")
        print(f"  Skewness: {df_features[col].skew():.4f}")
        print(f"  Kurtosis: {df_features[col].kurtosis():.4f}")
        print(f"  CV (Coefficient of Variation): {(df_features[col].std() / df_features[col].mean() * 100):.2f}%")
    
    # By label groups
    print("\n3. DESCRIPTIVE STATISTICS BY LABEL")
    print("-" * 70)
    for col in numeric_cols:
        print(f"\n{col.upper()} by Label:")
        grouped = df_features.groupby('Labels')[col].describe()
        print(grouped)
    
    return desc_stats

def inferential_statistics(df_features):
    """Perform inferential statistical analysis"""
    print("\n" + "=" * 70)
    print("INFERENTIAL STATISTICAL ANALYSIS")
    print("=" * 70)
    
    numeric_cols = ['length', 'gc_content', 'a_freq', 't_freq', 'g_freq', 'c_freq', 'entropy']
    
    # Normality tests
    print("\n1. NORMALITY TESTS (Shapiro-Wilk Test)")
    print("-" * 70)
    for col in numeric_cols:
        stat, p_value = stats.shapiro(df_features[col].sample(min(5000, len(df_features))))
        print(f"{col}: W-statistic={stat:.4f}, p-value={p_value:.4f} {'(Normal)' if p_value > 0.05 else '(Not Normal)'}")
    
    # T-tests (comparing means between labels)
    print("\n2. INDEPENDENT T-TESTS (Label 0 vs Label 1)")
    print("-" * 70)
    for col in numeric_cols:
        group_0 = df_features[df_features['Labels'] == 0][col]
        group_1 = df_features[df_features['Labels'] == 1][col]
        t_stat, p_value = stats.ttest_ind(group_0, group_1)
        print(f"{col}: t-statistic={t_stat:.4f}, p-value={p_value:.4f} {'***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else ' (not significant)'}")
    
    # Mann-Whitney U test (non-parametric alternative)
    print("\n3. MANN-WHITNEY U TESTS (Non-parametric)")
    print("-" * 70)
    for col in numeric_cols:
        group_0 = df_features[df_features['Labels'] == 0][col]
        group_1 = df_features[df_features['Labels'] == 1][col]
        u_stat, p_value = mannwhitneyu(group_0, group_1, alternative='two-sided')
        print(f"{col}: U-statistic={u_stat:.4f}, p-value={p_value:.4f} {'***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else ' (not significant)'}")
    
    # Confidence intervals
    print("\n4. CONFIDENCE INTERVALS (95%)")
    print("-" * 70)
    for col in numeric_cols:
        mean = df_features[col].mean()
        std = df_features[col].std()
        n = len(df_features[col])
        se = std / np.sqrt(n)
        ci_lower = mean - 1.96 * se
        ci_upper = mean + 1.96 * se
        print(f"{col}: [{ci_lower:.4f}, {ci_upper:.4f}]")

def exploratory_analysis(df_features):
    """Perform exploratory data analysis"""
    print("\n" + "=" * 70)
    print("EXPLORATORY DATA ANALYSIS")
    print("=" * 70)
    
    numeric_cols = ['length', 'gc_content', 'a_freq', 't_freq', 'g_freq', 'c_freq', 'entropy']
    
    # Correlation analysis
    print("\n1. CORRELATION ANALYSIS")
    print("-" * 70)
    corr_matrix = df_features[numeric_cols].corr()
    print(corr_matrix)
    
    # Outlier detection
    print("\n2. OUTLIER DETECTION (IQR Method)")
    print("-" * 70)
    for col in numeric_cols:
        Q1 = df_features[col].quantile(0.25)
        Q3 = df_features[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df_features[(df_features[col] < lower_bound) | (df_features[col] > upper_bound)]
        print(f"{col}: {len(outliers)} outliers ({len(outliers)/len(df_features)*100:.2f}%)")
    
    # Distribution analysis
    print("\n3. DISTRIBUTION ANALYSIS")
    print("-" * 70)
    for col in numeric_cols:
        skew = df_features[col].skew()
        kurt = df_features[col].kurtosis()
        dist_type = "Normal" if abs(skew) < 0.5 and abs(kurt) < 0.5 else "Skewed" if abs(skew) > 1 else "Moderately Skewed"
        print(f"{col}: Skewness={skew:.4f}, Kurtosis={kurt:.4f} -> {dist_type}")

def main():
    # Load data
    df = pd.read_csv('../data/genomics_data.csv')
    print(f"Dataset shape: {df.shape}")
    
    # Extract features
    feature_df = extract_sequence_features(df['Sequences'])
    df_features = pd.concat([df, feature_df], axis=1)
    
    # Perform analyses
    descriptive_statistics(df_features)
    inferential_statistics(df_features)
    exploratory_analysis(df_features)
    
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()

