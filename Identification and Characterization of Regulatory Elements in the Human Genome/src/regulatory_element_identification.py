"""
Regulatory Element Identification in Genomic Sequences

This module provides comprehensive tools for identifying regulatory elements
(promoters, enhancers, silencers, insulators) in DNA sequences using machine learning
and bioinformatics approaches.

Author: Regulatory Element Identification Project
Date: 2025
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score,
    precision_score, recall_score, f1_score, roc_auc_score, roc_curve
)
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Set style for plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)


class RegulatoryElementIdentifier:
    """
    A comprehensive class for identifying regulatory elements in genomic sequences.
    
    Regulatory elements include:
    - Promoters: Sequences that initiate transcription (typically upstream of genes)
    - Enhancers: Sequences that increase transcription rates
    - Silencers: Sequences that repress transcription
    - Insulators: Sequences that block enhancer-promoter interactions
    """
    
    def __init__(self, data_path):
        """
        Initialize the RegulatoryElementIdentifier.
        
        Parameters:
        -----------
        data_path : str
            Path to the CSV file containing sequences and labels
        """
        self.data_path = data_path
        self.df = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.models = {}
        self.feature_names = []
        
    def load_data(self):
        """Load and preprocess the genomic data."""
        print("Loading genomic data...")
        self.df = pd.read_csv(self.data_path)
        print(f"Loaded {len(self.df)} sequences")
        print(f"Sequence length: {len(self.df['Sequences'].iloc[0])} nucleotides")
        print(f"Label distribution:\n{self.df['Labels'].value_counts()}")
        return self.df
    
    def extract_kmer_features(self, sequences, k=3):
        """
        Extract k-mer frequency features from DNA sequences.
        
        K-mers are subsequences of length k. This captures local sequence patterns
        that are characteristic of regulatory elements.
        
        Parameters:
        -----------
        sequences : array-like
            DNA sequences
        k : int
            Length of k-mers (default: 3 for trinucleotides)
            
        Returns:
        --------
        numpy.ndarray
            Feature matrix with k-mer frequencies
        """
        print(f"Extracting {k}-mer features...")
        
        # Generate all possible k-mers
        nucleotides = ['A', 'T', 'G', 'C']
        kmers = []
        
        def generate_kmers(k, prefix=''):
            if k == 0:
                kmers.append(prefix)
                return
            for nuc in nucleotides:
                generate_kmers(k - 1, prefix + nuc)
        
        generate_kmers(k)
        self.feature_names = kmers
        
        # Count k-mer frequencies in each sequence
        features = []
        for seq in sequences:
            kmer_counts = Counter()
            for i in range(len(seq) - k + 1):
                kmer = seq[i:i+k]
                kmer_counts[kmer] += 1
            
            # Normalize by sequence length
            seq_features = [kmer_counts.get(kmer, 0) / (len(seq) - k + 1) 
                          for kmer in kmers]
            features.append(seq_features)
        
        return np.array(features)
    
    def extract_composition_features(self, sequences):
        """
        Extract nucleotide composition features.
        
        These include:
        - GC content
        - Individual nucleotide frequencies
        - Dinucleotide frequencies
        - Sequence complexity measures
        """
        print("Extracting composition features...")
        features = []
        
        for seq in sequences:
            seq = seq.upper()
            length = len(seq)
            
            # Basic nucleotide frequencies
            a_freq = seq.count('A') / length
            t_freq = seq.count('T') / length
            g_freq = seq.count('G') / length
            c_freq = seq.count('C') / length
            
            # GC content
            gc_content = (seq.count('G') + seq.count('C')) / length
            
            # AT/GC ratio
            at_gc_ratio = (seq.count('A') + seq.count('T')) / (seq.count('G') + seq.count('C') + 1e-10)
            
            # Dinucleotide frequencies
            dinucleotides = ['AA', 'AT', 'AG', 'AC', 'TA', 'TT', 'TG', 'TC',
                           'GA', 'GT', 'GG', 'GC', 'CA', 'CT', 'CG', 'CC']
            dinuc_freqs = [seq.count(dinuc) / (length - 1) for dinuc in dinucleotides]
            
            # Sequence complexity (Shannon entropy)
            nuc_counts = Counter(seq)
            entropy = -sum((count/length) * np.log2(count/length + 1e-10) 
                          for count in nuc_counts.values())
            
            feature_vector = ([a_freq, t_freq, g_freq, c_freq, gc_content, 
                             at_gc_ratio, entropy] + dinuc_freqs)
            features.append(feature_vector)
        
        return np.array(features)
    
    def extract_motif_features(self, sequences):
        """
        Extract features based on known regulatory element motifs.
        
        Regulatory elements often contain specific sequence motifs:
        - Promoters: TATA box (TATAAA), CAAT box, GC box
        - Enhancers: Various transcription factor binding sites
        - Silencers: Repressor binding sites
        """
        print("Extracting motif features...")
        
        # Common regulatory motifs
        motifs = {
            'TATA_box': 'TATAAA',
            'TATA_variant': 'TATAA',
            'CAAT_box': 'CCAAT',
            'GC_box': 'GGGCGG',
            'Inr': 'YYANWYY',  # Initiator element (Y=pyrimidine, W=A/T, N=any)
            'DPE': 'RGWYV',  # Downstream promoter element
        }
        
        features = []
        for seq in sequences:
            seq_upper = seq.upper()
            motif_counts = []
            
            for motif_name, motif_seq in motifs.items():
                if 'N' in motif_seq or 'Y' in motif_seq or 'W' in motif_seq or 'R' in motif_seq or 'V' in motif_seq:
                    # Handle degenerate motifs with pattern matching
                    count = self._match_degenerate_motif(seq_upper, motif_seq)
                else:
                    count = seq_upper.count(motif_seq)
                motif_counts.append(count)
            
            features.append(motif_counts)
        
        return np.array(features)
    
    def _match_degenerate_motif(self, sequence, pattern):
        """Match degenerate nucleotide patterns."""
        # Simple implementation for common IUPAC codes
        iupac = {
            'Y': '[CT]',  # Pyrimidine
            'R': '[AG]',  # Purine
            'W': '[AT]',  # Weak
            'S': '[GC]',  # Strong
            'M': '[AC]',  # Amino
            'K': '[GT]',  # Keto
            'B': '[CGT]', # Not A
            'D': '[AGT]', # Not C
            'H': '[ACT]', # Not G
            'V': '[ACG]', # Not T
            'N': '[ATGC]' # Any
        }
        
        import re
        regex_pattern = pattern
        for code, replacement in iupac.items():
            regex_pattern = regex_pattern.replace(code, replacement)
        
        return len(re.findall(regex_pattern, sequence))
    
    def prepare_features(self, k=3):
        """
        Prepare all features for machine learning.
        
        Parameters:
        -----------
        k : int
            k-mer size for k-mer feature extraction
        """
        print("\n" + "="*60)
        print("FEATURE EXTRACTION")
        print("="*60)
        
        sequences = self.df['Sequences'].values
        self.y = self.df['Labels'].values
        
        # Extract different feature types
        kmer_features = self.extract_kmer_features(sequences, k=k)
        composition_features = self.extract_composition_features(sequences)
        motif_features = self.extract_motif_features(sequences)
        
        # Combine all features
        self.X = np.hstack([kmer_features, composition_features, motif_features])
        
        print(f"\nTotal features: {self.X.shape[1]}")
        print(f"  - {k}-mer features: {kmer_features.shape[1]}")
        print(f"  - Composition features: {composition_features.shape[1]}")
        print(f"  - Motif features: {motif_features.shape[1]}")
        
        return self.X, self.y
    
    def split_data(self, test_size=0.2, random_state=42):
        """Split data into training and testing sets."""
        print("\n" + "="*60)
        print("DATA SPLITTING")
        print("="*60)
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=random_state, stratify=self.y
        )
        
        # Scale features
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)
        
        print(f"Training set: {self.X_train.shape[0]} sequences")
        print(f"Test set: {self.X_test.shape[0]} sequences")
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def train_models(self):
        """Train multiple machine learning models."""
        print("\n" + "="*60)
        print("MODEL TRAINING")
        print("="*60)
        
        models_to_train = {
            'Random Forest': RandomForestClassifier(
                n_estimators=100, 
                max_depth=10, 
                random_state=42,
                n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                random_state=42
            ),
            'SVM': SVC(
                kernel='rbf',
                probability=True,
                random_state=42
            ),
            'Neural Network': MLPClassifier(
                hidden_layer_sizes=(100, 50),
                max_iter=500,
                random_state=42
            )
        }
        
        for name, model in models_to_train.items():
            print(f"\nTraining {name}...")
            model.fit(self.X_train, self.y_train)
            self.models[name] = model
            
            # Evaluate on training set
            train_pred = model.predict(self.X_train)
            train_acc = accuracy_score(self.y_train, train_pred)
            print(f"  Training Accuracy: {train_acc:.4f}")
        
        return self.models
    
    def evaluate_models(self):
        """Evaluate all trained models on test set."""
        print("\n" + "="*60)
        print("MODEL EVALUATION")
        print("="*60)
        
        results = {}
        
        for name, model in self.models.items():
            print(f"\n{name}:")
            print("-" * 40)
            
            # Predictions
            y_pred = model.predict(self.X_test)
            y_pred_proba = model.predict_proba(self.X_test)[:, 1]
            
            # Metrics
            accuracy = accuracy_score(self.y_test, y_pred)
            precision = precision_score(self.y_test, y_pred)
            recall = recall_score(self.y_test, y_pred)
            f1 = f1_score(self.y_test, y_pred)
            auc = roc_auc_score(self.y_test, y_pred_proba)
            
            print(f"Accuracy:  {accuracy:.4f}")
            print(f"Precision: {precision:.4f}")
            print(f"Recall:    {recall:.4f}")
            print(f"F1-Score:  {f1:.4f}")
            print(f"AUC-ROC:   {auc:.4f}")
            
            # Classification report
            print("\nClassification Report:")
            print(classification_report(self.y_test, y_pred, 
                                      target_names=['Non-regulatory', 'Regulatory']))
            
            results[name] = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1': f1,
                'auc': auc,
                'predictions': y_pred,
                'probabilities': y_pred_proba
            }
        
        return results
    
    def plot_results(self, results, save_path='results'):
        """Generate visualization plots."""
        print("\n" + "="*60)
        print("GENERATING VISUALIZATIONS")
        print("="*60)
        
        import os
        os.makedirs(save_path, exist_ok=True)
        
        # 1. Model comparison
        model_names = list(results.keys())
        metrics = ['accuracy', 'precision', 'recall', 'f1', 'auc']
        
        fig, ax = plt.subplots(figsize=(12, 6))
        x = np.arange(len(model_names))
        width = 0.15
        
        for i, metric in enumerate(metrics):
            values = [results[name][metric] for name in model_names]
            ax.bar(x + i*width, values, width, label=metric.capitalize())
        
        ax.set_xlabel('Models')
        ax.set_ylabel('Score')
        ax.set_title('Model Performance Comparison')
        ax.set_xticks(x + width * 2)
        ax.set_xticklabels(model_names)
        ax.legend()
        ax.set_ylim([0, 1])
        plt.tight_layout()
        plt.savefig(f'{save_path}/model_comparison.png', dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}/model_comparison.png")
        plt.close()
        
        # 2. ROC curves
        fig, ax = plt.subplots(figsize=(10, 8))
        for name, result in results.items():
            fpr, tpr, _ = roc_curve(self.y_test, result['probabilities'])
            ax.plot(fpr, tpr, label=f'{name} (AUC = {result["auc"]:.3f})')
        
        ax.plot([0, 1], [0, 1], 'k--', label='Random')
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title('ROC Curves')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'{save_path}/roc_curves.png', dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}/roc_curves.png")
        plt.close()
        
        # 3. Confusion matrices
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        axes = axes.flatten()
        
        for idx, (name, result) in enumerate(results.items()):
            cm = confusion_matrix(self.y_test, result['predictions'])
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                       xticklabels=['Non-regulatory', 'Regulatory'],
                       yticklabels=['Non-regulatory', 'Regulatory'])
            axes[idx].set_title(f'{name}\nAccuracy: {result["accuracy"]:.3f}')
            axes[idx].set_ylabel('True Label')
            axes[idx].set_xlabel('Predicted Label')
        
        plt.tight_layout()
        plt.savefig(f'{save_path}/confusion_matrices.png', dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}/confusion_matrices.png")
        plt.close()
        
        # 4. Feature importance (for Random Forest)
        if 'Random Forest' in self.models:
            rf_model = self.models['Random Forest']
            importances = rf_model.feature_importances_
            indices = np.argsort(importances)[::-1][:20]  # Top 20 features
            
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.barh(range(len(indices)), importances[indices])
            ax.set_yticks(range(len(indices)))
            if len(self.feature_names) > 0:
                feature_labels = [f'Feature {i}' for i in indices]
            else:
                feature_labels = [f'Feature {i}' for i in indices]
            ax.set_yticklabels(feature_labels)
            ax.set_xlabel('Importance')
            ax.set_title('Top 20 Feature Importances (Random Forest)')
            plt.tight_layout()
            plt.savefig(f'{save_path}/feature_importance.png', dpi=300, bbox_inches='tight')
            print(f"Saved: {save_path}/feature_importance.png")
            plt.close()
    
    def identify_regulatory_elements(self, sequences, model_name='Random Forest'):
        """
        Identify regulatory elements in new sequences.
        
        Parameters:
        -----------
        sequences : list or array
            DNA sequences to analyze
        model_name : str
            Name of the model to use for prediction
            
        Returns:
        --------
        numpy.ndarray
            Predictions (0 = non-regulatory, 1 = regulatory)
        numpy.ndarray
            Prediction probabilities
        """
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found. Available: {list(self.models.keys())}")
        
        # Extract features
        kmer_features = self.extract_kmer_features(sequences, k=3)
        composition_features = self.extract_composition_features(sequences)
        motif_features = self.extract_motif_features(sequences)
        X_new = np.hstack([kmer_features, composition_features, motif_features])
        
        # Scale features
        X_new_scaled = self.scaler.transform(X_new)
        
        # Predict
        model = self.models[model_name]
        predictions = model.predict(X_new_scaled)
        probabilities = model.predict_proba(X_new_scaled)[:, 1]
        
        return predictions, probabilities


def main():
    """Main execution function."""
    print("="*60)
    print("REGULATORY ELEMENT IDENTIFICATION")
    print("="*60)
    print("\nThis tool identifies regulatory elements in genomic sequences.")
    print("Regulatory elements include:")
    print("  - Promoters: Initiate transcription")
    print("  - Enhancers: Increase transcription rates")
    print("  - Silencers: Repress transcription")
    print("  - Insulators: Block enhancer-promoter interactions")
    print("="*60 + "\n")
    
    # Initialize
    identifier = RegulatoryElementIdentifier('data/genomics_data.csv')
    
    # Load data
    identifier.load_data()
    
    # Prepare features
    identifier.prepare_features(k=3)
    
    # Split data
    identifier.split_data(test_size=0.2, random_state=42)
    
    # Train models
    identifier.train_models()
    
    # Evaluate models
    results = identifier.evaluate_models()
    
    # Generate visualizations
    identifier.plot_results(results, save_path='results')
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print("\nResults saved in 'results/' directory")
    print("\nBest performing model:")
    best_model = max(results.items(), key=lambda x: x[1]['f1'])
    print(f"  {best_model[0]}: F1-Score = {best_model[1]['f1']:.4f}")
    
    return identifier, results


if __name__ == "__main__":
    identifier, results = main()

