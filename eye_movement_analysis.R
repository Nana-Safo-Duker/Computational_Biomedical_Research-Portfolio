# Eye Movement Analysis for Brain Disorder Detection
# ===================================================
#
# This R script provides comprehensive tools for analyzing eye movement data
# collected from wearable sensors to detect brain disorders.
#
# Author: Research Team
# Date: 2024
# License: MIT

# Load required libraries
library(dplyr)
library(tidyr)
library(ggplot2)
library(corrplot)
library(caret)
library(randomForest)
library(e1071)
library(pROC)
library(psych)

# Set random seed for reproducibility
set.seed(42)

#' Load eye movement data from CSV file
#'
#' @param filepath Path to the CSV file
#' @return Data frame containing eye movement data
load_eye_movement_data <- function(filepath) {
  tryCatch({
    data <- read.csv(filepath, stringsAsFactors = FALSE)
    cat(sprintf("Data loaded successfully: %d samples, %d features\n", 
                nrow(data), ncol(data))))
    return(data)
  }, error = function(e) {
    cat(sprintf("Error loading data: %s\n", e$message))
    stop(e)
  })
}

#' Preprocess eye movement data
#'
#' @param data Raw eye movement data
#' @param sampling_rate Sampling rate in Hz (default: 1000)
#' @return Preprocessed data frame
preprocess_eye_data <- function(data, sampling_rate = 1000) {
  processed_data <- data
  
  # Remove outliers (values beyond 3 standard deviations)
  numeric_cols <- sapply(processed_data, is.numeric)
  
  for (col in names(processed_data)[numeric_cols]) {
    mean_val <- mean(processed_data[[col]], na.rm = TRUE)
    std_val <- sd(processed_data[[col]], na.rm = TRUE)
    processed_data <- processed_data[
      processed_data[[col]] >= (mean_val - 3 * std_val) &
      processed_data[[col]] <= (mean_val + 3 * std_val),
    ]
  }
  
  cat(sprintf("Data preprocessed: %d samples remaining\n", nrow(processed_data)))
  return(processed_data)
}

#' Extract features from eye movement data
#'
#' @param data Preprocessed eye movement data
#' @param sampling_rate Sampling rate in Hz
#' @return Data frame with extracted features
extract_eye_features <- function(data, sampling_rate = 1000) {
  features_list <- list()
  
  if ("x_position" %in% colnames(data) && "y_position" %in% colnames(data)) {
    # Calculate velocity
    x_velocity <- diff(data$x_position) * sampling_rate
    y_velocity <- diff(data$y_position) * sampling_rate
    velocity <- sqrt(x_velocity^2 + y_velocity^2)
    
    # Calculate acceleration
    acceleration <- diff(velocity) * sampling_rate
    
    # Saccade detection (rapid eye movements)
    saccade_threshold <- quantile(velocity, 0.95, na.rm = TRUE)
    saccades <- velocity > saccade_threshold
    
    # Extract features
    features_list$mean_velocity <- mean(velocity, na.rm = TRUE)
    features_list$std_velocity <- sd(velocity, na.rm = TRUE)
    features_list$max_velocity <- max(velocity, na.rm = TRUE)
    features_list$mean_acceleration <- mean(acceleration, na.rm = TRUE)
    features_list$std_acceleration <- sd(acceleration, na.rm = TRUE)
    features_list$saccade_count <- sum(saccades, na.rm = TRUE)
    features_list$saccade_rate <- sum(saccades, na.rm = TRUE) / length(velocity)
    features_list$mean_fixation_duration <- calculate_fixation_duration(
      velocity, saccade_threshold, sampling_rate
    )
    features_list$fixation_stability <- calculate_fixation_stability(data)
  }
  
  # Add statistical features for other numeric columns
  numeric_cols <- sapply(data, is.numeric)
  for (col in names(data)[numeric_cols]) {
    if (!col %in% c("x_position", "y_position")) {
      features_list[[paste0(col, "_mean")]] <- mean(data[[col]], na.rm = TRUE)
      features_list[[paste0(col, "_std")]] <- sd(data[[col]], na.rm = TRUE)
      features_list[[paste0(col, "_median")]] <- median(data[[col]], na.rm = TRUE)
    }
  }
  
  return(as.data.frame(features_list))
}

