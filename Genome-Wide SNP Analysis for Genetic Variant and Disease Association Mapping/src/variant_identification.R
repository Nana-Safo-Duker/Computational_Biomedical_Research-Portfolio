# Genetic Variant Identification in R
# 
# This script provides functions to identify:
# - Single-nucleotide polymorphisms (SNPs)
# - Insertions/Deletions (Indels)
# - Structural variants
#
# Author: Genetic Variants Analysis Project
# Date: 2025

library(stringr)
library(dplyr)  # Note: dplyr masks some base/stats functions (filter, lag, etc.) - this is normal

# Check if Biostrings is available, otherwise use base R functions
# Note: Biostrings is optional and requires BiocManager to install
if (!requireNamespace("Biostrings", quietly = TRUE)) {
  cat("Note: Biostrings package not available. Using base R functions.\n")
  cat("  To install: BiocManager::install('Biostrings')\n")
  use_biostrings <- FALSE
} else {
  # Only load if available
  library(Biostrings)
  use_biostrings <- TRUE
}

#' Validate DNA sequence
#' @param sequence Character string of DNA sequence
#' @return Logical indicating if sequence is valid
validate_sequence <- function(sequence) {
  valid_nucleotides <- c("A", "C", "G", "T", "N")
  sequence_upper <- toupper(sequence)
  all(strsplit(sequence_upper, "")[[1]] %in% valid_nucleotides)
}

#' Calculate consensus sequence from multiple sequences
#' @param sequences Vector of DNA sequences
#' @return Consensus sequence as character string
calculate_consensus_sequence <- function(sequences) {
  if (length(sequences) == 0) {
    return("")
  }
  
  seq_length <- nchar(sequences[1])
  consensus <- character(seq_length)
  
  for (pos in 1:seq_length) {
    # Extract nucleotides at this position
    nucleotides <- sapply(sequences, function(seq) {
      if (pos <= nchar(seq)) {
        substr(seq, pos, pos)
      } else {
        NA
      }
    })
    nucleotides <- toupper(nucleotides[!is.na(nucleotides)])
    
    # Count nucleotides
    nuc_counts <- table(nucleotides)
    
    # Get most common nucleotide
    most_common <- names(nuc_counts)[which.max(nuc_counts)]
    consensus[pos] <- most_common
  }
  
  return(paste(consensus, collapse = ""))
}

#' Identify Single-Nucleotide Polymorphisms (SNPs)
#' @param sequence Query sequence
#' @param reference Reference sequence
#' @return Data frame with SNP information
identify_snps <- function(sequence, reference) {
  snps <- data.frame(
    position = integer(),
    reference = character(),
    alternate = character(),
    type = character(),
    stringsAsFactors = FALSE
  )
  
  seq_upper <- toupper(sequence)
  ref_upper <- toupper(reference)
  min_length <- min(nchar(seq_upper), nchar(ref_upper))
  valid_nucleotides <- c("A", "C", "G", "T")
  
  for (pos in 1:min_length) {
    ref_nuc <- substr(ref_upper, pos, pos)
    alt_nuc <- substr(seq_upper, pos, pos)
    
    # Check if it's a valid SNP
    if (ref_nuc != alt_nuc && 
        ref_nuc %in% valid_nucleotides && 
        alt_nuc %in% valid_nucleotides) {
      snps <- rbind(snps, data.frame(
        position = pos,
        reference = ref_nuc,
        alternate = alt_nuc,
        type = "SNP",
        stringsAsFactors = FALSE
      ))
    }
  }
  
  return(snps)
}

#' Identify Insertions and Deletions (Indels)
#' @param sequence Query sequence
#' @param reference Reference sequence
#' @return Data frame with indel information
identify_indels <- function(sequence, reference) {
  indels <- data.frame(
    position = integer(),
    type = character(),
    length = integer(),
    sequence = character(),
    stringsAsFactors = FALSE
  )
  
  seq_upper <- toupper(sequence)
  ref_upper <- toupper(reference)
  seq_len <- nchar(seq_upper)
  ref_len <- nchar(ref_upper)
  
  # Simple alignment approach
  i <- 1
  j <- 1
  
  while (i <= seq_len || j <= ref_len) {
    if (i > seq_len) {
      # Deletion: reference continues but sequence ends
      if (j <= ref_len) {
        deletion_length <- ref_len - j + 1
        deletion_seq <- substr(ref_upper, j, ref_len)
        indels <- rbind(indels, data.frame(
          position = j,
          type = "DELETION",
          length = deletion_length,
          sequence = deletion_seq,
          stringsAsFactors = FALSE
        ))
      }
      break
    }
    
    if (j > ref_len) {
      # Insertion: sequence continues but reference ends
      if (i <= seq_len) {
        insertion_length <- seq_len - i + 1
        insertion_seq <- substr(seq_upper, i, seq_len)
        indels <- rbind(indels, data.frame(
          position = i,
          type = "INSERTION",
          length = insertion_length,
          sequence = insertion_seq,
          stringsAsFactors = FALSE
        ))
      }
      break
    }
    
    seq_char <- substr(seq_upper, i, i)
    ref_char <- substr(ref_upper, j, j)
    
    if (seq_char == ref_char) {
      # Match
      i <- i + 1
      j <- j + 1
    } else {
      # Mismatch - check for insertion or deletion
      # Check for insertion
      if (i + 1 <= seq_len && substr(seq_upper, i + 1, i + 1) == ref_char) {
        insertion_start <- i
        insertion_seq <- seq_char
        i <- i + 1
        
        while (i <= seq_len && j <= ref_len && 
               substr(seq_upper, i, i) != substr(ref_upper, j, j)) {
          insertion_seq <- paste0(insertion_seq, substr(seq_upper, i, i))
          i <- i + 1
        }
        
        indels <- rbind(indels, data.frame(
          position = insertion_start,
          type = "INSERTION",
          length = nchar(insertion_seq),
          sequence = insertion_seq,
          stringsAsFactors = FALSE
        ))
      } else if (j + 1 <= ref_len && seq_char == substr(ref_upper, j + 1, j + 1)) {
        # Deletion
        deletion_start <- j
        deletion_seq <- ref_char
        j <- j + 1
        
        while (j <= ref_len && i <= seq_len && 
               substr(seq_upper, i, i) != substr(ref_upper, j, j)) {
          deletion_seq <- paste0(deletion_seq, substr(ref_upper, j, j))
          j <- j + 1
        }
        
        indels <- rbind(indels, data.frame(
          position = deletion_start,
          type = "DELETION",
          length = nchar(deletion_seq),
          sequence = deletion_seq,
          stringsAsFactors = FALSE
        ))
      } else {
        # Single base mismatch - treat as SNP and continue
        i <- i + 1
        j <- j + 1
      }
    }
  }
  
  return(indels)
}

