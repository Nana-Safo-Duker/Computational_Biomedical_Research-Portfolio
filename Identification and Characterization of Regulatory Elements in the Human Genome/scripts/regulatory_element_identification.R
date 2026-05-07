################################################################################
# Regulatory Element Identification in Genomic Sequences
# R Implementation
#
# This script provides comprehensive tools for identifying regulatory elements
# (promoters, enhancers, silencers, insulators) in DNA sequences using machine
# learning and bioinformatics approaches.
#
# Regulatory Elements:
# - Promoters: Sequences that initiate transcription (typically upstream of genes)
# - Enhancers: Sequences that increase transcription rates
# - Silencers: Sequences that repress transcription
# - Insulators: Sequences that block enhancer-promoter interactions
#
# Author: Regulatory Element Identification Project
# Date: 2025
################################################################################

# Load required libraries
suppressPackageStartupMessages({
  library(dplyr)
  library(caret)
  library(randomForest)
  library(e1071)
  library(pROC)
  library(ggplot2)
  library(gridExtra)
  library(stringr)
})

# Set seed for reproducibility
set.seed(42)

################################################################################
# Feature Extraction Functions
################################################################################

#' Extract k-mer frequency features from DNA sequences
#'
#' @param sequences Character vector of DNA sequences
#' @param k Integer, length of k-mers (default: 3 for trinucleotides)
#' @return Matrix with k-mer frequencies
extract_kmer_features <- function(sequences, k = 3) {
  cat("Extracting", k, "-mer features...\n")
  
  # Generate all possible k-mers
  nucleotides <- c("A", "T", "G", "C")
  kmers <- expand.grid(rep(list(nucleotides), k))
  kmers <- apply(kmers, 1, paste, collapse = "")
  
  # Count k-mer frequencies in each sequence
  features <- matrix(0, nrow = length(sequences), ncol = length(kmers))
  colnames(features) <- kmers
  
  for (i in seq_along(sequences)) {
    seq <- toupper(sequences[i])
    seq_length <- nchar(seq)
    
    # Count k-mers
    for (j in 1:(seq_length - k + 1)) {
      kmer <- substr(seq, j, j + k - 1)
      if (kmer %in% kmers) {
        features[i, kmer] <- features[i, kmer] + 1
      }
    }
    
    # Normalize by sequence length
    features[i, ] <- features[i, ] / (seq_length - k + 1)
  }
  
  return(features)
}

#' Extract nucleotide composition features
#'
#' @param sequences Character vector of DNA sequences
#' @return Matrix with composition features
extract_composition_features <- function(sequences) {
  cat("Extracting composition features...\n")
  
  features <- matrix(0, nrow = length(sequences), ncol = 0)
  
  for (seq in sequences) {
    seq <- toupper(seq)
    length_seq <- nchar(seq)
    
    # Basic nucleotide frequencies
    a_freq <- str_count(seq, "A") / length_seq
    t_freq <- str_count(seq, "T") / length_seq
    g_freq <- str_count(seq, "G") / length_seq
    c_freq <- str_count(seq, "C") / length_seq
    
    # GC content
    gc_content <- (str_count(seq, "G") + str_count(seq, "C")) / length_seq
    
    # AT/GC ratio
    at_count <- str_count(seq, "A") + str_count(seq, "T")
    gc_count <- str_count(seq, "G") + str_count(seq, "C")
    at_gc_ratio <- at_count / (gc_count + 1e-10)
    
    # Dinucleotide frequencies
    dinucleotides <- c("AA", "AT", "AG", "AC", "TA", "TT", "TG", "TC",
                      "GA", "GT", "GG", "GC", "CA", "CT", "CG", "CC")
    dinuc_freqs <- sapply(dinucleotides, function(dinuc) {
      str_count(seq, fixed(dinuc)) / (length_seq - 1)
    })
    
    # Sequence complexity (Shannon entropy)
    nuc_counts <- table(strsplit(seq, "")[[1]])
    probs <- nuc_counts / length_seq
    entropy <- -sum(probs * log2(probs + 1e-10))
    
    feature_vector <- c(a_freq, t_freq, g_freq, c_freq, gc_content,
                       at_gc_ratio, entropy, dinuc_freqs)
    features <- rbind(features, feature_vector)
  }
  
  colnames(features) <- c("A_freq", "T_freq", "G_freq", "C_freq", "GC_content",
                         "AT_GC_ratio", "entropy", names(dinuc_freqs))
  
  return(features)
}