#' Calculate mean fixation duration
#'
#' @param velocity Velocity vector
#' @param threshold Saccade threshold
#' @param sampling_rate Sampling rate in Hz
#' @return Mean fixation duration in seconds
calculate_fixation_duration <- function(velocity, threshold, sampling_rate) {
  fixations <- velocity <= threshold
  fixation_durations <- numeric()
  current_duration <- 0
  
  for (is_fixation in fixations) {
    if (is_fixation && !is.na(is_fixation)) {
      current_duration <- current_duration + 1
    } else {
      if (current_duration > 0) {
        fixation_durations <- c(fixation_durations, current_duration / sampling_rate)
      }
      current_duration <- 0
    }
  }
  
  if (current_duration > 0) {
    fixation_durations <- c(fixation_durations, current_duration / sampling_rate)
  }
  
  return(ifelse(length(fixation_durations) > 0, mean(fixation_durations), 0.0))
}

#' Calculate fixation stability
#'
#' @param data Eye movement data
#' @return Fixation stability metric
calculate_fixation_stability <- function(data) {
  if ("x_position" %in% colnames(data) && "y_position" %in% colnames(data)) {
    position_variance <- var(c(data$x_position, data$y_position), na.rm = TRUE)
    return(1.0 / (1.0 + position_variance))
  }
  return(0.0)
}

#' Perform statistical analysis comparing groups
#'
#' @param features Feature data frame
#' @param labels Group labels
#' @return List containing statistical test results
perform_statistical_analysis <- function(features, labels) {
  results <- list()
  unique_labels <- unique(labels)
  
  if (length(unique_labels) != 2) {
    cat("Warning: Statistical analysis requires exactly 2 groups\n")
    return(results)
  }
  
  group1 <- unique_labels[1]
  group2 <- unique_labels[2]
  group1_data <- features[labels == group1, ]
  group2_data <- features[labels == group2, ]
  
  for (feature in colnames(features)) {
    # Perform t-test
    test_result <- t.test(
      group1_data[[feature]],
      group2_data[[feature]]
    )
    
    # Calculate descriptive statistics
    results[[feature]] <- list(
      t_statistic = test_result$statistic,
      p_value = test_result$p.value,
      significant = test_result$p.value < 0.05,
      group1_mean = mean(group1_data[[feature]], na.rm = TRUE),
      group1_std = sd(group1_data[[feature]], na.rm = TRUE),
      group2_mean = mean(group2_data[[feature]], na.rm = TRUE),
      group2_std = sd(group2_data[[feature]], na.rm = TRUE)
    )
  }
  
  return(results)
}

#' Apply Principal Component Analysis
#'
#' @param features Feature matrix
#' @param n_components Number of principal components
#' @return List containing transformed features and PCA object
apply_pca <- function(features, n_components = 10) {
  # Remove any columns with all NA values
  features_clean <- features[, colSums(is.na(features)) < nrow(features)]
  
  # Scale features
  features_scaled <- scale(features_clean)
  
  # Apply PCA
  pca_result <- prcomp(features_scaled, center = FALSE, scale. = FALSE)
  
  # Extract specified number of components
  n_components <- min(n_components, ncol(pca_result$x))
  features_pca <- pca_result$x[, 1:n_components]
  
  explained_variance <- sum(summary(pca_result)$importance[2, 1:n_components])
  cat(sprintf("PCA applied: %d components explain %.2f%% of variance\n",
              n_components, explained_variance * 100))
  
  return(list(
    features = as.data.frame(features_pca),
    pca_object = pca_result,
    explained_variance = explained_variance
  ))
}

