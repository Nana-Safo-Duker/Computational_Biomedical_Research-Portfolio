# Install required R packages for gene expression prediction
# Run this script first to install all necessary packages

# List of required packages
required_packages <- c(
  "readr",        # Reading CSV files
  "dplyr",        # Data manipulation
  "ggplot2",      # Visualization
  "caret",        # Machine learning
  "randomForest", # Random Forest
  "xgboost",      # XGBoost
  "e1071",        # SVM
  "pROC",         # ROC curves
  "doParallel"    # Parallel processing (optional but recommended)
)

# Function to install packages if not already installed
install_if_missing <- function(packages) {
  new_packages <- packages[!(packages %in% installed.packages()[,"Package"])]
  if(length(new_packages)) {
    install.packages(new_packages, repos = "https://cran.rstudio.com/")
  }
  # Load all packages
  lapply(packages, library, character.only = TRUE)
}

# Install and load packages
cat("Installing and loading required packages...\n")
install_if_missing(required_packages)
cat("All packages installed and loaded successfully!\n")

