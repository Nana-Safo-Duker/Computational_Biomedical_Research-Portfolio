# DNA-Based Biomarker Discovery and Drug Target Identification

A comprehensive machine learning pipeline for identifying potential biomarkers and drug targets from DNA sequences through advanced feature extraction and predictive modeling.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Data](#data)
- [Methods](#methods)
- [Results](#results)
- [License](#license)
- [Contributing](#contributing)
- [Citation](#citation)

## 🔬 Overview

This project implements a machine learning pipeline to analyze DNA sequences and identify potential biomarkers and drug targets. The pipeline extracts comprehensive sequence features including nucleotide composition, k-mer frequencies, GC content, sequence complexity, and other biologically relevant characteristics. These features are then used to train multiple machine learning models to classify sequences as potential drug targets or biomarkers.

### Key Objectives

1. **Feature Extraction**: Extract comprehensive features from DNA sequences that can highlight potential drug targets or biomarkers
2. **Model Training**: Train and compare multiple machine learning models (Random Forest, Gradient Boosting, SVM, Logistic Regression)
3. **Biomarker Identification**: Identify the most important DNA sequence features that serve as biomarkers
4. **Drug Target Prediction**: Predict which DNA sequences are likely to be drug targets

## ✨ Features

- **Comprehensive Feature Extraction**:
  - Nucleotide composition (A, T, G, C frequencies)
  - GC content and GC skew
  - AT content and AT skew
  - Dinucleotide frequencies (16 combinations)
  - Trinucleotide frequencies (20 most common)
  - K-mer frequencies
  - Sequence complexity (Shannon entropy)
  - Purine/Pyrimidine ratio
  - Homopolymer runs
  - Sequence length (normalized)

- **Multiple ML Models**:
  - Random Forest Classifier
  - Gradient Boosting Classifier
  - Support Vector Machine (SVM)
  - Logistic Regression

- **Comprehensive Evaluation**:
  - Cross-validation
  - ROC curves
  - Confusion matrices
  - Feature importance analysis
  - Model comparison

- **Dual Language Support**:
  - Python implementation (`.py` scripts and Jupyter notebooks)
  - R implementation (`.R` scripts and Jupyter notebooks)

## 📁 Project Structure

```
DNA-Based Biomarker Discovery and Drug Target Identification/
│
├── data/                          # Data directory
│   ├── genomics_data.csv         # Input DNA sequence data
│   └── .gitkeep
│
├── notebooks/                     # Jupyter notebooks
│   ├── dna_sequence_analysis.ipynb    # Python analysis notebook
│   └── dna_sequence_analysis.Rmd      # R analysis notebook
│
├── scripts/                       # Python and R scripts
│   ├── dna_feature_extraction.py # Python feature extraction
│   ├── dna_ml_pipeline.py        # Python ML pipeline
│   ├── dna_feature_extraction.R  # R feature extraction
│   └── dna_ml_pipeline.R         # R ML pipeline
│
├── results/                       # Results directory
│   ├── figures/                  # Generated figures
│   │   ├── feature_importance.png
│   │   ├── model_comparison.png
│   │   ├── roc_curves.png
│   │   └── confusion_matrices.png
│   ├── models/                   # Saved models
│   │   ├── best_model_*.pkl
│   │   ├── scaler.pkl
│   │   └── feature_names.pkl
│   ├── top_biomarkers.csv        # Top identified biomarkers
│   └── model_comparison.csv      # Model performance comparison
│
├── docs/                          # Documentation
│
├── .gitignore                     # Git ignore file
├── requirements.txt               # Python dependencies
├── environment.yml                # Conda environment file
├── R_requirements.txt            # R dependencies
└── README.md                      # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.8+ or R 4.0+
- Git

### Python Environment Setup

#### Option 1: Using pip

```bash
# Clone the repository
git clone <repository-url>
cd "DNA-Based Biomarker Discovery and Drug Target Identification"

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Option 2: Using conda

```bash
# Clone the repository
git clone <repository-url>
cd "DNA-Based Biomarker Discovery and Drug Target Identification"

# Create conda environment
conda env create -f environment.yml

# Activate environment
conda activate dna-biomarker-discovery
```

### R Environment Setup

```bash
# Install R packages
Rscript -e "install.packages(c('dplyr', 'data.table', 'stringr', 'caret', 'randomForest', 'e1071', 'pROC', 'ggplot2', 'plotly', 'devtools'), repos='https://cran.rstudio.com/')"

# Or install from requirements file
Rscript -e "source('R_requirements.txt')"
```

## 💻 Usage

### Python Usage

#### 1. Feature Extraction

```bash
# Extract features from DNA sequences
python scripts/dna_feature_extraction.py --input data/genomics_data.csv --output results/dna_features.csv
```

#### 2. Train ML Models

```bash
# Train models using extracted features
python scripts/dna_ml_pipeline.py --input data/genomics_data.csv --output-dir results/models
```

#### 3. Jupyter Notebook

```bash
# Start Jupyter notebook
jupyter notebook notebooks/dna_sequence_analysis.ipynb
```

### R Usage

#### 1. Feature Extraction

```bash
# Extract features from DNA sequences
Rscript scripts/dna_feature_extraction.R data/genomics_data.csv results/dna_features.csv
```

#### 2. Train ML Models

```bash
# Train models using extracted features
Rscript scripts/dna_ml_pipeline.R data/genomics_data.csv results/models
```

#### 3. R Notebook

```bash
# Open R notebook in RStudio or Jupyter
# File: notebooks/dna_sequence_analysis.Rmd
```

## 📊 Data

### Dataset Description

The dataset (`genomics_data.csv`) contains DNA sequences with binary labels indicating whether a sequence is associated with a potential drug target or biomarker (label=1) or not (label=0).

### Data Format

```csv
Sequences,Labels
CCGAGGGCTATGGTTTGGAAGTTAGAACCCTGGGGCTTCTCGCGGACACC,0
GAGTTTATATGGCGCGAGCCTAGTGGTTTTTGTACTTGTTTGTCGCGTCG,0
GTCCACGACCGAACTCCCACCTTGACCGCAGAGGTACCACCAGAGCCCTG,1
...
```

### Dataset License

**Note**: Please refer to the original dataset's license for usage terms. This project uses the dataset for research and educational purposes. If you are the dataset owner and wish to specify the license, please update this section accordingly.

**Default License Assumption**: This dataset is assumed to be available for research and educational purposes. If you have specific licensing requirements, please:
1. Add a `LICENSE` file in the `data/` directory
2. Update this section with the specific license information
3. Include attribution requirements if applicable

## 🔬 Methods

### Feature Extraction

The pipeline extracts 48 features from each DNA sequence:

1. **Basic Composition** (4 features):
   - A, T, G, C nucleotide frequencies

2. **Content Metrics** (4 features):
   - GC content
   - AT content
   - GC skew
   - AT skew

3. **Complexity Metrics** (4 features):
   - Shannon entropy
   - Purine/Pyrimidine ratio
   - Normalized sequence length
   - Maximum homopolymer run

4. **K-mer Frequencies** (36 features):
   - 16 dinucleotide frequencies
   - 20 trinucleotide frequencies

### Machine Learning Models

1. **Random Forest**: Ensemble method using multiple decision trees
2. **Gradient Boosting**: Sequential ensemble method
3. **Support Vector Machine (SVM)**: Kernel-based classifier
4. **Logistic Regression**: Linear classifier with regularization

### Evaluation Metrics

- **Accuracy**: Overall classification accuracy
- **AUC-ROC**: Area under the receiver operating characteristic curve
- **Cross-Validation**: 5-fold cross-validation for robust evaluation
- **Feature Importance**: Identification of most predictive features

## 📈 Results

The pipeline generates several outputs:

1. **Feature Importance**: Ranking of DNA sequence features by predictive power
2. **Model Performance**: Comparison of different ML models
3. **ROC Curves**: Visualization of model performance across different thresholds
4. **Confusion Matrices**: Detailed classification results
5. **Top Biomarkers**: List of most important DNA sequence features

Results are saved in the `results/` directory:
- `results/figures/`: Visualization files
- `results/models/`: Trained models
- `results/top_biomarkers.csv`: Identified biomarkers
- `results/model_comparison.csv`: Model performance comparison

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Dataset License**: Please refer to the original dataset's license for usage terms. See the [Data](#data) section for more information.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📚 Citation

If you use this project in your research, please cite:

```bibtex
@software{dna_biomarker_discovery,
  title={DNA-Based Biomarker Discovery and Drug Target Identification},
  author={Your Name},
  year={2025},
  url={https://github.com/yourusername/dna-biomarker-discovery}
}
```

## 🙏 Acknowledgments

- Thanks to all contributors and researchers in the field of bioinformatics and machine learning
- Special thanks to the developers of scikit-learn, pandas, and other open-source libraries used in this project

## 📧 Contact

For questions or suggestions, please open an issue on GitHub or contact the project maintainers.

## 🔗 Related Projects

- [scikit-learn](https://scikit-learn.org/) - Machine learning library
- [pandas](https://pandas.pydata.org/) - Data analysis library
- [Biopython](https://biopython.org/) - Bioinformatics library (optional)

---

**Note**: This project is for research and educational purposes. Always validate predictions with experimental data before making clinical or pharmaceutical decisions.