#' Identify Structural Variants
#' @param sequence Query sequence
#' @param reference Reference sequence
#' @param min_length Minimum length to consider as structural variant
#' @return Data frame with structural variant information
identify_structural_variants <- function(sequence, reference, min_length = 10) {
  structural_variants <- data.frame(
    position = integer(),
    type = character(),
    length = integer(),
    sequence = character(),
    stringsAsFactors = FALSE
  )
  
  # Large insertions/deletions
  indels <- identify_indels(sequence, reference)
  large_indels <- indels[indels$length >= min_length, ]
  
  if (nrow(large_indels) > 0) {
    for (i in seq_len(nrow(large_indels))) {
      structural_variants <- rbind(structural_variants, data.frame(
        position = large_indels$position[i],
        type = paste0("STRUCTURAL_", large_indels$type[i]),
        length = large_indels$length[i],
        sequence = large_indels$sequence[i],
        stringsAsFactors = FALSE
      ))
    }
  }
  
  # Check for duplications
  seq_upper <- toupper(sequence)
  for (length in min_length:(nchar(seq_upper) %/% 2)) {
    for (i in 1:(nchar(seq_upper) - 2 * length + 1)) {
      segment <- substr(seq_upper, i, i + length - 1)
      next_segment <- substr(seq_upper, i + length, i + 2 * length - 1)
      
      if (segment == next_segment) {
        structural_variants <- rbind(structural_variants, data.frame(
          position = i,
          type = "DUPLICATION",
          length = length,
          sequence = segment,
          stringsAsFactors = FALSE
        ))
      }
    }
  }
  
  return(structural_variants)
}

#' Comprehensive analysis of a sequence for all variant types
#' @param sequence Query sequence
#' @param reference Reference sequence
#' @return List containing all identified variants
analyze_sequence <- function(sequence, reference) {
  if (!validate_sequence(sequence)) {
    stop("Invalid characters in sequence")
  }
  if (!validate_sequence(reference)) {
    stop("Invalid characters in reference")
  }
  
  results <- list(
    sequence = sequence,
    reference = reference,
    snps = identify_snps(sequence, reference),
    indels = identify_indels(sequence, reference),
    structural_variants = identify_structural_variants(sequence, reference)
  )
  
  results$total_variants <- nrow(results$snps) + 
                            nrow(results$indels) + 
                            nrow(results$structural_variants)
  
  return(results)
}

#' Process genomics data file and identify variants
#' @param data_path Path to CSV file with sequences and labels
#' @param output_path Optional path to save results CSV
#' @return Data frame with variant analysis results
process_genomics_data <- function(data_path, output_path = NULL) {
  # Load data
  df <- read.csv(data_path, stringsAsFactors = FALSE)
  
  # Calculate consensus sequence
  sequences <- df$Sequences
  consensus <- calculate_consensus_sequence(sequences)
  
  # Analyze each sequence
  results_list <- list()
  
  for (idx in seq_len(nrow(df))) {
    sequence <- df$Sequences[idx]
    label <- df$Labels[idx]
    
    analysis <- analyze_sequence(sequence, consensus)
    
    results_list[[idx]] <- data.frame(
      sequence_id = idx - 1,  # 0-indexed
      label = label,
      num_snps = nrow(analysis$snps),
      num_indels = nrow(analysis$indels),
      num_structural_variants = nrow(analysis$structural_variants),
      total_variants = analysis$total_variants,
      stringsAsFactors = FALSE
    )
  }
  
  results_df <- do.call(rbind, results_list)
  
  if (!is.null(output_path)) {
    write.csv(results_df, output_path, row.names = FALSE)
    cat("Results saved to:", output_path, "\n")
  }
  
  return(results_df)
}

# Main execution
if (!interactive()) {
  cat("Genetic Variant Identification in R\n")
  cat("==================================\n\n")
  
  data_file <- "data/genomics_data.csv"
  output_file <- "results/variant_analysis_results_R.csv"
  
  cat("Processing genomics data...\n")
  results <- process_genomics_data(data_file, output_file)
  
  cat("\nAnalysis complete!\n")
  cat("Total sequences analyzed:", nrow(results), "\n")
  cat("Average SNPs per sequence:", mean(results$num_snps), "\n")
  cat("Average Indels per sequence:", mean(results$num_indels), "\n")
  cat("Average Structural Variants per sequence:", mean(results$num_structural_variants), "\n")
  cat("\nResults saved to:", output_file, "\n")
}

