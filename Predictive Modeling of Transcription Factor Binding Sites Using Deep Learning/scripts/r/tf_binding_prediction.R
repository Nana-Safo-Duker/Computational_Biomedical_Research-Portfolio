# Transcription Factor Binding Prediction using Machine Learning in R
#
# This script implements multiple models for predicting transcription factor binding sites:
# 1. Random Forest
# 2. XGBoost
# 3. SVM (Support Vector Machine)
# 4. Neural Network
# 5. Logistic Regression
#
# Author: AI-ML Bioinformatics Team
# Date: 2024

# Load required libraries
suppressPackageStartupMessages({
  library(tidyverse)
  library(caret)
  library(randomForest)
  library(xgboost)
  library(e1071)
  library(neuralnet)
  library(pROC)
  library(ggplot2)
  library(reshape2)
  library(doParallel)
  library(gridExtra)
})

# Set random seed for reproducibility
set.seed(42)

# Enable parallel processing
cl <- makeCluster(detectCores() - 1)
registerDoParallel(cl)

#' Encode DNA sequences to numerical representations
#' 
#' @param sequences Vector of DNA sequences (strings)
#' @return Matrix of one-hot encoded sequences
encode_dna_sequences <- function(sequences) {
  nucleotide_to_int <- c('A' = 1, 'T' = 2, 'G' = 3, 'C' = 4)
  max_len <- max(nchar(sequences))
  n_seqs <- length(sequences)
  
  # Create one-hot encoded matrix
  encoded <- matrix(0, nrow = n_seqs, ncol = max_len * 4)
  
  for (i in 1:n_seqs) {
    seq <- strsplit(sequences[i], "")[[1]]
    for (j in 1:length(seq)) {
      if (seq[j] %in% names(nucleotide_to_int)) {
        idx <- (j - 1) * 4 + nucleotide_to_int[seq[j]]
        encoded[i, idx] <- 1
      }
    }
  }
  
  return(encoded)
}

#' Load and preprocess genomics data
#' 
#' @param data_path Path to the CSV file
#' @return List containing training and test sets
load_and_preprocess_data <- function(data_path = "data/genomics_data.csv") {
  cat("Loading data...\n")
  
  # Load data
  df <- read.csv(data_path, stringsAsFactors = FALSE)
  cat(sprintf("Data shape: %d rows, %d columns\n", nrow(df), ncol(df)))
  cat(sprintf("Label distribution:\n"))
  print(table(df$Labels))
  
  # Encode sequences
  sequences <- df$Sequences
  labels <- as.factor(df$Labels)
  
  cat("Encoding DNA sequences...\n")
  X_encoded <- encode_dna_sequences(sequences)
  
  # Create data frame
  data_df <- as.data.frame(X_encoded)
  data_df$Label <- labels
  
  # Split data
  train_index <- createDataPartition(data_df$Label, p = 0.8, list = FALSE)
  train_data <- data_df[train_index, ]
  test_data <- data_df[-train_index, ]
  
  X_train <- train_data[, -ncol(train_data)]
  y_train <- train_data$Label
  X_test <- test_data[, -ncol(test_data)]
  y_test <- test_data$Label
  
  cat(sprintf("Training set size: %d\n", nrow(X_train)))
  cat(sprintf("Test set size: %d\n", nrow(X_test)))
  
  return(list(
    X_train = X_train,
    y_train = y_train,
    X_test = X_test,
    y_test = y_test,
    train_data = train_data,
    test_data = test_data
  ))
}

#' Train Random Forest model
#' 
#' @param X_train Training features
#' @param y_train Training labels
#' @return Trained model
train_random_forest <- function(X_train, y_train) {
  cat("\nTraining Random Forest model...\n")
  
  model <- randomForest(
    x = X_train,
    y = y_train,
    ntree = 100,
    mtry = sqrt(ncol(X_train)),
    importance = TRUE,
    do.trace = FALSE
  )
  
  return(model)
}

