# Detailed statistical workflow for: Machine Learning for Drug Target Identification in Bioinformatics

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
})

set.seed(333)
n <- 380
half <- floor(n / 2)
shift <- 0.55

synthesize <- function() {
  x_a <- matrix(rnorm(half * 16, mean = 0, sd = 1), nrow = half)
  x_b <- matrix(rnorm((n - half) * 16, mean = shift, sd = 1.05), nrow = n - half)
  X <- rbind(x_a, x_b)
  colnames(X) <- paste0("f", seq_len(16))
  colnames(X)[1:8] <- c(
    "binding_affinity", "sequence_conservation", "structure_score",
    "offtarget_risk", "assay_activity", "chemogenomic_hit", "ppi_degree", "go_similarity"
  )
  data.frame(X, label = c(rep(0L, half), rep(1L, n - half)))
}

df <- synthesize()
summary_tbl <- df %>%
  group_by(label) %>%
  summarise(
    n = n(),
    mean_binding = mean(binding_affinity),
    mean_conservation = mean(sequence_conservation),
    .groups = "drop"
  )
print(summary_tbl)

p <- ggplot(df, aes(x = binding_affinity, fill = factor(label))) +
  geom_histogram(bins = 25, alpha = 0.7, position = "identity") +
  theme_minimal() +
  labs(
    title = "Drug-target binding affinity by class",
    fill = "Target label",
    x = "Binding affinity score"
  )
dir.create("assets", showWarnings = FALSE, recursive = TRUE)
ggsave("assets/overview_r.png", p, width = 8, height = 4.5, dpi = 150)
cat("R workflow complete for Machine Learning for Drug Target Identification in Bioinformatics\n")
cat(sprintf("n=%d seed=333 mean label rate=%.3f\n", nrow(df), mean(df$label)))
