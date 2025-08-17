# Computational Approaches to Cancer Treatment Optimization
# Statistical Analysis Script
#
# Author: Cancer Research Team
# Date: 2024
# License: MIT
#
# This script performs statistical analysis of cancer treatment data,
# including survival analysis, differential expression, and biomarker identification.

# =============================================================================
# Libraries and Setup
# =============================================================================

# Load required libraries
suppressPackageStartupMessages({
  library(dplyr)
  library(survival)
  library(survminer)
  library(ggplot2)
  library(DESeq2)
  library(pheatmap)
  library(VennDiagram)
  library(corrplot)
  library(RColorBrewer)
})

# Set seed for reproducibility
set.seed(42)

# =============================================================================
# Data Preparation Functions
# =============================================================================

#' Generate synthetic cancer treatment data for demonstration
#'
#' @param n_samples Number of samples (patients)
#' @param n_genes Number of genes/features
#' @return List containing expression data, clinical data, and survival data
generate_synthetic_data <- function(n_samples = 100, n_genes = 1000) {
  
  # Generate synthetic gene expression data
  expression_data <- matrix(
    rnorm(n_samples * n_genes, mean = 10, sd = 2),
    nrow = n_samples,
    ncol = n_genes
  )
  colnames(expression_data) <- paste0("Gene_", 1:n_genes)
  rownames(expression_data) <- paste0("Patient_", 1:n_samples)
  
  # Generate clinical data
  clinical_data <- data.frame(
    patient_id = paste0("Patient_", 1:n_samples),
    age = round(rnorm(n_samples, mean = 60, sd = 15)),
    stage = sample(c("I", "II", "III", "IV"), n_samples, replace = TRUE,
                   prob = c(0.2, 0.3, 0.3, 0.2)),
    treatment_group = sample(c("Control", "Treatment"), n_samples, replace = TRUE),
    gender = sample(c("M", "F"), n_samples, replace = TRUE),
    mutational_burden = rpois(n_samples, lambda = 10)
  )
  
  # Generate survival data based on treatment and expression patterns
  # Treatment group and high expression of certain genes favor survival
  risk_score <- (
    0.3 * (clinical_data$treatment_group == "Control") +
    0.2 * (expression_data[, "Gene_1"] > quantile(expression_data[, "Gene_1"], 0.75)) +
    0.1 * (clinical_data$stage %in% c("III", "IV")) +
    rnorm(n_samples, mean = 0, sd = 0.2)
  )
  
  # Generate survival times (exponential distribution)
  baseline_hazard <- 0.05
  hazard_rate <- baseline_hazard * exp(risk_score)
  survival_time <- rexp(n_samples, rate = hazard_rate) * 365  # Convert to days
  
  # Generate censoring (30% censored)
  censor_indicator <- sample(c(0, 1), n_samples, replace = TRUE, prob = c(0.3, 0.7))
  survival_time[censor_indicator == 0] <- pmin(
    survival_time[censor_indicator == 0],
    runif(sum(censor_indicator == 0), 100, 365)
  )
  
  survival_data <- data.frame(
    patient_id = clinical_data$patient_id,
    time = survival_time,
    event = censor_indicator
  )
  
  return(list(
    expression = expression_data,
    clinical = clinical_data,
    survival = survival_data
  ))
}

#' Prepare data for DESeq2 analysis
#'
#' @param expression_matrix Gene expression count matrix
#' @param metadata Sample metadata
#' @param design_formula Design formula for differential expression
#' @return DESeqDataSet object
prepare_deseq2_data <- function(expression_matrix, metadata, design_formula) {
  
  # Ensure expression data are counts (round and convert to integers)
  count_data <- round(abs(expression_matrix))
  count_data <- count_data + 1  # Add pseudocount for log transformation
  
  # Create DESeqDataSet
  dds <- DESeqDataSetFromMatrix(
    countData = count_data,
    colData = metadata,
    design = design_formula
  )
  
  # Filter low count genes
  keep <- rowSums(counts(dds)) >= 10
  dds <- dds[keep, ]
  
  return(dds)
}

# =============================================================================
# Statistical Analysis Functions
# =============================================================================