#' Train a machine learning classifier
#'
#' @param features Feature matrix
#' @param labels Class labels
#' @param model_type Type of classifier ('random_forest' or 'svm')
#' @param test_size Proportion of data for testing
#' @return List containing model and performance metrics
train_classifier <- function(features, labels, model_type = "random_forest", 
                            test_size = 0.2) {
  # Create train/test split
  train_indices <- createDataPartition(labels, p = 1 - test_size, list = FALSE)
  
  X_train <- features[train_indices, ]
  X_test <- features[-train_indices, ]
  y_train <- labels[train_indices]
  y_test <- labels[-train_indices]
  
  # Train model
  if (model_type == "random_forest") {
    model <- randomForest(
      x = X_train,
      y = as.factor(y_train),
      ntree = 100,
      mtry = sqrt(ncol(X_train)),
      importance = TRUE
    )
  } else if (model_type == "svm") {
    model <- svm(
      x = X_train,
      y = as.factor(y_train),
      kernel = "radial",
      probability = TRUE
    )
  } else {
    stop(sprintf("Unknown model type: %s", model_type))
  }
  
  # Make predictions
  y_pred <- predict(model, X_test)
  
  # Calculate performance metrics
  accuracy <- mean(y_pred == y_test)
  confusion_matrix <- table(Predicted = y_pred, Actual = y_test)
  
  # Calculate ROC curve if binary classification
  if (length(unique(y_test)) == 2) {
    y_pred_proba <- predict(model, X_test, probability = TRUE)
    proba_matrix <- attr(y_pred_proba, "probabilities")
    roc_curve <- roc(y_test, proba_matrix[, 2])
    auc <- auc(roc_curve)
  } else {
    roc_curve <- NULL
    auc <- NULL
  }
  
  cat(sprintf("\nModel Performance (%s):\n", model_type))
  cat(sprintf("Accuracy: %.4f\n", accuracy))
  if (!is.null(auc)) {
    cat(sprintf("AUC: %.4f\n", auc))
  }
  cat("\nConfusion Matrix:\n")
  print(confusion_matrix)
  
  return(list(
    model = model,
    accuracy = accuracy,
    auc = auc,
    confusion_matrix = confusion_matrix,
    roc_curve = roc_curve,
    model_type = model_type
  ))
}

#' Create visualizations of analysis results
#'
#' @param features Feature matrix
#' @param labels Class labels
#' @param save_path Optional path to save the figure
create_visualizations <- function(features, labels, save_path = NULL) {
  # Create feature distribution plot
  if (ncol(features) > 0) {
    feature_name <- colnames(features)[1]
    plot_data <- data.frame(
      value = features[[feature_name]],
      group = labels
    )
    
    p1 <- ggplot(plot_data, aes(x = value, fill = group)) +
      geom_histogram(alpha = 0.7, bins = 30, position = "identity") +
      labs(x = feature_name, y = "Frequency", title = "Feature Distribution by Group") +
      theme_minimal() +
      theme(legend.position = "bottom")
    
    print(p1)
  }
  
  # Correlation matrix
  if (ncol(features) > 1) {
    corr_matrix <- cor(features, use = "complete.obs")
    png(filename = ifelse(is.null(save_path), "correlation_matrix.png", 
                          paste0(save_path, "_correlation.png")),
        width = 800, height = 800)
    corrplot(corr_matrix, method = "color", type = "upper", 
             order = "hclust", tl.cex = 0.8, tl.col = "black")
    dev.off()
  }
  
  # Box plot for key features
  if (ncol(features) > 0) {
    key_features <- colnames(features)[1:min(4, ncol(features))]
    plot_data <- features[, key_features, drop = FALSE]
    plot_data$group <- labels
    plot_data_long <- pivot_longer(plot_data, cols = -group, 
                                   names_to = "feature", values_to = "value")
    
    p2 <- ggplot(plot_data_long, aes(x = feature, y = value, fill = group)) +
      geom_boxplot(alpha = 0.7) +
      labs(x = "Feature", y = "Value", title = "Feature Comparison by Group") +
      theme_minimal() +
      theme(axis.text.x = element_text(angle = 45, hjust = 1),
            legend.position = "bottom")
    
    print(p2)
  }
  
  if (!is.null(save_path)) {
    cat(sprintf("Figures saved (prefix: %s)\n", save_path))
  }
}

# Example usage
if (!interactive()) {
  cat("Eye Movement Analysis Script\n")
  cat("============================\n\n")
  
  # Note: This is a template script. In practice, you would load your actual data:
  # data <- load_eye_movement_data("path/to/your/data.csv")
  
  cat("This script provides functions for analyzing eye movement data.\n")
  cat("To use this script, load your data and call the appropriate functions.\n")
}

