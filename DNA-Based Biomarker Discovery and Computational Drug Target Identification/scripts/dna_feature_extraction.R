# DNA Sequence Feature Extraction for Biomarker Discovery
# 
# This script extracts comprehensive features from DNA sequences that can be used
# to identify potential biomarkers and drug targets.
#
# Author: DNA-Based Biomarker Discovery Project
# Date: 2025

# Load required libraries
library(dplyr)
library(stringr)
library(data.table)

#' Extract comprehensive features from DNA sequences
#'
#' Features include:
#' - Nucleotide composition (A, T, G, C frequencies)
#' - GC content and GC skew
#' - AT content and AT skew
#' - Dinucleotide frequencies (16 combinations)
#' - Trinucleotide frequencies (20 most common)
#' - Sequence complexity (Shannon entropy)
#' - Purine/Pyrimidine ratio
#' - Homopolymer runs
#' - Sequence length (normalized)
#'
#' @param sequences Character vector of DNA sequences
#' @return Data frame with extracted features
extract_dna_features <- function(sequences) {
  n_seqs <- length(sequences)
  
  # Initialize feature vectors
  features <- data.frame(
    A_freq = numeric(n_seqs),
    T_freq = numeric(n_seqs),
    G_freq = numeric(n_seqs),
    C_freq = numeric(n_seqs),
    GC_content = numeric(n_seqs),
    AT_content = numeric(n_seqs),
    GC_skew = numeric(n_seqs),
    AT_skew = numeric(n_seqs),
    Shannon_entropy = numeric(n_seqs),
    Pur_Pyr_ratio = numeric(n_seqs),
    Normalized_length = numeric(n_seqs),
    Max_homopolymer = numeric(n_seqs)
  )
  
  # Dinucleotide frequencies
  dinucleotides <- c("AA", "AT", "AG", "AC", "TA", "TT", "TG", "TC",
                     "GA", "GT", "GG", "GC", "CA", "CT", "CG", "CC")
  for (dinuc in dinucleotides) {
    features[[paste0("Dinuc_", dinuc)]] <- numeric(n_seqs)
  }
  
  # Trinucleotide frequencies
  trinucleotides <- c("AAA", "AAT", "AAG", "AAC", "ATA", "ATT", "ATG", "ATC",
                      "AGA", "AGT", "AGG", "AGC", "ACA", "ACT", "ACG", "ACC",
                      "TAA", "TAT", "TAG", "TAC")
  for (trinuc in trinucleotides) {
    features[[paste0("Trinuc_", trinuc)]] <- numeric(n_seqs)
  }
  
  # Process each sequence
  for (i in seq_along(sequences)) {
    seq <- toupper(sequences[i])
    seq_len <- nchar(seq)
    
    if (seq_len == 0) {
      next
    }
    
    # Nucleotide composition
    features$A_freq[i] <- str_count(seq, "A") / seq_len
    features$T_freq[i] <- str_count(seq, "T") / seq_len
    features$G_freq[i] <- str_count(seq, "G") / seq_len
    features$C_freq[i] <- str_count(seq, "C") / seq_len
    
    # GC content
    features$GC_content[i] <- (str_count(seq, "G") + str_count(seq, "C")) / seq_len
    
    # AT content
    features$AT_content[i] <- (str_count(seq, "A") + str_count(seq, "T")) / seq_len
    
    # GC skew
    g_count <- str_count(seq, "G")
    c_count <- str_count(seq, "C")
    features$GC_skew[i] <- ifelse((g_count + c_count) > 0,
                                   (g_count - c_count) / (g_count + c_count),
                                   0)
    
    # AT skew
    a_count <- str_count(seq, "A")
    t_count <- str_count(seq, "T")
    features$AT_skew[i] <- ifelse((a_count + t_count) > 0,
                                   (a_count - t_count) / (a_count + t_count),
                                   0)
    
    # Dinucleotide frequencies
    for (dinuc in dinucleotides) {
      count <- str_count(seq, dinuc)
      features[[paste0("Dinuc_", dinuc)]][i] <- ifelse(seq_len > 1,
                                                        count / (seq_len - 1),
                                                        0)
    }
    
    # Trinucleotide frequencies
    for (trinuc in trinucleotides) {
      count <- str_count(seq, trinuc)
      features[[paste0("Trinuc_", trinuc)]][i] <- ifelse(seq_len > 2,
                                                          count / (seq_len - 2),
                                                          0)
    }
    
    # Shannon entropy
    nucleotide_counts <- c(
      str_count(seq, "A"),
      str_count(seq, "T"),
      str_count(seq, "G"),
      str_count(seq, "C")
    )
    nucleotide_probs <- nucleotide_counts / seq_len
    nucleotide_probs <- nucleotide_probs[nucleotide_probs > 0]
    features$Shannon_entropy[i] <- -sum(nucleotide_probs * log2(nucleotide_probs))
    
    # Purine/Pyrimidine ratio
    purine_count <- str_count(seq, "A") + str_count(seq, "G")
    pyrimidine_count <- str_count(seq, "C") + str_count(seq, "T")
    features$Pur_Pyr_ratio[i] <- ifelse(pyrimidine_count > 0,
                                         purine_count / pyrimidine_count,
                                         0)
    
    # Normalized length
    features$Normalized_length[i] <- seq_len / 100.0
    
    # Max homopolymer run
    max_homopolymer <- 0
    for (nuc in c("A", "T", "G", "C")) {
      if (grepl(nuc, seq)) {
        parts <- strsplit(seq, paste0("[^", nuc, "]+"))[[1]]
        parts <- parts[parts != ""]
        if (length(parts) > 0) {
          max_run <- max(nchar(parts))
          max_homopolymer <- max(max_homopolymer, max_run)
        }
      }
    }
    features$Max_homopolymer[i] <- max_homopolymer
  }
  
  return(features)
}

#' Main function to extract features from DNA sequences
main <- function() {
  # Parse command line arguments
  args <- commandArgs(trailingOnly = TRUE)
  
  if (length(args) < 1) {
    input_file <- "../data/genomics_data.csv"
  } else {
    input_file <- args[1]
  }
  
  if (length(args) < 2) {
    output_file <- "../results/dna_features.csv"
  } else {
    output_file <- args[2]
  }
  
  # Load data
  cat("Loading data from", input_file, "...\n")
  df <- read.csv(input_file, stringsAsFactors = FALSE)
  
  if (!"Sequences" %in% colnames(df)) {
    stop("Column 'Sequences' not found in data. Available columns: ", 
         paste(colnames(df), collapse = ", "))
  }
  
  # Extract features
  cat("Extracting features from DNA sequences...\n")
  sequences <- df$Sequences
  features <- extract_dna_features(sequences)
  
  # Add labels if they exist
  if ("Labels" %in% colnames(df)) {
    features$Labels <- df$Labels
  }
  
  # Create output directory if it doesn't exist
  output_dir <- dirname(output_file)
  if (!dir.exists(output_dir)) {
    dir.create(output_dir, recursive = TRUE)
  }
  
  # Save features
  cat("Saving features to", output_file, "...\n")
  write.csv(features, output_file, row.names = FALSE)
  
  cat("Feature extraction complete!\n")
  cat("  - Number of sequences:", length(sequences), "\n")
  cat("  - Number of features:", ncol(features), "\n")
  cat("  - Features saved to:", output_file, "\n")
}

# Run main function if script is executed directly
if (!interactive()) {
  main()
}

