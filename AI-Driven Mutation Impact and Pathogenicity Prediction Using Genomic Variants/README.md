# Mutation Impact and Pathogenicity Prediction

A comprehensive machine learning project for predicting the functional impact of mutations (missense, nonsense, regulatory) in genomic sequences. This project provides implementations in both Python and R, with multiple machine learning models and ensemble methods.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Dataset](#dataset)
- [Models](#models)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)
- [References](#references)

## Overview

This project aims to predict the functional impact of mutations in DNA sequences using machine learning techniques. The models can classify mutations as either pathogenic (high functional impact) or benign (low functional impact), which is crucial for understanding disease mechanisms and developing precision medicine approaches.

### Key Objectives

1. **Predict Functional Impact**: Classify mutations as pathogenic or benign
2. **Multiple Model Comparison**: Evaluate various ML algorithms
3. **Ensemble Methods**: Combine multiple models for improved accuracy
4. **Comprehensive Analysis**: Provide detailed evaluation metrics and visualizations

## Features

- **Multiple Encoding Methods**: One-hot encoding, K-mer frequency encoding, and numerical encoding
- **Various ML Models**: Random Forest, SVM, Logistic Regression, Gradient Boosting, Neural Networks, XGBoost
- **Ensemble Learning**: Voting and averaging ensemble methods
- **Comprehensive Evaluation**: Accuracy, Precision, Recall, F1-score, ROC-AUC metrics
- **Dual Implementation**: Both Python and R implementations
- **Jupyter Notebooks**: Interactive analysis notebooks for both languages
- **Model Persistence**: Save and load trained models

## Project Structure

```
.
├── data/
│   └── genomics_data.csv          # Dataset (CSV format)
├── src/
│   ├── data_loader.py             # Python data loading and preprocessing
│   ├── data_loader.R              # R data loading and preprocessing
│   ├── models.py                  # Python ML models
│   ├── models.R                   # R ML models
│   ├── main.py                    # Python main script
│   └── main.R                     # R main script
├── notebooks/
│   ├── mutation_prediction_python.ipynb  # Python analysis notebook
│   └── mutation_prediction_R.ipynb       # R analysis notebook
├── examples/
│   └── quick_start.py            # Quick start example script
├── models/                        # Saved trained models
├── results/                       # Results and visualizations
├── docs/                          # Documentation
├── tests/                         # Unit tests
├── requirements.txt               # Python dependencies
├── environment.yml                # Conda environment
├── R_requirements.R               # R package dependencies
├── .gitignore                     # Git ignore file
└── README.md                      # This file
```

## Installation

### Python Setup

1. **Clone the repository**:
```bash
git clone <repository-url>
cd "Mutation Impact and Pathogenicity Prediction"
```

2. **Create a virtual environment** (recommended):
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda env create -f environment.yml
conda activate mutation_prediction
```

3. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

### R Setup

1. **Install R packages**:
```r
# Run the R requirements script
source("R_requirements.R")

# Or install manually
install.packages(c("randomForest", "e1071", "xgboost", "caret", "pROC", "ggplot2", "dplyr", "readr"))
```

2. **Install Jupyter Kernel for R** (optional, for R notebooks):
```r
install.packages("IRkernel")
IRkernel::installspec()
```

## Usage

### Python

#### Command Line Interface

```bash
# Basic usage with default parameters
python src/main.py

# With custom parameters
python src/main.py --data_path data/genomics_data.csv --encoding onehot --model random_forest --test_size 0.2

# Available options:
# --data_path: Path to CSV file
# --encoding: onehot, kmer, or numerical
# --model: random_forest, svm, logistic, gradient_boosting, neural_network, or ensemble
# --test_size: Test set proportion (default: 0.2)
# --random_state: Random seed (default: 42)
```

#### Jupyter Notebook

```bash
# Start Jupyter Notebook
jupyter notebook

# Open notebooks/mutation_prediction_python.ipynb
```

#### Python Script Usage

```python
from src.data_loader import GenomicsDataLoader
from src.models import MutationPredictor

# Load and prepare data
loader = GenomicsDataLoader(data_path="data/genomics_data.csv")
X_train, X_test, y_train, y_test = loader.prepare_data(
    encoding_method='onehot',
    test_size=0.2,
    random_state=42
)

# Train model
model = MutationPredictor(model_type='random_forest')
model.train(X_train, y_train)

# Evaluate model
metrics = model.evaluate(X_test, y_test)

# Make predictions
predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)

# Save model
model.save_model('models/my_model.pkl')
```

#### Quick Start Example

```bash
# Run the quick start example
python examples/quick_start.py
```

### R

#### Command Line Interface

```r
# Run main R script
Rscript src/main.R

# With custom parameters
Rscript src/main.R --data_path data/genomics_data.csv --encoding onehot --model random_forest
```

#### R Script Usage

```r
# Source required modules
source("src/data_loader.R")
source("src/models.R")

# Load and prepare data
data_split <- prepare_data(
    data_path = "data/genomics_data.csv",
    encoding_method = "onehot",
    test_size = 0.2,
    random_state = 42
)

# Train model
model <- train_random_forest(data_split$X_train, data_split$y_train)

# Evaluate model
metrics <- evaluate_model(model, data_split$X_test, data_split$y_test, "random_forest")

# Make predictions
predictions <- predict(model, data_split$X_test)

# Save model
save_model_r(model, "models/my_model.rds")
```

## Dataset

### Dataset Description

The dataset contains DNA sequences and their corresponding labels (0 = benign, 1 = pathogenic). Each sequence represents a genomic region that may contain mutations affecting protein function or regulatory elements.

### Dataset Format

- **Sequences**: DNA sequences (A, T, G, C nucleotides)
- **Labels**: Binary classification (0 = benign, 1 = pathogenic)

### Dataset License

**Important**: This dataset is provided for research and educational purposes. The original dataset's license should be referenced here. If you are using a publicly available dataset, please include:

- Dataset source and citation
- License type (e.g., CC0, CC BY, etc.)
- Any usage restrictions
- Original dataset URL

**Example License Reference**:
```
Dataset: Genomics Mutation Dataset
Source: [Original Source]
License: [License Type - e.g., CC0 1.0 Universal Public Domain Dedication]
Citation: [If applicable]
URL: [Dataset URL]
```

**Note**: Please ensure you have the right to use the dataset and comply with the original dataset's license terms. If this is a custom dataset, please specify the license under which it is released.

### Data Preprocessing

The project includes several encoding methods:

1. **One-hot Encoding**: Each nucleotide (A, T, G, C) is encoded as a 4-dimensional binary vector
2. **K-mer Encoding**: Extracts k-mer frequencies from sequences (default k=3)
3. **Numerical Encoding**: Simple numerical mapping (A=1, T=2, G=3, C=4)

## Models

### Available Models

1. **Random Forest**: Ensemble of decision trees
2. **Support Vector Machine (SVM)**: Kernel-based classifier
3. **Logistic Regression**: Linear classifier with logistic function
4. **Gradient Boosting**: Sequential ensemble of weak learners
5. **Neural Network**: Multi-layer perceptron
6. **XGBoost**: Optimized gradient boosting framework
7. **Ensemble**: Combination of multiple models

### Model Evaluation Metrics

- **Accuracy**: Overall classification accuracy
- **Precision**: Ratio of true positives to predicted positives
- **Recall**: Ratio of true positives to actual positives
- **F1-Score**: Harmonic mean of precision and recall
- **ROC-AUC**: Area under the ROC curve

## Results

### Model Performance

The models are evaluated on a held-out test set. Results include:

- Classification reports
- Confusion matrices
- ROC curves (if applicable)
- Feature importance (for tree-based models)

### Expected Performance

Performance may vary based on:
- Dataset characteristics
- Encoding method
- Model hyperparameters
- Class distribution

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards

- Follow PEP 8 for Python code
- Follow Google R Style Guide for R code
- Add docstrings/documentation for functions
- Include unit tests for new features

## License

This project is licensed under the MIT License - see the LICENSE file for details.

**Dataset License**: Please refer to the original dataset's license for data usage terms.

## References

### Machine Learning in Genomics

1. Angermueller, C., Pärnamaa, T., Parts, L., & Stegle, O. (2016). Deep learning for computational biology. *Molecular systems biology*, 12(7), 878.

2. Zou, J., Huss, M., Abid, A., Mohammadi, P., Torkamani, A., & Telenti, A. (2019). A primer on deep learning in genomics. *Nature genetics*, 51(1), 12-18.

### Mutation Prediction

1. Adzhubei, I., Jordan, D. M., & Sunyaev, S. R. (2013). Predicting functional effect of human missense mutations using PolyPhen-2. *Current protocols in human genetics*, 76(1), 7-20.

2. Kircher, M., Witten, D. M., Jain, P., O'Roak, B. J., Cooper, G. M., & Shendure, J. (2014). A general framework for estimating the relative pathogenicity of human genetic variants. *Nature genetics*, 46(3), 310-315.

### Tools and Libraries

- **scikit-learn**: Machine learning library for Python
- **XGBoost**: Gradient boosting framework
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **R**: Statistical computing and graphics
- **caret**: Classification and regression training for R

## Acknowledgments

- Thanks to the open-source community for excellent tools and libraries
- Dataset providers and contributors
- Researchers in computational biology and precision medicine

## Contact

For questions, issues, or suggestions, please open an issue on GitHub or contact the project maintainers.

---

**Disclaimer**: This tool is for research and educational purposes only. It should not be used for clinical decision-making without proper validation and regulatory approval.

