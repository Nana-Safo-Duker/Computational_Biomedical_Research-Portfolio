# Cardiovascular Risk Prediction from Retinal Images

License: MIT | Python 3.8+ | R 4.0+

A comprehensive computational medicine project for analyzing how retinal fundus image-derived signals can support cardiovascular risk prediction workflows through machine learning and visual analytics.

## Table of Contents

- Overview
- Features
- Project Structure
- Installation
- Usage
- Methodology
- Results
- Contributing
- License
- References

## Overview

This project provides a full analysis and visualization toolkit inspired by retinal imaging research for cardiovascular risk stratification. It includes notebook workflows, two Python script variants, and an R implementation for reproducible comparison.

### Key Objectives

- Reproduce core cardiovascular risk visualization workflows
- Compare prediction quality for risk factors and outcomes
- Provide robust plotting scripts with fallback handling
- Support educational and research-oriented exploration

## Features

- Interactive notebook: `cardiovascular_prediction_visualization.ipynb`
- Python script: `cardiovascular_visualization.py`
- Advanced Python script: `cardiovascular_visualization_complete.py`
- R implementation: `cardiovascular_visualization.R`
- Extensive supplemental documentation files for project tracking

## Project Structure

```text
.
├── README.md
├── requirements.txt
├── cardiovascular_prediction_visualization.ipynb
├── cardiovascular_visualization.py
├── cardiovascular_visualization_complete.py
├── cardiovascular_visualization.R
├── VISUALIZATION_COMPARISON.md
└── project summary/checklist documents
```

## Installation

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Optional R packages:

```r
install.packages(c("ggplot2", "dplyr", "pROC", "caret"))
```

## Usage

### Notebook

```bash
jupyter notebook cardiovascular_prediction_visualization.ipynb
```

### Python scripts

```bash
python cardiovascular_visualization.py
python cardiovascular_visualization_complete.py
```

### R script

```bash
Rscript cardiovascular_visualization.R
```

## Methodology

- Synthetic-data-backed reproduction of published-style metrics
- Risk-factor prediction and outcome risk stratification workflows
- ROC, calibration, and error-analysis visual reporting
- Multi-script fallback logic for robust figure generation

## Results

Expected outputs include:

- model performance figures (ROC, calibration, scatter/error plots)
- risk stratification graphics and summary metrics
- notebook-generated exploratory analyses for reporting

## Contributing

Contributions are welcome via pull requests and issue discussions.

## License

MIT License. See project license files.

## References

- Poplin et al. retinal imaging cardiovascular risk literature
- Supporting deep learning and clinical risk modeling references

