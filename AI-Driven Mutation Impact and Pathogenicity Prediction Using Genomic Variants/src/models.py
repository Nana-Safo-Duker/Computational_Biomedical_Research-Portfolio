"""
Machine Learning Models for Mutation Impact Prediction
Includes various models for predicting functional impact of mutations
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report, confusion_matrix
import joblib
import os
from datetime import datetime


class MutationPredictor:
    """Main class for mutation impact prediction models"""
    
    def __init__(self, model_type='random_forest'):
        """
        Initialize the predictor
        
        Args:
            model_type: Type of model ('random_forest', 'svm', 'logistic', 'gradient_boosting', 'neural_network')
        """
        self.model_type = model_type
        self.model = self._create_model()
        self.is_trained = False
        
    def _create_model(self):
        """Create model based on model_type"""
        models = {
            'random_forest': RandomForestClassifier(
                n_estimators=100,
                max_depth=20,
                random_state=42,
                n_jobs=-1,
                class_weight='balanced'
            ),
            'svm': SVC(
                kernel='rbf',
                probability=True,
                random_state=42,
                class_weight='balanced',
                C=1.0,
                gamma='scale'
            ),
            'logistic': LogisticRegression(
                max_iter=1000,
                random_state=42,
                class_weight='balanced',
                solver='lbfgs'
            ),
            'gradient_boosting': GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            ),
            'neural_network': MLPClassifier(
                hidden_layer_sizes=(100, 50),
                max_iter=500,
                random_state=42,
                learning_rate_init=0.001,
                early_stopping=True,
                validation_fraction=0.1
            )
        }
        
        if self.model_type not in models:
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        return models[self.model_type]
    
    def train(self, X_train, y_train):
        """
        Train the model
        
        Args:
            X_train: Training features
            y_train: Training labels
        """
        print(f"Training {self.model_type} model...")
        self.model.fit(X_train, y_train)
        self.is_trained = True
        print("Training completed!")
    
    def predict(self, X):
        """
        Predict labels for given features
        
        Args:
            X: Features to predict
            
        Returns:
            Predicted labels
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """
        Predict probabilities for given features
        
        Args:
            X: Features to predict
            
        Returns:
            Predicted probabilities
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        return self.model.predict_proba(X)
    
    def evaluate(self, X_test, y_test):
        """
        Evaluate model performance
        
        Args:
            X_test: Test features
            y_test: Test labels
            
        Returns:
            Dictionary with evaluation metrics
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")
        
        y_pred = self.predict(X_test)
        y_proba = self.predict_proba(X_test)[:, 1]
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_test, y_pred, average='weighted', zero_division=0),
            'roc_auc': roc_auc_score(y_test, y_proba) if len(np.unique(y_test)) > 1 else 0.0
        }
        
        print("\n" + "="*50)
        print(f"Model: {self.model_type.upper()}")
        print("="*50)
        print(f"Accuracy:  {metrics['accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall:    {metrics['recall']:.4f}")
        print(f"F1 Score:  {metrics['f1_score']:.4f}")
        print(f"ROC-AUC:   {metrics['roc_auc']:.4f}")
        print("="*50)
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, zero_division=0))
        
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        return metrics
    
    def save_model(self, filepath=None):
        """
        Save the trained model
        
        Args:
            filepath: Path to save the model
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        
        if filepath is None:
            models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
            os.makedirs(models_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(models_dir, f"{self.model_type}_{timestamp}.pkl")
        
        joblib.dump(self.model, filepath)
        print(f"Model saved to {filepath}")
        return filepath
    
    def load_model(self, filepath):
        """
        Load a trained model
        
        Args:
            filepath: Path to the model file
        """
        self.model = joblib.load(filepath)
        self.is_trained = True
        print(f"Model loaded from {filepath}")


class ModelEnsemble:
    """Ensemble of multiple models for improved prediction"""
    
    def __init__(self, model_types=None):
        """
        Initialize ensemble
        
        Args:
            model_types: List of model types to include in ensemble
        """
        if model_types is None:
            model_types = ['random_forest', 'gradient_boosting', 'logistic']
        
        self.models = [MutationPredictor(mt) for mt in model_types]
        self.is_trained = False
    
    def train(self, X_train, y_train):
        """Train all models in the ensemble"""
        for model in self.models:
            model.train(X_train, y_train)
        self.is_trained = True
    
    def predict(self, X, method='voting'):
        """
        Predict using ensemble
        
        Args:
            X: Features to predict
            method: Ensemble method ('voting', 'averaging')
            
        Returns:
            Predicted labels
        """
        if not self.is_trained:
            raise ValueError("Models must be trained before prediction")
        
        if method == 'voting':
            predictions = np.array([model.predict(X) for model in self.models])
            # Majority voting
            return np.round(predictions.mean(axis=0)).astype(int)
        elif method == 'averaging':
            probabilities = np.array([model.predict_proba(X)[:, 1] for model in self.models])
            # Average probabilities
            avg_proba = probabilities.mean(axis=0)
            return (avg_proba > 0.5).astype(int)
        else:
            raise ValueError(f"Unknown ensemble method: {method}")
    
    def evaluate(self, X_test, y_test, method='voting'):
        """Evaluate ensemble performance"""
        y_pred = self.predict(X_test, method=method)
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_test, y_pred, average='weighted', zero_division=0)
        }
        
        print("\n" + "="*50)
        print("ENSEMBLE MODEL RESULTS")
        print("="*50)
        print(f"Accuracy:  {metrics['accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall:    {metrics['recall']:.4f}")
        print(f"F1 Score:  {metrics['f1_score']:.4f}")
        print("="*50)
        
        return metrics



