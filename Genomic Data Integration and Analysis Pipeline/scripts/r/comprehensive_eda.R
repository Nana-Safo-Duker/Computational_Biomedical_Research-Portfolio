# Comprehensive Exploratory Data Analysis (EDA)
# Genomics Sequence Classification Dataset

library(dplyr)
library(ggplot2)
library(stringr)
library(corrplot)
library(gridExtra)

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

numeric_cols <- c("length", "gc_content", "a_freq", "t_freq", "g_freq", "c_freq", "entropy")

cat("================================================================================\n")
cat("COMPREHENSIVE EXPLORATORY DATA ANALYSIS\n")
cat("================================================================================\n")

# 1. Data Overview
cat("\n1. DATA OVERVIEW\n")
cat("Dataset Shape:", dim(df_features), "\n")
cat("Column Names:", paste(names(df_features), collapse = ", "), "\n")
cat("Missing Values:\n")
print(colSums(is.na(df_features)))
cat("Duplicate Rows:", sum(duplicated(df_features)), "\n")

# 2. Target Variable Analysis
cat("\n2. TARGET VARIABLE ANALYSIS\n")
label_counts <- table(df_features$Labels)
print(label_counts)
print(prop.table(label_counts))
cat("Class Balance:", ifelse(abs(label_counts[1] - label_counts[2]) < 50, "Balanced", "Imbalanced"), "\n")

# 3. Feature Statistics
cat("\n3. FEATURE STATISTICS\n")
print(summary(df_features[numeric_cols]))

# 4. Correlation Analysis
cat("\n4. CORRELATION ANALYSIS\n")
cor_matrix <- cor(df_features[numeric_cols])
print(cor_matrix)

# 5. Feature Differences by Label
cat("\n5. FEATURE DIFFERENCES BY LABEL\n")
for (col in numeric_cols) {
  group_0 <- df_features[df_features$Labels == 0, col]
  group_1 <- df_features[df_features$Labels == 1, col]
  mean_diff <- mean(group_1) - mean(group_0)
  test_result <- t.test(group_0, group_1)
  cat(col, ": Mean difference =", mean_diff, ", p-value =", test_result$p.value, "\n")
}

# 6. Outlier Analysis
cat("\n6. OUTLIER ANALYSIS\n")
for (col in numeric_cols) {
  Q1 <- quantile(df_features[[col]], 0.25)
  Q3 <- quantile(df_features[[col]], 0.75)
  IQR_val <- Q3 - Q1
  outliers <- sum(df_features[[col]] < (Q1 - 1.5*IQR_val) | df_features[[col]] > (Q3 + 1.5*IQR_val))
  cat(col, ":", outliers, "outliers (", round(outliers/nrow(df_features)*100, 2), "%)\n")
}

# Visualizations
# Distribution plots
png("../results/r_eda_distributions.png", width = 2000, height = 1500, res = 300)
par(mfrow = c(2, 4))
for (col in numeric_cols) {
  hist(df_features[[col]], main = paste("Distribution of", col), 
       xlab = col, col = "skyblue", border = "black", breaks = 30)
}
dev.off()

# Correlation heatmap
png("../results/r_eda_correlation.png", width = 1200, height = 1000, res = 300)
corrplot(cor_matrix, method = "color", type = "upper", 
         order = "hclust", tl.cex = 0.8, tl.col = "black")
dev.off()

# Box plots by label
png("../results/r_eda_boxplots.png", width = 2000, height = 1500, res = 300)
par(mfrow = c(2, 4))
for (col in numeric_cols) {
  boxplot(df_features[[col]] ~ df_features$Labels, 
          main = paste(col, "by Label"), 
          xlab = "Label", ylab = col, col = c("skyblue", "salmon"))
}
dev.off()

cat("\n================================================================================\n")
cat("EDA COMPLETE - Visualizations saved to ../results/\n")
cat("================================================================================\n")