#' Train XGBoost model
#' 
#' @param X_train Training features
#' @param y_train Training labels
#' @return Trained model
train_xgboost <- function(X_train, y_train) {
  cat("\nTraining XGBoost model...\n")
  
  # Convert to matrix and numeric labels
  train_matrix <- as.matrix(X_train)
  train_labels <- as.numeric(y_train) - 1  # Convert to 0/1
  
  # Train XGBoost
  model <- xgboost(
    data = train_matrix,
    label = train_labels,
    nrounds = 100,
    max_depth = 6,
    eta = 0.1,
    objective = "binary:logistic",
    eval_metric = "logloss",
    verbose = 0
  )
  
  return(model)
}

#' Train SVM model
#' 
#' @param X_train Training features
#' @param y_train Training labels
#' @return Trained model
train_svm <- function(X_train, y_train) {
  cat("\nTraining SVM model...\n")
  
  # Use a subset for SVM due to computational complexity
  sample_size <- min(5000, nrow(X_train))
  sample_idx <- sample(nrow(X_train), sample_size)
  X_train_sample <- X_train[sample_idx, ]
  y_train_sample <- y_train[sample_idx]
  
  model <- svm(
    x = X_train_sample,
    y = y_train_sample,
    kernel = "radial",
    probability = TRUE,
    scale = TRUE
  )
  
  return(model)
}

#' Train Neural Network model
#' 
#' @param train_data Training data with labels
#' @return Trained model
train_neural_network <- function(train_data) {
  cat("\nTraining Neural Network model...\n")
  
  # Prepare formula
  n_features <- ncol(train_data) - 1
  feature_names <- paste0("V", 1:n_features)
  formula_str <- paste("Label ~", paste(feature_names, collapse = " + "))
  formula <- as.formula(formula_str)
  
  # Scale data for neural network
  scaled_data <- train_data
  for (i in 1:n_features) {
    col_name <- feature_names[i]
    scaled_data[[col_name]] <- scale(scaled_data[[col_name]])
  }
  
  # Convert labels to numeric
  scaled_data$Label <- as.numeric(scaled_data$Label) - 1
  
  # Train neural network
  model <- neuralnet(
    formula = formula,
    data = scaled_data,
    hidden = c(64, 32),
    act.fct = "logistic",
    linear.output = FALSE,
    stepmax = 1e6
  )
  
  return(model)
}

#' Train Logistic Regression model
#' 
#' @param train_data Training data with labels
#' @return Trained model
train_logistic_regression <- function(train_data) {
  cat("\nTraining Logistic Regression model...\n")
  
  model <- glm(
    Label ~ .,
    data = train_data,
    family = binomial(link = "logit")
  )
  
  return(model)
}

#' Evaluate model performance
#' 
#' @param model Trained model
#' @param X_test Test features
#' @param y_test Test labels
#' @param model_type Type of model ("random_forest", "xgboost", "svm", "neural_network", "logistic")
#' @return List of performance metrics
evaluate_model <- function(model, X_test, y_test, model_type) {
  cat(sprintf("\nEvaluating %s model...\n", model_type))
  
  # Make predictions based on model type
  if (model_type == "random_forest") {
    y_pred <- predict(model, X_test, type = "response")
    y_pred_proba <- predict(model, X_test, type = "prob")[, 2]
  } else if (model_type == "xgboost") {
    test_matrix <- as.matrix(X_test)
    y_pred_proba <- predict(model, test_matrix)
    y_pred <- ifelse(y_pred_proba > 0.5, 1, 0)
    y_pred <- factor(y_pred, levels = c(0, 1))
  } else if (model_type == "svm") {
    y_pred <- predict(model, X_test)
    y_pred_proba <- attr(predict(model, X_test, probability = TRUE), "probabilities")[, 2]
  } else if (model_type == "neural_network") {
    # Scale test data
    test_scaled <- X_test
    for (i in 1:ncol(X_test)) {
      test_scaled[, i] <- scale(X_test[, i])
    }
    
    # Predict
    predictions <- compute(model, test_scaled)
    y_pred_proba <- predictions$net.result
    y_pred <- ifelse(y_pred_proba > 0.5, 1, 0)
    y_pred <- factor(y_pred, levels = c(0, 1))
  } else if (model_type == "logistic") {
    y_pred_proba <- predict(model, X_test, type = "response")
    y_pred <- ifelse(y_pred_proba > 0.5, 1, 0)
    y_pred <- factor(y_pred, levels = levels(y_test))
  }
  
  # Calculate metrics
  y_test_numeric <- as.numeric(y_test) - 1
  
  accuracy <- mean(y_pred == y_test)
  precision <- precision_score_func(y_test, y_pred)
  recall <- recall_score_func(y_test, y_pred)
  f1 <- f1_score_func(y_test, y_pred)
  
  # ROC AUC
  roc_obj <- roc(y_test_numeric, y_pred_proba, quiet = TRUE)
  roc_auc <- auc(roc_obj)
  
  # Confusion matrix
  cm <- confusionMatrix(y_pred, y_test)
  
  metrics <- list(
    accuracy = accuracy,
    precision = precision,
    recall = recall,
    f1 = f1,
    roc_auc = as.numeric(roc_auc),
    confusion_matrix = cm$table,
    y_pred = y_pred,
    y_pred_proba = y_pred_proba,
    roc_obj = roc_obj
  )
  
  return(metrics)
}

