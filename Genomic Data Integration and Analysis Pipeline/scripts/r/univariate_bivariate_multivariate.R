# Univariate, Bivariate, and Multivariate Analysis
# Genomics Sequence Classification Dataset

# Load required libraries
library(dplyr)
library(ggplot2)
library(corrplot)
library(FactoMineR)
library(factoextra)
library(gridExtra)

# Set working directory and load data
df <- read.csv("../data/genomics_data.csv", stringsAsFactors = FALSE)
cat("Dataset shape:", dim(df), "\n")

# Feature extraction function
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
    
    # Basic composition
    gc_content <- (str_count(seq, "G") + str_count(seq, "C")) / length
    a_freq <- str_count(seq, "A") / length
    t_freq <- str_count(seq, "T") / length
    g_freq <- str_count(seq, "G") / length
    c_freq <- str_count(seq, "C") / length
    
    # Sequence entropy
    nucleotides <- strsplit(seq, "")[[1]]
    freq_table <- table(nucleotides)
    probs <- freq_table / length
    entropy <- -sum(probs * log2(probs))
    
    features <- rbind(features, data.frame(
      length = length,
      gc_content = gc_content,
      a_freq = a_freq,
      t_freq = t_freq,
      g_freq = g_freq,
      c_freq = c_freq,
      entropy = entropy
    ))
  }
  
  return(features)
}

# Extract features
library(stringr)
feature_df <- extract_sequence_features(df$Sequences)
df_features <- cbind(df, feature_df)

cat("\n=== UNIVARIATE ANALYSIS ===\n")
numeric_cols <- c("length", "gc_content", "a_freq", "t_freq", "g_freq", "c_freq", "entropy")

# Univariate statistics
for (col in numeric_cols) {
  cat("\n", toupper(col), ":\n")
  cat("  Mean:", mean(df_features[[col]]), "\n")
  cat("  Median:", median(df_features[[col]]), "\n")
  cat("  Std Dev:", sd(df_features[[col]]), "\n")
  cat("  Min:", min(df_features[[col]]), "\n")
  cat("  Max:", max(df_features[[col]]), "\n")
  cat("  Skewness:", moments::skewness(df_features[[col]]), "\n")
}

# Univariate visualizations
png("../results/r_univariate_continuous.png", width = 2000, height = 1500, res = 300)
par(mfrow = c(2, 4))
for (col in numeric_cols) {
  hist(df_features[[col]], main = paste("Distribution of", col), 
       xlab = col, col = "skyblue", border = "black")
  abline(v = mean(df_features[[col]]), col = "red", lty = 2, lwd = 2)
  abline(v = median(df_features[[col]]), col = "green", lty = 2, lwd = 2)
}
dev.off()

cat("\n=== BIVARIATE ANALYSIS ===\n")
# Correlation matrix
cor_matrix <- cor(df_features[numeric_cols])
print("Correlation Matrix:")
print(cor_matrix)

# Correlation plot
png("../results/r_bivariate_correlation.png", width = 1200, height = 1000, res = 300)
corrplot(cor_matrix, method = "color", type = "upper", 
         order = "hclust", tl.cex = 0.8, tl.col = "black")
dev.off()

# T-tests
cat("\nT-tests (Features by Label):\n")
for (col in numeric_cols) {
  group_0 <- df_features[df_features$Labels == 0, col]
  group_1 <- df_features[df_features$Labels == 1, col]
  test_result <- t.test(group_0, group_1)
  cat(col, ": t-stat =", test_result$statistic, 
      ", p-value =", test_result$p.value, "\n")
}

cat("\n=== MULTIVARIATE ANALYSIS ===\n")
# PCA
X <- df_features[numeric_cols]
X_scaled <- scale(X)

pca_result <- prcomp(X_scaled, center = FALSE, scale. = FALSE)
summary(pca_result)

# PCA plot
png("../results/r_multivariate_pca.png", width = 1200, height = 1000, res = 300)
fviz_pca_ind(pca_result, geom.ind = "point", 
             col.ind = as.factor(df_features$Labels),
             palette = c("#00AFBB", "#E7B800"),
             addEllipses = TRUE, legend.title = "Label",
             title = "PCA - Multivariate Analysis")
dev.off()

cat("\nAnalysis complete!\n")

