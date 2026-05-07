"""
DNA Sequence Feature Extraction for Biomarker Discovery and Drug Target Identification

This script extracts comprehensive features from DNA sequences that can be used
to identify potential biomarkers and drug targets.

Author: DNA-Based Biomarker Discovery Project
Date: 2025
"""

import pandas as pd
import numpy as np
from typing import List, Tuple
import argparse
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def extract_dna_features(sequences: List[str]) -> np.ndarray:
    """
    Extract comprehensive features from DNA sequences.
    
    Features include:
    - Nucleotide composition (A, T, G, C frequencies)
    - GC content and GC skew
    - AT content and AT skew
    - Dinucleotide frequencies (16 combinations)
    - Trinucleotide frequencies (20 most common)
    - K-mer frequencies
    - Sequence complexity (Shannon entropy)
    - Purine/Pyrimidine ratio
    - Homopolymer runs
    - Sequence length (normalized)
    
    Parameters:
    -----------
    sequences : List[str]
        List of DNA sequences
        
    Returns:
    --------
    np.ndarray
        Feature matrix with shape (n_sequences, n_features)
    """
    features = []
    
    for seq in sequences:
        seq = seq.upper()
        seq_len = len(seq)
        
        if seq_len == 0:
            # Return zero vector for empty sequences
            features.append([0] * 48)
            continue
        
        # 1. Nucleotide composition
        a_count = seq.count('A') / seq_len
        t_count = seq.count('T') / seq_len
        g_count = seq.count('G') / seq_len
        c_count = seq.count('C') / seq_len
        
        # 2. GC content
        gc_content = (seq.count('G') + seq.count('C')) / seq_len
        
        # 3. AT content
        at_content = (seq.count('A') + seq.count('T')) / seq_len
        
        # 4. GC skew
        g_count_abs = seq.count('G')
        c_count_abs = seq.count('C')
        gc_skew = (g_count_abs - c_count_abs) / (g_count_abs + c_count_abs) if (g_count_abs + c_count_abs) > 0 else 0
        
        # 5. AT skew
        a_count_abs = seq.count('A')
        t_count_abs = seq.count('T')
        at_skew = (a_count_abs - t_count_abs) / (a_count_abs + t_count_abs) if (a_count_abs + t_count_abs) > 0 else 0
        
        # 6. Dinucleotide frequencies (16 possible combinations)
        dinucleotides = ['AA', 'AT', 'AG', 'AC', 'TA', 'TT', 'TG', 'TC', 
                        'GA', 'GT', 'GG', 'GC', 'CA', 'CT', 'CG', 'CC']
        dinuc_freq = [seq.count(dinuc) / (seq_len - 1) if seq_len > 1 else 0 for dinuc in dinucleotides]
        
        # 7. Trinucleotide frequencies (20 most common trinucleotides)
        trinucleotides = ['AAA', 'AAT', 'AAG', 'AAC', 'ATA', 'ATT', 'ATG', 'ATC',
                         'AGA', 'AGT', 'AGG', 'AGC', 'ACA', 'ACT', 'ACG', 'ACC',
                         'TAA', 'TAT', 'TAG', 'TAC']
        trinuc_freq = [seq.count(trinuc) / (seq_len - 2) if seq_len > 2 else 0 for trinuc in trinucleotides]
        
        # 8. Sequence complexity (Shannon entropy)
        nucleotide_counts = [seq.count('A'), seq.count('T'), seq.count('G'), seq.count('C')]
        nucleotide_probs = [count / seq_len for count in nucleotide_counts if seq_len > 0]
        shannon_entropy = -sum(p * np.log2(p) for p in nucleotide_probs if p > 0)
        
        # 9. Purine/Pyrimidine ratio
        purine_count = seq.count('A') + seq.count('G')
        pyrimidine_count = seq.count('C') + seq.count('T')
        pur_pyr_ratio = purine_count / pyrimidine_count if pyrimidine_count > 0 else 0
        
        # 10. Sequence length (normalized)
        normalized_length = seq_len / 100.0  # Assuming max length around 100
        
        # 11. Homopolymer runs (consecutive same nucleotides)
        max_homopolymer = max(
            len(max(seq.split('A'), key=len)) if 'A' in seq else 0,
            len(max(seq.split('T'), key=len)) if 'T' in seq else 0,
            len(max(seq.split('G'), key=len)) if 'G' in seq else 0,
            len(max(seq.split('C'), key=len)) if 'C' in seq else 0
        ) if seq_len > 0 else 0
        
        # Combine all features
        feature_vector = [
            a_count, t_count, g_count, c_count,
            gc_content, at_content, gc_skew, at_skew,
            shannon_entropy, pur_pyr_ratio, normalized_length, max_homopolymer
        ] + dinuc_freq + trinuc_freq
        
        features.append(feature_vector)
    
    return np.array(features)


