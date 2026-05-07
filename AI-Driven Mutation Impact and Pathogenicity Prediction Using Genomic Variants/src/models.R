# Machine Learning Models for Mutation Impact Prediction
# Includes various models for predicting functional impact of mutations

library(randomForest)
library(e1071)
library(glmnet)
library(xgboost)
library(caret)

#' Train Random Forest model
#' 
#' @param X_train Training features
#' @param y_train Training labels
#' @param ntree Number of trees (default: 100)
#' @param mtry Number of variables randomly sampled (default: sqrt(ncol(X_train)))
#' @return Trained Random Forest model
train_random_forest <- function(X_train, y_train, ntree = 100, mtry = NULL) {
  if (is.null(mtry)) {
    mtry <- floor(sqrt(ncol(X_train)))
  }
  
  cat("Training Random Forest model...\n")
  model <- randomForest(
    x = X_train,
    y = as.factor(y_train),
    ntree = ntree,
    mtry = mtry,
    importance = TRUE
  )
  
  cat("Training completed!\n")
  return(model)
}

#' Train SVM model
#' 
#' @param X_train Training features
#' @param y_train Training labels
#' @param kernel Kernel type (default: 'radial')
#' @param cost Cost parameter (default: 1.0)
#' @return Trained SVM model
train_svm <- function(X_train, y_train, kernel = 'radial', cost = 1.0) {
  cat("Training SVM model...\n")
  model <- svm(
    x = X_train,
    y = as.factor(y_train),
    kernel = kernel,
    cost = cost,
    probability = TRUE
  )
  
  cat("Training completed!\n")
  return(model)
}

#' Train Logistic Regression model
#' 
#' @param X_train Training features
#' @param y_train Training labels
#' @return Trained Logistic Regression model
train_logistic_regression <- function(X_train, y_train) {
  cat("Training Logistic Regression model...\n")
  
  # Convert to data frame
  train_data <- as.data.frame(X_train)
  train_data$label <- as.factor(y_train)
  
  model <- glm(
    label ~ .,
    data = train_data,
    family = binomial(link = "logit")
  )
  
  cat("Training completed!\n")
  return(model)
}

#' Train XGBoost model
#' 
#' @param X_train Training features
#' @param y_train Training labels
#' @param nrounds Number of boosting rounds (default: 100)
#' @param max_depth Maximum tree depth (default: 6)
#' @param eta Learning rate (default: 0.3)
#' @return Trained XGBoost model
train_xgboost <- function(X_train, y_train, nrounds = 100, max_depth = 6, eta = 0.3) {
  cat("Training XGBoost model...\n")
  
  # Convert to matrix
  X_train_matrix <- as.matrix(X_train)
  
  # Train model
  model <- xgboost(
    data = X_train_matrix,
    label = y_train,
    nrounds = nrounds,
    max_depth = max_depth,
    eta = eta,
    objective = "binary:logistic",
    eval_metric = "logloss",
    verbose = 0
  )
  
  cat("Training completed!\n")
  return(model)
}

