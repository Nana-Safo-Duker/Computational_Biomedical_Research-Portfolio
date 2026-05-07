"""
Genetic Variant Identification Module

This module provides functions to identify:
- Single-nucleotide polymorphisms (SNPs)
- Insertions/Deletions (Indels)
- Structural variants

Author: Genetic Variants Analysis Project
Date: 2025
"""

import pandas as pd
import numpy as np
from collections import Counter
from typing import Dict, List, Tuple, Optional
import re


class VariantIdentifier:
    """Class for identifying genetic variants in DNA sequences."""
    
    def __init__(self, reference_sequence: Optional[str] = None):
        """
        Initialize the VariantIdentifier.
        
        Parameters:
        -----------
        reference_sequence : str, optional
            Reference sequence for comparison. If None, will use consensus sequence.
        """
        self.reference_sequence = reference_sequence
        self.valid_nucleotides = set('ACGTN')
    
    def validate_sequence(self, sequence: str) -> bool:
        """Validate that sequence contains only valid nucleotides."""
        return all(nuc in self.valid_nucleotides for nuc in sequence.upper())
    
    def calculate_consensus_sequence(self, sequences: List[str]) -> str:
        """
        Calculate consensus sequence from multiple sequences.
        
        Parameters:
        -----------
        sequences : List[str]
            List of DNA sequences
            
        Returns:
        --------
        str : Consensus sequence
        """
        if not sequences:
            return ""
        
        seq_length = len(sequences[0])
        consensus = []
        
        for pos in range(seq_length):
            nucleotides = [seq[pos].upper() for seq in sequences if pos < len(seq)]
            # Count nucleotides at this position
            nuc_counts = Counter(nucleotides)
            # Get most common nucleotide
            most_common = nuc_counts.most_common(1)[0][0]
            consensus.append(most_common)
        
        return ''.join(consensus)
    
    def identify_snps(self, sequence: str, reference: str) -> List[Dict]:
        """
        Identify Single-Nucleotide Polymorphisms (SNPs).
        
        Parameters:
        -----------
        sequence : str
            Query sequence
        reference : str
            Reference sequence
            
        Returns:
        --------
        List[Dict] : List of SNP dictionaries with position, ref, alt
        """
        snps = []
        min_length = min(len(sequence), len(reference))
        
        for pos in range(min_length):
            ref_nuc = reference[pos].upper()
            alt_nuc = sequence[pos].upper()
            
            # Check if it's a valid SNP (different nucleotides, both valid)
            if (ref_nuc != alt_nuc and 
                ref_nuc in self.valid_nucleotides and 
                alt_nuc in self.valid_nucleotides and
                ref_nuc != 'N' and alt_nuc != 'N'):
                snps.append({
                    'position': pos + 1,  # 1-indexed
                    'reference': ref_nuc,
                    'alternate': alt_nuc,
                    'type': 'SNP'
                })
        
        return snps
    
    def identify_indels(self, sequence: str, reference: str) -> List[Dict]:
        """
        Identify Insertions and Deletions (Indels).
        
        Parameters:
        -----------
        sequence : str
            Query sequence
        reference : str
            Reference sequence
            
        Returns:
        --------
        List[Dict] : List of indel dictionaries
        """
        indels = []
        
        # Use sequence alignment approach
        # Simple approach: find gaps and insertions
        seq_upper = sequence.upper()
        ref_upper = reference.upper()
        
        # Find deletions (gaps in sequence relative to reference)
        # Find insertions (gaps in reference relative to sequence)
        
        # Use a simple alignment approach
        i, j = 0, 0
        seq_len = len(seq_upper)
        ref_len = len(ref_upper)
        
        while i < seq_len or j < ref_len:
            if i >= seq_len:
                # Deletion: reference continues but sequence ends
                if j < ref_len:
                    deletion_length = ref_len - j
                    indels.append({
                        'position': j + 1,
                        'type': 'DELETION',
                        'length': deletion_length,
                        'sequence': ref_upper[j:j+deletion_length]
                    })
                break
            
            if j >= ref_len:
                # Insertion: sequence continues but reference ends
                if i < seq_len:
                    insertion_length = seq_len - i
                    indels.append({
                        'position': i + 1,
                        'type': 'INSERTION',
                        'length': insertion_length,
                        'sequence': seq_upper[i:i+insertion_length]
                    })
                break
            
            if seq_upper[i] == ref_upper[j]:
                # Match
                i += 1
                j += 1
            else:
                # Mismatch - could be SNP, insertion, or deletion
                # Check for insertion (sequence has extra bases)
                if (i + 1 < seq_len and 
                    seq_upper[i+1] == ref_upper[j] and
                    seq_upper[i] != ref_upper[j]):
                    # Potential insertion
                    insertion_start = i
                    insertion_seq = seq_upper[i]
                    i += 1
                    while i < seq_len and j < ref_len and seq_upper[i] != ref_upper[j]:
                        insertion_seq += seq_upper[i]
                        i += 1
                    
                    indels.append({
                        'position': insertion_start + 1,
                        'type': 'INSERTION',
                        'length': len(insertion_seq),
                        'sequence': insertion_seq
                    })
                
                # Check for deletion (reference has extra bases)
                elif (j + 1 < ref_len and 
                      seq_upper[i] == ref_upper[j+1] and
                      seq_upper[i] != ref_upper[j]):
                    # Potential deletion
                    deletion_start = j
                    deletion_seq = ref_upper[j]
                    j += 1
                    while j < ref_len and i < seq_len and seq_upper[i] != ref_upper[j]:
                        deletion_seq += ref_upper[j]
                        j += 1
                    
                    indels.append({
                        'position': deletion_start + 1,
                        'type': 'DELETION',
                        'length': len(deletion_seq),
                        'sequence': deletion_seq
                    })
                else:
                    # Single base mismatch - treat as SNP and continue
                    i += 1
                    j += 1
        
        return indels
    
    def identify_structural_variants(self, sequence: str, reference: str, 
                                     min_length: int = 10) -> List[Dict]:
        """
        Identify Structural Variants (large insertions, deletions, inversions, duplications).
        
        Parameters:
        -----------
        sequence : str
            Query sequence
        reference : str
            Reference sequence
        min_length : int
            Minimum length to consider as structural variant (default: 10)
            
        Returns:
        --------
        List[Dict] : List of structural variant dictionaries
        """
        structural_variants = []
        
        # Large insertions/deletions (already captured by indels if > min_length)
        indels = self.identify_indels(sequence, reference)
        for indel in indels:
            if indel['length'] >= min_length:
                structural_variants.append({
                    'position': indel['position'],
                    'type': f"STRUCTURAL_{indel['type']}",
                    'length': indel['length'],
                    'sequence': indel['sequence']
                })
        
        # Check for inversions (reverse complement matches)
        seq_upper = sequence.upper()
        ref_upper = reference.upper()
        
        def reverse_complement(seq):
            complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N'}
            return ''.join(complement.get(nuc, nuc) for nuc in reversed(seq))
        
        # Look for inverted segments
        for i in range(len(ref_upper) - min_length + 1):
            ref_segment = ref_upper[i:i+min_length]
            rev_comp = reverse_complement(ref_segment)
            
            # Check if reverse complement appears in sequence
            if rev_comp in seq_upper:
                pos = seq_upper.find(rev_comp)
                structural_variants.append({
                    'position': pos + 1,
                    'type': 'INVERSION',
                    'length': len(rev_comp),
                    'reference_position': i + 1,
                    'sequence': rev_comp
                })
        
        # Check for duplications (repeated segments)
        for length in range(min_length, min(len(seq_upper), len(ref_upper)) // 2):
            for i in range(len(seq_upper) - 2 * length + 1):
                segment = seq_upper[i:i+length]
                if seq_upper[i+length:i+2*length] == segment:
                    structural_variants.append({
                        'position': i + 1,
                        'type': 'DUPLICATION',
                        'length': length,
                        'sequence': segment
                    })
        
        return structural_variants
    
    def analyze_sequence(self, sequence: str, reference: str) -> Dict:
        """
        Comprehensive analysis of a sequence for all variant types.
        
        Parameters:
        -----------
        sequence : str
            Query sequence
        reference : str
            Reference sequence
            
        Returns:
        --------
        Dict : Dictionary containing all identified variants
        """
        if not self.validate_sequence(sequence):
            raise ValueError("Invalid characters in sequence")
        if not self.validate_sequence(reference):
            raise ValueError("Invalid characters in reference")
        
        results = {
            'sequence': sequence,
            'reference': reference,
            'snps': self.identify_snps(sequence, reference),
            'indels': self.identify_indels(sequence, reference),
            'structural_variants': self.identify_structural_variants(sequence, reference)
        }
        
        results['total_variants'] = (
            len(results['snps']) + 
            len(results['indels']) + 
            len(results['structural_variants'])
        )
        
        return results


def process_genomics_data(data_path: str, output_path: Optional[str] = None) -> pd.DataFrame:
    """
    Process genomics data file and identify variants.
    
    Parameters:
    -----------
    data_path : str
        Path to CSV file with sequences and labels
    output_path : str, optional
        Path to save results CSV
        
    Returns:
    --------
    pd.DataFrame : DataFrame with variant analysis results
    """
    # Load data
    df = pd.read_csv(data_path)
    
    # Initialize variant identifier
    sequences = df['Sequences'].tolist()
    consensus = VariantIdentifier().calculate_consensus_sequence(sequences)
    identifier = VariantIdentifier(reference_sequence=consensus)
    
    # Analyze each sequence
    results = []
    for idx, row in df.iterrows():
        sequence = row['Sequences']
        label = row['Labels']
        
        analysis = identifier.analyze_sequence(sequence, consensus)
        
        results.append({
            'sequence_id': idx,
            'label': label,
            'num_snps': len(analysis['snps']),
            'num_indels': len(analysis['indels']),
            'num_structural_variants': len(analysis['structural_variants']),
            'total_variants': analysis['total_variants'],
            'snps': analysis['snps'],
            'indels': analysis['indels'],
            'structural_variants': analysis['structural_variants']
        })
    
    results_df = pd.DataFrame(results)
    
    if output_path:
        results_df.to_csv(output_path, index=False)
    
    return results_df


if __name__ == "__main__":
    # Example usage
    import sys
    
    data_file = "data/genomics_data.csv"
    output_file = "results/variant_analysis_results.csv"
    
    print("Processing genomics data...")
    results = process_genomics_data(data_file, output_file)
    print(f"\nAnalysis complete!")
    print(f"Total sequences analyzed: {len(results)}")
    print(f"Average SNPs per sequence: {results['num_snps'].mean():.2f}")
    print(f"Average Indels per sequence: {results['num_indels'].mean():.2f}")
    print(f"Average Structural Variants per sequence: {results['num_structural_variants'].mean():.2f}")
    print(f"\nResults saved to: {output_file}")

