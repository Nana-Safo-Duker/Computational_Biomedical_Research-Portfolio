# Genomics Sequence Classification - Comprehensive Analysis

A comprehensive bioinformatics project analyzing genomics sequence data using statistical and machine learning approaches in both Python and R.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Analysis Components](#analysis-components)
- [Results](#results)
- [License](#license)
- [Contributing](#contributing)

## 🎯 Project Overview

This project performs comprehensive statistical and machine learning analysis on genomics sequence data for binary classification. The analysis includes:

- **Univariate, Bivariate, and Multivariate Analysis**: Statistical exploration of individual and combined features
- **Descriptive, Inferential, and Exploratory Statistics**: Comprehensive statistical summaries and hypothesis testing
- **Exploratory Data Analysis (EDA)**: Deep dive into data patterns, distributions, and relationships
- **Machine Learning Analysis**: Multiple ML algorithms for sequence classification

## 📊 Dataset

### Dataset Information

- **Name**: Genomics Sequence Classification Dataset
- **Type**: DNA sequence classification
- **Size**: 2,000 sequences
- **Features**: 
  - DNA sequences (variable length)
  - Binary labels (0 or 1)
- **Balance**: Approximately balanced (1013 class 0, 987 class 1)

### Dataset License

**Note**: This dataset is provided for educational and research purposes. Please refer to the original dataset source for specific licensing terms. If you are the dataset owner or have licensing information, please update this section accordingly.

**Recommended Attribution**: If using this dataset, please cite the original source and maintain appropriate attribution as required by the dataset license.

## 📁 Project Structure

```
genomics_data/
│
├── data/
│   └── genomics_data.csv          # Main dataset
│
├── notebooks/
│   ├── python/
│   │   ├── 1_univariate_bivariate_multivariate_analysis.ipynb
│   │   ├── 2_descriptive_inferential_exploratory.ipynb
│   │   ├── 3_comprehensive_eda.ipynb
│   │   └── 4_ml_analysis.ipynb
│   │
│   └── r/
│       ├── 1_univariate_bivariate_multivariate_analysis.Rmd
│       ├── 2_descriptive_inferential_exploratory.Rmd
│       ├── 3_comprehensive_eda.Rmd
│       └── 4_ml_analysis.Rmd
│
├── scripts/
│   ├── python/
│   │   ├── univariate_bivariate_multivariate.py
│   │   ├── descriptive_inferential_exploratory.py
│   │   ├── comprehensive_eda.py
│   │   └── ml_analysis.py
│   │
│   └── r/
│       ├── univariate_bivariate_multivariate.R
│       ├── descriptive_inferential_exploratory.R
│       ├── comprehensive_eda.R
│       └── ml_analysis.R
│
├── results/
│   └── [Generated visualizations and outputs]
│
├── docs/
│   └── [Documentation files]
│
├── .gitignore
├── requirements.txt
├── environment.yml
└── README.md
```

## ✨ Features

### Feature Engineering

The analysis extracts comprehensive features from DNA sequences:

- **Basic Features**:
  - Sequence length
  - GC content
  - AT content
  - Nucleotide frequencies (A, T, G, C)

- **K-mer Features**:
  - 2-mer frequencies (dinucleotides)
  - 3-mer frequencies (trinucleotides)

- **Complexity Features**:
  - Shannon entropy
  - GC skew

### Analysis Types

1. **Univariate Analysis**: Distribution analysis of individual features
2. **Bivariate Analysis**: Correlation and relationship analysis between feature pairs
3. **Multivariate Analysis**: PCA and feature importance analysis
4. **Descriptive Statistics**: Summary statistics, measures of central tendency and dispersion
5. **Inferential Statistics**: Hypothesis testing, confidence intervals, t-tests
6. **Exploratory Analysis**: Outlier detection, distribution analysis, correlation matrices
7. **Machine Learning**: Multiple classification algorithms with performance evaluation

## 🚀 Installation

### Python Environment

1. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### R Environment

1. **Install required R packages**:
```r
install.packages(c("dplyr", "ggplot2", "corrplot", "FactoMineR", 
                   "factoextra", "caret", "randomForest", "e1071", 
                   "pROC", "stringr", "moments"))
```

2. **Or use the R script**:
```r
source("install_r_packages.R")  # If created
```

## 📖 Usage

### Python Analysis

#### Using Notebooks:
```bash
jupyter notebook notebooks/python/
```

#### Using Scripts:
```bash
cd scripts/python
python univariate_bivariate_multivariate.py
python descriptive_inferential_exploratory.py
python comprehensive_eda.py
python ml_analysis.py
```

### R Analysis

#### Using R Markdown Notebooks:
```r
# In RStudio, open and knit the .Rmd files
```

#### Using R Scripts:
```r
# In R console
source("scripts/r/univariate_bivariate_multivariate.R")
source("scripts/r/descriptive_inferential_exploratory.R")
source("scripts/r/comprehensive_eda.R")
source("scripts/r/ml_analysis.R")
```

## 🔬 Analysis Components

### 1. Univariate, Bivariate, Multivariate Analysis

**Python**: `notebooks/python/1_univariate_bivariate_multivariate_analysis.ipynb`  
**R**: `notebooks/r/1_univariate_bivariate_multivariate_analysis.Rmd`

- Univariate distributions and statistics
- Correlation analysis
- PCA for dimensionality reduction
- Feature importance analysis

### 2. Descriptive, Inferential, Exploratory Statistics

**Python**: `notebooks/python/2_descriptive_inferential_exploratory.ipynb`  
**R**: `notebooks/r/2_descriptive_inferential_exploratory.Rmd`

- Descriptive statistics (mean, median, std, etc.)
- Inferential statistics (t-tests, Mann-Whitney U tests)
- Normality tests
- Confidence intervals
- Exploratory correlation and outlier analysis

### 3. Comprehensive EDA

**Python**: `notebooks/python/3_comprehensive_eda.ipynb`  
**R**: `notebooks/r/3_comprehensive_eda.Rmd`

- Data overview and quality checks
- Target variable analysis
- Feature statistics
- Correlation heatmaps
- Distribution visualizations
- Outlier detection

### 4. Machine Learning Analysis

**Python**: `notebooks/python/4_ml_analysis.ipynb`  
**R**: `notebooks/r/4_ml_analysis.Rmd`

**Algorithms Implemented**:
- Random Forest
- Gradient Boosting
- Support Vector Machine (SVM)
- Logistic Regression
- K-Nearest Neighbors (KNN)
- Naive Bayes
- AdaBoost

**Evaluation Metrics**:
- Accuracy
- Precision
- Recall
- F1-Score
- AUC-ROC
- Confusion Matrix
- Cross-validation scores

## 📈 Results

All results and visualizations are saved in the `results/` directory:

- Distribution plots
- Correlation heatmaps
- PCA visualizations
- Box plots by label
- Model comparison charts
- ROC curves
- Confusion matrices

## 📄 License

### Dataset License

**Important**: Please refer to the original dataset source for licensing information. This project assumes the dataset is used in accordance with its original license terms.

If you have specific licensing information, please update this section with:
- License type (e.g., CC BY 4.0, MIT, etc.)
- Attribution requirements
- Usage restrictions (if any)

### Project Code License

This project code is provided for educational and research purposes. Please ensure compliance with all applicable licenses when using this code.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📚 References

- Bioinformatics analysis techniques
- Statistical methods for genomics
- Machine learning for sequence classification
- DNA sequence feature extraction

## 👤 Author

[Your Name/Institution]

## 🙏 Acknowledgments

- Original dataset creators
- Open-source libraries and tools used
- Bioinformatics community

## 📧 Contact

For questions or suggestions, please open an issue in the repository.

---

**Last Updated**: 2024

**Version**: 1.0.0

