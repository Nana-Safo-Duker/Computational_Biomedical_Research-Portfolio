"""
Main script for Mutation Impact and Pathogenicity Prediction
"""

import os
import sys
import argparse
from data_loader import GenomicsDataLoader
from models import MutationPredictor, ModelEnsemble


def main():
    """Main function to run the mutation prediction pipeline"""
    
    parser = argparse.ArgumentParser(description='Mutation Impact Prediction')
    parser.add_argument('--data_path', type=str, default=None, help='Path to genomics data CSV')
    parser.add_argument('--encoding', type=str, default='onehot', 
                       choices=['onehot', 'kmer', 'numerical'],
                       help='Sequence encoding method')
    parser.add_argument('--model', type=str, default='random_forest',
                       choices=['random_forest', 'svm', 'logistic', 'gradient_boosting', 'neural_network', 'ensemble'],
                       help='Model type to use')
    parser.add_argument('--test_size', type=float, default=0.2, help='Test set size')
    parser.add_argument('--random_state', type=int, default=42, help='Random state')
    
    args = parser.parse_args()
    
    # Load and prepare data
    print("="*60)
    print("MUTATION IMPACT AND PATHOGENICITY PREDICTION")
    print("="*60)
    
    loader = GenomicsDataLoader(data_path=args.data_path)
    data_info = loader.get_data_info()
    
    print("\nDataset Information:")
    print(f"  Total samples: {data_info['total_samples']}")
    print(f"  Sequence length: {data_info['sequence_length']}")
    print(f"  Class distribution: {data_info['class_distribution']}")
    
    # Prepare data
    X_train, X_test, y_train, y_test = loader.prepare_data(
        encoding_method=args.encoding,
        test_size=args.test_size,
        random_state=args.random_state
    )
    
    # Train model
    if args.model == 'ensemble':
        print("\nTraining ensemble model...")
        model = ModelEnsemble()
        model.train(X_train, y_train)
        model.evaluate(X_test, y_test)
    else:
        print(f"\nTraining {args.model} model...")
        model = MutationPredictor(model_type=args.model)
        model.train(X_train, y_train)
        metrics = model.evaluate(X_test, y_test)
        
        # Save model
        model_path = model.save_model()
        print(f"\nModel saved to: {model_path}")
    
    print("\n" + "="*60)
    print("Pipeline completed successfully!")
    print("="*60)


if __name__ == "__main__":
    main()



