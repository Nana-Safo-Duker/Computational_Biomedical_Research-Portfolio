# Detailed statistical workflow for: AI-cancer target identification-drug-discovery

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
})

set.seed(111)
n <- 420
half <- floor(n / 2)
shift <- 0.85

synthesize <- function() {
  x_a <- matrix(rnorm(half * 18, mean = 0, sd = 1), nrow = half)
  x_b <- matrix(rnorm((n - half) * 18, mean = shift, sd = 1.05), nrow = n - half)
  X <- rbind(x_a, x_b)
  colnames(X) <- paste0("f", seq_len(18))
  colnames(X)[1:8] <- c(
    "expression_z", "mutation_burden", "druggability", "network_centrality",
    "pathway_enrichment", "essentiality", "tissue_specificity", "literature_score"
  )
  data.frame(X, label = c(rep(0L, half), rep(1L, n - half)))
}

df <- synthesize()
summary_tbl <- df %>%
  group_by(label) %>%
  summarise(n = n(), mean_expression = mean(expression_z), .groups = "drop")
print(summary_tbl)

p <- ggplot(df, aes(x = expression_z, fill = factor(label))) +
  geom_density(alpha = 0.5) +
  theme_minimal() +
  labs(
    title = "Cancer target priority features",
    fill = "Priority label",
    x = "Expression z-score"
  )
dir.create("assets", showWarnings = FALSE, recursive = TRUE)
ggsave("assets/overview_r.png", p, width = 8, height = 4.5, dpi = 150)
cat("R workflow complete for AI-cancer target identification-drug-discovery\n")
cat(sprintf("n=%d seed=111 mean label rate=%.3f\n", nrow(df), mean(df$label)))