#' Evaluate model performance
#' 
#' @param model Trained model
#' @param X_test Test features
#' @param y_test Test labels
#' @param model_type Type of model ('random_forest', 'svm', 'logistic', 'xgboost')
#' @return List containing evaluation metrics
evaluate_model <- function(model, X_test, y_test, model_type) {
  # Make predictions
  if (model_type == 'random_forest') {
    y_pred <- predict(model, X_test)
    y_proba <- predict(model, X_test, type = 'prob')[, 2]
  } else if (model_type == 'svm') {
    y_pred <- predict(model, X_test)
    y_proba <- attr(predict(model, X_test, probability = TRUE), "probabilities")[, 2]
  } else if (model_type == 'logistic') {
    test_data <- as.data.frame(X_test)
    y_proba <- predict(model, test_data, type = 'response')
    y_pred <- ifelse(y_proba > 0.5, 1, 0)
  } else if (model_type == 'xgboost') {
    X_test_matrix <- as.matrix(X_test)
    y_proba <- predict(model, X_test_matrix)
    y_pred <- ifelse(y_proba > 0.5, 1, 0)
  } else {
    stop(paste("Unknown model type:", model_type))
  }
  
  # Convert to factors for confusion matrix
  y_test_factor <- as.factor(y_test)
  y_pred_factor <- as.factor(y_pred)
  
  # Calculate metrics
  cm <- confusionMatrix(y_pred_factor, y_test_factor)
  
  # Calculate ROC-AUC
  if (requireNamespace("pROC", quietly = TRUE)) {
    library(pROC)
    roc_auc <- as.numeric(auc(y_test, y_proba))
  } else {
    roc_auc <- NA
    cat("Warning: pROC package not available. ROC-AUC not calculated.\n")
  }
  
  metrics <- list(
    accuracy = cm$overall['Accuracy'],
    precision = cm$byClass['Precision'],
    recall = cm$byClass['Recall'],
    f1_score = cm$byClass['F1'],
    roc_auc = roc_auc,
    confusion_matrix = cm$table
  )
  
  # Print results
  cat("\n", rep("=", 50), "\n", sep = "")
  cat("Model:", toupper(model_type), "\n")
  cat(rep("=", 50), "\n", sep = "")
  cat("Accuracy: ", sprintf("%.4f", metrics$accuracy), "\n", sep = "")
  cat("Precision:", sprintf("%.4f", metrics$precision), "\n", sep = "")
  cat("Recall:   ", sprintf("%.4f", metrics$recall), "\n", sep = "")
  cat("F1 Score: ", sprintf("%.4f", metrics$f1_score), "\n", sep = "")
  if (!is.na(metrics$roc_auc)) {
    cat("ROC-AUC:  ", sprintf("%.4f", metrics$roc_auc), "\n", sep = "")
  }
  cat(rep("=", 50), "\n", sep = "")
  
  cat("\nConfusion Matrix:\n")
  print(metrics$confusion_matrix)
  
  return(metrics)
}

#' Save model to file
#' 
#' @param model Trained model
#' @param filepath Path to save the model
save_model_r <- function(model, filepath) {
  saveRDS(model, filepath)
  cat("Model saved to", filepath, "\n")
}

#' Load model from file
#' 
#' @param filepath Path to the model file
#' @return Loaded model
load_model_r <- function(filepath) {
  model <- readRDS(filepath)
  cat("Model loaded from", filepath, "\n")
  return(model)
}

#' Train ensemble model
#' 
#' @param X_train Training features
#' @param y_train Training labels
#' @param model_types Vector of model types to include
#' @return List of trained models
train_ensemble <- function(X_train, y_train, model_types = c('random_forest', 'xgboost', 'svm')) {
  models <- list()
  
  for (model_type in model_types) {
    cat("\nTraining", model_type, "model...\n")
    
    if (model_type == 'random_forest') {
      models[[model_type]] <- train_random_forest(X_train, y_train)
    } else if (model_type == 'svm') {
      models[[model_type]] <- train_svm(X_train, y_train)
    } else if (model_type == 'xgboost') {
      models[[model_type]] <- train_xgboost(X_train, y_train)
    } else {
      cat("Warning: Unknown model type", model_type, "\n")
    }
  }
  
  return(models)
}

#' Predict using ensemble
#' 
#' @param models List of trained models
#' @param X_test Test features
#' @param method Ensemble method ('voting', 'averaging')
#' @return Vector of predictions
predict_ensemble <- function(models, X_test, method = 'voting') {
  predictions_list <- list()
  probabilities_list <- list()
  
  for (model_name in names(models)) {
    model <- models[[model_name]]
    
    if (model_name == 'random_forest') {
      pred <- predict(model, X_test)
      proba <- predict(model, X_test, type = 'prob')[, 2]
    } else if (model_name == 'svm') {
      pred <- predict(model, X_test)
      proba <- attr(predict(model, X_test, probability = TRUE), "probabilities")[, 2]
    } else if (model_name == 'xgboost') {
      X_test_matrix <- as.matrix(X_test)
      proba <- predict(model, X_test_matrix)
      pred <- ifelse(proba > 0.5, 1, 0)
    }
    
    predictions_list[[model_name]] <- as.numeric(as.character(pred))
    probabilities_list[[model_name]] <- proba
  }
  
  if (method == 'voting') {
    # Majority voting
    pred_matrix <- do.call(cbind, predictions_list)
    ensemble_pred <- apply(pred_matrix, 1, function(x) {
      as.numeric(mean(x) > 0.5)
    })
  } else if (method == 'averaging') {
    # Average probabilities
    prob_matrix <- do.call(cbind, probabilities_list)
    avg_proba <- rowMeans(prob_matrix)
    ensemble_pred <- ifelse(avg_proba > 0.5, 1, 0)
  }
  
  return(ensemble_pred)
}



