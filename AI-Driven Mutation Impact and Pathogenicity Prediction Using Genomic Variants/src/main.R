# Main script for Mutation Impact and Pathogenicity Prediction

# Source required modules
source("src/data_loader.R")
source("src/models.R")

# Parse command line arguments (if using Rscript)
args <- commandArgs(trailingOnly = TRUE)

# Default parameters
data_path <- NULL
encoding_method <- "onehot"
model_type <- "random_forest"
test_size <- 0.2
random_state <- 42

# Parse arguments (simplified version)
if (length(args) > 0) {
  for (i in 1:length(args)) {
    if (args[i] == "--data_path" && i + 1 <= length(args)) {
      data_path <- args[i + 1]
    } else if (args[i] == "--encoding" && i + 1 <= length(args)) {
      encoding_method <- args[i + 1]
    } else if (args[i] == "--model" && i + 1 <= length(args)) {
      model_type <- args[i + 1]
    } else if (args[i] == "--test_size" && i + 1 <= length(args)) {
      test_size <- as.numeric(args[i + 1])
    } else if (args[i] == "--random_state" && i + 1 <= length(args)) {
      random_state <- as.numeric(args[i + 1])
    }
  }
}

# Main pipeline
cat(rep("=", 60), "\n", sep = "")
cat("MUTATION IMPACT AND PATHOGENICITY PREDICTION\n")
cat(rep("=", 60), "\n", sep = "")

# Load and prepare data
data_info <- get_data_info(data_path)
cat("\nDataset Information:\n")
cat("  Total samples:", data_info$total_samples, "\n")
cat("  Sequence length:", data_info$sequence_length, "\n")
cat("  Class distribution:\n")
print(data_info$class_distribution)

# Prepare data
cat("\nPreparing data...\n")
data_split <- prepare_data(
  data_path = data_path,
  encoding_method = encoding_method,
  test_size = test_size,
  random_state = random_state
)

X_train <- data_split$X_train
X_test <- data_split$X_test
y_train <- data_split$y_train
y_test <- data_split$y_test

# Train model
if (model_type == "ensemble") {
  cat("\nTraining ensemble model...\n")
  models <- train_ensemble(X_train, y_train)
  
  # Evaluate ensemble
  ensemble_pred <- predict_ensemble(models, X_test, method = "voting")
  
  # Calculate metrics
  y_test_factor <- as.factor(y_test)
  ensemble_pred_factor <- as.factor(ensemble_pred)
  cm <- confusionMatrix(ensemble_pred_factor, y_test_factor)
  
  cat("\n", rep("=", 50), "\n", sep = "")
  cat("ENSEMBLE MODEL RESULTS\n")
  cat(rep("=", 50), "\n", sep = "")
  cat("Accuracy: ", sprintf("%.4f", cm$overall['Accuracy']), "\n", sep = "")
  cat("Precision:", sprintf("%.4f", cm$byClass['Precision']), "\n", sep = "")
  cat("Recall:   ", sprintf("%.4f", cm$byClass['Recall']), "\n", sep = "")
  cat("F1 Score: ", sprintf("%.4f", cm$byClass['F1']), "\n", sep = "")
  cat(rep("=", 50), "\n", sep = "")
  
} else {
  cat("\nTraining", model_type, "model...\n")
  
  # Train model
  if (model_type == "random_forest") {
    model <- train_random_forest(X_train, y_train)
  } else if (model_type == "svm") {
    model <- train_svm(X_train, y_train)
  } else if (model_type == "logistic") {
    model <- train_logistic_regression(X_train, y_train)
  } else if (model_type == "xgboost") {
    model <- train_xgboost(X_train, y_train)
  } else {
    stop(paste("Unknown model type:", model_type))
  }
  
  # Evaluate model
  metrics <- evaluate_model(model, X_test, y_test, model_type)
  
  # Save model
  models_dir <- "models"
  if (!dir.exists(models_dir)) {
    dir.create(models_dir)
  }
  timestamp <- format(Sys.time(), "%Y%m%d_%H%M%S")
  model_path <- file.path(models_dir, paste0(model_type, "_", timestamp, ".rds"))
  save_model_r(model, model_path)
  cat("\nModel saved to:", model_path, "\n")
}

cat("\n", rep("=", 60), "\n", sep = "")
cat("Pipeline completed successfully!\n")
cat(rep("=", 60), "\n", sep = "")


