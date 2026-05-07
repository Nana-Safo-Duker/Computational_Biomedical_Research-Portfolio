# Gene Expression Prediction from DNA Sequences

A comprehensive machine learning project for predicting gene expression levels from DNA sequences using both Python and R implementations.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Dataset](#dataset)
- [Installation](#installation)
- [Usage](#usage)
- [Methods](#methods)
- [Results](#results)
- [License](#license)
- [Contributing](#contributing)

## 🎯 Overview

This project implements machine learning models to predict gene expression levels (binary classification: high/low expression) from DNA sequences. The project includes:

- **Feature Engineering**: K-mer encoding, nucleotide composition analysis
- **Multiple ML Models**: Random Forest, Gradient Boosting, XGBoost, LightGBM, SVM
- **Comprehensive Evaluation**: Accuracy, ROC-AUC, confusion matrices, feature importance
- **Dual Implementation**: Complete implementations in both Python and R

## 📁 Project Structure

```
GeneExpression_DNA_sequence/
│
├── data/
│   ├── genomics_data.csv          # Dataset (2000 DNA sequences)
│   └── .gitkeep
│
├── notebooks/
│   └── gene_expression_prediction.ipynb  # Python Jupyter notebook
│
├── scripts/
│   ├── gene_expression_prediction.py     # Python script
│   ├── gene_expression_prediction.R      # R script
│   └── install_R_packages.R             # R package installer
│
├── models/
│   └── .gitkeep                          # Trained models will be saved here
│
├── results/
│   └── .gitkeep                          # Results and visualizations
│
├── docs/
│   └── .gitkeep                          # Additional documentation
│
├── requirements.txt                      # Python dependencies
├── environment.yml                       # Conda environment file
├── .gitignore                           # Git ignore file
└── README.md                            # This file
```

## 📊 Dataset

### Dataset Information

- **Source**: Genomics data for gene expression prediction
- **Size**: 2000 DNA sequences
- **Sequence Length**: 50 nucleotides per sequence
- **Labels**: Binary classification (0 = low expression, 1 = high expression)
- **Format**: CSV with columns: `Sequences`, `Labels`

### Dataset License

**Important**: This dataset is provided for educational and research purposes. The original dataset license information should be referenced here. If you are using a dataset from a specific source, please:

1. **Reference the original source** in your publications and code
2. **Check the dataset license** before redistribution
3. **Follow any attribution requirements** specified by the dataset provider

#### Common Dataset Sources and Licenses:

- **NCBI/GenBank**: Public domain, but check specific dataset terms
- **UCSC Genome Browser**: Free for academic use, check terms for commercial use
- **Ensembl**: Apache 2.0 or similar open licenses
- **Custom/Proprietary**: Follow the specific license terms provided

**Note**: If this dataset was obtained from a specific source, please update this section with:
- Dataset name and version
- Original source URL
- License type (e.g., CC0, MIT, Apache 2.0, etc.)
- Citation information
- Any usage restrictions

### Dataset Statistics

- Total sequences: 2000
- Sequence length: 50 nucleotides
- Label distribution: Balanced (approximately 50/50 split)
- Nucleotides: A, T, G, C

## 🚀 Installation

### Python Environment

#### Option 1: Using pip

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Option 2: Using Conda

```bash
# Create conda environment
conda env create -f environment.yml

# Activate environment
conda activate gene_expression_prediction

# Install additional packages if needed
pip install -r requirements.txt
```

### R Environment

```bash
# Install R packages
Rscript scripts/install_R_packages.R

# Or install manually in R:
# install.packages(c("readr", "dplyr", "ggplot2", "caret", "randomForest", 
#                    "xgboost", "e1071", "pROC", "doParallel"))
```

## 💻 Usage

### Python Implementation

#### Using Jupyter Notebook

```bash
# Start Jupyter Notebook
jupyter notebook

# Open notebooks/gene_expression_prediction.ipynb
```

#### Using Python Script

```bash
# Run the Python script
python scripts/gene_expression_prediction.py
```

The script will:
1. Load and preprocess the data
2. Encode DNA sequences using k-mer features
3. Train multiple ML models
4. Evaluate model performance
5. Save the best model and generate visualizations

### R Implementation

#### Using R Script

```bash
# Run the R script
Rscript scripts/gene_expression_prediction.R
```

The script will:
1. Load and preprocess the data
2. Encode DNA sequences using k-mer features
3. Train multiple ML models (Random Forest, XGBoost, SVM)
4. Evaluate model performance
5. Save the best model and generate visualizations

#### Using R in Jupyter

To use R in Jupyter notebooks, you need to install the IRkernel:

```r
# In R console:
install.packages('IRkernel')
IRkernel::installspec()
```

Then you can create R notebooks in Jupyter.

## 🔬 Methods

### Feature Engineering

#### 1. K-mer Encoding
- Extracts k-mers (subsequences of length k) from DNA sequences
- Default: k=3 (trinucleotides)
- Creates a frequency matrix of k-mer occurrences
- Normalizes frequencies by sequence length

#### 2. Nucleotide Composition
- Calculates frequencies of individual nucleotides (A, T, G, C)
- Computes GC content
- Optional: Dinucleotide frequencies

### Machine Learning Models

1. **Random Forest**: Ensemble of decision trees
2. **Gradient Boosting**: Sequential ensemble learning
3. **XGBoost**: Optimized gradient boosting
4. **LightGBM**: Fast gradient boosting framework
5. **SVM**: Support Vector Machine with RBF kernel

### Evaluation Metrics

- **Accuracy**: Overall classification accuracy
- **ROC-AUC**: Area under the ROC curve
- **Confusion Matrix**: True/False positives and negatives
- **Classification Report**: Precision, recall, F1-score

## 📈 Results

### Expected Performance

The models typically achieve:
- **Accuracy**: 0.85 - 0.95
- **ROC-AUC**: 0.90 - 0.98

### Model Comparison

Results are saved in the `results/` directory:
- `model_comparison.png`: Accuracy and ROC-AUC comparisons
- `roc_curves_R.png`: ROC curves for R models

### Best Model

The best-performing model is automatically saved in the `models/` directory.

## 📝 Notes

### Data Preprocessing

- Sequences are converted to uppercase
- K-mer encoding handles variable-length sequences
- Features are normalized for better model performance

### Model Selection

- Models are evaluated using stratified train-test split (80/20)
- Best model is selected based on accuracy
- Cross-validation can be added for more robust evaluation

### Future Improvements

1. **Deep Learning**: Implement CNN or LSTM for sequence analysis
2. **Feature Selection**: Reduce dimensionality using feature importance
3. **Hyperparameter Tuning**: Grid search or Bayesian optimization
4. **Cross-Validation**: K-fold cross-validation for robust evaluation
5. **Different K-mer Sizes**: Experiment with k=2, k=4, k=5
6. **Sequence Alignment**: Consider sequence alignment features
7. **Biological Features**: Incorporate known regulatory motifs

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

**Dataset License**: Please refer to the original dataset source for license information. Ensure compliance with the dataset's license terms before use.

## 🙏 Acknowledgments

- Thanks to the open-source community for excellent ML libraries
- Dataset providers (please update with actual source)
- Contributors and reviewers

## 📧 Contact

For questions or issues, please open an issue on GitHub.

## 🔗 References

1. **K-mer Encoding**: A common technique in bioinformatics for sequence analysis
2. **Scikit-learn**: Pedregosa et al., JMLR 12, pp. 2825-2830, 2011
3. **XGBoost**: Chen & Guestrin, KDD '16
4. **LightGBM**: Ke et al., NIPS, 2017

---

**Last Updated**: 2025

**Project Status**: Active Development

