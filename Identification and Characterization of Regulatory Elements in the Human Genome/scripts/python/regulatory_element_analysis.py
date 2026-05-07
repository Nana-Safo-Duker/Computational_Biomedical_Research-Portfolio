"""
Regulatory Element Identification Analysis
Identifies sequences encoding promoters, enhancers, silencers, and insulators
"""

import pandas as pd
import numpy as np
from collections import Counter
import re
from Bio import motifs
from Bio.Seq import Seq
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(filepath):
    """Load genomics data"""
    df = pd.read_csv(filepath)
    return df

def identify_regulatory_motifs(sequences, labels):
    """
    Identify common motifs in regulatory sequences
    
    Regulatory elements typically contain:
    - Promoters: TATA box (TATAAA), CAAT box (CCAAT), GC box (GGGCGG)
    - Enhancers: Various TF binding sites
    - Silencers: Repressor binding sites
    - Insulators: CTCF binding sites (CCCTC)
    """
    regulatory_seqs = [seq for seq, label in zip(sequences, labels) if label == 1]
    non_regulatory_seqs = [seq for seq, label in zip(sequences, labels) if label == 0]
    
    # Known regulatory motifs
    known_motifs = {
        'TATA_box': r'TATAAA|TATAA',
        'CAAT_box': r'CCAAT|CAAT',
        'GC_box': r'GGGCGG|GGCGGG',
        'CTCF_site': r'CCCTC|CTCCC',
        'SP1_site': r'GGGCGG',
        'NF1_site': r'TTGGC',
        'AP1_site': r'TGACTC|TGAGTCA',
        'CREB_site': r'TGACGTCA',
    }
    
    print("=" * 80)
    print("REGULATORY ELEMENT MOTIF ANALYSIS")
    print("=" * 80)
    
    motif_counts = {}
    for motif_name, pattern in known_motifs.items():
        reg_count = sum(1 for seq in regulatory_seqs if re.search(pattern, seq))
        non_reg_count = sum(1 for seq in non_regulatory_seqs if re.search(pattern, seq))
        
        reg_percent = (reg_count / len(regulatory_seqs) * 100) if regulatory_seqs else 0
        non_reg_percent = (non_reg_count / len(non_regulatory_seqs) * 100) if non_regulatory_seqs else 0
        
        motif_counts[motif_name] = {
            'regulatory': reg_count,
            'non_regulatory': non_reg_count,
            'reg_percent': reg_percent,
            'non_reg_percent': non_reg_percent
        }
        
        print(f"\n{motif_name}:")
        print(f"  Found in {reg_count}/{len(regulatory_seqs)} regulatory sequences ({reg_percent:.1f}%)")
        print(f"  Found in {non_reg_count}/{len(non_regulatory_seqs)} non-regulatory sequences ({non_reg_percent:.1f}%)")
    
    return motif_counts

def find_common_patterns(sequences, labels, min_length=8, max_length=15):
    """
    Find common sequence patterns in regulatory elements
    """
    regulatory_seqs = [seq for seq, label in zip(sequences, labels) if label == 1]
    
    print("\n" + "=" * 80)
    print("COMMON PATTERNS IN REGULATORY SEQUENCES")
    print("=" * 80)
    
    # Extract all k-mers of different lengths
    kmer_counts = Counter()
    for seq in regulatory_seqs:
        for k in range(min_length, max_length + 1):
            for i in range(len(seq) - k + 1):
                kmer = seq[i:i+k]
                kmer_counts[kmer] += 1
    
    # Find most common patterns
    print(f"\nTop 20 most frequent patterns in regulatory sequences:")
    for pattern, count in kmer_counts.most_common(20):
        frequency = count / len(regulatory_seqs)
        print(f"  {pattern}: {count} occurrences ({frequency:.2%} of sequences)")
    
    return kmer_counts

def analyze_sequence_features(sequences, labels):
    """
    Analyze sequence composition features
    """
    regulatory_seqs = [seq for seq, label in zip(sequences, labels) if label == 1]
    non_regulatory_seqs = [seq for seq, label in zip(sequences, labels) if label == 0]
    
    print("\n" + "=" * 80)
    print("SEQUENCE COMPOSITION ANALYSIS")
    print("=" * 80)
    
    def calculate_features(seq_list, name):
        features = {
            'GC_content': [],
            'CpG_count': [],
            'length': []
        }
        
        for seq in seq_list:
            features['GC_content'].append((seq.count('G') + seq.count('C')) / len(seq) * 100)
            features['CpG_count'].append(seq.count('CG'))
            features['length'].append(len(seq))
        
        print(f"\n{name} Sequences:")
        print(f"  Average GC content: {np.mean(features['GC_content']):.2f}%")
        print(f"  Average CpG count: {np.mean(features['CpG_count']):.2f}")
        print(f"  Average length: {np.mean(features['length']):.2f} bp")
        
        return features
    
    reg_features = calculate_features(regulatory_seqs, "Regulatory")
    non_reg_features = calculate_features(non_regulatory_seqs, "Non-regulatory")
    
    return reg_features, non_reg_features

