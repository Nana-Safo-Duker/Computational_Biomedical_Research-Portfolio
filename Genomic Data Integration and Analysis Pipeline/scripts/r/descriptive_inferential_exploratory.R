# Descriptive, Inferential, and Exploratory Statistical Analysis
# Genomics Sequence Classification Dataset

library(dplyr)
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

numeric_cols <- c("length", "gc_content", "a_freq", "t_freq", "g_freq", "c_freq", "entropy")

cat("======================================================================\n")
cat("DESCRIPTIVE STATISTICAL ANALYSIS\n")
cat("======================================================================\n")

# Summary statistics
cat("\n1. SUMMARY STATISTICS\n")
print(summary(df_features[numeric_cols]))

# Additional descriptive measures
cat("\n2. ADDITIONAL DESCRIPTIVE MEASURES\n")
for (col in numeric_cols) {
  cat("\n", toupper(col), ":\n")
  cat("  Mean:", mean(df_features[[col]]), "\n")
  cat("  Median:", median(df_features[[col]]), "\n")
  cat("  Std Dev:", sd(df_features[[col]]), "\n")
  cat("  Variance:", var(df_features[[col]]), "\n")
  cat("  Range:", max(df_features[[col]]) - min(df_features[[col]]), "\n")
  cat("  IQR:", IQR(df_features[[col]]), "\n")
  if (requireNamespace("moments", quietly = TRUE)) {
    cat("  Skewness:", moments::skewness(df_features[[col]]), "\n")
    cat("  Kurtosis:", moments::kurtosis(df_features[[col]]), "\n")
  }
}

# By label groups
cat("\n3. DESCRIPTIVE STATISTICS BY LABEL\n")
for (col in numeric_cols) {
  cat("\n", toupper(col), " by Label:\n")
  print(aggregate(df_features[[col]], by = list(df_features$Labels), FUN = summary))
}

cat("\n======================================================================\n")
cat("INFERENTIAL STATISTICAL ANALYSIS\n")
cat("======================================================================\n")

# Normality tests
cat("\n1. NORMALITY TESTS (Shapiro-Wilk Test)\n")
for (col in numeric_cols) {
  sample_data <- sample(df_features[[col]], min(5000, nrow(df_features)))
  test_result <- shapiro.test(sample_data)
  cat(col, ": W =", test_result$statistic, 
      ", p-value =", test_result$p.value, 
      ifelse(test_result$p.value > 0.05, " (Normal)", " (Not Normal)"), "\n")
}

# T-tests
cat("\n2. INDEPENDENT T-TESTS (Label 0 vs Label 1)\n")
for (col in numeric_cols) {
  group_0 <- df_features[df_features$Labels == 0, col]
  group_1 <- df_features[df_features$Labels == 1, col]
  test_result <- t.test(group_0, group_1)
  significance <- ifelse(test_result$p.value < 0.001, "***",
                        ifelse(test_result$p.value < 0.01, "**",
                               ifelse(test_result$p.value < 0.05, "*", "")))
  cat(col, ": t-stat =", test_result$statistic, 
      ", p-value =", test_result$p.value, significance, "\n")
}

# Mann-Whitney U test
cat("\n3. MANN-WHITNEY U TESTS (Non-parametric)\n")
for (col in numeric_cols) {
  group_0 <- df_features[df_features$Labels == 0, col]
  group_1 <- df_features[df_features$Labels == 1, col]
  test_result <- wilcox.test(group_0, group_1)
  significance <- ifelse(test_result$p.value < 0.001, "***",
                        ifelse(test_result$p.value < 0.01, "**",
                               ifelse(test_result$p.value < 0.05, "*", "")))
  cat(col, ": W =", test_result$statistic, 
      ", p-value =", test_result$p.value, significance, "\n")
}

# Confidence intervals
cat("\n4. CONFIDENCE INTERVALS (95%)\n")
for (col in numeric_cols) {
  mean_val <- mean(df_features[[col]])
  std_val <- sd(df_features[[col]])
  n <- length(df_features[[col]])
  se <- std_val / sqrt(n)
  ci_lower <- mean_val - 1.96 * se
  ci_upper <- mean_val + 1.96 * se
  cat(col, ": [", ci_lower, ",", ci_upper, "]\n")
}

cat("\n======================================================================\n")
cat("EXPLORATORY DATA ANALYSIS\n")
cat("======================================================================\n")

# Correlation analysis
cat("\n1. CORRELATION ANALYSIS\n")
cor_matrix <- cor(df_features[numeric_cols])
print(cor_matrix)

# Outlier detection
cat("\n2. OUTLIER DETECTION (IQR Method)\n")
for (col in numeric_cols) {
  Q1 <- quantile(df_features[[col]], 0.25)
  Q3 <- quantile(df_features[[col]], 0.75)
  IQR_val <- Q3 - Q1
  lower_bound <- Q1 - 1.5 * IQR_val
  upper_bound <- Q3 + 1.5 * IQR_val
  outliers <- sum(df_features[[col]] < lower_bound | df_features[[col]] > upper_bound)
  cat(col, ":", outliers, "outliers (", 
      round(outliers/nrow(df_features)*100, 2), "%)\n")
}

cat("\n======================================================================\n")
cat("ANALYSIS COMPLETE\n")
cat("======================================================================\n")

