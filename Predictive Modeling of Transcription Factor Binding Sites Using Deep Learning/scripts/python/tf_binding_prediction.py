"""
Transcription Factor Binding Prediction using Deep Learning and Machine Learning

This script implements multiple models for predicting transcription factor binding sites:
1. CNN (Convolutional Neural Network)
2. LSTM (Long Short-Term Memory)
3. Random Forest
4. XGBoost
5. SVM (Support Vector Machine)

Author: AI-ML Bioinformatics Team
Date: 2024
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report, roc_curve, auc
)
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.utils import to_categorical
import warnings
import os
import pickle
import json
from datetime import datetime

warnings.filterwarnings('ignore')

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

class DNASequenceEncoder:
    """Encode DNA sequences to numerical representations."""
    
    def __init__(self):
        self.nucleotide_to_int = {'A': 0, 'T': 1, 'G': 2, 'C': 3}
        self.int_to_nucleotide = {0: 'A', 1: 'T', 2: 'G', 3: 'C'}
    
    def one_hot_encode(self, sequences):
        """
        Convert DNA sequences to one-hot encoded format.
        
        Args:
            sequences: List of DNA sequences (strings)
            
        Returns:
            numpy array of shape (n_samples, sequence_length, 4)
        """
        encoded = np.zeros((len(sequences), len(sequences[0]), 4))
        for i, seq in enumerate(sequences):
            for j, nucleotide in enumerate(seq):
                if nucleotide in self.nucleotide_to_int:
                    encoded[i, j, self.nucleotide_to_int[nucleotide]] = 1
        return encoded
    
    def integer_encode(self, sequences):
        """
        Convert DNA sequences to integer encoding.
        
        Args:
            sequences: List of DNA sequences (strings)
            
        Returns:
            numpy array of shape (n_samples, sequence_length)
        """
        encoded = np.zeros((len(sequences), len(sequences[0])), dtype=int)
        for i, seq in enumerate(sequences):
            for j, nucleotide in enumerate(seq):
                if nucleotide in self.nucleotide_to_int:
                    encoded[i, j] = self.nucleotide_to_int[nucleotide]
        return encoded

class TFBindingPredictor:
    """Main class for Transcription Factor Binding Prediction."""
    
    def __init__(self, data_path='data/genomics_data.csv'):
        self.data_path = data_path
        self.encoder = DNASequenceEncoder()
        self.models = {}
        self.history = {}
        self.results = {}
        
    def load_data(self):
        """Load and preprocess the genomics data."""
        print("Loading data...")
        df = pd.read_csv(self.data_path)
        print(f"Data shape: {df.shape}")
        print(f"Label distribution:\n{df['Labels'].value_counts()}")
        
        sequences = df['Sequences'].values
        labels = df['Labels'].values
        
        # Encode sequences
        X_one_hot = self.encoder.one_hot_encode(sequences)
        X_int = self.encoder.integer_encode(sequences)
        
        # Split data
        self.X_train_oh, self.X_test_oh, self.y_train, self.y_test = train_test_split(
            X_one_hot, labels, test_size=0.2, random_state=42, stratify=labels
        )
        self.X_train_int, self.X_test_int, _, _ = train_test_split(
            X_int, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        # Reshape for traditional ML models (flatten one-hot)
        self.X_train_flat = self.X_train_oh.reshape(self.X_train_oh.shape[0], -1)
        self.X_test_flat = self.X_test_oh.reshape(self.X_test_oh.shape[0], -1)
        
        print(f"Training set size: {self.X_train_oh.shape[0]}")
        print(f"Test set size: {self.X_test_oh.shape[0]}")
        
    def build_cnn_model(self, input_shape, num_classes=1):
        """Build a CNN model for sequence classification."""
        model = models.Sequential([
            layers.Conv1D(64, kernel_size=3, activation='relu', input_shape=input_shape),
            layers.BatchNormalization(),
            layers.MaxPooling1D(2),
            layers.Conv1D(128, kernel_size=3, activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling1D(2),
            layers.Conv1D(256, kernel_size=3, activation='relu'),
            layers.BatchNormalization(),
            layers.GlobalMaxPooling1D(),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(num_classes, activation='sigmoid')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        return model
    
    def build_lstm_model(self, input_shape, num_classes=1):
        """Build an LSTM model for sequence classification."""
        model = models.Sequential([
            layers.LSTM(128, return_sequences=True, input_shape=input_shape),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            layers.LSTM(64, return_sequences=False),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(num_classes, activation='sigmoid')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        return model
    
    def train_cnn(self, epochs=50, batch_size=32):
        """Train CNN model."""
        print("\nTraining CNN model...")
        input_shape = (self.X_train_oh.shape[1], self.X_train_oh.shape[2])
        model = self.build_cnn_model(input_shape)
        
        early_stopping = callbacks.EarlyStopping(
            monitor='val_loss', patience=10, restore_best_weights=True
        )
        reduce_lr = callbacks.ReduceLROnPlateau(
            monitor='val_loss', factor=0.5, patience=5, min_lr=1e-7
        )
        
        self.history['cnn'] = model.fit(
            self.X_train_oh, self.y_train,
            validation_split=0.2,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping, reduce_lr],
            verbose=1
        )
        
        self.models['cnn'] = model
        return model
    
    def train_lstm(self, epochs=50, batch_size=32):
        """Train LSTM model."""
        print("\nTraining LSTM model...")
        input_shape = (self.X_train_oh.shape[1], self.X_train_oh.shape[2])
        model = self.build_lstm_model(input_shape)
        
        early_stopping = callbacks.EarlyStopping(
            monitor='val_loss', patience=10, restore_best_weights=True
        )
        reduce_lr = callbacks.ReduceLROnPlateau(
            monitor='val_loss', factor=0.5, patience=5, min_lr=1e-7
        )
        
        self.history['lstm'] = model.fit(
            self.X_train_oh, self.y_train,
            validation_split=0.2,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping, reduce_lr],
            verbose=1
        )
        
        self.models['lstm'] = model
        return model
    
    def train_random_forest(self, n_estimators=100, max_depth=20):
        """Train Random Forest model."""
        print("\nTraining Random Forest model...")
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42,
            n_jobs=-1,
            class_weight='balanced'
        )
        model.fit(self.X_train_flat, self.y_train)
        self.models['random_forest'] = model
        return model
    
    def train_xgboost(self, n_estimators=100, max_depth=6):
        """Train XGBoost model."""
        print("\nTraining XGBoost model...")
        model = xgb.XGBClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=0.1,
            random_state=42,
            eval_metric='logloss',
            use_label_encoder=False
        )
        model.fit(self.X_train_flat, self.y_train)
        self.models['xgboost'] = model
        return model
    
    def train_svm(self):
        """Train SVM model."""
        print("\nTraining SVM model...")
        # Use a subset for SVM due to computational complexity
        sample_size = min(5000, len(self.X_train_flat))
        indices = np.random.choice(len(self.X_train_flat), sample_size, replace=False)
        X_train_sample = self.X_train_flat[indices]
        y_train_sample = self.y_train[indices]
        
        model = SVC(kernel='rbf', probability=True, random_state=42, class_weight='balanced')
        model.fit(X_train_sample, y_train_sample)
        self.models['svm'] = model
        return model
    
    def evaluate_model(self, model_name, model, X_test, y_test):
        """Evaluate a model and return metrics."""
        if model_name in ['cnn', 'lstm']:
            y_pred_proba = model.predict(X_test, verbose=0).flatten()
            y_pred = (y_pred_proba > 0.5).astype(int)
        else:
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1': f1_score(y_test, y_pred, zero_division=0),
            'roc_auc': roc_auc_score(y_test, y_pred_proba),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'y_pred': y_pred.tolist(),
            'y_pred_proba': y_pred_proba.tolist()
        }
        
        return metrics
    
    def evaluate_all_models(self):
        """Evaluate all trained models."""
        print("\nEvaluating all models...")
        
        for model_name, model in self.models.items():
            if model_name in ['cnn', 'lstm']:
                X_test = self.X_test_oh
            else:
                X_test = self.X_test_flat
            
            metrics = self.evaluate_model(model_name, model, X_test, self.y_test)
            self.results[model_name] = metrics
            
            print(f"\n{model_name.upper()} Results:")
            print(f"Accuracy: {metrics['accuracy']:.4f}")
            print(f"Precision: {metrics['precision']:.4f}")
            print(f"Recall: {metrics['recall']:.4f}")
            print(f"F1-Score: {metrics['f1']:.4f}")
            print(f"ROC-AUC: {metrics['roc_auc']:.4f}")
    
    def plot_training_history(self, model_name):
        """Plot training history for deep learning models."""
        if model_name not in self.history:
            return
        
        history = self.history[model_name].history
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
        # Plot accuracy
        axes[0].plot(history['accuracy'], label='Train Accuracy')
        axes[0].plot(history['val_accuracy'], label='Val Accuracy')
        axes[0].set_title(f'{model_name.upper()} - Accuracy')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Accuracy')
        axes[0].legend()
        axes[0].grid(True)
        
        # Plot loss
        axes[1].plot(history['loss'], label='Train Loss')
        axes[1].plot(history['val_loss'], label='Val Loss')
        axes[1].set_title(f'{model_name.upper()} - Loss')
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('Loss')
        axes[1].legend()
        axes[1].grid(True)
        
        plt.tight_layout()
        plt.savefig(f'results/{model_name}_training_history.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_confusion_matrices(self):
        """Plot confusion matrices for all models."""
        n_models = len(self.results)
        fig, axes = plt.subplots(1, n_models, figsize=(5*n_models, 4))
        
        if n_models == 1:
            axes = [axes]
        
        for idx, (model_name, metrics) in enumerate(self.results.items()):
            cm = np.array(metrics['confusion_matrix'])
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx])
            axes[idx].set_title(f'{model_name.upper()} Confusion Matrix')
            axes[idx].set_ylabel('True Label')
            axes[idx].set_xlabel('Predicted Label')
        
        plt.tight_layout()
        plt.savefig('results/confusion_matrices.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_roc_curves(self):
        """Plot ROC curves for all models."""
        plt.figure(figsize=(10, 8))
        
        for model_name, metrics in self.results.items():
            fpr, tpr, _ = roc_curve(self.y_test, metrics['y_pred_proba'])
            roc_auc = metrics['roc_auc']
            plt.plot(fpr, tpr, label=f'{model_name.upper()} (AUC = {roc_auc:.3f})')
        
        plt.plot([0, 1], [0, 1], 'k--', label='Random')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curves for All Models')
        plt.legend(loc='lower right')
        plt.grid(True)
        plt.savefig('results/roc_curves.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def save_models(self, directory='models'):
        """Save all trained models."""
        os.makedirs(directory, exist_ok=True)
        
        for model_name, model in self.models.items():
            if model_name in ['cnn', 'lstm']:
                model.save(f'{directory}/{model_name}_model.h5')
            else:
                with open(f'{directory}/{model_name}_model.pkl', 'wb') as f:
                    pickle.dump(model, f)
        
        # Save results
        with open(f'{directory}/results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\nModels saved to {directory}/")
    
    def predict(self, sequences, model_name='cnn'):
        """Predict TF binding for new sequences."""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found. Available models: {list(self.models.keys())}")
        
        model = self.models[model_name]
        
        if model_name in ['cnn', 'lstm']:
            X = self.encoder.one_hot_encode(sequences)
            predictions = model.predict(X, verbose=0).flatten()
        else:
            X_one_hot = self.encoder.one_hot_encode(sequences)
            X_flat = X_one_hot.reshape(X_one_hot.shape[0], -1)
            predictions = model.predict_proba(X_flat)[:, 1]
        
        return predictions

def main():
    """Main function to run the TF binding prediction pipeline."""
    # Create results directory
    os.makedirs('results', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    # Initialize predictor
    predictor = TFBindingPredictor(data_path='data/genomics_data.csv')
    
    # Load data
    predictor.load_data()
    
    # Train models
    predictor.train_cnn(epochs=50, batch_size=32)
    predictor.train_lstm(epochs=50, batch_size=32)
    predictor.train_random_forest(n_estimators=100, max_depth=20)
    predictor.train_xgboost(n_estimators=100, max_depth=6)
    predictor.train_svm()
    
    # Evaluate all models
    predictor.evaluate_all_models()
    
    # Plot results
    predictor.plot_training_history('cnn')
    predictor.plot_training_history('lstm')
    predictor.plot_confusion_matrices()
    predictor.plot_roc_curves()
    
    # Save models
    predictor.save_models()
    
    print("\nPipeline completed successfully!")
    print("Results saved in 'results/' directory")
    print("Models saved in 'models/' directory")

if __name__ == '__main__':
    main()

