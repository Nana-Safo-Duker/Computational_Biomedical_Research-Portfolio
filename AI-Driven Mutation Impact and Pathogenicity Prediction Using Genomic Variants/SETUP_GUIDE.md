# Setup Guide

This guide will help you set up the Mutation Impact and Pathogenicity Prediction project on your local machine.

## Prerequisites

### Python Setup

- Python 3.8 or higher
- pip (Python package installer)
- Optional: Anaconda/Miniconda for environment management

### R Setup

- R version 4.0 or higher
- RStudio (recommended) or any R IDE
- Optional: Jupyter with R kernel for notebook support

### Git

- Git installed and configured
- GitHub account (for cloning and contributing)

## Step-by-Step Setup

### 1. Clone the Repository

```bash
# Clone the repository
git clone <repository-url>
cd "Mutation Impact and Pathogenicity Prediction"
```

### 2. Python Environment Setup

#### Option A: Using venv (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Option B: Using Conda

```bash
# Create conda environment
conda env create -f environment.yml

# Activate environment
conda activate mutation_prediction

# Install additional packages if needed
pip install -r requirements.txt
```

### 3. R Environment Setup

```r
# Install R packages
# Option 1: Using the provided script
source("R_requirements.R")

# Option 2: Manual installation
install.packages(c(
  "randomForest",
  "e1071",
  "xgboost",
  "caret",
  "pROC",
  "ggplot2",
  "dplyr",
  "readr",
  "tidyr"
))
```

### 4. Install Jupyter (Optional)

```bash
# Install Jupyter
pip install jupyter

# Install Jupyter R kernel (optional)
# In R:
install.packages("IRkernel")
IRkernel::installspec()
```

### 5. Verify Installation

#### Python

```bash
# Test Python installation
python -c "import pandas, numpy, sklearn; print('All packages installed successfully!')"

# Run a quick test
python src/main.py --help
```

#### R

```r
# Test R installation
library(randomForest)
library(e1071)
library(xgboost)
cat("All R packages installed successfully!\n")
```

## Project Structure

After setup, your project should have the following structure:

```
.
├── data/
│   └── genomics_data.csv
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_loader.R
│   ├── models.py
│   ├── models.R
│   ├── main.py
│   └── main.R
├── notebooks/
│   ├── mutation_prediction_python.ipynb
│   └── mutation_prediction_R.ipynb
├── models/          # Will contain saved models
├── results/         # Will contain results and visualizations
├── tests/           # Test files
├── docs/            # Documentation
├── requirements.txt
├── environment.yml
├── R_requirements.R
├── README.md
└── LICENSE
```

## Quick Start

### Python

```bash
# Run the main script
python src/main.py

# Or use Jupyter Notebook
jupyter notebook notebooks/mutation_prediction_python.ipynb
```

### R

```r
# Run the main R script
source("src/main.R")

# Or use RStudio to open the notebook
# File -> Open File -> notebooks/mutation_prediction_R.ipynb
```

## Common Issues and Solutions

### Issue: ModuleNotFoundError in Python

**Solution**: Make sure you've activated your virtual environment and installed all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Package not found in R

**Solution**: Install the missing package:
```r
install.packages("package_name")
```

### Issue: Jupyter kernel not found

**Solution**: Install the kernel:
```bash
# For Python
python -m ipykernel install --user --name=mutation_prediction

# For R
install.packages("IRkernel")
IRkernel::installspec()
```

### Issue: Data file not found

**Solution**: Ensure the `genomics_data.csv` file is in the `data/` directory:
```bash
ls data/genomics_data.csv
```

## Next Steps

1. Read the [README.md](README.md) for detailed usage instructions
2. Explore the [notebooks](notebooks/) for interactive analysis
3. Check [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute

## Getting Help

- Open an issue on GitHub for bugs or questions
- Check the documentation in the `docs/` directory
- Review the code comments for detailed explanations

## Troubleshooting

If you encounter any issues:

1. Check that all dependencies are installed
2. Verify your Python/R versions meet the requirements
3. Ensure you're in the correct directory
4. Check that the data file exists and is accessible
5. Review error messages carefully

For additional help, please open an issue on GitHub.


