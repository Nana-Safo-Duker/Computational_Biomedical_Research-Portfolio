# Data Loading and Preprocessing Module for R
# Handles loading and preprocessing of genomics mutation data

#' Load genomics data from CSV file
#' 
#' @param data_path Path to the CSV file containing genomics data
#' @return Data frame containing the loaded data
load_genomics_data <- function(data_path = NULL) {
  if (is.null(data_path)) {
    # Default path relative to project root
    data_path <- file.path("data", "genomics_data.csv")
  }
  
  if (!file.exists(data_path)) {
    stop(paste("Error: File not found at", data_path))
  }
  
  data <- read.csv(data_path, stringsAsFactors = FALSE)
  cat("Data loaded successfully. Shape:", nrow(data), "x", ncol(data), "\n")
  
  return(data)
}

#' One-hot encode DNA sequences
#' 
#' @param sequences Vector of DNA sequences
#' @return Matrix of one-hot encoded sequences
onehot_encode <- function(sequences) {
  encoding_map <- list(
    'A' = c(1, 0, 0, 0),
    'T' = c(0, 1, 0, 0),
    'G' = c(0, 0, 1, 0),
    'C' = c(0, 0, 0, 1)
  )
  
  encoded_list <- lapply(sequences, function(seq) {
    seq_upper <- toupper(seq)
    seq_chars <- strsplit(seq_upper, "")[[1]]
    
    encoded_seq <- lapply(seq_chars, function(base) {
      if (base %in% names(encoding_map)) {
        return(encoding_map[[base]])
      } else {
        return(c(0, 0, 0, 0))  # Unknown base
      }
    })
    
    return(unlist(encoded_seq))
  })
  
  return(do.call(rbind, encoded_list))
}

#' K-mer frequency encoding
#' 
#' @param sequences Vector of DNA sequences
#' @param k Length of k-mers (default: 3)
#' @return Matrix of k-mer frequency features
kmer_encode <- function(sequences, k = 3) {
  bases <- c('A', 'T', 'G', 'C')
  
  # Generate all possible k-mers
  generate_kmers <- function(k, prefix = "") {
    if (k == 0) {
      return(prefix)
    }
    result <- c()
    for (base in bases) {
      result <- c(result, generate_kmers(k - 1, paste0(prefix, base)))
    }
    return(result)
  }
  
  kmer_list <- generate_kmers(k)
  kmer_dict <- setNames(1:length(kmer_list), kmer_list)
  
  encoded_list <- lapply(sequences, function(seq) {
    seq_upper <- toupper(seq)
    seq_length <- nchar(seq_upper)
    
    # Extract k-mers
    kmers <- sapply(1:(seq_length - k + 1), function(i) {
      substring(seq_upper, i, i + k - 1)
    })
    
    # Count k-mer frequencies
    kmer_counts <- table(kmers)
    feature_vector <- rep(0, length(kmer_list))
    names(feature_vector) <- kmer_list
    
    for (kmer in names(kmer_counts)) {
      if (kmer %in% kmer_list) {
        feature_vector[kmer] <- kmer_counts[kmer]
      }
    }
    
    return(as.numeric(feature_vector))
  })
  
  return(do.call(rbind, encoded_list))
}

#' Numerical encoding (A=1, T=2, G=3, C=4)
#' 
#' @param sequences Vector of DNA sequences
#' @return Matrix of numerically encoded sequences
numerical_encode <- function(sequences) {
  encoding_map <- c('A' = 1, 'T' = 2, 'G' = 3, 'C' = 4)
  
  encoded_list <- lapply(sequences, function(seq) {
    seq_upper <- toupper(seq)
    seq_chars <- strsplit(seq_upper, "")[[1]]
    return(sapply(seq_chars, function(base) {
      if (base %in% names(encoding_map)) {
        return(encoding_map[base])
      } else {
        return(0)
      }
    }))
  })
  
  # Pad sequences to same length
  max_length <- max(sapply(encoded_list, length))
  padded_list <- lapply(encoded_list, function(seq) {
    if (length(seq) < max_length) {
      return(c(seq, rep(0, max_length - length(seq))))
    }
    return(seq)
  })
  
  return(do.call(rbind, padded_list))
}

#' Encode DNA sequences using specified method
#' 
#' @param sequences Vector of DNA sequences
#' @param method Encoding method ('onehot', 'kmer', 'numerical')
#' @return Matrix of encoded sequences
encode_sequences <- function(sequences, method = 'onehot') {
  if (method == 'onehot') {
    return(onehot_encode(sequences))
  } else if (method == 'kmer') {
    return(kmer_encode(sequences))
  } else if (method == 'numerical') {
    return(numerical_encode(sequences))
  } else {
    stop(paste("Unknown encoding method:", method))
  }
}

#' Prepare data for machine learning
#' 
#' @param data_path Path to the CSV file
#' @param encoding_method Encoding method ('onehot', 'kmer', 'numerical')
#' @param test_size Proportion of data for testing (default: 0.2)
#' @param random_state Random state for reproducibility (default: 42)
#' @return List containing X_train, X_test, y_train, y_test
prepare_data <- function(data_path = NULL, encoding_method = 'onehot', 
                        test_size = 0.2, random_state = 42) {
  # Load data
  data <- load_genomics_data(data_path)
  
  # Extract sequences and labels
  sequences <- data$Sequences
  labels <- data$Labels
  
  # Encode sequences
  cat("Encoding sequences using", encoding_method, "method...\n")
  X <- encode_sequences(sequences, method = encoding_method)
  y <- labels
  
  # Split data
  set.seed(random_state)
  train_indices <- sample(1:nrow(X), size = floor((1 - test_size) * nrow(X)))
  
  X_train <- X[train_indices, ]
  X_test <- X[-train_indices, ]
  y_train <- y[train_indices]
  y_test <- y[-train_indices]
  
  cat("Training set:", nrow(X_train), "x", ncol(X_train), "\n")
  cat("Test set:", nrow(X_test), "x", ncol(X_test), "\n")
  cat("Class distribution - Train:", table(y_train), "\n")
  cat("Class distribution - Test:", table(y_test), "\n")
  
  return(list(
    X_train = X_train,
    X_test = X_test,
    y_train = y_train,
    y_test = y_test
  ))
}

#' Get information about the dataset
#' 
#' @param data_path Path to the CSV file
#' @return List containing dataset information
get_data_info <- function(data_path = NULL) {
  data <- load_genomics_data(data_path)
  
  info <- list(
    total_samples = nrow(data),
    sequence_length = nchar(data$Sequences[1]),
    class_distribution = table(data$Labels),
    features = colnames(data)
  )
  
  return(info)
}



