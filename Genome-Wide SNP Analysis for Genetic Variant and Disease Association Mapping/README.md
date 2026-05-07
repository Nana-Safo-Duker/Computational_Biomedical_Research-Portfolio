# Genetic Variants and Disease Association Analysis

A comprehensive bioinformatics project for identifying and analyzing genetic variants (SNPs, Indels, and Structural Variants) in DNA sequences and their association with disease phenotypes.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dataset](#dataset)
- [Methods](#methods)
- [Results](#results)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)

## 🔬 Overview

This project provides a comprehensive toolkit for genetic variant identification and analysis, including:

- **Single-Nucleotide Polymorphisms (SNPs)**: Single base pair changes in DNA sequences
- **Insertions/Deletions (Indels)**: Small insertions or deletions of DNA segments
- **Structural Variants**: Large-scale genomic alterations including duplications, inversions, and large indels

The project includes implementations in both **Python** and **R**, with Jupyter notebooks for interactive analysis and command-line scripts for batch processing.

## 📁 Project Structure

```
Genetic Variants and Disease Association_(SNPs)/
│
├── data/                          # Data directory
│   └── genomics_data.csv          # Input genomics dataset
│
├── src/                           # Source code
│   ├── variant_identification.py  # Python: Core variant identification functions
│   ├── variant_analysis.py        # Python: Analysis and visualization
│   ├── variant_identification.R    # R: Core variant identification functions
│   └── variant_analysis.R          # R: Analysis and visualization
│
├── notebooks/                     # Jupyter notebooks
│   ├── variant_analysis.ipynb     # Python notebook for interactive analysis
│   └── variant_analysis.Rmd        # R notebook for interactive analysis
│
├── results/                       # Output directory
│   ├── variant_analysis_results.csv
│   ├── summary_statistics.csv
│   ├── disease_association_analysis.csv
│   └── *.png                      # Visualization plots
│
├── tests/                         # Unit tests
├── docs/                          # Documentation
│
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore file
└── README.md                      # This file
```

## ✨ Features

### Variant Identification
- **SNP Detection**: Identifies single nucleotide polymorphisms by comparing sequences to a reference
- **Indel Detection**: Detects insertions and deletions using sequence alignment approaches
- **Structural Variant Detection**: Identifies large-scale variants including:
  - Large insertions/deletions (≥10 bp)
  - Duplications
  - Inversions

### Analysis Capabilities
- Consensus sequence calculation from multiple sequences
- Statistical summaries of variant distributions
- Disease association analysis (case-control comparison)
- Comprehensive visualizations:
  - Variant distribution histograms
  - Disease association box plots
  - Correlation heatmaps

### Implementation
- **Python**: Object-oriented design with pandas, numpy, matplotlib, seaborn
- **R**: Functional programming with dplyr, ggplot2, corrplot
- **Jupyter Notebooks**: Interactive analysis environments for both languages

## 🚀 Installation

### Prerequisites

- Python 3.7+ or R 4.0+ (R 4.5.2 recommended)
- Git (for cloning the repository)

**Note**: If you need to update R, see [docs/UPDATE_R.md](docs/UPDATE_R.md) for detailed instructions.

### Python Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd "Genetic Variants and Disease Association_(SNPs)"
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

### R Setup

1. Install required R packages:
```r
install.packages(c("dplyr", "ggplot2", "gridExtra", "corrplot", "stringr", "rmarkdown"))
```

2. **Install Pandoc** (required for R Markdown rendering):
   - **Windows**: Download and install from [Pandoc Releases](https://github.com/jgm/pandoc/releases)
   - **macOS**: `brew install pandoc` or download from the releases page
   - **Linux**: `sudo apt-get install pandoc` (Ubuntu/Debian) or use your package manager
   
   After installation, verify with:
   ```r
   rmarkdown::pandoc_available()
   ```

3. Optional: Install Biostrings for advanced sequence analysis:
```r
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
BiocManager::install("Biostrings")
```

**Note**: If you don't have Pandoc installed, you can still use the R scripts (`.R` files) directly without rendering the R Markdown notebook.

## 📊 Usage

### Python

#### Command Line

1. **Basic variant identification**:
```bash
python src/variant_identification.py
```

2. **Comprehensive analysis with visualizations**:
```bash
python src/variant_analysis.py
```

#### Jupyter Notebook

1. Start Jupyter:
```bash
jupyter notebook
```

2. Open `notebooks/variant_analysis.ipynb` and run all cells

### R

#### Command Line

1. **Basic variant identification**:
```r
Rscript src/variant_identification.R
```

2. **Comprehensive analysis with visualizations**:
```r
Rscript src/variant_analysis.R
```

#### R Notebook

1. **Option 1: Use RStudio** (recommended - handles Pandoc automatically):
   - Open `notebooks/variant_analysis.Rmd` in RStudio
   - Click "Knit" to render the notebook

2. **Option 2: Render from command line** (requires Pandoc):
```r
rmarkdown::render("notebooks/variant_analysis.Rmd")
```

**Note**: If Pandoc is not installed, you can still run the R scripts directly:
```r
source("src/variant_identification.R")
source("src/variant_analysis.R")
main()
```

### Example Code

#### Python
```python
from src.variant_identification import VariantIdentifier

# Initialize identifier
identifier = VariantIdentifier()

# Analyze a sequence
sequence = "ATCGATCGATCG"
reference = "ATCGATCGATCG"

results = identifier.analyze_sequence(sequence, reference)
print(f"SNPs: {len(results['snps'])}")
print(f"Indels: {len(results['indels'])}")
print(f"Structural Variants: {len(results['structural_variants'])}")
```

#### R
```r
source("src/variant_identification.R")

# Analyze a sequence
sequence <- "ATCGATCGATCG"
reference <- "ATCGATCGATCG"

results <- analyze_sequence(sequence, reference)
cat("SNPs:", nrow(results$snps), "\n")
cat("Indels:", nrow(results$indels), "\n")
cat("Structural Variants:", nrow(results$structural_variants), "\n")
```

## 📦 Dataset

### Data Format

The input dataset (`data/genomics_data.csv`) contains:
- **Sequences**: DNA sequences (50 nucleotides each)
- **Labels**: Binary classification (0 = Control, 1 = Disease)

### Dataset License

**Note**: This project uses a genomics dataset for analysis. The original dataset's license and terms of use should be referenced here. Please ensure you have proper permissions to use the dataset and comply with:

- Data usage agreements
- Privacy and ethical guidelines
- Publication restrictions (if any)

**If you are using a publicly available dataset**, please cite the original source:
- Include dataset citation
- Reference the original publication
- Link to the dataset repository

**If this is a custom/proprietary dataset**, please:
- Document the data source
- Include any required attribution
- Specify usage restrictions

For example, if using a dataset from a public repository:
```
Dataset: [Dataset Name]
Source: [Repository URL]
License: [License Type]
Citation: [Citation Information]
```

## 🔬 Methods

### Variant Identification Algorithms

1. **SNP Detection**:
   - Position-by-position comparison with reference sequence
   - Filters for valid nucleotide substitutions (A, C, G, T)

2. **Indel Detection**:
   - Simple alignment-based approach
   - Identifies gaps and insertions by comparing sequence positions

3. **Structural Variant Detection**:
   - Large indels (≥10 bp)
   - Duplication detection through pattern matching
   - Inversion detection via reverse complement matching

### Consensus Sequence Calculation

The consensus sequence is calculated as the most frequent nucleotide at each position across all sequences in the dataset.

### Statistical Analysis

- Descriptive statistics for variant distributions
- T-tests for disease association (case vs. control)
- Correlation analysis between variant types

## 📈 Results

The analysis pipeline generates:

1. **Variant Counts**: Number of SNPs, indels, and structural variants per sequence
2. **Summary Statistics**: Mean, median, max variant counts
3. **Disease Association**: Comparison of variant frequencies between cases and controls
4. **Visualizations**: 
   - Distribution plots
   - Box plots for disease association
   - Correlation heatmaps

Results are saved in the `results/` directory.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

**Important**: Please ensure compliance with the original dataset's license and terms of use when using this code with external datasets.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions or suggestions, please open an issue on the GitHub repository.

## 🙏 Acknowledgments

- Bioinformatics community for tools and resources
- Contributors to open-source genomics libraries
- Dataset providers (please cite appropriately)

---

**Last Updated**: 2025

**Version**: 1.0.0

