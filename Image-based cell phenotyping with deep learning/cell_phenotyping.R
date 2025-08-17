# Detailed statistical workflow for: Image-based cell phenotyping with deep learning

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
})

set.seed(222)
n <- 560
half <- floor(n / 2)
shift <- 1.15

synthesize <- function() {
  x_a <- matrix(rnorm(half * 24, mean = 0, sd = 1), nrow = half)
  x_b <- matrix(rnorm((n - half) * 24, mean = shift, sd = 1.05), nrow = n - half)
  X <- rbind(x_a, x_b)
  colnames(X) <- paste0("f", seq_len(24))
  colnames(X)[1:8] <- c(
    "area", "perimeter", "eccentricity", "texture_entropy",
    "intensity_mean", "intensity_std", "solidity", "aspect_ratio"
  )
  data.frame(X, label = c(rep(0L, half), rep(1L, n - half)))
}

df <- synthesize()
summary_tbl <- df %>%
  group_by(label) %>%
  summarise(n = n(), mean_area = mean(area), mean_texture = mean(texture_entropy), .groups = "drop")
print(summary_tbl)

p <- ggplot(df, aes(x = area, y = texture_entropy, color = factor(label))) +
  geom_point(alpha = 0.55, size = 1.6) +
  theme_minimal() +
  labs(
    title = "Cell phenotype morphology embedding (proxy)",
    color = "Phenotype",
    x = "Area",
    y = "Texture entropy"
  )
dir.create("assets", showWarnings = FALSE, recursive = TRUE)
ggsave("assets/overview_r.png", p, width = 8, height = 4.5, dpi = 150)
cat("R workflow complete for Image-based cell phenotyping with deep learning\n")
cat(sprintf("n=%d seed=222 mean label rate=%.3f\n", nrow(df), mean(df$label)))
