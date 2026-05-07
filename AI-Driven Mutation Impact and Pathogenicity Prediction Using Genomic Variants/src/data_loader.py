"""
Data Loading and Preprocessing Module
Handles loading and preprocessing of genomics mutation data
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os


class GenomicsDataLoader:
    """Class for loading and preprocessing genomics mutation data"""
    
    def __init__(self, data_path=None):
        """
        Initialize the data loader
        
        Args:
            data_path: Path to the CSV file containing genomics data
        """
        if data_path is None:
            # Default path relative to project root
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_path = os.path.join(current_dir, 'data', 'genomics_data.csv')
            # Also try relative path from current working directory
            if not os.path.exists(data_path):
                alt_path = os.path.join('data', 'genomics_data.csv')
                if os.path.exists(alt_path):
                    data_path = alt_path
        
        self.data_path = data_path
        self.data = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
    def load_data(self):
        """Load data from CSV file"""
        try:
            self.data = pd.read_csv(self.data_path)
            print(f"Data loaded successfully. Shape: {self.data.shape}")
            return self.data
        except FileNotFoundError:
            print(f"Error: File not found at {self.data_path}")
            raise
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            raise
    
    def encode_sequences(self, sequences, method='onehot'):
        """
        Encode DNA sequences to numerical features
        
        Args:
            sequences: List or array of DNA sequences
            method: Encoding method ('onehot', 'kmer', 'numerical')
            
        Returns:
            Encoded sequences as numpy array
        """
        if method == 'onehot':
            return self._onehot_encode(sequences)
        elif method == 'kmer':
            return self._kmer_encode(sequences)
        elif method == 'numerical':
            return self._numerical_encode(sequences)
        else:
            raise ValueError(f"Unknown encoding method: {method}")
    
    def _onehot_encode(self, sequences):
        """One-hot encode DNA sequences"""
        encoding_map = {'A': [1, 0, 0, 0], 'T': [0, 1, 0, 0], 
                       'G': [0, 0, 1, 0], 'C': [0, 0, 0, 1]}
        
        encoded = []
        for seq in sequences:
            seq_encoded = []
            for base in seq.upper():
                if base in encoding_map:
                    seq_encoded.extend(encoding_map[base])
                else:
                    seq_encoded.extend([0, 0, 0, 0])  # Unknown base
            encoded.append(seq_encoded)
        
        return np.array(encoded)
    
    def _kmer_encode(self, sequences, k=3):
        """K-mer frequency encoding"""
        from collections import Counter
        
        # Generate all possible k-mers
        bases = ['A', 'T', 'G', 'C']
        kmer_list = []
        
        def generate_kmers(k, prefix=''):
            if k == 0:
                kmer_list.append(prefix)
                return
            for base in bases:
                generate_kmers(k-1, prefix + base)
        
        generate_kmers(k)
        kmer_dict = {kmer: i for i, kmer in enumerate(kmer_list)}
        
        encoded = []
        for seq in sequences:
            seq = seq.upper()
            kmer_counts = Counter([seq[i:i+k] for i in range(len(seq)-k+1)])
            feature_vector = [kmer_counts.get(kmer, 0) for kmer in kmer_list]
            encoded.append(feature_vector)
        
        return np.array(encoded)
    
    def _numerical_encode(self, sequences):
        """Simple numerical encoding (A=1, T=2, G=3, C=4)"""
        encoding_map = {'A': 1, 'T': 2, 'G': 3, 'C': 4}
        
        encoded = []
        for seq in sequences:
            seq_encoded = [encoding_map.get(base.upper(), 0) for base in seq]
            encoded.append(seq_encoded)
        
        return np.array(encoded)
    
    def prepare_data(self, encoding_method='onehot', test_size=0.2, random_state=42):
        """
        Prepare data for machine learning
        
        Args:
            encoding_method: Method for encoding sequences
            test_size: Proportion of data for testing
            random_state: Random state for reproducibility
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        if self.data is None:
            self.load_data()
        
        # Extract sequences and labels
        sequences = self.data['Sequences'].values
        labels = self.data['Labels'].values
        
        # Encode sequences
        print(f"Encoding sequences using {encoding_method} method...")
        self.X = self.encode_sequences(sequences, method=encoding_method)
        self.y = labels
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=random_state, stratify=self.y
        )
        
        print(f"Training set: {self.X_train.shape}, Test set: {self.X_test.shape}")
        print(f"Class distribution - Train: {np.bincount(self.y_train)}, Test: {np.bincount(self.y_test)}")
        
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    def get_data_info(self):
        """Get information about the dataset"""
        if self.data is None:
            self.load_data()
        
        info = {
            'total_samples': len(self.data),
            'sequence_length': len(self.data['Sequences'].iloc[0]),
            'class_distribution': self.data['Labels'].value_counts().to_dict(),
            'features': list(self.data.columns)
        }
        
        return info

