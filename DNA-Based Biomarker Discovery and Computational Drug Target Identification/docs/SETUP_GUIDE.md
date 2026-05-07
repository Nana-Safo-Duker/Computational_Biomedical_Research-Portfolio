# Setup Guide

This guide will help you set up the DNA-Based Biomarker Discovery and Drug Target Identification project.

## Prerequisites

- Python 3.8+ or R 4.0+
- Git
- (Optional) Conda or Miniconda for environment management

## Quick Start

### Option 1: Python Setup (Recommended)

1. **Clone the repository** (if using Git):
   ```bash
   git clone <repository-url>
   cd "DNA-Based Biomarker Discovery and Drug Target Identification"
   ```

2. **Create a virtual environment**:
   ```bash
   # Using venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Or using conda
   conda env create -f environment.yml
   conda activate dna-biomarker-discovery
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the analysis**:
   ```bash
   # Extract features
   python scripts/dna_feature_extraction.py --input data/genomics_data.csv --output results/dna_features.csv
   
   # Train models
   python scripts/dna_ml_pipeline.py --input data/genomics_data.csv --output-dir results/models
   
   # Or use Jupyter notebook
   jupyter notebook notebooks/dna_sequence_analysis.ipynb
   ```

### Option 2: R Setup

1. **Install R packages**:
   ```bash
   Rscript -e "install.packages(c('dplyr', 'data.table', 'stringr', 'caret', 'randomForest', 'e1071', 'pROC', 'ggplot2', 'plotly', 'devtools'), repos='https://cran.rstudio.com/')"
   ```

2. **Run the analysis**:
   ```bash
   # Extract features
   Rscript scripts/dna_feature_extraction.R data/genomics_data.csv results/dna_features.csv
   
   # Train models
   Rscript scripts/dna_ml_pipeline.R data/genomics_data.csv results/models
   
   # Or use R Markdown notebook
   # Open notebooks/dna_sequence_analysis.Rmd in RStudio
   ```

## Project Structure

```
DNA-Based Biomarker Discovery and Drug Target Identification/
├── data/                          # Data directory
│   ├── genomics_data.csv         # Input DNA sequence data
│   └── DATASET_LICENSE.md        # Dataset license information
├── notebooks/                     # Jupyter notebooks
│   ├── dna_sequence_analysis.ipynb    # Python analysis notebook
│   └── dna_sequence_analysis.Rmd      # R analysis notebook
├── scripts/                       # Python and R scripts
│   ├── dna_feature_extraction.py # Python feature extraction
│   ├── dna_ml_pipeline.py        # Python ML pipeline
│   ├── dna_feature_extraction.R  # R feature extraction
│   └── dna_ml_pipeline.R         # R ML pipeline
├── results/                       # Results directory
│   ├── figures/                  # Generated figures
│   └── models/                   # Saved models
├── docs/                          # Documentation
├── requirements.txt               # Python dependencies
├── environment.yml                # Conda environment file
├── R_requirements.txt            # R dependencies
└── README.md                      # Main documentation
```

## Data Preparation

1. **Place your data file** in the `data/` directory:
   - File name: `genomics_data.csv`
   - Format: CSV with columns `Sequences` and `Labels`
   - `Sequences`: DNA sequences (strings)
   - `Labels`: Binary labels (0 or 1)

2. **Check dataset license**:
   - Review `data/DATASET_LICENSE.md`
   - Update with appropriate license information if needed

## Running the Analysis

### Using Python Scripts

1. **Feature Extraction**:
   ```bash
   python scripts/dna_feature_extraction.py \
       --input data/genomics_data.csv \
       --output results/dna_features.csv
   ```

2. **Train ML Models**:
   ```bash
   python scripts/dna_ml_pipeline.py \
       --input data/genomics_data.csv \
       --output-dir results/models \
       --test-size 0.2
   ```

### Using R Scripts

1. **Feature Extraction**:
   ```bash
   Rscript scripts/dna_feature_extraction.R \
       data/genomics_data.csv \
       results/dna_features.csv
   ```

2. **Train ML Models**:
   ```bash
   Rscript scripts/dna_ml_pipeline.R \
       data/genomics_data.csv \
       results/models
   ```

### Using Jupyter Notebooks

1. **Start Jupyter**:
   ```bash
   jupyter notebook
   ```

2. **Open the notebook**:
   - Python: `notebooks/dna_sequence_analysis.ipynb`
   - R: `notebooks/dna_sequence_analysis.Rmd` (open in RStudio)

3. **Run all cells** to perform the complete analysis

## Troubleshooting

### Python Issues

1. **Import errors**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check that you're in the correct virtual environment

2. **File not found errors**:
   - Ensure you're running scripts from the project root directory
   - Check that data file exists in `data/genomics_data.csv`

3. **Memory errors**:
   - Reduce dataset size for testing
   - Use smaller models (fewer trees, lower max_depth)

### R Issues

1. **Package installation errors**:
   - Update R to the latest version
   - Install packages from CRAN: `install.packages("package_name")`

2. **String manipulation errors**:
   - Ensure `stringr` package is installed and loaded
   - Check that sequences are valid DNA sequences (A, T, G, C only)

## Next Steps

1. **Review results** in the `results/` directory:
   - `results/figures/`: Visualization files
   - `results/models/`: Trained models
   - `results/top_biomarkers.csv`: Identified biomarkers

2. **Experiment with different models**:
   - Modify model parameters in scripts
   - Try different feature combinations
   - Test with different datasets

3. **Extend the analysis**:
   - Add new feature extraction methods
   - Implement deep learning models
   - Perform statistical analysis

## Getting Help

- Check the [README.md](../README.md) for detailed documentation
- Review code comments in scripts
- Open an issue on GitHub for bugs or questions

## License

See [LICENSE](../LICENSE) for project license information.
See [data/DATASET_LICENSE.md](../data/DATASET_LICENSE.md) for dataset license information.

