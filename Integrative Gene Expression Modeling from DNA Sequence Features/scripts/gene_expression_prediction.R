# Gene Expression Prediction from DNA Sequences
# =============================================
# This script predicts gene expression levels from DNA sequences using various
# machine learning approaches in R.

# Load required libraries
library(readr)
library(dplyr)
library(ggplot2)
library(caret)
library(randomForest)
library(xgboost)
library(e1071)
library(pROC)
library(doParallel)

# Set random seed for reproducibility
set.seed(42)

# ============================================================================
# 1. DATA LOADING AND PREPROCESSING
# ============================================================================

cat(paste0(rep("=", 80), collapse = ""), "\n")
cat("Gene Expression Prediction from DNA Sequences\n")
cat(paste0(rep("=", 80), collapse = ""), "\n\n")

# Load data
cat("1. Loading data...\n")
# Determine the correct data path based on where the script is run from
# If running from project root: use "data/genomics_data.csv"
# If running from scripts directory: use "../data/genomics_data.csv"
data_path <- file.path("data", "genomics_data.csv")
if (!file.exists(data_path)) {
  data_path <- file.path("..", "data", "genomics_data.csv")
}

if (!file.exists(data_path)) {
  stop("Error: Could not find genomics_data.csv. Please ensure you're running from the project root directory.")
}

df <- read_csv(data_path, show_col_types = FALSE)

cat(sprintf("Dataset shape: %d rows, %d columns\n", nrow(df), ncol(df)))
cat(sprintf("Label distribution:\n"))
print(table(df$Labels))

# ============================================================================
# 2. FEATURE ENGINEERING
# ============================================================================

cat("\n2. Encoding DNA sequences...\n")

# K-mer encoding function
kmer_encoding <- function(sequences, k = 3) {
  # Extract k-mers from each sequence
  kmers_list <- lapply(sequences, function(seq) {
    seq_length <- nchar(seq)
    if (seq_length < k) {
      return(character(0))
    }
    kmers <- character(seq_length - k + 1)
    for (i in 1:(seq_length - k + 1)) {
      kmers[i] <- substr(seq, i, i + k - 1)
    }
    return(kmers)
  })
  
  # Create a list of all unique k-mers
  all_kmers <- unique(unlist(kmers_list))
  
  # Create frequency matrix
  n_sequences <- length(sequences)
  n_kmers <- length(all_kmers)
  freq_matrix <- matrix(0, nrow = n_sequences, ncol = n_kmers)
  colnames(freq_matrix) <- all_kmers
  
  # Count k-mer frequencies
  for (i in 1:n_sequences) {
    kmers <- kmers_list[[i]]
    if (length(kmers) > 0) {
      kmers_table <- table(kmers)
      for (kmer in names(kmers_table)) {
        if (kmer %in% all_kmers) {
          freq_matrix[i, kmer] <- kmers_table[kmer]
        }
      }
      # Normalize by sequence length
      freq_matrix[i, ] <- freq_matrix[i, ] / length(kmers)
    }
  }
  
  return(list(matrix = freq_matrix, kmers = all_kmers))
}

# Nucleotide composition function
nucleotide_composition <- function(sequences) {
  nucleotides <- c("A", "T", "G", "C")
  n_sequences <- length(sequences)
  n_features <- 4 + 1  # 4 nucleotides + GC content
  composition_matrix <- matrix(0, nrow = n_sequences, ncol = n_features)
  colnames(composition_matrix) <- c(nucleotides, "GC_content")
  
  for (i in 1:n_sequences) {
    seq <- toupper(sequences[i])
    seq_chars <- strsplit(seq, "")[[1]]
    seq_length <- length(seq_chars)
    
    # Nucleotide frequencies
    for (j in 1:4) {
      composition_matrix[i, j] <- sum(seq_chars == nucleotides[j]) / seq_length
    }
    
    # GC content
    composition_matrix[i, 5] <- (composition_matrix[i, 3] + composition_matrix[i, 4])
  }
  
  return(composition_matrix)
}