#' Perform survival analysis comparing treatment groups
#'
#' @param survival_data Data frame with survival data
#' @param clinical_data Clinical metadata
#' @param group_variable Variable to group by (e.g., "treatment_group")
#' @return Survival fit object and plot
perform_survival_analysis <- function(survival_data, clinical_data, 
                                      group_variable = "treatment_group") {
  
  # Merge survival and clinical data
  surv_data <- merge(survival_data, clinical_data, by = "patient_id")
  
  # Create survival object
  surv_obj <- Surv(time = surv_data$time, event = surv_data$event)
  
  # Fit Cox proportional hazards model
  cox_formula <- as.formula(paste("surv_obj ~", group_variable))
  cox_model <- coxph(cox_formula, data = surv_data)
  
  # Fit Kaplan-Meier survival curves
  km_formula <- as.formula(paste("surv_obj ~", group_variable))
  km_fit <- survfit(km_formula, data = surv_data)
  
  # Perform log-rank test
  logrank_test <- survdiff(km_formula, data = surv_data)
  
  # Create survival plot
  p <- ggsurvplot(
    km_fit,
    data = surv_data,
    pval = TRUE,
    conf.int = TRUE,
    risk.table = TRUE,
    legend.title = group_variable,
    legend.labs = unique(surv_data[[group_variable]]),
    palette = c("#E7B800", "#2E9FDF"),
    ggtheme = theme_minimal()
  )
  
  results <- list(
    cox_model = cox_model,
    km_fit = km_fit,
    logrank_test = logrank_test,
    plot = p
  )
  
  return(results)
}

#' Identify differentially expressed genes
#'
#' @param dds DESeqDataSet object
#' @param contrast Vector specifying the contrast
#' @param alpha Adjusted p-value threshold
#' @return Data frame with differentially expressed genes
identify_differential_genes <- function(dds, contrast, alpha = 0.05) {
  
  # Run DESeq2 analysis
  dds <- DESeq(dds)
  
  # Get results
  results <- results(dds, contrast = contrast, alpha = alpha)
  
  # Convert to data frame and add gene names
  deg_df <- as.data.frame(results)
  deg_df$gene <- rownames(deg_df)
  rownames(deg_df) <- NULL
  
  # Filter significant genes
  significant_genes <- deg_df %>%
    filter(padj < alpha & !is.na(padj)) %>%
    arrange(padj)
  
  return(list(
    all_results = deg_df,
    significant = significant_genes
  ))
}

#' Calculate correlation matrix for gene expression
#'
#' @param expression_data Gene expression matrix
#' @param gene_list List of genes to analyze (optional)
#' @return Correlation matrix
calculate_gene_correlation <- function(expression_data, gene_list = NULL) {
  
  if (!is.null(gene_list)) {
    expression_data <- expression_data[, gene_list]
  }
  
  # Calculate correlation (using top 50 genes if too many)
  if (ncol(expression_data) > 50) {
    # Select genes with highest variance
    gene_vars <- apply(expression_data, 2, var)
    top_genes <- names(sort(gene_vars, decreasing = TRUE))[1:50]
    expression_data <- expression_data[, top_genes]
  }
  
  cor_matrix <- cor(expression_data, use = "pairwise.complete.obs")
  
  return(cor_matrix)
}

#' Perform statistical comparison between groups
#'
#' @param data Data frame with data
#' @param variable Variable to compare
#' @param group_variable Grouping variable
#' @param test_type Type of test ("t.test", "wilcox", "anova")
#' @return Test results
compare_groups <- function(data, variable, group_variable, test_type = "t.test") {
  
  groups <- unique(data[[group_variable]])
  
  if (length(groups) < 2) {
    stop("Need at least 2 groups for comparison")
  }
  
  group_data <- lapply(groups, function(g) {
    data[data[[group_variable]] == g, variable]
  })
  
  if (test_type == "t.test" && length(groups) == 2) {
    result <- t.test(group_data[[1]], group_data[[2]])
    return(list(
      test = "t-test",
      statistic = result$statistic,
      p_value = result$p.value,
      means = sapply(group_data, mean),
      sds = sapply(group_data, sd)
    ))
  } else if (test_type == "wilcox" && length(groups) == 2) {
    result <- wilcox.test(group_data[[1]], group_data[[2]])
    return(list(
      test = "Wilcoxon rank-sum test",
      statistic = result$statistic,
      p_value = result$p.value,
      medians = sapply(group_data, median)
    ))
  } else if (test_type == "anova") {
    formula_str <- paste(variable, "~", group_variable)
    aov_result <- aov(as.formula(formula_str), data = data)
    return(summary(aov_result))
  }
}

