# Transcription Factor Binding Prediction

A comprehensive machine learning and deep learning project for predicting transcription factor (TF) binding sites in DNA sequences. This project implements multiple algorithms including Convolutional Neural Networks (CNN), Long Short-Term Memory (LSTM) networks, Random Forest, XGBoost, and Support Vector Machines (SVM).

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Models](#models)
- [Results](#results)
- [Dataset](#dataset)
- [License](#license)
- [Contributing](#contributing)
- [Citation](#citation)

## Overview

Transcription factors are proteins that bind to specific DNA sequences to control the rate of transcription of genetic information from DNA to messenger RNA. Predicting TF binding sites is crucial for understanding gene regulation, disease mechanisms, and developing therapeutic interventions.

This project provides:
- **Multiple ML/DL models** for TF binding prediction
- **Comprehensive evaluation** with multiple metrics
- **Visualization tools** for results analysis
- **Both Python and R implementations**
- **Jupyter notebooks** for interactive analysis

## Features

### Implemented Models

1. **Deep Learning Models**
   - Convolutional Neural Network (CNN)
   - Long Short-Term Memory (LSTM)

2. **Traditional Machine Learning Models**
   - Random Forest
   - XGBoost
   - Support Vector Machine (SVM)

3. **R Implementation Additional Models**
   - Neural Network (MLP)
   - Logistic Regression

### Key Features

- ✅ One-hot encoding of DNA sequences
- ✅ Comprehensive model evaluation (Accuracy, Precision, Recall, F1-Score, ROC-AUC)
- ✅ Visualization of training history, confusion matrices, and ROC curves
- ✅ Model persistence (save/load trained models)
- ✅ Cross-validation support
- ✅ Hyperparameter tuning capabilities
- ✅ Both Python and R implementations
- ✅ Jupyter notebook support

## Project Structure

```
Transcription-Factor-Binding-Prediction/
│
├── data/                          # Data directory
│   └── genomics_data.csv          # Dataset (DNA sequences and labels)
│
├── scripts/                       # Source code
│   ├── python/                    # Python scripts
│   │   └── tf_binding_prediction.py
│   └── r/                         # R scripts
│       └── tf_binding_prediction.R
│
├── notebooks/                     # Jupyter notebooks
│   ├── python/                    # Python notebooks
│   │   └── tf_binding_prediction.ipynb
│   └── r/                         # R notebooks (optional)
│
├── models/                        # Saved models (generated)
│   ├── cnn_model.h5
│   ├── lstm_model.h5
│   ├── random_forest_model.pkl
│   ├── xgboost_model.pkl
│   └── svm_model.pkl
│
├── results/                       # Results and visualizations (generated)
│   ├── cnn_training_history.png
│   ├── lstm_training_history.png
│   ├── confusion_matrices.png
│   ├── roc_curves.png
│   └── model_comparison.csv
│
├── docs/                          # Documentation
│
├── requirements.txt               # Python dependencies
├── requirements-r.txt             # R dependencies
├── .gitignore                     # Git ignore file
└── README.md                      # This file
```

## Installation

### Prerequisites

- Python 3.8+ or R 4.0+
- pip (Python) or CRAN (R)
- Git

### Python Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/transcription-factor-binding-prediction.git
cd transcription-factor-binding-prediction
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### R Installation

1. Install R from [CRAN](https://cran.r-project.org/)

2. Install required R packages:
```r
# Install packages from CRAN
install.packages(c(
  "tidyverse", "caret", "randomForest", "xgboost", 
  "e1071", "neuralnet", "pROC", "ggplot2", 
  "reshape2", "doParallel", "gridExtra"
))

# Or use the requirements file as a guide
```

3. For Jupyter notebook support in R:
```r
install.packages("IRkernel")
IRkernel::installspec()
```

## Usage

### Python

#### Command Line

```bash
# Run the main script
python scripts/python/tf_binding_prediction.py
```

#### Jupyter Notebook

```bash
# Start Jupyter notebook
jupyter notebook

# Open notebooks/python/tf_binding_prediction.ipynb
```

#### Programmatic Usage

```python
from scripts.python.tf_binding_prediction import TFBindingPredictor

# Initialize predictor
predictor = TFBindingPredictor(data_path='data/genomics_data.csv')

# Load data
predictor.load_data()

# Train models
predictor.train_cnn(epochs=50, batch_size=32)
predictor.train_lstm(epochs=50, batch_size=32)
predictor.train_random_forest(n_estimators=100, max_depth=20)
predictor.train_xgboost(n_estimators=100, max_depth=6)
predictor.train_svm()

# Evaluate models
predictor.evaluate_all_models()

# Make predictions on new sequences
new_sequences = ['CCGAGGGCTATGGTTTGGAAGTTAGAACCCTGGGGCTTCTCGCGGACACC']
predictions = predictor.predict(new_sequences, model_name='cnn')
print(predictions)

# Save models
predictor.save_models(directory='models')
```

### R

#### Command Line

```r
# Run the main script
Rscript scripts/r/tf_binding_prediction.R
```

#### Interactive R Session

```r
# Source the script
source("scripts/r/tf_binding_prediction.R")

# Run main function
main()
```

## Models

### Deep Learning Models

#### CNN (Convolutional Neural Network)
- **Architecture**: Multiple Conv1D layers with BatchNorm and MaxPooling
- **Advantages**: Captures local patterns and motifs in DNA sequences
- **Best for**: Detecting short binding motifs

#### LSTM (Long Short-Term Memory)
- **Architecture**: Bidirectional LSTM layers
- **Advantages**: Captures long-range dependencies in sequences
- **Best for**: Sequences with complex patterns

### Machine Learning Models

#### Random Forest
- **Algorithm**: Ensemble of decision trees
- **Advantages**: Robust, handles non-linear relationships
- **Hyperparameters**: n_estimators, max_depth

#### XGBoost
- **Algorithm**: Gradient boosting
- **Advantages**: High performance, feature importance
- **Hyperparameters**: n_estimators, max_depth, learning_rate

#### SVM
- **Algorithm**: Support Vector Machine with RBF kernel
- **Advantages**: Effective for high-dimensional data
- **Note**: Uses subset of data due to computational complexity

## Results

The models are evaluated using multiple metrics:

- **Accuracy**: Overall correctness
- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / (True positives + False negatives)
- **F1-Score**: Harmonic mean of precision and recall
- **ROC-AUC**: Area under the ROC curve

Results are saved in:
- `results/model_comparison.csv`: Comparative metrics
- `results/*.png`: Visualizations (confusion matrices, ROC curves, training history)
- `models/results.json`: Detailed results (Python)

## Dataset

### Data Format

The dataset (`data/genomics_data.csv`) contains:
- **Sequences**: DNA sequences (50 nucleotides long)
- **Labels**: Binary labels (0 = no TF binding, 1 = TF binding)

### Dataset License

**Important**: This dataset is provided for research and educational purposes only.

#### Dataset Attribution

The genomics data used in this project follows standard open data practices for bioinformatics research. If you use this dataset, please:

1. **Cite the original source** (if applicable)
2. **Respect data usage terms** from the original provider
3. **Follow ethical guidelines** for genomics data usage

#### Data Usage Guidelines

- ✅ **Allowed**: Research, education, academic publications
- ✅ **Allowed**: Model development and benchmarking
- ✅ **Required**: Proper attribution and citation
- ❌ **Not Allowed**: Commercial use without permission
- ❌ **Not Allowed**: Redistribution without attribution

#### Recommended Citation Format

If you use this dataset in your research, please cite:

```
Transcription Factor Binding Prediction Dataset
Source: [Original Dataset Source/Repository]
License: [License Type - e.g., CC BY 4.0, MIT, etc.]
Accessed: [Date]
```

#### Data Source Information

For the most up-to-date license information and data source attribution, please refer to:
- The original dataset repository (if available)
- The data provider's website
- Associated publications or documentation

**Note**: If this dataset was obtained from a public repository (e.g., Kaggle, UCI, etc.), please refer to their specific license terms. Common licenses for genomics datasets include:
- Creative Commons (CC BY, CC0)
- Open Data Commons (ODC)
- Academic use licenses

If you are the dataset creator or have specific license requirements, please update this section accordingly.

### Data Preprocessing

1. **Sequence Encoding**: DNA sequences are one-hot encoded (A, T, G, C → [1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1])
2. **Data Splitting**: 80% training, 20% testing (stratified)
3. **Normalization**: Applied where necessary for neural networks

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Dataset License**: Please refer to the [Dataset](#dataset) section for dataset-specific license information.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines

- Follow PEP 8 (Python) or tidyverse style guide (R)
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass

## Citation

If you use this project in your research, please cite:

```bibtex
@software{transcription_factor_binding_prediction,
  title = {Transcription Factor Binding Prediction},
  author = {Your Name},
  year = {2024},
  url = {https://github.com/yourusername/transcription-factor-binding-prediction},
  version = {1.0.0}
}
```

## Acknowledgments

- Thanks to the open-source community for excellent ML/DL libraries
- Dataset providers and contributors
- Research community for valuable feedback

## Contact

For questions or suggestions, please open an issue on GitHub or contact:
- Email: [your.email@example.com]
- GitHub: [@yourusername]

## References

1. Alipanahi, B., et al. (2015). Predicting the sequence specificities of DNA- and RNA-binding proteins by deep learning. Nature Biotechnology, 33(8), 831-838.

2. Quang, D., & Xie, X. (2016). DanQ: a hybrid convolutional and recurrent deep neural network for quantifying the function of DNA sequences. Nucleic Acids Research, 44(11), e107.

3. Kelley, D. R., et al. (2016). Basset: learning the regulatory code of the accessible genome with deep convolutional neural networks. Genome Research, 26(7), 990-999.

## Changelog

### Version 1.0.0 (2024)
- Initial release
- Implemented CNN, LSTM, Random Forest, XGBoost, SVM models
- Added Python and R implementations
- Created comprehensive documentation
- Added Jupyter notebook support

---

**Note**: This project is for research and educational purposes. Always verify predictions with experimental validation.