def get_feature_names() -> List[str]:
    """
    Get names of all extracted features.
    
    Returns:
    --------
    List[str]
        List of feature names
    """
    feature_names = [
        'A_freq', 'T_freq', 'G_freq', 'C_freq',
        'GC_content', 'AT_content', 'GC_skew', 'AT_skew',
        'Shannon_entropy', 'Pur_Pyr_ratio', 'Normalized_length', 'Max_homopolymer'
    ]
    
    # Dinucleotide feature names
    dinucleotides = ['AA', 'AT', 'AG', 'AC', 'TA', 'TT', 'TG', 'TC', 
                    'GA', 'GT', 'GG', 'GC', 'CA', 'CT', 'CG', 'CC']
    feature_names.extend([f'Dinuc_{dinuc}' for dinuc in dinucleotides])
    
    # Trinucleotide feature names
    trinucleotides = ['AAA', 'AAT', 'AAG', 'AAC', 'ATA', 'ATT', 'ATG', 'ATC',
                     'AGA', 'AGT', 'AGG', 'AGC', 'ACA', 'ACT', 'ACG', 'ACC',
                     'TAA', 'TAT', 'TAG', 'TAC']
    feature_names.extend([f'Trinuc_{trinuc}' for trinuc in trinucleotides])
    
    return feature_names


def main():
    """Main function to extract features from DNA sequences."""
    parser = argparse.ArgumentParser(
        description='Extract features from DNA sequences for biomarker discovery'
    )
    parser.add_argument(
        '--input', 
        type=str, 
        default='../data/genomics_data.csv',
        help='Path to input CSV file with DNA sequences'
    )
    parser.add_argument(
        '--output', 
        type=str, 
        default='../results/dna_features.csv',
        help='Path to output CSV file with extracted features'
    )
    parser.add_argument(
        '--sequence-column',
        type=str,
        default='Sequences',
        help='Name of the column containing DNA sequences'
    )
    
    args = parser.parse_args()
    
    # Load data
    print(f"Loading data from {args.input}...")
    df = pd.read_csv(args.input)
    
    if args.sequence_column not in df.columns:
        raise ValueError(f"Column '{args.sequence_column}' not found in data. Available columns: {df.columns.tolist()}")
    
    # Extract features
    print("Extracting features from DNA sequences...")
    sequences = df[args.sequence_column].values.tolist()
    X = extract_dna_features(sequences)
    
    # Create feature DataFrame
    feature_names = get_feature_names()
    features_df = pd.DataFrame(X, columns=feature_names)
    
    # Add original columns if they exist (e.g., Labels)
    if 'Labels' in df.columns:
        features_df['Labels'] = df['Labels'].values
    
    # Save features
    print(f"Saving features to {args.output}...")
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    features_df.to_csv(args.output, index=False)
    
    print(f"Feature extraction complete!")
    print(f"  - Number of sequences: {len(sequences)}")
    print(f"  - Number of features: {X.shape[1]}")
    print(f"  - Features saved to: {args.output}")


if __name__ == "__main__":
    main()

