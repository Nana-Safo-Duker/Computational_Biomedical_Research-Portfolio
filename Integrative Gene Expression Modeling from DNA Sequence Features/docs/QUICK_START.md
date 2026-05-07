# Quick Start Guide

## Prerequisites

- Python 3.8+ or R 4.0+
- Git (for cloning the repository)

## Python Setup

### 1. Install Dependencies

```bash
# Using pip
pip install -r requirements.txt

# Or using conda
conda env create -f environment.yml
conda activate gene_expression_prediction
```

### 2. Run the Analysis

#### Option A: Jupyter Notebook
```bash
jupyter notebook notebooks/gene_expression_prediction.ipynb
```

#### Option B: Python Script
```bash
python scripts/gene_expression_prediction.py
```

## R Setup

### 1. Install R Packages

```bash
Rscript scripts/install_R_packages.R
```

### 2. Run the Analysis

#### Option A: R Script
```bash
Rscript scripts/gene_expression_prediction.R
```

#### Option B: R Markdown (Render to HTML)
```r
# In R or RStudio
rmarkdown::render("notebooks/gene_expression_prediction.Rmd")
```

## Expected Output

After running the scripts, you should see:

1. **Models trained** in the `models/` directory
2. **Visualizations** in the `results/` directory
3. **Performance metrics** printed to console

## Next Steps

- Explore the notebooks for detailed analysis
- Modify hyperparameters in the scripts
- Try different k-mer sizes
- Experiment with additional features

## Troubleshooting

### Python Issues

- **Import errors**: Make sure all packages are installed: `pip install -r requirements.txt`
- **Memory issues**: Reduce the dataset size or use a machine with more RAM
- **Path errors**: Run scripts from the project root directory

### R Issues

- **Package installation**: Run `install_R_packages.R` first
- **XGBoost errors**: Make sure XGBoost is properly installed
- **Memory issues**: Consider using a subset of the data for testing

## Getting Help

- Check the README.md for detailed documentation
- Review the code comments in the scripts
- Open an issue on GitHub if you encounter problems



