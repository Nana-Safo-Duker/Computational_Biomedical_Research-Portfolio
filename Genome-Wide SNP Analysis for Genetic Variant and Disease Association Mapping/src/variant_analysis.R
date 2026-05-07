# Comprehensive Variant Analysis Script in R
#
# This script performs comprehensive analysis of genetic variants including:
# - Statistical summaries
# - Visualization
# - Disease association analysis
#
# Author: Genetic Variants Analysis Project
# Date: 2025

library(ggplot2)
library(dplyr)  # Note: dplyr masks some base/stats functions (filter, lag, etc.) - this is normal
library(gridExtra)
library(corrplot)

source("src/variant_identification.R")

#' Create summary statistics for variant analysis
#' @param results_df Data frame with variant analysis results
#' @return Data frame with summary statistics
create_summary_statistics <- function(results_df) {
  summary_data <- data.frame(
    Metric = c(
      "Total Sequences",
      "Sequences with SNPs",
      "Sequences with Indels",
      "Sequences with Structural Variants",
      "Average SNPs per Sequence",
      "Average Indels per Sequence",
      "Average Structural Variants per Sequence",
      "Max SNPs in a Sequence",
      "Max Indels in a Sequence",
      "Max Structural Variants in a Sequence"
    ),
    Value = c(
      nrow(results_df),
      sum(results_df$num_snps > 0),
      sum(results_df$num_indels > 0),
      sum(results_df$num_structural_variants > 0),
      mean(results_df$num_snps),
      mean(results_df$num_indels),
      mean(results_df$num_structural_variants),
      max(results_df$num_snps),
      max(results_df$num_indels),
      max(results_df$num_structural_variants)
    )
  )
  
  return(summary_data)
}

#' Analyze association between variants and disease labels
#' @param results_df Data frame with variant analysis results
#' @return Summary statistics by disease label
analyze_disease_association <- function(results_df) {
  disease_assoc <- results_df %>%
    group_by(label) %>%
    summarise(
      mean_snps = mean(num_snps),
      sd_snps = sd(num_snps),
      median_snps = median(num_snps),
      mean_indels = mean(num_indels),
      sd_indels = sd(num_indels),
      median_indels = median(num_indels),
      mean_structural = mean(num_structural_variants),
      sd_structural = sd(num_structural_variants),
      median_structural = median(num_structural_variants),
      mean_total = mean(total_variants),
      sd_total = sd(total_variants),
      median_total = median(total_variants),
      .groups = 'drop'
    )
  
  return(disease_assoc)
}