#' Calculate precision score
#' 
#' @param y_true True labels
#' @param y_pred Predicted labels
#' @return Precision score
precision_score_func <- function(y_true, y_pred) {
  cm <- table(y_true, y_pred)
  if (ncol(cm) == 2 && nrow(cm) == 2) {
    tp <- cm[2, 2]
    fp <- cm[1, 2]
    if (tp + fp == 0) return(0)
    return(tp / (tp + fp))
  }
  return(0)
}

#' Calculate recall score
#' 
#' @param y_true True labels
#' @param y_pred Predicted labels
#' @return Recall score
recall_score_func <- function(y_true, y_pred) {
  cm <- table(y_true, y_pred)
  if (ncol(cm) == 2 && nrow(cm) == 2) {
    tp <- cm[2, 2]
    fn <- cm[2, 1]
    if (tp + fn == 0) return(0)
    return(tp / (tp + fn))
  }
  return(0)
}

#' Calculate F1 score
#' 
#' @param y_true True labels
#' @param y_pred Predicted labels
#' @return F1 score
f1_score_func <- function(y_true, y_pred) {
  precision <- precision_score_func(y_true, y_pred)
  recall <- recall_score_func(y_true, y_pred)
  if (precision + recall == 0) return(0)
  return(2 * (precision * recall) / (precision + recall))
}

#' Plot confusion matrices
#' 
#' @param results List of results from all models
plot_confusion_matrices <- function(results) {
  models <- names(results)
  n_models <- length(models)
  
  plots <- list()
  for (i in 1:n_models) {
    model_name <- models[i]
    cm <- results[[model_name]]$confusion_matrix
    
    cm_df <- as.data.frame(cm)
    colnames(cm_df) <- c("Predicted", "Actual", "Freq")
    
    p <- ggplot(cm_df, aes(x = Predicted, y = Actual, fill = Freq)) +
      geom_tile() +
      geom_text(aes(label = Freq), color = "white", size = 5) +
      scale_fill_gradient(low = "lightblue", high = "darkblue") +
      labs(title = paste(toupper(model_name), "Confusion Matrix"),
           x = "Predicted Label", y = "True Label") +
      theme_minimal() +
      theme(plot.title = element_text(hjust = 0.5, size = 12, face = "bold"))
    
    plots[[i]] <- p
  }
  
  # Save plots
  if (n_models == 1) {
    ggsave("results/confusion_matrices.png", plots[[1]], width = 8, height = 6, dpi = 300)
  } else {
    # Combine plots using gridExtra
    library(gridExtra)
    combined_plot <- do.call(grid.arrange, c(plots, ncol = min(3, n_models)))
    ggsave("results/confusion_matrices.png", combined_plot, width = 5 * n_models, height = 4, dpi = 300)
  }
}

#' Plot ROC curves
#' 
#' @param results List of results from all models
plot_roc_curves <- function(results) {
  png("results/roc_curves.png", width = 10, height = 8, units = "in", res = 300)
  
  plot(0, 0, type = "n", xlim = c(0, 1), ylim = c(0, 1),
       xlab = "False Positive Rate", ylab = "True Positive Rate",
       main = "ROC Curves for All Models")
  
  colors <- rainbow(length(results))
  for (i in 1:length(results)) {
    model_name <- names(results)[i]
    roc_obj <- results[[model_name]]$roc_obj
    lines(1 - roc_obj$specificities, roc_obj$sensitivities,
          col = colors[i], lwd = 2, type = "l")
  }
  
  # Add diagonal line
  abline(0, 1, lty = 2, col = "gray")
  
  # Add legend
  legend("bottomright", legend = paste(toupper(names(results)), 
                                       sprintf("(AUC = %.3f)", 
                                               sapply(results, function(x) x$roc_auc))),
         col = colors, lwd = 2)
  
  grid()
  dev.off()
}

