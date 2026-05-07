"""
Machine Learning Pipeline for DNA-Based Biomarker Discovery

This script trains machine learning models to identify potential biomarkers
and drug targets from DNA sequence features.

Author: DNA-Based Biomarker Discovery Project
Date: 2025
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report, confusion_matrix, 
    roc_auc_score, roc_curve, accuracy_score
)
from sklearn.preprocessing import StandardScaler
import joblib
import argparse
import os
import sys

# Import feature extraction function
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dna_feature_extraction import extract_dna_features, get_feature_names


def train_models(X_train, y_train, X_test, y_test, use_scaling=True):
    """
    Train multiple machine learning models and evaluate their performance.
    
    Parameters:
    -----------
    X_train : np.ndarray
        Training feature matrix
    y_train : np.ndarray
        Training labels
    X_test : np.ndarray
        Test feature matrix
    y_test : np.ndarray
        Test labels
    use_scaling : bool
        Whether to scale features for models that require it
        
    Returns:
    --------
    dict
        Dictionary containing trained models and their performance metrics
    """
    # Scale features if needed
    scaler = None
    if use_scaling:
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
    
    # Define models
    models = {
        'Random Forest': RandomForestClassifier(
            n_estimators=100, 
            random_state=42, 
            n_jobs=-1,
            max_depth=10
        ),
        'Gradient Boosting': GradientBoostingClassifier(
            n_estimators=100, 
            random_state=42,
            max_depth=5
        ),
        'SVM': SVC(
            kernel='rbf', 
            probability=True, 
            random_state=42,
            C=1.0,
            gamma='scale'
        ),
        'Logistic Regression': LogisticRegression(
            random_state=42, 
            max_iter=1000, 
            n_jobs=-1,
            C=1.0
        )
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\n{'='*50}")
        print(f"Training {name}...")
        print(f"{'='*50}")
        
        # Use scaled data for SVM and Logistic Regression
        if name in ['SVM', 'Logistic Regression'] and use_scaling:
            X_train_use = X_train_scaled
            X_test_use = X_test_scaled
        else:
            X_train_use = X_train
            X_test_use = X_test
        
        # Train model
        model.fit(X_train_use, y_train)
        
        # Predictions
        y_pred = model.predict(X_test_use)
        y_pred_proba = model.predict_proba(X_test_use)[:, 1]
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        auc_score = roc_auc_score(y_test, y_pred_proba)
        
        # Cross-validation
        cv_scores = cross_val_score(
            model, X_train_use, y_train, 
            cv=5, scoring='accuracy', n_jobs=-1
        )
        
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'auc': auc_score,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba
        }
        
        print(f"Accuracy: {accuracy:.4f}")
        print(f"AUC-ROC: {auc_score:.4f}")
        print(f"CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred))
    
    return results, scaler


def get_feature_importance(model, feature_names):
    """
    Get feature importance from a tree-based model.
    
    Parameters:
    -----------
    model : sklearn model
        Trained model with feature_importances_ attribute
    feature_names : List[str]
        List of feature names
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with features and their importance scores
    """
    if hasattr(model, 'feature_importances_'):
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        return importance_df
    else:
        return None


def main():
    """Main function to run the ML pipeline."""
    parser = argparse.ArgumentParser(
        description='Train ML models for DNA biomarker discovery'
    )
    parser.add_argument(
        '--input', 
        type=str, 
        default='../data/genomics_data.csv',
        help='Path to input CSV file with DNA sequences'
    )
    parser.add_argument(
        '--features', 
        type=str, 
        default=None,
        help='Path to pre-extracted features CSV (optional)'
    )
    parser.add_argument(
        '--output-dir', 
        type=str, 
        default='../results/models',
        help='Directory to save trained models'
    )
    parser.add_argument(
        '--test-size',
        type=float,
        default=0.2,
        help='Proportion of data to use for testing'
    )
    parser.add_argument(
        '--random-state',
        type=int,
        default=42,
        help='Random state for reproducibility'
    )
    
    args = parser.parse_args()
    
    # Load data
    print(f"Loading data from {args.input}...")
    df = pd.read_csv(args.input)
    
    # Extract or load features
    if args.features and os.path.exists(args.features):
        print(f"Loading pre-extracted features from {args.features}...")
        features_df = pd.read_csv(args.features)
        if 'Labels' in features_df.columns:
            X = features_df.drop('Labels', axis=1).values
            y = features_df['Labels'].values
        else:
            X = features_df.values
            y = df['Labels'].values
        feature_names = features_df.columns.tolist()
        if 'Labels' in feature_names:
            feature_names.remove('Labels')
    else:
        print("Extracting features from DNA sequences...")
        sequences = df['Sequences'].values.tolist()
        X = extract_dna_features(sequences)
        y = df['Labels'].values
        feature_names = get_feature_names()
    
    print(f"Feature matrix shape: {X.shape}")
    print(f"Number of features: {X.shape[1]}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=args.test_size, 
        random_state=args.random_state, 
        stratify=y
    )
    
    print(f"\nTraining set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")
    
    # Train models
    results, scaler = train_models(X_train, y_train, X_test, y_test)
    
    # Find best model
    best_model_name = max(results.keys(), key=lambda x: results[x]['auc'])
    best_model = results[best_model_name]['model']
    
    print(f"\n{'='*50}")
    print(f"Best model: {best_model_name}")
    print(f"Best AUC-ROC: {results[best_model_name]['auc']:.4f}")
    print(f"Best accuracy: {results[best_model_name]['accuracy']:.4f}")
    print(f"{'='*50}")
    
    # Get feature importance
    if hasattr(best_model, 'feature_importances_'):
        importance_df = get_feature_importance(best_model, feature_names)
        print(f"\nTop 10 Most Important Features:")
        print(importance_df.head(10))
        
        # Save feature importance
        importance_path = os.path.join(args.output_dir, 'feature_importance.csv')
        os.makedirs(args.output_dir, exist_ok=True)
        importance_df.to_csv(importance_path, index=False)
        print(f"\nFeature importance saved to {importance_path}")
    
    # Save models
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Save best model
    best_model_path = os.path.join(
        args.output_dir, 
        f'best_model_{best_model_name.lower().replace(" ", "_")}.pkl'
    )
    joblib.dump(best_model, best_model_path)
    print(f"Best model saved to {best_model_path}")
    
    # Save scaler if used
    if scaler is not None:
        scaler_path = os.path.join(args.output_dir, 'scaler.pkl')
        joblib.dump(scaler, scaler_path)
        print(f"Scaler saved to {scaler_path}")
    
    # Save feature names
    feature_names_path = os.path.join(args.output_dir, 'feature_names.pkl')
    joblib.dump(feature_names, feature_names_path)
    print(f"Feature names saved to {feature_names_path}")
    
    # Save results summary
    results_summary = pd.DataFrame({
        'Model': list(results.keys()),
        'Accuracy': [results[m]['accuracy'] for m in results.keys()],
        'AUC-ROC': [results[m]['auc'] for m in results.keys()],
        'CV Accuracy': [results[m]['cv_mean'] for m in results.keys()],
        'CV Std': [results[m]['cv_std'] for m in results.keys()]
    })
    results_path = os.path.join(args.output_dir, 'model_comparison.csv')
    results_summary.to_csv(results_path, index=False)
    print(f"Results summary saved to {results_path}")
    
    print("\nPipeline complete!")


if __name__ == "__main__":
    main()