#' Extract features based on known regulatory element motifs
#'
#' @param sequences Character vector of DNA sequences
#' @return Matrix with motif counts
extract_motif_features <- function(sequences) {
  cat("Extracting motif features...\n")
  
  # Common regulatory motifs
  motifs <- list(
    TATA_box = "TATAAA",
    TATA_variant = "TATAA",
    CAAT_box = "CCAAT",
    GC_box = "GGGCGG"
  )
  
  features <- matrix(0, nrow = length(sequences), ncol = length(motifs))
  colnames(features) <- names(motifs)
  
  for (i in seq_along(sequences)) {
    seq <- toupper(sequences[i])
    motif_counts <- sapply(motifs, function(motif) {
      str_count(seq, fixed(motif))
    })
    features[i, ] <- motif_counts
  }
  
  return(features)
}

#' Prepare all features for machine learning
#'
#' @param df Data frame with Sequences and Labels columns
#' @param k Integer, k-mer size (default: 3)
#' @return List with feature matrix X and labels y
prepare_features <- function(df, k = 3) {
  cat("\n", rep("=", 60), "\n", sep = "")
  cat("FEATURE EXTRACTION\n")
  cat(rep("=", 60), "\n", sep = "")
  
  sequences <- df$Sequences
  y <- df$Labels
  
  # Extract different feature types
  kmer_features <- extract_kmer_features(sequences, k = k)
  composition_features <- extract_composition_features(sequences)
  motif_features <- extract_motif_features(sequences)
  
  # Combine all features
  X <- cbind(kmer_features, composition_features, motif_features)
  
  cat("\nTotal features:", ncol(X), "\n")
  cat("  -", k, "-mer features:", ncol(kmer_features), "\n")
  cat("  - Composition features:", ncol(composition_features), "\n")
  cat("  - Motif features:", ncol(motif_features), "\n")
  
  return(list(X = X, y = y))
}

################################################################################
# Model Training and Evaluation
################################################################################

#' Train multiple machine learning models
#'
#' @param X_train Training feature matrix
#' @param y_train Training labels
#' @return List of trained models
train_models <- function(X_train, y_train) {
  cat("\n", rep("=", 60), "\n", sep = "")
  cat("MODEL TRAINING\n")
  cat(rep("=", 60), "\n", sep = "")
  
  models <- list()
  
  # Random Forest
  cat("\nTraining Random Forest...\n")
  models$RandomForest <- randomForest(
    x = X_train,
    y = as.factor(y_train),
    ntree = 100,
    mtry = sqrt(ncol(X_train)),
    importance = TRUE
  )
  cat("  Training Accuracy:", mean(models$RandomForest$predicted == y_train), "\n")
  
  # Support Vector Machine
  cat("\nTraining SVM...\n")
  models$SVM <- svm(
    x = X_train,
    y = as.factor(y_train),
    kernel = "radial",
    probability = TRUE
  )
  train_pred_svm <- predict(models$SVM, X_train)
  cat("  Training Accuracy:", mean(train_pred_svm == y_train), "\n")
  
  # Gradient Boosting (using caret)
  cat("\nTraining Gradient Boosting...\n")
  train_data <- data.frame(X_train, Label = as.factor(y_train))
  models$GradientBoosting <- train(
    Label ~ .,
    data = train_data,
    method = "gbm",
    trControl = trainControl(method = "cv", number = 5, verboseIter = FALSE),
    verbose = FALSE
  )
  cat("  Training Accuracy:", max(models$GradientBoosting$results$Accuracy), "\n")
  
  return(models)
}

