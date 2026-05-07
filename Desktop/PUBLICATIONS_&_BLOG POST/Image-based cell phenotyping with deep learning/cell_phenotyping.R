# Detailed statistical workflow for: Image-based cell phenotyping with deep learning

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
})

load_data <- function(path) {
  read.csv(path, stringsAsFactors = FALSE)
}

preprocess_data <- function(df, target_col) {
  num_cols <- names(df)[sapply(df, is.numeric)]
  for (col in num_cols) {
    df[[col]][is.na(df[[col]])] <- median(df[[col]], na.rm = TRUE)
  }
  list(
    X = df[, setdiff(names(df), target_col), drop = FALSE],
    y = df[[target_col]]
  )
}

summarize_features <- function(df) {
  df %>%
    summarise(across(where(is.numeric), list(mean = mean, sd = sd), na.rm = TRUE))
}

plot_distribution <- function(df, feature) {
  ggplot(df, aes(x = .data[[feature]])) +
    geom_histogram(bins = 30, fill = "steelblue", alpha = 0.8) +
    theme_minimal() +
    labs(title = paste("Distribution of", feature))
}

cat("R workflow template ready.\n")
