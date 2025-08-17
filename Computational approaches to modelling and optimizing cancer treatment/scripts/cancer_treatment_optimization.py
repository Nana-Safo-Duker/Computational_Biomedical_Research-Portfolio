"""
Computational Approaches to Cancer Treatment Optimization

This module contains functions for modeling and optimizing cancer treatment
using machine learning and optimization algorithms.

Author: Cancer Research Team
Date: 2024
License: MIT
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, roc_auc_score, mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import minimize
from scipy.stats import ttest_ind
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(171)


class TreatmentResponsePredictor:
    """
    Predicts patient response to cancer treatment based on genomic and clinical features.
    """
    
    def __init__(self, n_estimators=100, random_state=42):
        """
        Initialize the treatment response predictor.
        
        Parameters:
        -----------
        n_estimators : int
            Number of trees in the random forest
        random_state : int
            Random seed for reproducibility
        """
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=random_state,
            max_depth=10,
            min_samples_split=5
        )
        self.scaler = StandardScaler()
        self.feature_names = None
        
    def prepare_data(self, genomic_data, clinical_data, response_labels):
        """
        Prepare and combine genomic and clinical data for model training.
        
        Parameters:
        -----------
        genomic_data : pd.DataFrame
            Genomic features (mutations, expression levels, etc.)
        clinical_data : pd.DataFrame
            Clinical features (age, stage, etc.)
        response_labels : pd.Series
            Binary response labels (1 = responder, 0 = non-responder)
            
        Returns:
        --------
        X : pd.DataFrame
            Combined feature matrix
        y : pd.Series
            Response labels
        """
        # Combine genomic and clinical features
        X = pd.concat([genomic_data, clinical_data], axis=1)
        self.feature_names = X.columns.tolist()
        
        # Remove any missing values
        X = X.dropna()
        y = response_labels.loc[X.index]
        
        return X, y
    
    def train(self, X, y):
        """
        Train the treatment response prediction model.
        
        Parameters:
        -----------
        X : pd.DataFrame
            Feature matrix
        y : pd.Series
            Response labels
        """
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
        
        # Train model
        self.model.fit(X_scaled_df, y)
        
        # Calculate feature importance
        self.feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
    def predict(self, X):
        """
        Predict treatment response for new patients.
        
        Parameters:
        -----------
        X : pd.DataFrame
            Feature matrix for prediction
            
        Returns:
        --------
        predictions : np.array
            Predicted response probabilities
        """
        X_scaled = self.scaler.transform(X)
        X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
        return self.model.predict_proba(X_scaled_df)[:, 1]
    
    def evaluate(self, X, y):
        """
        Evaluate model performance.
        
        Parameters:
        -----------
        X : pd.DataFrame
            Feature matrix
        y : pd.Series
            True labels
            
        Returns:
        --------
        metrics : dict
            Dictionary of evaluation metrics
        """
        predictions = self.predict(X)
        predictions_binary = (predictions > 0.5).astype(int)
        
        accuracy = accuracy_score(y, predictions_binary)
        auc = roc_auc_score(y, predictions)
        
        return {
            'accuracy': accuracy,
            'roc_auc': auc,
            'predictions': predictions
        }


class DrugDosingOptimizer:
    """
    Optimizes drug dosing schedules using pharmacokinetic modeling.
    """
    
    def __init__(self, half_life, max_dose, target_concentration):
        """
        Initialize the dosing optimizer.
        
        Parameters:
        -----------
        half_life : float
            Drug half-life in hours
        max_dose : float
            Maximum safe dose (mg)
        target_concentration : float
            Target therapeutic concentration (mg/L)
        """
        self.half_life = half_life
        self.max_dose = max_dose
        self.target_concentration = target_concentration
        
    def pharmacokinetic_model(self, dose, time_points, clearance_rate, volume):
        """
        Simple one-compartment pharmacokinetic model.
        
        Parameters:
        -----------
        dose : float
            Drug dose (mg)
        time_points : np.array
            Time points for simulation (hours)
        clearance_rate : float
            Drug clearance rate (L/h)
        volume : float
            Volume of distribution (L)
            
        Returns:
        --------
        concentrations : np.array
            Drug concentrations over time
        """
        # Calculate elimination rate constant
        k_el = np.log(2) / self.half_life
        
        # Calculate concentrations (simple exponential decay)
        concentrations = (dose / volume) * np.exp(-k_el * time_points)
        
        return concentrations
    
    def objective_function(self, doses, time_points, clearance_rate, volume):
        """
        Objective function for dose optimization.
        Minimizes deviation from target concentration while maximizing efficacy.
        
        Parameters:
        -----------
        doses : np.array
            Array of doses for each administration
        time_points : np.array
            Time points for simulation
        clearance_rate : float
            Drug clearance rate
        volume : float
            Volume of distribution
            
        Returns:
        --------
        objective_value : float
            Objective function value to minimize
        """
        # Simulate pharmacokinetics for all doses
        total_concentration = np.zeros_like(time_points)
        
        for i, dose in enumerate(doses):
            # Time offset for each dose administration
            dose_times = time_points - (i * 24)  # Assuming 24-hour intervals
            dose_times = dose_times[dose_times >= 0]
            
            if len(dose_times) > 0:
                concentrations = self.pharmacokinetic_model(
                    dose, dose_times, clearance_rate, volume
                )
                # Add to total concentration
                total_concentration[len(time_points) - len(dose_times):] += concentrations
        
        # Calculate deviation from target
        deviation = np.mean((total_concentration - self.target_concentration) ** 2)
        
        # Penalty for exceeding max dose
        penalty = np.sum(np.maximum(0, doses - self.max_dose) ** 2) * 100
        
        return deviation + penalty
    
    def optimize_dosing_schedule(self, n_doses=7, clearance_rate=2.0, volume=50.0):
        """
        Optimize dosing schedule for a treatment cycle.
        
        Parameters:
        -----------
        n_doses : int
            Number of doses in the treatment cycle
        clearance_rate : float
            Drug clearance rate (L/h)
        volume : float
            Volume of distribution (L)
            
        Returns:
        --------
        optimal_doses : np.array
            Optimized doses
        """
        # Initialize time points (7 days, hourly resolution)
        time_points = np.arange(0, 7 * 24, 1)
        
        # Initial guess (equal doses)
        initial_doses = np.ones(n_doses) * self.max_dose * 0.7
        
        # Constraints: doses must be positive and <= max_dose
        bounds = [(0, self.max_dose) for _ in range(n_doses)]
        
        # Optimize
        result = minimize(
            self.objective_function,
            initial_doses,
            args=(time_points, clearance_rate, volume),
            method='L-BFGS-B',
            bounds=bounds
        )
        
        return result.x


def generate_synthetic_data(n_samples=200, n_genomic_features=50, random_state=42):
    """
    Generate synthetic genomic and clinical data for demonstration.
    
    Parameters:
    -----------
    n_samples : int
        Number of samples
    n_genomic_features : int
        Number of genomic features
    random_state : int
        Random seed
        
    Returns:
    --------
    genomic_data : pd.DataFrame
        Synthetic genomic features
    clinical_data : pd.DataFrame
        Synthetic clinical features
    response_labels : pd.Series
        Binary response labels
    """
    np.random.seed(random_state)
    
    # Generate genomic features (e.g., gene expression, mutation counts)
    genomic_data = pd.DataFrame(
        np.random.randn(n_samples, n_genomic_features),
        columns=[f'gene_{i}' for i in range(n_genomic_features)]
    )
    
    # Generate clinical features
    clinical_data = pd.DataFrame({
        'age': np.random.normal(60, 15, n_samples),
        'stage': np.random.choice([1, 2, 3, 4], n_samples),
        'tumor_size': np.random.gamma(2, 5, n_samples),
        'mutational_burden': np.random.poisson(10, n_samples)
    })
    
    # Generate response labels based on a simple rule (for demonstration)
    # Higher expression of certain genes and younger age favor response
    response_probability = (
        0.3 +
        0.2 * (genomic_data['gene_0'] > 0) +
        0.2 * (genomic_data['gene_1'] > 0) +
        0.1 * (clinical_data['age'] < 65) +
        0.1 * (clinical_data['mutational_burden'] > 8)
    )
    response_labels = (np.random.rand(n_samples) < response_probability).astype(int)
    response_labels = pd.Series(response_labels)
    
    return genomic_data, clinical_data, response_labels


def statistical_comparison(group1, group2, test_name='t-test'):
    """
    Perform statistical comparison between two groups.
    
    Parameters:
    -----------
    group1 : np.array
        Data for group 1
    group2 : np.array
        Data for group 2
    test_name : str
        Name of the statistical test
        
    Returns:
    --------
    results : dict
        Statistical test results
    """
    if test_name == 't-test':
        statistic, p_value = ttest_ind(group1, group2)
        
        return {
            'test': 't-test',
            'statistic': statistic,
            'p_value': p_value,
            'mean_group1': np.mean(group1),
            'mean_group2': np.mean(group2),
            'std_group1': np.std(group1),
            'std_group2': np.std(group2)
        }


def plot_results(predictor, X_test, y_test, save_path='treatment_response_analysis.png'):
    """
    Create visualization of treatment response predictions.
    
    Parameters:
    -----------
    predictor : TreatmentResponsePredictor
        Trained predictor model
    X_test : pd.DataFrame
        Test feature matrix
    y_test : pd.Series
        True test labels
    save_path : str
        Path to save the figure
    """
    # Get predictions
    predictions = predictor.predict(X_test)
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Plot 1: Prediction distribution
    axes[0, 0].hist(predictions[y_test == 0], bins=30, alpha=0.7, label='Non-responders', color='red')
    axes[0, 0].hist(predictions[y_test == 1], bins=30, alpha=0.7, label='Responders', color='green')
    axes[0, 0].set_xlabel('Predicted Response Probability')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].set_title('Distribution of Predicted Response Probabilities')
    axes[0, 0].legend()
    axes[0, 0].axvline(0.5, color='black', linestyle='--', label='Decision Threshold')
    
    # Plot 2: ROC curve data
    from sklearn.metrics import roc_curve
    fpr, tpr, thresholds = roc_curve(y_test, predictions)
    axes[0, 1].plot(fpr, tpr, linewidth=2)
    axes[0, 1].plot([0, 1], [0, 1], 'k--', label='Random')
    axes[0, 1].set_xlabel('False Positive Rate')
    axes[0, 1].set_ylabel('True Positive Rate')
    axes[0, 1].set_title('ROC Curve')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Feature importance (top 10)
    top_features = predictor.feature_importance.head(10)
    axes[1, 0].barh(range(len(top_features)), top_features['importance'])
    axes[1, 0].set_yticks(range(len(top_features)))
    axes[1, 0].set_yticklabels(top_features['feature'])
    axes[1, 0].set_xlabel('Importance')
    axes[1, 0].set_title('Top 10 Most Important Features')
    axes[1, 0].invert_yaxis()
    
    # Plot 4: Confusion matrix
    from sklearn.metrics import confusion_matrix
    predictions_binary = (predictions > 0.5).astype(int)
    cm = confusion_matrix(y_test, predictions_binary)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1, 1])
    axes[1, 1].set_xlabel('Predicted')
    axes[1, 1].set_ylabel('Actual')
    axes[1, 1].set_title('Confusion Matrix')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Figure saved to {save_path}")


def main():
    """
    Main function demonstrating cancer treatment optimization pipeline.
    """
    print("=" * 60)
    print("Computational Cancer Treatment Optimization Pipeline")
    print("=" * 60)
    
    # Step 1: Generate or load data
    print("\n[1] Generating synthetic data...")
    genomic_data, clinical_data, response_labels = generate_synthetic_data(
        n_samples=200,
        n_genomic_features=50
    )
    print(f"Generated data: {len(genomic_data)} samples, {len(genomic_data.columns)} genomic features")
    
    # Step 2: Prepare data
    print("\n[2] Preparing data...")
    predictor = TreatmentResponsePredictor()
    X, y = predictor.prepare_data(genomic_data, clinical_data, response_labels)
    
    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    print(f"Response rate: {y.mean():.2%}")
    
    # Step 3: Train model
    print("\n[3] Training treatment response predictor...")
    predictor.train(X_train, y_train)
    print("Model training completed!")
    
    # Step 4: Evaluate model
    print("\n[4] Evaluating model performance...")
    train_metrics = predictor.evaluate(X_train, y_train)
    test_metrics = predictor.evaluate(X_test, y_test)
    
    print(f"\nTraining Metrics:")
    print(f"  Accuracy: {train_metrics['accuracy']:.3f}")
    print(f"  ROC-AUC: {train_metrics['roc_auc']:.3f}")
    
    print(f"\nTest Metrics:")
    print(f"  Accuracy: {test_metrics['accuracy']:.3f}")
    print(f"  ROC-AUC: {test_metrics['roc_auc']:.3f}")
    
    # Step 5: Statistical comparison
    print("\n[5] Performing statistical analysis...")
    responders = X_test[y_test == 1]
    non_responders = X_test[y_test == 0]
    
    # Compare a key feature between groups
    key_feature = predictor.feature_importance.iloc[0]['feature']
    stat_results = statistical_comparison(
        responders[key_feature].values,
        non_responders[key_feature].values
    )
    
    print(f"\nStatistical comparison for '{key_feature}':")
    print(f"  Mean (Responders): {stat_results['mean_group1']:.3f}")
    print(f"  Mean (Non-responders): {stat_results['mean_group2']:.3f}")
    print(f"  t-statistic: {stat_results['statistic']:.3f}")
    print(f"  p-value: {stat_results['p_value']:.3f}")
    
    # Step 6: Drug dosing optimization
    print("\n[6] Optimizing drug dosing schedule...")
    optimizer = DrugDosingOptimizer(
        half_life=12.0,  # 12 hours
        max_dose=100.0,  # 100 mg
        target_concentration=5.0  # 5 mg/L
    )
    
    optimal_doses = optimizer.optimize_dosing_schedule(
        n_doses=7,
        clearance_rate=2.0,
        volume=50.0
    )
    
    print(f"\nOptimized dosing schedule (7-day cycle):")
    for i, dose in enumerate(optimal_doses):
        print(f"  Day {i+1}: {dose:.2f} mg")
    print(f"  Total dose per cycle: {np.sum(optimal_doses):.2f} mg")
    
    # Step 7: Create visualizations
    print("\n[7] Generating visualizations...")
    plot_results(predictor, X_test, y_test)
    print("Visualization complete!")
    
    print("\n" + "=" * 60)
    print("Pipeline execution completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