#' Evaluate models on test set
#'
#' @param models List of trained models
#' @param X_test Test feature matrix
#' @param y_test Test labels
#' @return List with evaluation results
evaluate_models <- function(models, X_test, y_test) {
  cat("\n", rep("=", 60), "\n", sep = "")
  cat("MODEL EVALUATION\n")
  cat(rep("=", 60), "\n", sep = "")
  
  results <- list()
  
  for (model_name in names(models)) {
    cat("\n", model_name, ":\n", sep = "")
    cat(rep("-", 40), "\n", sep = "")
    
    model <- models[[model_name]]
    
    # Predictions
    if (model_name == "GradientBoosting") {
      y_pred <- predict(model, X_test)
      y_pred_proba <- predict(model, X_test, type = "prob")[, 2]
    } else {
      y_pred <- predict(model, X_test)
      y_pred_proba <- attr(predict(model, X_test, probability = TRUE), "probabilities")[, 2]
    }
    
    # Convert to numeric if needed
    if (is.factor(y_pred)) {
      y_pred <- as.numeric(as.character(y_pred))
    }
    
    # Metrics
    cm <- confusionMatrix(as.factor(y_pred), as.factor(y_test), positive = "1")
    accuracy <- cm$overall["Accuracy"]
    precision <- cm$byClass["Precision"]
    recall <- cm$byClass["Recall"]
    f1 <- cm$byClass["F1"]
    
    # AUC-ROC
    roc_obj <- roc(y_test, y_pred_proba, quiet = TRUE)
    auc <- as.numeric(auc(roc_obj))
    
    cat("Accuracy: ", round(accuracy, 4), "\n", sep = "")
    cat("Precision:", round(precision, 4), "\n", sep = "")
    cat("Recall:   ", round(recall, 4), "\n", sep = "")
    cat("F1-Score: ", round(f1, 4), "\n", sep = "")
    cat("AUC-ROC:  ", round(auc, 4), "\n", sep = "")
    
    results[[model_name]] <- list(
      accuracy = accuracy,
      precision = precision,
      recall = recall,
      f1 = f1,
      auc = auc,
      predictions = y_pred,
      probabilities = y_pred_proba,
      confusion_matrix = cm,
      roc = roc_obj
    )
  }
  
  return(results)
}

################################################################################
# Visualization Functions
################################################################################

#' Generate visualization plots
#'
#' @param results List with evaluation results
#' @param save_path Character, path to save plots
generate_plots <- function(results, save_path = "results") {
  cat("\n", rep("=", 60), "\n", sep = "")
  cat("GENERATING VISUALIZATIONS\n")
  cat(rep("=", 60), "\n", sep = "")
  
  dir.create(save_path, showWarnings = FALSE, recursive = TRUE)
  
  # 1. Model comparison
  model_names <- names(results)
  metrics <- c("accuracy", "precision", "recall", "f1", "auc")
  
  comparison_data <- data.frame(
    Model = rep(model_names, each = length(metrics)),
    Metric = rep(metrics, length(model_names)),
    Value = unlist(lapply(results, function(r) {
      c(r$accuracy, r$precision, r$recall, r$f1, r$auc)
    }))
  )
  
  p1 <- ggplot(comparison_data, aes(x = Model, y = Value, fill = Metric)) +
    geom_bar(stat = "identity", position = "dodge") +
    labs(title = "Model Performance Comparison", y = "Score") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  ggsave(file.path(save_path, "model_comparison.png"), p1, 
         width = 12, height = 6, dpi = 300)
  cat("Saved:", file.path(save_path, "model_comparison.png"), "\n")
  
  # 2. ROC curves
  roc_data <- lapply(names(results), function(name) {
    roc_obj <- results[[name]]$roc
    data.frame(
      FPR = 1 - roc_obj$specificities,
      TPR = roc_obj$sensitivities,
      Model = name,
      AUC = results[[name]]$auc
    )
  })
  roc_df <- do.call(rbind, roc_data)
  
  p2 <- ggplot(roc_df, aes(x = FPR, y = TPR, color = Model)) +
    geom_line(size = 1) +
    geom_abline(intercept = 0, slope = 1, linetype = "dashed", color = "gray") +
    labs(title = "ROC Curves", x = "False Positive Rate", y = "True Positive Rate") +
    theme_minimal() +
    scale_color_brewer(type = "qual", palette = "Set1")
  
  ggsave(file.path(save_path, "roc_curves.png"), p2, 
         width = 10, height = 8, dpi = 300)
  cat("Saved:", file.path(save_path, "roc_curves.png"), "\n")
  
  # 3. Confusion matrices
  cm_plots <- lapply(names(results), function(name) {
    cm <- results[[name]]$confusion_matrix$table
    cm_df <- as.data.frame(cm)
    colnames(cm_df) <- c("Predicted", "Actual", "Freq")
    
    p <- ggplot(cm_df, aes(x = Predicted, y = Actual, fill = Freq)) +
      geom_tile() +
      geom_text(aes(label = Freq), color = "white", size = 6) +
      scale_fill_gradient(low = "lightblue", high = "darkblue") +
      labs(title = paste0(name, "\nAccuracy: ", 
                         round(results[[name]]$accuracy, 3))) +
      theme_minimal()
    
    return(p)
  })
  
  p3 <- do.call(grid.arrange, c(cm_plots, ncol = 2))
  ggsave(file.path(save_path, "confusion_matrices.png"), p3, 
         width = 14, height = 12, dpi = 300)
  cat("Saved:", file.path(save_path, "confusion_matrices.png"), "\n")
  
  # 4. Feature importance (for Random Forest)
  if ("RandomForest" %in% names(results)) {
    rf_model <- models$RandomForest
    importance_df <- data.frame(
      Feature = rownames(rf_model$importance),
      Importance = rf_model$importance[, "MeanDecreaseGini"]
    )
    importance_df <- importance_df[order(importance_df$Importance, decreasing = TRUE), ]
    importance_df <- head(importance_df, 20)
    importance_df$Feature <- factor(importance_df$Feature, 
                                   levels = importance_df$Feature[order(importance_df$Importance)])
    
    p4 <- ggplot(importance_df, aes(x = Feature, y = Importance)) +
      geom_bar(stat = "identity", fill = "steelblue") +
      coord_flip() +
      labs(title = "Top 20 Feature Importances (Random Forest)", 
           x = "Feature", y = "Importance") +
      theme_minimal()
    
    ggsave(file.path(save_path, "feature_importance.png"), p4, 
           width = 12, height = 8, dpi = 300)
    cat("Saved:", file.path(save_path, "feature_importance.png"), "\n")
  }
}

