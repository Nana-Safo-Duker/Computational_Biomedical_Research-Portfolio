# Quick Start Guide

## Prerequisites

- Python 3.8+ or R 4.0+
- Git

## Python Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Place Data File

Ensure `genomics_data.csv` is in the `data/` directory.

### 3. Run the Script

```bash
python scripts/python/tf_binding_prediction.py
```

Or use Jupyter Notebook:

```bash
jupyter notebook notebooks/python/tf_binding_prediction.ipynb
```

## R Quick Start

### 1. Install R Packages

```r
install.packages(c("tidyverse", "caret", "randomForest", "xgboost", 
                   "e1071", "neuralnet", "pROC", "ggplot2", 
                   "reshape2", "doParallel", "gridExtra"))
```

### 2. Place Data File

Ensure `genomics_data.csv` is in the `data/` directory.

### 3. Run the Script

```r
Rscript scripts/r/tf_binding_prediction.R
```

Or use R Markdown:

```r
# In RStudio or R
rmarkdown::render("notebooks/r/tf_binding_prediction.Rmd")
```

## Expected Output

After running the scripts, you should see:

1. **Trained models** in the `models/` directory
2. **Results and visualizations** in the `results/` directory:
   - Training history plots (CNN, LSTM)
   - Confusion matrices
   - ROC curves
   - Model comparison CSV

## Troubleshooting

### Data File Not Found

If you get an error about missing data file:
1. Check that `genomics_data.csv` is in the `data/` directory
2. Verify the file has the correct format (Sequences, Labels columns)

### Missing Dependencies

If you get import errors:
- Python: Run `pip install -r requirements.txt`
- R: Install missing packages using `install.packages("package_name")`

### Memory Issues

If you encounter memory issues:
- Reduce batch size for deep learning models
- Use a subset of data for SVM (already implemented)
- Close other applications to free up memory

## Next Steps

1. Explore the Jupyter notebooks for detailed analysis
2. Modify hyperparameters to improve model performance
3. Try different model architectures
4. Add your own sequences for prediction

## Getting Help

- Check the main [README.md](README.md) for detailed documentation
- Open an issue on GitHub for bugs or questions
- Review the code comments for implementation details

