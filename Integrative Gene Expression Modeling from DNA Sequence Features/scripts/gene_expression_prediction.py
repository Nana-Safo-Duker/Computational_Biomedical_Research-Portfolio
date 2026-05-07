"""
Gene Expression Prediction from DNA Sequences
=============================================
This script predicts gene expression levels from DNA sequences using various
machine learning approaches including traditional ML and deep learning models.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.feature_extraction.text import CountVectorizer
import xgboost as xgb
import lightgbm as lgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

class DNASequenceEncoder:
    """Encode DNA sequences into numerical features."""
    
    def __init__(self, method='kmer'):
        """
        Initialize encoder.
        
        Parameters:
        -----------
        method : str
            Encoding method: 'kmer', 'onehot', or 'nucleotide_composition'
        """
        self.method = method
        self.vectorizer = None
        self.kmer_size = 3
        
    def kmer_encoding(self, sequences, k=3):
        """
        Convert DNA sequences to k-mer frequency features.
        
        Parameters:
        -----------
        sequences : list
            List of DNA sequences
        k : int
            k-mer size (default: 3 for trinucleotides)
            
        Returns:
        --------
        array : numpy array of k-mer frequencies
        """
        kmers = []
        for seq in sequences:
            seq_kmers = [seq[i:i+k] for i in range(len(seq) - k + 1)]
            kmers.append(' '.join(seq_kmers))
        
        if self.vectorizer is None:
            self.vectorizer = CountVectorizer(analyzer='word', token_pattern=r'\S+')
            X = self.vectorizer.fit_transform(kmers).toarray()
        else:
            X = self.vectorizer.transform(kmers).toarray()
        
        return X
    
    def nucleotide_composition(self, sequences):
        """
        Calculate nucleotide composition features.
        
        Parameters:
        -----------
        sequences : list
            List of DNA sequences
            
        Returns:
        --------
        array : numpy array of nucleotide composition features
        """
        features = []
        nucleotides = ['A', 'T', 'G', 'C']
        
        for seq in sequences:
            seq = seq.upper()
            seq_features = []
            
            # Nucleotide frequencies
            for nuc in nucleotides:
                seq_features.append(seq.count(nuc) / len(seq))
            
            # GC content
            gc_content = (seq.count('G') + seq.count('C')) / len(seq)
            seq_features.append(gc_content)
            
            # Dinucleotide frequencies
            for nuc1 in nucleotides:
                for nuc2 in nucleotides:
                    dinuc = nuc1 + nuc2
                    seq_features.append(seq.count(dinuc) / (len(seq) - 1) if len(seq) > 1 else 0)
            
            features.append(seq_features)
        
        return np.array(features)
    
    def onehot_encoding(self, sequences, max_length=50):
        """
        One-hot encode DNA sequences.
        
        Parameters:
        -----------
        sequences : list
            List of DNA sequences
        max_length : int
            Maximum sequence length (default: 50)
            
        Returns:
        --------
        array : numpy array of one-hot encoded sequences
        """
        nuc_to_int = {'A': 0, 'T': 1, 'G': 2, 'C': 3, 'N': 4}
        onehot = np.zeros((len(sequences), max_length, 4))
        
        for i, seq in enumerate(sequences):
            seq = seq.upper()
            for j, nuc in enumerate(seq[:max_length]):
                if nuc in nuc_to_int and nuc_to_int[nuc] < 4:
                    onehot[i, j, nuc_to_int[nuc]] = 1
        
        # Flatten for traditional ML models
        return onehot.reshape(len(sequences), -1)
    
    def encode(self, sequences, fit=True):
        """
        Encode sequences using the specified method.
        
        Parameters:
        -----------
        sequences : list
            List of DNA sequences
        fit : bool
            Whether to fit the encoder (for training data)
            
        Returns:
        --------
        array : Encoded sequences
        """
        if self.method == 'kmer':
            return self.kmer_encoding(sequences, k=self.kmer_size)
        elif self.method == 'nucleotide_composition':
            return self.nucleotide_composition(sequences)
        elif self.method == 'onehot':
            return self.onehot_encoding(sequences)
        else:
            raise ValueError(f"Unknown encoding method: {self.method}")

def load_data(data_path):
    """
    Load and preprocess the genomics data.
    
    Parameters:
    -----------
    data_path : str
        Path to the CSV file
        
    Returns:
    --------
    X : numpy array
        Features (DNA sequences)
    y : numpy array
        Labels (gene expression levels)
    """
    df = pd.read_csv(data_path)
    print(f"Dataset shape: {df.shape}")
    print(f"Label distribution:\n{df['Labels'].value_counts()}")
    
    sequences = df['Sequences'].tolist()
    labels = df['Labels'].values
    
    return sequences, labels

def evaluate_model(model, X_test, y_test, model_name):
    """
    Evaluate a trained model.
    
    Parameters:
    -----------
    model : sklearn model
        Trained model
    X_test : numpy array
        Test features
    y_test : numpy array
        Test labels
    model_name : str
        Name of the model
        
    Returns:
    --------
    dict : Dictionary containing evaluation metrics
    """
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
    
    accuracy = accuracy_score(y_test, y_pred)
    
    metrics = {
        'model_name': model_name,
        'accuracy': accuracy,
        'classification_report': classification_report(y_test, y_pred),
        'confusion_matrix': confusion_matrix(y_test, y_pred),
        'y_pred': y_pred,
        'y_pred_proba': y_pred_proba
    }
    
    if y_pred_proba is not None:
        metrics['roc_auc'] = roc_auc_score(y_test, y_pred_proba)
        metrics['roc_curve'] = roc_curve(y_test, y_pred_proba)
    
    return metrics

def plot_results(metrics_dict, save_path=None):
    """
    Plot evaluation results.
    
    Parameters:
    -----------
    metrics_dict : dict
        Dictionary containing metrics for different models
    save_path : str
        Path to save the plot
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Accuracy comparison
    model_names = list(metrics_dict.keys())
    accuracies = [metrics_dict[m]['accuracy'] for m in model_names]
    
    axes[0, 0].bar(model_names, accuracies, color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6'])
    axes[0, 0].set_title('Model Accuracy Comparison', fontsize=14, fontweight='bold')
    axes[0, 0].set_ylabel('Accuracy')
    axes[0, 0].set_ylim([0, 1])
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    for i, (name, acc) in enumerate(zip(model_names, accuracies)):
        axes[0, 0].text(i, acc + 0.01, f'{acc:.3f}', ha='center', fontweight='bold')
    
    # ROC Curves
    for model_name, metrics in metrics_dict.items():
        if 'roc_curve' in metrics:
            fpr, tpr, _ = metrics['roc_curve']
            auc = metrics.get('roc_auc', 0)
            axes[0, 1].plot(fpr, tpr, label=f'{model_name} (AUC = {auc:.3f})', linewidth=2)
    
    axes[0, 1].plot([0, 1], [0, 1], 'k--', label='Random')
    axes[0, 1].set_xlabel('False Positive Rate')
    axes[0, 1].set_ylabel('True Positive Rate')
    axes[0, 1].set_title('ROC Curves', fontsize=14, fontweight='bold')
    axes[0, 1].legend()
    axes[0, 1].grid(alpha=0.3)
    
    # Confusion Matrix for best model
    best_model = max(metrics_dict.items(), key=lambda x: x[1]['accuracy'])
    cm = best_model[1]['confusion_matrix']
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1, 0])
    axes[1, 0].set_title(f'Confusion Matrix - {best_model[0]}', fontsize=14, fontweight='bold')
    axes[1, 0].set_ylabel('True Label')
    axes[1, 0].set_xlabel('Predicted Label')
    
    # Feature importance (for tree-based models)
    if hasattr(best_model, 'feature_importances_'):
        # This would require the model object, which we don't store in metrics_dict
        # So we'll skip this for now
        axes[1, 1].text(0.5, 0.5, 'Feature Importance\n(available for tree-based models)', 
                       ha='center', va='center', fontsize=12)
        axes[1, 1].set_title('Feature Importance', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Main function to run the gene expression prediction pipeline."""
    
    # Setup paths
    base_path = Path(__file__).parent.parent
    data_path = base_path / 'data' / 'genomics_data.csv'
    results_path = base_path / 'results'
    models_path = base_path / 'models'
    
    results_path.mkdir(exist_ok=True)
    models_path.mkdir(exist_ok=True)
    
    print("=" * 80)
    print("Gene Expression Prediction from DNA Sequences")
    print("=" * 80)
    
    # Load data
    print("\n1. Loading data...")
    sequences, labels = load_data(data_path)
    
    # Encode sequences
    print("\n2. Encoding DNA sequences...")
    encoder = DNASequenceEncoder(method='kmer')
    X = encoder.encode(sequences, fit=True)
    print(f"Encoded feature shape: {X.shape}")
    
    # Split data
    print("\n3. Splitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, test_size=0.2, random_state=42, stratify=labels
    )
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Train multiple models
    print("\n4. Training models...")
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
        'XGBoost': xgb.XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss'),
        'LightGBM': lgb.LGBMClassifier(n_estimators=100, random_state=42, verbose=-1),
        'SVM': SVC(probability=True, random_state=42, kernel='rbf')
    }
    
    metrics_dict = {}
    trained_models = {}
    
    for name, model in models.items():
        print(f"\n   Training {name}...")
        model.fit(X_train, y_train)
        trained_models[name] = model
        
        # Evaluate
        metrics = evaluate_model(model, X_test, y_test, name)
        metrics_dict[name] = metrics
        
        print(f"   Accuracy: {metrics['accuracy']:.4f}")
        if 'roc_auc' in metrics:
            print(f"   ROC-AUC: {metrics['roc_auc']:.4f}")
    
    # Save best model
    best_model_name = max(metrics_dict.items(), key=lambda x: x[1]['accuracy'])[0]
    best_model = trained_models[best_model_name]
    model_file = models_path / f'best_model_{best_model_name.lower().replace(" ", "_")}.pkl'
    joblib.dump(best_model, model_file)
    joblib.dump(encoder, models_path / 'encoder.pkl')
    print(f"\n5. Best model ({best_model_name}) saved to {model_file}")
    
    # Plot results
    print("\n6. Generating plots...")
    plot_results(metrics_dict, save_path=results_path / 'model_comparison.png')
    print(f"   Plots saved to {results_path / 'model_comparison.png'}")
    
    # Print detailed results
    print("\n7. Detailed Results:")
    print("=" * 80)
    for name, metrics in metrics_dict.items():
        print(f"\n{name}:")
        print(f"  Accuracy: {metrics['accuracy']:.4f}")
        if 'roc_auc' in metrics:
            print(f"  ROC-AUC: {metrics['roc_auc']:.4f}")
        print(f"\n  Classification Report:\n{metrics['classification_report']}")
    
    print("\n" + "=" * 80)
    print("Pipeline completed successfully!")
    print("=" * 80)

if __name__ == "__main__":
    main()