#' Create visualization plots for variant analysis
#' @param results_df Data frame with variant analysis results
#' @param output_dir Directory to save plots
create_visualizations <- function(results_df, output_dir = "results") {
  dir.create(output_dir, showWarnings = FALSE)
  
  # 1. Distribution plots
  p1 <- ggplot(results_df, aes(x = num_snps)) +
    geom_histogram(bins = 30, fill = "steelblue", alpha = 0.7, color = "black") +
    labs(title = "Distribution of SNPs per Sequence",
         x = "Number of SNPs", y = "Frequency") +
    theme_minimal() +
    theme(plot.title = element_text(size = 14, face = "bold"))
  
  p2 <- ggplot(results_df, aes(x = num_indels)) +
    geom_histogram(bins = 30, fill = "orange", alpha = 0.7, color = "black") +
    labs(title = "Distribution of Indels per Sequence",
         x = "Number of Indels", y = "Frequency") +
    theme_minimal() +
    theme(plot.title = element_text(size = 14, face = "bold"))
  
  p3 <- ggplot(results_df, aes(x = num_structural_variants)) +
    geom_histogram(bins = 30, fill = "green", alpha = 0.7, color = "black") +
    labs(title = "Distribution of Structural Variants per Sequence",
         x = "Number of Structural Variants", y = "Frequency") +
    theme_minimal() +
    theme(plot.title = element_text(size = 14, face = "bold"))
  
  p4 <- ggplot(results_df, aes(x = total_variants)) +
    geom_histogram(bins = 30, fill = "red", alpha = 0.7, color = "black") +
    labs(title = "Distribution of Total Variants per Sequence",
         x = "Number of Total Variants", y = "Frequency") +
    theme_minimal() +
    theme(plot.title = element_text(size = 14, face = "bold"))
  
  ggsave(filename = file.path(output_dir, "variant_distributions.png"),
         plot = grid.arrange(p1, p2, p3, p4, ncol = 2, nrow = 2),
         width = 15, height = 12, dpi = 300)
  
  # 2. Disease association box plots
  results_df$label_factor <- factor(results_df$label, levels = c(0, 1), 
                                     labels = c("Control", "Disease"))
  
  p5 <- ggplot(results_df, aes(x = label_factor, y = num_snps, fill = label_factor)) +
    geom_boxplot() +
    labs(title = "SNPs by Disease Label",
         x = "Disease Label", y = "Number of SNPs") +
    theme_minimal() +
    theme(plot.title = element_text(size = 14, face = "bold"),
          legend.position = "none")
  
  p6 <- ggplot(results_df, aes(x = label_factor, y = num_indels, fill = label_factor)) +
    geom_boxplot() +
    labs(title = "Indels by Disease Label",
         x = "Disease Label", y = "Number of Indels") +
    theme_minimal() +
    theme(plot.title = element_text(size = 14, face = "bold"),
          legend.position = "none")
  
  p7 <- ggplot(results_df, aes(x = label_factor, y = num_structural_variants, fill = label_factor)) +
    geom_boxplot() +
    labs(title = "Structural Variants by Disease Label",
         x = "Disease Label", y = "Number of Structural Variants") +
    theme_minimal() +
    theme(plot.title = element_text(size = 14, face = "bold"),
          legend.position = "none")
  
  p8 <- ggplot(results_df, aes(x = label_factor, y = total_variants, fill = label_factor)) +
    geom_boxplot() +
    labs(title = "Total Variants by Disease Label",
         x = "Disease Label", y = "Number of Total Variants") +
    theme_minimal() +
    theme(plot.title = element_text(size = 14, face = "bold"),
          legend.position = "none")
  
  ggsave(filename = file.path(output_dir, "disease_association_analysis.png"),
         plot = grid.arrange(p5, p6, p7, p8, ncol = 2, nrow = 2),
         width = 15, height = 12, dpi = 300)
  
  # 3. Correlation heatmap
  correlation_cols <- c("num_snps", "num_indels", "num_structural_variants", "total_variants", "label")
  corr_matrix <- cor(results_df[, correlation_cols])
  
  png(filename = file.path(output_dir, "correlation_heatmap.png"),
      width = 10, height = 8, units = "in", res = 300)
  corrplot(corr_matrix, method = "color", type = "upper", 
           order = "hclust", tl.cex = 0.8, tl.col = "black",
           addCoef.col = "black", number.cex = 0.7)
  title("Variant Type Correlation Matrix", cex.main = 1.5, font.main = 2)
  dev.off()
  
  cat("Visualizations saved to", output_dir, "\n")
}

#' Main analysis pipeline
main <- function() {
  cat("============================================================\n")
  cat("Genetic Variant Analysis Pipeline\n")
  cat("============================================================\n\n")
  
  # Process data
  data_file <- "data/genomics_data.csv"
  output_file <- "results/variant_analysis_results_R.csv"
  
  cat("1. Processing genomics data and identifying variants...\n")
  results_df <- process_genomics_data(data_file, output_file)
  
  cat("\n2. Generating summary statistics...\n")
  summary_stats <- create_summary_statistics(results_df)
  cat("\nSummary Statistics:\n")
  print(summary_stats)
  write.csv(summary_stats, "results/summary_statistics_R.csv", row.names = FALSE)
  
  cat("\n3. Analyzing disease associations...\n")
  disease_assoc <- analyze_disease_association(results_df)
  cat("\nDisease Association Analysis:\n")
  print(disease_assoc)
  write.csv(disease_assoc, "results/disease_association_analysis_R.csv", row.names = FALSE)
  
  # Statistical test
  control_variants <- results_df$total_variants[results_df$label == 0]
  disease_variants <- results_df$total_variants[results_df$label == 1]
  t_test <- t.test(control_variants, disease_variants)
  
  cat("\nT-test results (Control vs Disease):\n")
  cat("  T-statistic:", t_test$statistic, "\n")
  cat("  P-value:", t_test$p.value, "\n")
  cat("  Significant difference:", ifelse(t_test$p.value < 0.05, "Yes", "No"), "(α=0.05)\n")
  
  cat("\n4. Creating visualizations...\n")
  create_visualizations(results_df, "results")
  
  cat("\n============================================================\n")
  cat("Analysis Complete!\n")
  cat("============================================================\n")
  cat("\nResults saved to:\n")
  cat("  - Variant analysis:", output_file, "\n")
  cat("  - Summary statistics: results/summary_statistics_R.csv\n")
  cat("  - Disease association: results/disease_association_analysis_R.csv\n")
  cat("  - Visualizations: results/*.png\n")
}

# Run main function if script is executed directly
if (!interactive()) {
  main()
}