#' Save models and results
#' 
#' @param models List of trained models
#' @param results List of results
save_models_and_results <- function(models, results) {
  dir.create("models", showWarnings = FALSE)
  dir.create("results", showWarnings = FALSE)
  
  # Save models
  for (model_name in names(models)) {
    if (model_name == "xgboost") {
      xgb.save(models[[model_name]], sprintf("models/%s_model.model", model_name))
    } else if (model_name == "neural_network") {
      saveRDS(models[[model_name]], sprintf("models/%s_model.rds", model_name))
    } else {
      saveRDS(models[[model_name]], sprintf("models/%s_model.rds", model_name))
    }
  }
  
  # Save results summary
  results_summary <- data.frame(
    Model = names(results),
    Accuracy = sapply(results, function(x) x$accuracy),
    Precision = sapply(results, function(x) x$precision),
    Recall = sapply(results, function(x) x$recall),
    F1_Score = sapply(results, function(x) x$f1),
    ROC_AUC = sapply(results, function(x) x$roc_auc)
  )
  
  write.csv(results_summary, "results/model_comparison.csv", row.names = FALSE)
  
  # Save detailed results
  saveRDS(results, "results/detailed_results.rds")
  
  cat("\nModels and results saved!\n")
}

#' Main function to run the TF binding prediction pipeline
main <- function() {
  cat("=== Transcription Factor Binding Prediction Pipeline ===\n\n")
  
  # Create directories
  dir.create("results", showWarnings = FALSE)
  dir.create("models", showWarnings = FALSE)
  
  # Load and preprocess data
  data_list <- load_and_preprocess_data("data/genomics_data.csv")
  
  # Train models
  models <- list()
  models$random_forest <- train_random_forest(data_list$X_train, data_list$y_train)
  models$xgboost <- train_xgboost(data_list$X_train, data_list$y_train)
  models$svm <- train_svm(data_list$X_train, data_list$y_train)
  models$neural_network <- train_neural_network(data_list$train_data)
  models$logistic <- train_logistic_regression(data_list$train_data)
  
  # Evaluate models
  results <- list()
  results$random_forest <- evaluate_model(models$random_forest, data_list$X_test, 
                                          data_list$y_test, "random_forest")
  results$xgboost <- evaluate_model(models$xgboost, data_list$X_test, 
                                    data_list$y_test, "xgboost")
  results$svm <- evaluate_model(models$svm, data_list$X_test, 
                                data_list$y_test, "svm")
  results$neural_network <- evaluate_model(models$neural_network, data_list$X_test, 
                                           data_list$y_test, "neural_network")
  results$logistic <- evaluate_model(models$logistic, data_list$X_test, 
                                     data_list$y_test, "logistic")
  
  # Print results
  cat("\n=== Model Performance Summary ===\n")
  for (model_name in names(results)) {
    cat(sprintf("\n%s:\n", toupper(model_name)))
    cat(sprintf("  Accuracy:  %.4f\n", results[[model_name]]$accuracy))
    cat(sprintf("  Precision: %.4f\n", results[[model_name]]$precision))
    cat(sprintf("  Recall:    %.4f\n", results[[model_name]]$recall))
    cat(sprintf("  F1-Score:  %.4f\n", results[[model_name]]$f1))
    cat(sprintf("  ROC-AUC:   %.4f\n", results[[model_name]]$roc_auc))
  }
  
  # Plot results
  plot_confusion_matrices(results)
  plot_roc_curves(results)
  
  # Save models and results
  save_models_and_results(models, results)
  
  # Stop cluster
  stopCluster(cl)
  
  cat("\nPipeline completed successfully!\n")
  cat("Results saved in 'results/' directory\n")
  cat("Models saved in 'models/' directory\n")
}

# Run main function
if (!interactive()) {
  main()
}