# Encode sequences
sequences <- df$Sequences
labels <- as.factor(df$Labels)

cat("Encoding sequences using k-mer approach (k=3)...\n")
kmer_result <- kmer_encoding(sequences, k = 3)
X <- kmer_result$matrix
cat(sprintf("Encoded feature shape: %d x %d\n", nrow(X), ncol(X)))

# ============================================================================
# 3. DATA SPLITTING
# ============================================================================

cat("\n3. Splitting data into train and test sets...\n")

# Create data frame for modeling
model_data <- as.data.frame(X)
model_data$Label <- labels

# Split data
train_indices <- createDataPartition(model_data$Label, p = 0.8, list = FALSE)
train_data <- model_data[train_indices, ]
test_data <- model_data[-train_indices, ]

X_train <- train_data[, !colnames(train_data) %in% "Label"]
y_train <- train_data$Label
X_test <- test_data[, !colnames(test_data) %in% "Label"]
y_test <- test_data$Label

cat(sprintf("Training set: %d samples\n", nrow(train_data)))
cat(sprintf("Test set: %d samples\n", nrow(test_data)))
cat(sprintf("Training label distribution: %s\n", paste(table(y_train), collapse = ", ")))
cat(sprintf("Test label distribution: %s\n", paste(table(y_test), collapse = ", ")))

# ============================================================================
# 4. MODEL TRAINING AND EVALUATION
# ============================================================================

cat("\n4. Training models...\n")

# Function to evaluate model
evaluate_model <- function(model, X_test, y_test, model_name, test_data_frame = NULL) {
  # Initialize variables
  y_pred <- NULL
  y_pred_proba <- NULL
  
  # Predictions
  if (class(model)[1] == "xgb.Booster") {
    # XGBoost requires matrix input
    test_matrix <- as.matrix(X_test)
    y_pred_proba <- predict(model, test_matrix)
    y_pred <- ifelse(y_pred_proba > 0.5, 1, 0)
    y_pred <- factor(y_pred, levels = levels(y_test))
  } else if (class(model)[1] == "randomForest") {
    # Random Forest
    y_pred <- predict(model, test_data_frame)
    prob_matrix <- predict(model, test_data_frame, type = "prob")
    if (ncol(prob_matrix) >= 2) {
      y_pred_proba <- prob_matrix[, 2]
    } else {
      y_pred_proba <- as.numeric(y_pred) - 1
    }
  } else if (class(model)[1] == "svm") {
    # SVM
    y_pred <- predict(model, test_data_frame)
    # Try to get probabilities from SVM
    tryCatch({
      svm_pred_prob <- predict(model, test_data_frame, probability = TRUE)
      prob_attr <- attr(svm_pred_prob, "probabilities")
      if (!is.null(prob_attr) && ncol(prob_attr) >= 2) {
        # Get probability for class "1" (high expression)
        if ("1" %in% colnames(prob_attr)) {
          y_pred_proba <- prob_attr[, "1"]
        } else {
          y_pred_proba <- prob_attr[, 2]
        }
      } else {
        # Fallback: convert predictions to numeric probabilities
        y_pred_proba <- as.numeric(y_pred) - 1
      }
    }, error = function(e) {
      # If probability extraction fails, use predictions as probabilities
      y_pred_proba <<- as.numeric(y_pred) - 1
    })
    
    # Ensure y_pred_proba is set
    if (is.null(y_pred_proba)) {
      y_pred_proba <- as.numeric(y_pred) - 1
    }
  } else {
    # Default: try to get predictions
    if (!is.null(test_data_frame)) {
      y_pred <- predict(model, test_data_frame)
      # Try to get probabilities
      tryCatch({
        prob_result <- predict(model, test_data_frame, type = "prob")
        if (is.matrix(prob_result) && ncol(prob_result) >= 2) {
          y_pred_proba <- prob_result[, 2]
        } else {
          y_pred_proba <- as.numeric(y_pred) - 1
        }
      }, error = function(e) {
        y_pred_proba <<- as.numeric(y_pred) - 1
      })
    } else {
      y_pred <- predict(model, X_test)
      y_pred_proba <- as.numeric(y_pred) - 1
    }
  }
  
  # Ensure both variables are set
  if (is.null(y_pred) || is.null(y_pred_proba)) {
    stop(sprintf("Error: Could not generate predictions for %s", model_name))
  }
  
  # Metrics
  accuracy <- mean(y_pred == y_test)
  cm <- confusionMatrix(y_pred, y_test)
  
  # ROC AUC
  roc_auc <- NA
  tryCatch({
    roc_obj <- roc(as.numeric(y_test) - 1, y_pred_proba, quiet = TRUE)
    roc_auc <- as.numeric(auc(roc_obj))
  }, error = function(e) {
    cat(sprintf("Warning: Could not calculate ROC-AUC for %s\n", model_name))
  })
  
  return(list(
    accuracy = accuracy,
    confusion_matrix = cm,
    y_pred = y_pred,
    y_pred_proba = y_pred_proba,
    roc_auc = roc_auc
  ))
}

