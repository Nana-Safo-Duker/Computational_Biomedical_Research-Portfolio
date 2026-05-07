"""
Quick Start Example for Mutation Impact Prediction

This script demonstrates a simple workflow for predicting mutation impact.
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_loader import GenomicsDataLoader
from models import MutationPredictor


def main():
    """Quick start example"""
    
    print("="*60)
    print("Mutation Impact Prediction - Quick Start")
    print("="*60)
    
    # Step 1: Load and prepare data
    print("\n1. Loading and preparing data...")
    loader = GenomicsDataLoader()
    
    # Get dataset information
    data_info = loader.get_data_info()
    print(f"   Total samples: {data_info['total_samples']}")
    print(f"   Sequence length: {data_info['sequence_length']}")
    print(f"   Class distribution: {data_info['class_distribution']}")
    
    # Prepare data with one-hot encoding
    X_train, X_test, y_train, y_test = loader.prepare_data(
        encoding_method='onehot',
        test_size=0.2,
        random_state=42
    )
    
    # Step 2: Train a model
    print("\n2. Training Random Forest model...")
    model = MutationPredictor(model_type='random_forest')
    model.train(X_train, y_train)
    
    # Step 3: Evaluate the model
    print("\n3. Evaluating model...")
    metrics = model.evaluate(X_test, y_test)
    
    # Step 4: Make predictions on example sequences
    print("\n4. Making predictions on example sequences...")
    example_sequences = [
        "CCGAGGGCTATGGTTTGGAAGTTAGAACCCTGGGGCTTCTCGCGGACACC",
        "GTCCACGACCGAACTCCCACCTTGACCGCAGAGGTACCACCAGAGCCCTG"
    ]
    
    example_X = loader.encode_sequences(example_sequences, method='onehot')
    predictions = model.predict(example_X)
    probabilities = model.predict_proba(example_X)
    
    for i, (seq, pred, prob) in enumerate(zip(example_sequences, predictions, probabilities)):
        status = "Pathogenic" if pred == 1 else "Benign"
        print(f"\n   Sequence {i+1}:")
        print(f"   Prediction: {status}")
        print(f"   Confidence: {prob[1]:.4f} (pathogenic), {prob[0]:.4f} (benign)")
    
    # Step 5: Save the model
    print("\n5. Saving model...")
    model_path = model.save_model()
    print(f"   Model saved to: {model_path}")
    
    print("\n" + "="*60)
    print("Quick start completed successfully!")
    print("="*60)


if __name__ == "__main__":
    main()


