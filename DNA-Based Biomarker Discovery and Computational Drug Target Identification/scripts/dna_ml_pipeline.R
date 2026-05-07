# Machine Learning Pipeline for DNA-Based Biomarker Discovery
#
# This script trains machine learning models to identify potential biomarkers
# and drug targets from DNA sequence features.
#
# Author: DNA-Based Biomarker Discovery Project
# Date: 2025

# Load required libraries
library(caret)
library(randomForest)
library(e1071)
library(pROC)
library(dplyr)
library(data.table)

# Source feature extraction script
source("dna_feature_extraction.R")

#' Train multiple machine learning models and evaluate their performance
#'
#' @param X_train Training feature matrix
#' @param y_train Training labels
#' @param X_test Test feature matrix
#' @param y_test Test labels
#' @param use_scaling Whether to scale features for models that require it
#' @return List containing trained models and their performance metrics
train_models <- function(X_train, y_train, X_test, y_test, use_scaling = TRUE) {
  results <- list()
  
  # Scale features if needed
  scaler <- NULL
  if (use_scaling) {
    preproc_params <- preProcess(X_train, method = c("center", "scale"))
    X_train_scaled <- predict(preproc_params, X_train)
    X_test_scaled <- predict(preproc_params, X_test)
    scaler <- preproc_params
  }
  
  # Convert labels to factors
  y_train_factor <- as.factor(y_train)
  y_test_factor <- as.factor(y_test)
  
  # 1. Random Forest
  cat("\n", rep("=", 50), "\n", sep = "")
  cat("Training Random Forest...\n")
  cat(rep("=", 50), "\n", sep = "")
  
  rf_model <- randomForest(
    x = X_train,
    y = y_train_factor,
    ntree = 100,
    mtry = sqrt(ncol(X_train)),
    importance = TRUE,
    do.trace = FALSE
  )
  
  rf_pred <- predict(rf_model, X_test, type = "response")
  rf_pred_proba <- predict(rf_model, X_test, type = "prob")[, 2]
  
  rf_accuracy <- mean(rf_pred == y_test_factor)
  rf_auc <- as.numeric(auc(roc(y_test, rf_pred_proba)))
  
  # Cross-validation for Random Forest
  rf_cv <- train(
    x = X_train,
    y = y_train_factor,
    method = "rf",
    trControl = trainControl(method = "cv", number = 5),
    tuneGrid = data.frame(mtry = sqrt(ncol(X_train)))
  )
  
  results$RandomForest <- list(
    model = rf_model,
    accuracy = rf_accuracy,
    auc = rf_auc,
    cv_accuracy = max(rf_cv$results$Accuracy),
    predictions = rf_pred,
    probabilities = rf_pred_proba
  )
  
  cat("Accuracy:", rf_accuracy, "\n")
  cat("AUC-ROC:", rf_auc, "\n")
  cat("CV Accuracy:", max(rf_cv$results$Accuracy), "\n")
  
  # 2. Support Vector Machine
  cat("\n", rep("=", 50), "\n", sep = "")
  cat("Training SVM...\n")
  cat(rep("=", 50), "\n", sep = "")
  
  svm_model <- svm(
    x = X_train_scaled,
    y = y_train_factor,
    kernel = "radial",
    probability = TRUE,
    cost = 1,
    gamma = 1 / ncol(X_train_scaled)
  )
  
  svm_pred <- predict(svm_model, X_test_scaled)
  svm_pred_proba <- attr(predict(svm_model, X_test_scaled, probability = TRUE), 
                         "probabilities")[, 2]
  
  svm_accuracy <- mean(svm_pred == y_test_factor)
  svm_auc <- as.numeric(auc(roc(y_test, svm_pred_proba)))
  
  # Cross-validation for SVM
  svm_cv <- train(
    x = X_train_scaled,
    y = y_train_factor,
    method = "svmRadial",
    trControl = trainControl(method = "cv", number = 5),
    tuneGrid = expand.grid(
      C = c(0.1, 1, 10),
      sigma = c(0.01, 0.1, 1)
    )
  )
  
  results$SVM <- list(
    model = svm_model,
    accuracy = svm_accuracy,
    auc = svm_auc,
    cv_accuracy = max(svm_cv$results$Accuracy),
    predictions = svm_pred,
    probabilities = svm_pred_proba
  )
  
  cat("Accuracy:", svm_accuracy, "\n")
  cat("AUC-ROC:", svm_auc, "\n")
  cat("CV Accuracy:", max(svm_cv$results$Accuracy), "\n")
  
  # 3. Logistic Regression
  cat("\n", rep("=", 50), "\n", sep = "")
  cat("Training Logistic Regression...\n")
  cat(rep("=", 50), "\n", sep = "")
  
  # Prepare data for logistic regression
  train_data <- data.frame(X_train_scaled, Labels = y_train_factor)
  test_data <- data.frame(X_test_scaled, Labels = y_test_factor)
  
  glm_model <- glm(
    Labels ~ .,
    data = train_data,
    family = binomial(link = "logit")
  )
  
  glm_pred_proba <- predict(glm_model, test_data, type = "response")
  glm_pred <- ifelse(glm_pred_proba > 0.5, 1, 0)
  glm_pred_factor <- factor(glm_pred, levels = levels(y_test_factor))
  
  glm_accuracy <- mean(glm_pred_factor == y_test_factor)
  glm_auc <- as.numeric(auc(roc(y_test, glm_pred_proba)))
  
  # Cross-validation for Logistic Regression
  glm_cv <- train(
    Labels ~ .,
    data = train_data,
    method = "glm",
    family = "binomial",
    trControl = trainControl(method = "cv", number = 5)
  )
  
  results$LogisticRegression <- list(
    model = glm_model,
    accuracy = glm_accuracy,
    auc = glm_auc,
    cv_accuracy = max(glm_cv$results$Accuracy),
    predictions = glm_pred_factor,
    probabilities = glm_pred_proba
  )
  
  cat("Accuracy:", glm_accuracy, "\n")
  cat("AUC-ROC:", glm_auc, "\n")
  cat("CV Accuracy:", max(glm_cv$results$Accuracy), "\n")
  
  # 4. Gradient Boosting (using caret's gbm)
  cat("\n", rep("=", 50), "\n", sep = "")
  cat("Training Gradient Boosting...\n")
  cat(rep("=", 50), "\n", sep = "")
  
  gbm_cv <- train(
    x = X_train,
    y = y_train_factor,
    method = "gbm",
    trControl = trainControl(method = "cv", number = 5),
    verbose = FALSE,
    tuneGrid = expand.grid(
      interaction.depth = c(3, 5),
      n.trees = c(50, 100),
      shrinkage = c(0.01, 0.1),
      n.minobsinnode = 10
    )
  )
  
  gbm_pred <- predict(gbm_cv, X_test)
  gbm_pred_proba <- predict(gbm_cv, X_test, type = "prob")[, 2]
  
  gbm_accuracy <- mean(gbm_pred == y_test_factor)
  gbm_auc <- as.numeric(auc(roc(y_test, gbm_pred_proba)))
  
  results$GradientBoosting <- list(
    model = gbm_cv,
    accuracy = gbm_accuracy,
    auc = gbm_auc,
    cv_accuracy = max(gbm_cv$results$Accuracy),
    predictions = gbm_pred,
    probabilities = gbm_pred_proba
  )
  
  cat("Accuracy:", gbm_accuracy, "\n")
  cat("AUC-ROC:", gbm_auc, "\n")
  cat("CV Accuracy:", max(gbm_cv$results$Accuracy), "\n")
  
  return(list(results = results, scaler = scaler))
}

