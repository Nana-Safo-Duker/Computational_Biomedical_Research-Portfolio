# R Package Dependencies for Mutation Impact Prediction

# Install required packages if not already installed
install_if_missing <- function(packages) {
  new_packages <- packages[!(packages %in% installed.packages()[,"Package"])]
  if(length(new_packages)) {
    install.packages(new_packages, repos = "https://cran.rstudio.com/")
  }
}

# Required packages
required_packages <- c(
  "randomForest",      # Random Forest
  "e1071",            # SVM
  "glmnet",           # Logistic Regression
  "xgboost",          # XGBoost
  "caret",            # Classification and Regression Training
  "pROC",             # ROC curves
  "ggplot2",          # Visualization
  "dplyr",            # Data manipulation
  "readr"             # Reading CSV files
)

# Install packages
cat("Installing required R packages...\n")
install_if_missing(required_packages)

cat("All required packages are installed!\n")


