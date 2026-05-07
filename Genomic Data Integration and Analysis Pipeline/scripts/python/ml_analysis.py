"""
Machine Learning Analysis
Genomics Sequence Classification Dataset

This script implements multiple ML algorithms to classify genomics sequences.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import (classification_report, confusion_matrix, 
                            accuracy_score, precision_score, recall_score, 
                            f1_score, roc_auc_score, roc_curve)
import warnings
warnings.filterwarnings('ignore')

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

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
        
        # K-mer frequencies (2-mers)
        kmer_2 = {}
        for i in range(len(seq) - 1):
            kmer = seq[i:i+2]
            kmer_2[kmer] = kmer_2.get(kmer, 0) + 1
        
        total_kmers = sum(kmer_2.values()) if kmer_2 else 1
        aa_freq = kmer_2.get('AA', 0) / total_kmers
        at_freq = kmer_2.get('AT', 0) / total_kmers
        ag_freq = kmer_2.get('AG', 0) / total_kmers
        ac_freq = kmer_2.get('AC', 0) / total_kmers
        ta_freq = kmer_2.get('TA', 0) / total_kmers
        tt_freq = kmer_2.get('TT', 0) / total_kmers
        tg_freq = kmer_2.get('TG', 0) / total_kmers
        tc_freq = kmer_2.get('TC', 0) / total_kmers
        ga_freq = kmer_2.get('GA', 0) / total_kmers
        gt_freq = kmer_2.get('GT', 0) / total_kmers
        gg_freq = kmer_2.get('GG', 0) / total_kmers
        gc_freq = kmer_2.get('GC', 0) / total_kmers
        ca_freq = kmer_2.get('CA', 0) / total_kmers
        ct_freq = kmer_2.get('CT', 0) / total_kmers
        cg_freq = kmer_2.get('CG', 0) / total_kmers
        cc_freq = kmer_2.get('CC', 0) / total_kmers
        
        # Sequence entropy
        counts = Counter(seq)
        entropy = -sum((count/len(seq)) * np.log2(count/len(seq)) 
                      for count in counts.values() if count > 0)
        
        features.append({
            'length': length, 'gc_content': gc_content,
            'a_freq': a_freq, 't_freq': t_freq, 'g_freq': g_freq, 'c_freq': c_freq,
            'aa_freq': aa_freq, 'at_freq': at_freq, 'ag_freq': ag_freq, 'ac_freq': ac_freq,
            'ta_freq': ta_freq, 'tt_freq': tt_freq, 'tg_freq': tg_freq, 'tc_freq': tc_freq,
            'ga_freq': ga_freq, 'gt_freq': gt_freq, 'gg_freq': gg_freq, 'gc_freq': gc_freq,
            'ca_freq': ca_freq, 'ct_freq': ct_freq, 'cg_freq': cg_freq, 'cc_freq': cc_freq,
            'entropy': entropy
        })
    
    return pd.DataFrame(features)

def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    """Train and evaluate multiple ML models"""
    
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42, max_depth=5),
        'SVM': SVC(kernel='rbf', probability=True, random_state=42),
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
        'Naive Bayes': GaussianNB(),
        'AdaBoost': AdaBoostClassifier(n_estimators=50, random_state=42)
    }
    
    results = {}
    
    print("=" * 80)
    print("MACHINE LEARNING MODEL EVALUATION")
    print("=" * 80)
    
    for name, model in models.items():
        print(f"\n{name}")
        print("-" * 80)
        
        # Train model
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_pred_proba) if y_pred_proba is not None else None
        
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'auc': auc,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba
        }
        
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1-Score: {f1:.4f}")
        if auc:
            print(f"AUC-ROC: {auc:.4f}")
        
        # Cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
        print(f"CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        print(f"\nConfusion Matrix:\n{cm}")
    
    return results

def plot_results(results, X_test, y_test):
    """Plot model comparison and ROC curves"""
    
    # Model comparison
    model_names = list(results.keys())
    accuracies = [results[m]['accuracy'] for m in model_names]
    f1_scores = [results[m]['f1'] for m in model_names]
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Accuracy comparison
    axes[0].barh(model_names, accuracies, color='skyblue', alpha=0.7, edgecolor='black')
    axes[0].set_xlabel('Accuracy')
    axes[0].set_title('Model Accuracy Comparison', fontweight='bold')
    axes[0].set_xlim([0, 1])
    for i, v in enumerate(accuracies):
        axes[0].text(v, i, f'{v:.3f}', va='center', fontweight='bold')
    
    # F1-score comparison
    axes[1].barh(model_names, f1_scores, color='salmon', alpha=0.7, edgecolor='black')
    axes[1].set_xlabel('F1-Score')
    axes[1].set_title('Model F1-Score Comparison', fontweight='bold')
    axes[1].set_xlim([0, 1])
    for i, v in enumerate(f1_scores):
        axes[1].text(v, i, f'{v:.3f}', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('../results/ml_model_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # ROC curves
    plt.figure(figsize=(10, 8))
    for name, result in results.items():
        if result['auc'] is not None:
            fpr, tpr, _ = roc_curve(y_test, result['y_pred_proba'])
            plt.plot(fpr, tpr, label=f"{name} (AUC = {result['auc']:.3f})", linewidth=2)
    
    plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves - Model Comparison', fontsize=14, fontweight='bold')
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../results/ml_roc_curves.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\nVisualizations saved to ../results/")

def main():
    # Load data
    df = pd.read_csv('../data/genomics_data.csv')
    print(f"Dataset shape: {df.shape}")
    
    # Extract features
    print("Extracting features...")
    feature_df = extract_sequence_features(df['Sequences'])
    df_features = pd.concat([df, feature_df], axis=1)
    
    # Prepare data
    X = df_features.drop(['Sequences', 'Labels'], axis=1).values
    y = df_features['Labels'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    print(f"Training set: {X_train.shape}, Test set: {X_test.shape}")
    
    # Train and evaluate models
    results = train_and_evaluate_models(X_train, X_test, y_train, y_test)
    
    # Plot results
    plot_results(results, X_test, y_test)
    
    # Best model
    best_model = max(results.items(), key=lambda x: x[1]['f1'])
    print(f"\n{'='*80}")
    print(f"BEST MODEL: {best_model[0]}")
    print(f"F1-Score: {best_model[1]['f1']:.4f}")
    print(f"Accuracy: {best_model[1]['accuracy']:.4f}")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()

