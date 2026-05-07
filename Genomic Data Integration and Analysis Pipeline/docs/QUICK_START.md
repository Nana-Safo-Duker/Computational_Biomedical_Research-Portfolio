# Quick Start Guide

## Python Quick Start

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run analysis scripts**:
```bash
cd scripts/python
python univariate_bivariate_multivariate.py
python descriptive_inferential_exploratory.py
python comprehensive_eda.py
python ml_analysis.py
```

3. **Or use Jupyter notebooks**:
```bash
jupyter notebook notebooks/python/
```

## R Quick Start

1. **Install R packages** (run in R console):
```r
install.packages(c("dplyr", "ggplot2", "corrplot", "FactoMineR", 
                   "factoextra", "caret", "randomForest", "e1071", 
                   "pROC", "stringr", "moments"))
```

2. **Run analysis scripts**:
```r
# In R console, set working directory to project root
setwd("path/to/genomics_data")
source("scripts/r/univariate_bivariate_multivariate.R")
source("scripts/r/descriptive_inferential_exploratory.R")
source("scripts/r/comprehensive_eda.R")
source("scripts/r/ml_analysis.R")
```

3. **Or use R Markdown notebooks**:
- Open `.Rmd` files in RStudio
- Click "Knit" to render

## Expected Outputs

All results and visualizations will be saved in the `results/` directory:
- Statistical summaries
- Distribution plots
- Correlation heatmaps
- PCA visualizations
- Model comparison charts
- ROC curves