# =============================================================================
# Visualization Functions
# =============================================================================

#' Create heatmap of gene expression
#'
#' @param expression_data Expression matrix
#' @param metadata Sample metadata
#' @param top_n Number of top variable genes
#' @param annotation_vars Variables to annotate
#' @return Heatmap plot
create_expression_heatmap <- function(expression_data, metadata, 
                                       top_n = 50, annotation_vars = NULL) {
  
  # Select top variable genes
  gene_vars <- apply(expression_data, 2, var)
  top_genes <- names(sort(gene_vars, decreasing = TRUE))[1:top_n]
  expression_subset <- expression_data[, top_genes]
  
  # Prepare annotation
  annotation_df <- NULL
  if (!is.null(annotation_vars)) {
    annotation_df <- metadata[, annotation_vars, drop = FALSE]
    rownames(annotation_df) <- metadata$patient_id
  }
  
  # Create heatmap
  pheatmap(
    expression_subset,
    annotation_col = annotation_df,
    scale = "row",
    clustering_distance_rows = "correlation",
    clustering_distance_cols = "correlation",
    color = colorRampPalette(c("blue", "white", "red"))(100),
    show_rownames = FALSE,
    show_colnames = FALSE,
    main = paste("Top", top_n, "Variable Genes")
  )
}

#' Create volcano plot for differential expression
#'
#' @param deg_results Differential expression results
#' @param pvalue_threshold P-value threshold for significance
#' @param foldchange_threshold Log2 fold change threshold
#' @return ggplot object
create_volcano_plot <- function(deg_results, pvalue_threshold = 0.05, 
                                foldchange_threshold = 1) {
  
  deg_results$significant <- (
    deg_results$padj < pvalue_threshold & 
    abs(deg_results$log2FoldChange) > foldchange_threshold &
    !is.na(deg_results$padj)
  )
  
  p <- ggplot(deg_results, aes(x = log2FoldChange, y = -log10(padj))) +
    geom_point(aes(color = significant), alpha = 0.6, size = 2) +
    scale_color_manual(values = c("grey", "red")) +
    geom_hline(yintercept = -log10(pvalue_threshold), 
               linetype = "dashed", color = "blue") +
    geom_vline(xintercept = c(-foldchange_threshold, foldchange_threshold), 
               linetype = "dashed", color = "blue") +
    labs(
      x = "Log2 Fold Change",
      y = "-Log10 Adjusted P-value",
      title = "Volcano Plot: Differential Gene Expression"
    ) +
    theme_minimal() +
    theme(legend.position = "none")
  
  return(p)
}

# =============================================================================
# Main Analysis Pipeline
# =============================================================================