# Train models
results <- list()

# Random Forest
cat("\n   Training Random Forest...\n")
rf_model <- randomForest(
  Label ~ .,
  data = train_data,
  ntree = 100,
  mtry = sqrt(ncol(X_train)),
  importance = TRUE
)
rf_results <- evaluate_model(rf_model, X_test, y_test, "Random Forest", test_data)
results[["Random Forest"]] <- list(model = rf_model, metrics = rf_results)
cat(sprintf("   Accuracy: %.4f\n", rf_results$accuracy))
if (!is.na(rf_results$roc_auc)) {
  cat(sprintf("   ROC-AUC: %.4f\n", rf_results$roc_auc))
}

# XGBoost
cat("\n   Training XGBoost...\n")
train_matrix <- as.matrix(X_train)
test_matrix <- as.matrix(X_test)
dtrain <- xgb.DMatrix(data = train_matrix, label = as.numeric(y_train) - 1)
dtest <- xgb.DMatrix(data = test_matrix, label = as.numeric(y_test) - 1)

xgb_model <- xgb.train(
  data = dtrain,
  nrounds = 100,
  objective = "binary:logistic",
  eval_metric = "logloss",
  max_depth = 6,
  eta = 0.3,
  verbose = 0
)
xgb_results <- evaluate_model(xgb_model, X_test, y_test, "XGBoost")
results[["XGBoost"]] <- list(model = xgb_model, metrics = xgb_results)
cat(sprintf("   Accuracy: %.4f\n", xgb_results$accuracy))
if (!is.na(xgb_results$roc_auc)) {
  cat(sprintf("   ROC-AUC: %.4f\n", xgb_results$roc_auc))
}

# SVM
cat("\n   Training SVM...\n")
svm_model <- svm(
  Label ~ .,
  data = train_data,
  kernel = "radial",
  probability = TRUE
)
svm_results <- evaluate_model(svm_model, X_test, y_test, "SVM", test_data)
results[["SVM"]] <- list(model = svm_model, metrics = svm_results)
cat(sprintf("   Accuracy: %.4f\n", svm_results$accuracy))
if (!is.na(svm_results$roc_auc)) {
  cat(sprintf("   ROC-AUC: %.4f\n", svm_results$roc_auc))
}

# ============================================================================
# 5. RESULTS AND VISUALIZATION
# ============================================================================

cat("\n5. Generating plots...\n")

# Create results directory if it doesn't exist
# Try project root first, then scripts directory parent
results_dir <- ifelse(dir.exists("results"), "results", file.path("..", "results"))
if (!dir.exists(results_dir)) {
  dir.create(results_dir, recursive = TRUE)
}

# Accuracy comparison
accuracies <- sapply(results, function(x) x$metrics$accuracy)
roc_aucs <- sapply(results, function(x) {
  if (!is.na(x$metrics$roc_auc)) {
    return(x$metrics$roc_auc)
  } else {
    return(NA)
  }
})

