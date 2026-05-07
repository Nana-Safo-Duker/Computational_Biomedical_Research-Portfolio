# Machine Learning Analysis
# Genomics Sequence Classification Dataset

library(dplyr)
library(caret)
library(randomForest)
library(e1071)
library(pROC)
library(ggplot2)
library(stringr)

# Load data
df <- read.csv("../data/genomics_data.csv", stringsAsFactors = FALSE)

# Feature extraction
extract_sequence_features <- function(sequences) {
  features <- data.frame(
    length = integer(),
    gc_content = numeric(),
    a_freq = numeric(),
    t_freq = numeric(),
    g_freq = numeric(),
    c_freq = numeric(),
    entropy = numeric()
  )
  
  for (seq in sequences) {
    seq <- toupper(seq)
    length <- nchar(seq)
    gc_content <- (str_count(seq, "G") + str_count(seq, "C")) / length
    a_freq <- str_count(seq, "A") / length
    t_freq <- str_count(seq, "T") / length
    g_freq <- str_count(seq, "G") / length
    c_freq <- str_count(seq, "C") / length
    
    nucleotides <- strsplit(seq, "")[[1]]
    freq_table <- table(nucleotides)
    probs <- freq_table / length
    entropy <- -sum(probs * log2(probs))
    
    features <- rbind(features, data.frame(
      length = length, gc_content = gc_content,
      a_freq = a_freq, t_freq = t_freq, g_freq = g_freq, c_freq = c_freq,
      entropy = entropy
    ))
  }
  
  return(features)
}

feature_df <- extract_sequence_features(df$Sequences)
df_features <- cbind(df, feature_df)

# Prepare data
X <- df_features[, !names(df_features) %in% c("Sequences", "Labels")]
y <- as.factor(df_features$Labels)

# Split data
set.seed(42)
trainIndex <- createDataPartition(y, p = 0.8, list = FALSE)
X_train <- X[trainIndex, ]
X_test <- X[-trainIndex, ]
y_train <- y[trainIndex]
y_test <- y[-trainIndex]

# Scale features
preProc <- preProcess(X_train, method = c("center", "scale"))
X_train_scaled <- predict(preProc, X_train)
X_test_scaled <- predict(preProc, X_test)

cat("================================================================================\n")
cat("MACHINE LEARNING MODEL EVALUATION\n")
cat("================================================================================\n")

# Train control for cross-validation
# Note: For binary classification, ensure labels are factors with proper levels
y_train_factor <- factor(y_train, levels = c("0", "1"), labels = c("Class0", "Class1"))
y_test_factor <- factor(y_test, levels = c("0", "1"), labels = c("Class0", "Class1"))

train_control <- trainControl(method = "cv", number = 5, 
                              classProbs = TRUE, summaryFunction = twoClassSummary)

# Models to train
models <- list()

# 1. Random Forest
cat("\n1. RANDOM FOREST\n")
cat("--------------------------------------------------------------------------------\n")
rf_model <- train(x = X_train_scaled, y = y_train_factor, method = "rf",
                  trControl = train_control, ntree = 100)
rf_pred <- predict(rf_model, X_test_scaled)
rf_pred_proba <- predict(rf_model, X_test_scaled, type = "prob")
models[["Random Forest"]] <- list(model = rf_model, pred = rf_pred, 
                                   pred_proba = rf_pred_proba[, 2])
print(confusionMatrix(rf_pred, y_test_factor))

# 2. SVM
cat("\n2. SUPPORT VECTOR MACHINE\n")
cat("--------------------------------------------------------------------------------\n")
svm_model <- train(x = X_train_scaled, y = y_train_factor, method = "svmRadial",
                   trControl = train_control)
svm_pred <- predict(svm_model, X_test_scaled)
svm_pred_proba <- predict(svm_model, X_test_scaled, type = "prob")
models[["SVM"]] <- list(model = svm_model, pred = svm_pred, 
                        pred_proba = svm_pred_proba[, 2])
print(confusionMatrix(svm_pred, y_test_factor))

# 3. Logistic Regression
cat("\n3. LOGISTIC REGRESSION\n")
cat("--------------------------------------------------------------------------------\n")
lr_model <- train(x = X_train_scaled, y = y_train_factor, method = "glm",
                  trControl = train_control, family = "binomial")
lr_pred <- predict(lr_model, X_test_scaled)
lr_pred_proba <- predict(lr_model, X_test_scaled, type = "prob")
models[["Logistic Regression"]] <- list(model = lr_model, pred = lr_pred, 
                                         pred_proba = lr_pred_proba[, 2])
print(confusionMatrix(lr_pred, y_test_factor))

# 4. K-Nearest Neighbors
cat("\n4. K-NEAREST NEIGHBORS\n")
cat("--------------------------------------------------------------------------------\n")
knn_model <- train(x = X_train_scaled, y = y_train_factor, method = "knn",
                   trControl = train_control, tuneGrid = data.frame(k = 5))
knn_pred <- predict(knn_model, X_test_scaled)
knn_pred_proba <- predict(knn_model, X_test_scaled, type = "prob")
models[["KNN"]] <- list(model = knn_model, pred = knn_pred, 
                        pred_proba = knn_pred_proba[, 2])
print(confusionMatrix(knn_pred, y_test_factor))

# 5. Naive Bayes
cat("\n5. NAIVE BAYES\n")
cat("--------------------------------------------------------------------------------\n")
nb_model <- train(x = X_train_scaled, y = y_train_factor, method = "nb",
                  trControl = train_control)
nb_pred <- predict(nb_model, X_test_scaled)
nb_pred_proba <- predict(nb_model, X_test_scaled, type = "prob")
models[["Naive Bayes"]] <- list(model = nb_model, pred = nb_pred, 
                                 pred_proba = nb_pred_proba[, 2])
print(confusionMatrix(nb_pred, y_test_factor))

# Model comparison
cat("\n================================================================================\n")
cat("MODEL COMPARISON\n")
cat("================================================================================\n")

results <- data.frame(
  Model = character(),
  Accuracy = numeric(),
  Precision = numeric(),
  Recall = numeric(),
  F1 = numeric(),
  AUC = numeric(),
  stringsAsFactors = FALSE
)

for (name in names(models)) {
  cm <- confusionMatrix(models[[name]]$pred, y_test_factor)
  roc_obj <- roc(as.numeric(y_test_factor) - 1, models[[name]]$pred_proba)
  
  results <- rbind(results, data.frame(
    Model = name,
    Accuracy = cm$overall["Accuracy"],
    Precision = cm$byClass["Precision"],
    Recall = cm$byClass["Recall"],
    F1 = cm$byClass["F1"],
    AUC = as.numeric(auc(roc_obj))
  ))
}

print(results)

# Best model
best_model_name <- results$Model[which.max(results$F1)]
cat("\nBest Model (by F1-Score):", best_model_name, "\n")
cat("F1-Score:", results$F1[results$Model == best_model_name], "\n")

# ROC curves
png("../results/r_ml_roc_curves.png", width = 1200, height = 1000, res = 300)
roc_curves <- list()
colors <- rainbow(length(models))
plot(roc(as.numeric(y_test_factor) - 1, models[[1]]$pred_proba), 
     col = colors[1], main = "ROC Curves - Model Comparison")
for (i in 2:length(models)) {
  lines(roc(as.numeric(y_test_factor) - 1, models[[i]]$pred_proba), col = colors[i])
}
legend("bottomright", legend = names(models), col = colors, lty = 1, lwd = 2)
dev.off()

cat("\nAnalysis complete! Visualizations saved to ../results/\n")