def identify_regulatory_element_sequences(df):
    """
    Main function to identify sequences encoding regulatory elements
    """
    sequences = df['Sequences'].tolist()
    labels = df['Labels'].tolist()
    
    print("=" * 80)
    print("REGULATORY ELEMENT IDENTIFICATION")
    print("=" * 80)
    print(f"\nTotal sequences: {len(sequences)}")
    print(f"Regulatory sequences (Label=1): {sum(labels)}")
    print(f"Non-regulatory sequences (Label=0): {len(labels) - sum(labels)}")
    
    # Find common patterns
    kmer_counts = find_common_patterns(sequences, labels)
    
    # Identify known motifs
    motif_counts = identify_regulatory_motifs(sequences, labels)
    
    # Analyze sequence features
    reg_features, non_reg_features = analyze_sequence_features(sequences, labels)
    
    # Identify the signature motif
    print("\n" + "=" * 80)
    print("SIGNATURE REGULATORY ELEMENT MOTIF")
    print("=" * 80)
    
    # Check for the most common pattern that appears in regulatory sequences
    regulatory_seqs = [seq for seq, label in zip(sequences, labels) if label == 1]
    non_regulatory_seqs = [seq for seq, label in zip(sequences, labels) if label == 0]
    
    # Look for the pattern that appears most frequently in regulatory vs non-regulatory
    signature_patterns = ['CGACCGAACTCC', 'GACCGAACTCC', 'CGACCGAACTC', 'CGACCGAACT']
    
    for pattern in signature_patterns:
        reg_matches = sum(1 for seq in regulatory_seqs if pattern in seq)
        non_reg_matches = sum(1 for seq in non_regulatory_seqs if pattern in seq)
        
        reg_percent = (reg_matches / len(regulatory_seqs) * 100) if regulatory_seqs else 0
        non_reg_percent = (non_reg_matches / len(non_regulatory_seqs) * 100) if non_regulatory_seqs else 0
        
        print(f"\nPattern: {pattern}")
        print(f"  Regulatory sequences: {reg_matches}/{len(regulatory_seqs)} ({reg_percent:.1f}%)")
        print(f"  Non-regulatory sequences: {non_reg_matches}/{len(non_regulatory_seqs)} ({non_reg_percent:.1f}%)")
        print(f"  Enrichment ratio: {reg_percent / non_reg_percent if non_reg_percent > 0 else 'N/A'}")
    
    print("\n" + "=" * 80)
    print("SUMMARY: WHAT SEQUENCES ENCODE REGULATORY ELEMENTS")
    print("=" * 80)
    print("""
Regulatory elements (promoters, enhancers, silencers, insulators) are encoded by:

1. SPECIFIC DNA SEQUENCE MOTIFS:
   - Promoters: Contain TATA box (TATAAA), CAAT box (CCAAT), or GC box (GGGCGG)
   - Enhancers: Contain transcription factor binding sites (varies by cell type)
   - Silencers: Contain repressor protein binding sites
   - Insulators: Contain CTCF binding sites (CCCTC motif)

2. SEQUENCE COMPOSITION:
   - GC-rich regions (often >50% GC content)
   - CpG islands (regions with high frequency of CG dinucleotides)
   - Specific spacing and orientation of motifs

3. IN THIS DATASET:
   - Sequences containing the motif "CGACCGAACTCC" or variants are highly enriched
     in regulatory elements (Label=1)
   - This appears to be a synthetic regulatory element signature motif

4. BIOLOGICAL REGULATORY ELEMENTS:
   - Promoters: Located upstream of genes, contain TATA box or initiator elements
   - Enhancers: Can be located far from genes, contain clusters of TF binding sites
   - Silencers: Similar to enhancers but repress transcription
   - Insulators: Block enhancer-promoter interactions, contain CTCF sites
    """)
    
    return {
        'kmer_counts': kmer_counts,
        'motif_counts': motif_counts,
        'reg_features': reg_features,
        'non_reg_features': non_reg_features
    }

if __name__ == "__main__":
    # Load data
    df = load_data('genomics_data.csv')
    
    # Analyze regulatory elements
    results = identify_regulatory_element_sequences(df)
    
    # Save regulatory sequences
    regulatory_df = df[df['Labels'] == 1]
    regulatory_df.to_csv('regulatory_sequences.csv', index=False)
    print(f"\n[SUCCESS] Saved {len(regulatory_df)} regulatory sequences to 'regulatory_sequences.csv'")