# Plot accuracy comparison
png(file.path(results_dir, "model_comparison_R.png"), width = 1200, height = 600)
par(mfrow = c(1, 2))

barplot(accuracies, 
        names.arg = names(accuracies),
        col = c("#3498db", "#e74c3c", "#2ecc71"),
        main = "Model Accuracy Comparison",
        ylab = "Accuracy",
        ylim = c(0, 1),
        las = 2)
text(x = 1:length(accuracies), 
     y = accuracies + 0.02,
     labels = sprintf("%.3f", accuracies),
     cex = 0.8)

# Plot ROC-AUC comparison (if available)
if (any(!is.na(roc_aucs))) {
  valid_aucs <- roc_aucs[!is.na(roc_aucs)]
  valid_names <- names(roc_aucs)[!is.na(roc_aucs)]
  barplot(valid_aucs,
          names.arg = valid_names,
          col = c("#3498db", "#e74c3c", "#2ecc71")[1:length(valid_aucs)],
          main = "Model ROC-AUC Comparison",
          ylab = "ROC-AUC",
          ylim = c(0, 1),
          las = 2)
  text(x = 1:length(valid_aucs),
       y = valid_aucs + 0.02,
       labels = sprintf("%.3f", valid_aucs),
       cex = 0.8)
}

dev.off()

# ROC curves
png(file.path(results_dir, "roc_curves_R.png"), width = 1000, height = 800)
plot(1, type = "n", 
     xlim = c(0, 1), ylim = c(0, 1),
     xlab = "False Positive Rate",
     ylab = "True Positive Rate",
     main = "ROC Curves")
abline(a = 0, b = 1, lty = 2, col = "gray")

colors <- c("#3498db", "#e74c3c", "#2ecc71")
i <- 1
for (model_name in names(results)) {
  metrics <- results[[model_name]]$metrics
  if (!is.na(metrics$roc_auc)) {
    roc_obj <- roc(as.numeric(y_test) - 1, metrics$y_pred_proba, quiet = TRUE)
    lines(roc_obj, col = colors[i], lwd = 2)
    i <- i + 1
  }
}

legend("bottomright",
       legend = paste(names(results), 
                     sprintf("(AUC = %.3f)", roc_aucs)),
       col = colors[1:length(results)],
       lwd = 2)
dev.off()

# ============================================================================
# 6. SAVE MODELS
# ============================================================================

cat("\n6. Saving models...\n")
# Try project root first, then scripts directory parent
models_dir <- ifelse(dir.exists("models"), "models", file.path("..", "models"))
if (!dir.exists(models_dir)) {
  dir.create(models_dir, recursive = TRUE)
}

# Find best model
best_model_name <- names(results)[which.max(accuracies)]
best_model <- results[[best_model_name]]$model

# Save best model
if (best_model_name == "XGBoost") {
  xgb.save(best_model, file.path(models_dir, "best_model_xgboost_R.model"))
} else {
  saveRDS(best_model, file.path(models_dir, "best_model_R.rds"))
}

cat(sprintf("Best model (%s) saved to %s\n", 
            best_model_name, 
            file.path(models_dir, "best_model_R.rds")))

# ============================================================================
# 7. PRINT DETAILED RESULTS
# ============================================================================

cat("\n7. Detailed Results:\n")
cat(strrep("=", 80) %+% "\n")

for (model_name in names(results)) {
  cat(sprintf("\n%s:\n", model_name))
  cat(sprintf("  Accuracy: %.4f\n", results[[model_name]]$metrics$accuracy))
  if (!is.na(results[[model_name]]$metrics$roc_auc)) {
    cat(sprintf("  ROC-AUC: %.4f\n", results[[model_name]]$metrics$roc_auc))
  }
  cat("\n  Confusion Matrix:\n")
  print(results[[model_name]]$metrics$confusion_matrix)
}

cat("\n", paste0(rep("=", 80), collapse = ""), "\n")
cat("Pipeline completed successfully!\n")
cat(paste0(rep("=", 80), collapse = ""), "\n")