#' Get feature importance from a random forest model
#'
#' @param model Trained random forest model
#' @param feature_names Vector of feature names
#' @return Data frame with features and their importance scores
get_feature_importance <- function(model, feature_names) {
  if (class(model)[1] == "randomForest") {
    importance_scores <- importance(model)[, "MeanDecreaseGini"]
    importance_df <- data.frame(
      feature = feature_names,
      importance = importance_scores
    ) %>%
      arrange(desc(importance))
    return(importance_df)
  } else {
    return(NULL)
  }
}

#' Main function to run the ML pipeline
main <- function() {
  # Parse command line arguments
  args <- commandArgs(trailingOnly = TRUE)
  
  if (length(args) < 1) {
    input_file <- "../data/genomics_data.csv"
  } else {
    input_file <- args[1]
  }
  
  if (length(args) < 2) {
    output_dir <- "../results/models"
  } else {
    output_dir <- args[2]
  }
  
  # Load data
  cat("Loading data from", input_file, "...\n")
  df <- read.csv(input_file, stringsAsFactors = FALSE)
  
  # Extract features
  cat("Extracting features from DNA sequences...\n")
  sequences <- df$Sequences
  features <- extract_dna_features(sequences)
  
  # Prepare data
  if ("Labels" %in% colnames(df)) {
    y <- df$Labels
    X <- features %>% select(-Labels) %>% as.matrix()
  } else {
    stop("Labels column not found in data")
  }
  
  cat("Feature matrix shape:", nrow(X), "x", ncol(X), "\n")
  cat("Number of features:", ncol(X), "\n")
  
  # Split data
  set.seed(42)
  train_indices <- createDataPartition(y, p = 0.8, list = FALSE)
  X_train <- X[train_indices, ]
  X_test <- X[-train_indices, ]
  y_train <- y[train_indices]
  y_test <- y[-train_indices]
  
  cat("\nTraining set size:", nrow(X_train), "\n")
  cat("Test set size:", nrow(X_test), "\n")
  
  # Train models
  model_results <- train_models(X_train, y_train, X_test, y_test)
  results <- model_results$results
  scaler <- model_results$scaler
  
  # Find best model
  best_model_name <- names(results)[which.max(sapply(results, function(x) x$auc))]
  best_model <- results[[best_model_name]]$model
  
  cat("\n", rep("=", 50), "\n", sep = "")
  cat("Best model:", best_model_name, "\n")
  cat("Best AUC-ROC:", results[[best_model_name]]$auc, "\n")
  cat("Best accuracy:", results[[best_model_name]]$accuracy, "\n")
  cat(rep("=", 50), "\n", sep = "")
  
  # Get feature importance for Random Forest
  if (best_model_name == "RandomForest") {
    feature_names <- colnames(X_train)
    importance_df <- get_feature_importance(best_model, feature_names)
    
    if (!is.null(importance_df)) {
      cat("\nTop 10 Most Important Features:\n")
      print(head(importance_df, 10))
      
      # Save feature importance
      importance_path <- file.path(output_dir, "feature_importance.csv")
      dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
      write.csv(importance_df, importance_path, row.names = FALSE)
      cat("\nFeature importance saved to", importance_path, "\n")
    }
  }
  
  # Save models
  dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
  
  # Save best model
  best_model_path <- file.path(output_dir, 
                                paste0("best_model_", 
                                       tolower(gsub(" ", "_", best_model_name)), 
                                       ".rds"))
  saveRDS(best_model, best_model_path)
  cat("Best model saved to", best_model_path, "\n")
  
  # Save scaler if used
  if (!is.null(scaler)) {
    scaler_path <- file.path(output_dir, "scaler.rds")
    saveRDS(scaler, scaler_path)
    cat("Scaler saved to", scaler_path, "\n")
  }
  
  # Save results summary
  results_summary <- data.frame(
    Model = names(results),
    Accuracy = sapply(results, function(x) x$accuracy),
    AUC_ROC = sapply(results, function(x) x$auc),
    CV_Accuracy = sapply(results, function(x) x$cv_accuracy)
  )
  results_path <- file.path(output_dir, "model_comparison.csv")
  write.csv(results_summary, results_path, row.names = FALSE)
  cat("Results summary saved to", results_path, "\n")
  
  cat("\nPipeline complete!\n")
}

# Run main function if script is executed directly
if (!interactive()) {
  main()
}

