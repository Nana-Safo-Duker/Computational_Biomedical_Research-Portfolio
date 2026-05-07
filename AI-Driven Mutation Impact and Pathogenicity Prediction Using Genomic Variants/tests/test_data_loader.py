"""
Unit tests for data_loader module
"""

import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_loader import GenomicsDataLoader


class TestDataLoader(unittest.TestCase):
    """Test cases for GenomicsDataLoader"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.loader = GenomicsDataLoader()
    
    def test_load_data(self):
        """Test data loading"""
        try:
            data = self.loader.load_data()
            self.assertIsNotNone(data)
            self.assertGreater(len(data), 0)
        except FileNotFoundError:
            self.skipTest("Data file not found")
    
    def test_encode_sequences_onehot(self):
        """Test one-hot encoding"""
        sequences = ["ATGC", "CGTA"]
        encoded = self.loader.encode_sequences(sequences, method='onehot')
        self.assertEqual(encoded.shape[0], 2)
        self.assertEqual(encoded.shape[1], 16)  # 4 bases * 4 features
    
    def test_encode_sequences_kmer(self):
        """Test k-mer encoding"""
        sequences = ["ATGC", "CGTA"]
        encoded = self.loader.encode_sequences(sequences, method='kmer')
        self.assertEqual(encoded.shape[0], 2)
        # Should have 4^3 = 64 features for k=3
        self.assertEqual(encoded.shape[1], 64)
    
    def test_encode_sequences_numerical(self):
        """Test numerical encoding"""
        sequences = ["ATGC", "CGTA"]
        encoded = self.loader.encode_sequences(sequences, method='numerical')
        self.assertEqual(encoded.shape[0], 2)


if __name__ == '__main__':
    unittest.main()