################################################################################
# Main Execution
################################################################################

main <- function() {
  cat(rep("=", 60), "\n", sep = "")
  cat("REGULATORY ELEMENT IDENTIFICATION\n")
  cat(rep("=", 60), "\n", sep = "")
  cat("\nThis tool identifies regulatory elements in genomic sequences.\n")
  cat("Regulatory elements include:\n")
  cat("  - Promoters: Initiate transcription\n")
  cat("  - Enhancers: Increase transcription rates\n")
  cat("  - Silencers: Repress transcription\n")
  cat("  - Insulators: Block enhancer-promoter interactions\n")
  cat(rep("=", 60), "\n\n", sep = "")
  
  # Load data
  cat("Loading genomic data...\n")
  df <- read.csv("data/genomics_data.csv", stringsAsFactors = FALSE)
  cat("Loaded", nrow(df), "sequences\n")
  cat("Sequence length:", nchar(df$Sequences[1]), "nucleotides\n")
  cat("Label distribution:\n")
  print(table(df$Labels))
  
  # Prepare features
  features <- prepare_features(df, k = 3)
  X <- features$X
  y <- features$y
  
  # Split data
  cat("\n", rep("=", 60), "\n", sep = "")
  cat("DATA SPLITTING\n")
  cat(rep("=", 60), "\n", sep = "")
  
  train_indices <- createDataPartition(y, p = 0.8, list = FALSE)
  X_train <- X[train_indices, ]
  X_test <- X[-train_indices, ]
  y_train <- y[train_indices]
  y_test <- y[-train_indices]
  
  cat("Training set:", nrow(X_train), "sequences\n")
  cat("Test set:", nrow(X_test), "sequences\n")
  
  # Scale features
  preProc <- preProcess(X_train, method = c("center", "scale"))
  X_train <- predict(preProc, X_train)
  X_test <- predict(preProc, X_test)
  
  # Train models
  models <<- train_models(X_train, y_train)
  
  # Evaluate models
  results <- evaluate_models(models, X_test, y_test)
  
  # Generate visualizations
  generate_plots(results, save_path = "results")
  
  cat("\n", rep("=", 60), "\n", sep = "")
  cat("ANALYSIS COMPLETE\n")
  cat(rep("=", 60), "\n", sep = "")
  cat("\nResults saved in 'results/' directory\n")
  
  # Find best model
  best_model <- names(results)[which.max(sapply(results, function(r) r$f1))]
  cat("\nBest performing model:\n")
  cat("  ", best_model, ": F1-Score = ", 
      round(results[[best_model]]$f1, 4), "\n", sep = "")
  
  return(list(models = models, results = results))
}

# Run main function if script is executed directly
if (!interactive()) {
  result <- main()
}

