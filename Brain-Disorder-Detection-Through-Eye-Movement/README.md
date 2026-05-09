# Brain Disorder Detection Through Eye Movement Analysis

License: MIT | Python 3.9+ | R 4.0+

A comprehensive wearable-sensor and eye-movement analytics project for identifying neurological disorder patterns using statistical analysis and machine learning.

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

This project analyzes eye-movement trajectories as potential biomarkers for brain disorders. It includes reproducible Python and R workflows with notebook-based exploration and visualization.

### Key Objectives

- Extract eye-movement features (velocity, acceleration, saccade/fixation proxies)
- Compare healthy vs disorder groups statistically
- Train classification models for screening support
- Provide reproducible scripts for educational research

## Features

- Python analysis: `eye_movement_analysis.py`
- R analysis: `eye_movement_analysis.R`
- Notebook workflow: `eye_movement_analysis.ipynb`
- Visualization and feature engineering support
- Structured environment via `requirements.txt`

## Project Structure

```text
.
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── .gitattributes
├── eye_movement_analysis.py
├── eye_movement_analysis.R
└── eye_movement_analysis.ipynb
```

## Installation

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Optional R packages:

```r
install.packages(c("dplyr", "ggplot2", "caret", "randomForest", "e1071", "pROC"))
```

## Usage

### Python

```bash
python eye_movement_analysis.py
```

### R

```bash
Rscript eye_movement_analysis.R
```

### Notebook

```bash
jupyter notebook eye_movement_analysis.ipynb
```

## Methodology

- Time-series preprocessing of eye-position traces
- Derived kinematic feature extraction
- Group-level hypothesis testing
- PCA/feature-space exploration
- Supervised classification evaluation

## Results

Outputs typically include:

- summary statistics and group comparisons
- classifier performance metrics
- visual diagnostics for feature distributions and model behavior

## Contributing

Contributions are welcome via issue reports and pull requests.

## License

MIT License. See `LICENSE`.

## References

- Literature on eye-movement biomarkers in neurological disorders
- Wearable sensor analytics and ML diagnostics methods