main <- function() {
  
  cat("=" %&% strrep("=", 59) %&% "\n")
  cat("Computational Cancer Treatment Optimization - Statistical Analysis\n")
  cat("=" %&% strrep("=", 59) %&% "\n\n")
  
  # Step 1: Generate synthetic data
  cat("[1] Generating synthetic cancer treatment data...\n")
  data <- generate_synthetic_data(n_samples = 100, n_genes = 1000)
  cat(sprintf("Generated data: %d samples, %d genes\n\n", 
              nrow(data$expression), ncol(data$expression)))
  
  # Step 2: Descriptive statistics
  cat("[2] Computing descriptive statistics...\n")
  cat("Survival time statistics:\n")
  cat(sprintf("  Mean: %.2f days\n", mean(data$survival$time)))
  cat(sprintf("  Median: %.2f days\n", median(data$survival$time)))
  cat(sprintf("  Event rate: %.2f%%\n\n", mean(data$survival$event) * 100))
  
  # Step 3: Survival analysis
  cat("[3] Performing survival analysis...\n")
  surv_results <- perform_survival_analysis(
    data$survival, 
    data$clinical, 
    "treatment_group"
  )
  
  # Print Cox model summary
  cat("\nCox Proportional Hazards Model:\n")
  print(summary(surv_results$cox_model))
  
  # Print log-rank test
  cat("\nLog-rank test results:\n")
  print(surv_results$logrank_test)
  
  # Save survival plot
  pdf("survival_analysis.pdf", width = 10, height = 8)
  print(surv_results$plot)
  dev.off()
  cat("\nSurvival plot saved to 'survival_analysis.pdf'\n\n")
  
  # Step 4: Group comparisons
  cat("[4] Performing statistical comparisons between treatment groups...\n")
  age_comparison <- compare_groups(
    data$clinical,
    "age",
    "treatment_group",
    "t.test"
  )
  cat("\nAge comparison (t-test):\n")
  cat(sprintf("  Control mean: %.2f (SD: %.2f)\n", 
              age_comparison$means[1], age_comparison$sds[1]))
  cat(sprintf("  Treatment mean: %.2f (SD: %.2f)\n", 
              age_comparison$means[2], age_comparison$sds[2]))
  cat(sprintf("  t-statistic: %.3f\n", age_comparison$statistic))
  cat(sprintf("  p-value: %.4f\n\n", age_comparison$p_value))
  
  mutational_comparison <- compare_groups(
    data$clinical,
    "mutational_burden",
    "treatment_group",
    "wilcox"
  )
  cat("Mutational burden comparison (Wilcoxon test):\n")
  cat(sprintf("  p-value: %.4f\n\n", mutational_comparison$p_value))
  
  # Step 5: Differential expression analysis
  cat("[5] Performing differential expression analysis...\n")
  
  # Prepare metadata for DESeq2
  metadata <- data$clinical
  metadata$treatment <- factor(metadata$treatment_group)
  rownames(metadata) <- metadata$patient_id
  
  # Align expression data with metadata
  expression_aligned <- data$expression[metadata$patient_id, ]
  
  # Create DESeq2 object
  dds <- prepare_deseq2_data(
    expression_aligned,
    metadata,
    ~ treatment
  )
  
  # Identify differential genes
  contrast <- c("treatment", "Treatment", "Control")
  deg_results <- identify_differential_genes(dds, contrast, alpha = 0.05)
  
  cat(sprintf("\nDifferential expression results:\n"))
  cat(sprintf("  Total genes analyzed: %d\n", nrow(deg_results$all_results)))
  cat(sprintf("  Significantly differentially expressed: %d\n", 
              nrow(deg_results$significant)))
  cat(sprintf("  Upregulated (log2FC > 1): %d\n", 
              sum(deg_results$significant$log2FoldChange > 1)))
  cat(sprintf("  Downregulated (log2FC < -1): %d\n", 
              sum(deg_results$significant$log2FoldChange < -1)))
  
  # Create volcano plot
  volcano_plot <- create_volcano_plot(deg_results$all_results)
  ggsave("volcano_plot.png", volcano_plot, width = 10, height = 8, dpi = 300)
  cat("\nVolcano plot saved to 'volcano_plot.png'\n\n")
  
  # Step 6: Correlation analysis
  cat("[6] Calculating gene expression correlations...\n")
  if (nrow(deg_results$significant) > 0) {
    top_deg_genes <- deg_results$significant$gene[1:min(30, nrow(deg_results$significant))]
    cor_matrix <- calculate_gene_correlation(data$expression, top_deg_genes)
    
    png("correlation_heatmap.png", width = 1200, height = 1200, res = 300)
    corrplot(cor_matrix, method = "color", type = "upper", 
             order = "hclust", tl.cex = 0.6, tl.col = "black")
    dev.off()
    cat("Correlation heatmap saved to 'correlation_heatmap.png'\n\n")
  }
  
  # Step 7: Expression heatmap
  cat("[7] Creating expression heatmap...\n")
  png("expression_heatmap.png", width = 1200, height = 800, res = 300)
  create_expression_heatmap(
    data$expression,
    data$clinical,
    top_n = 50,
    annotation_vars = c("treatment_group", "stage")
  )
  dev.off()
  cat("Expression heatmap saved to 'expression_heatmap.png'\n\n")
  
  cat("=" %&% strrep("=", 59) %&% "\n")
  cat("Statistical analysis pipeline completed successfully!\n")
  cat("=" %&% strrep("=", 59) %&% "\n")
  
  return(list(
    data = data,
    survival_results = surv_results,
    deg_results = deg_results
  ))
}

# Helper function for string concatenation (since %+% doesn't exist in base R)
`%&%` <- function(a, b) paste0(a, b)

# Run main analysis if script is executed directly
if (!interactive()) {
  results <- main()
}
