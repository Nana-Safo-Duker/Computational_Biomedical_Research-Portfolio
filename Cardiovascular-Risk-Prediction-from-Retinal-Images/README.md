# Cardiovascular Risk Prediction from Retinal Images

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![R 4.0+](https://img.shields.io/badge/R-4.0+-blue.svg)](https://www.r-project.org/)

A comprehensive visual analytics project for retinal-image-based cardiovascular risk prediction, inspired by published deep learning findings.

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Usage](#-usage)
- [Methodology](#-methodology)
- [Results](#-results)
- [Contributing](#-contributing)
- [License](#-license)
- [Citation](#-citation)
- [Contact](#-contact)

## 🌟 Overview

This repository provides reproducible scripts and notebooks for exploring cardiovascular risk factor prediction and outcome stratification from retinal image-derived signals.

## ✨ Key Features

- Notebook workflow: `cardiovascular_prediction_visualization.ipynb`
- Python scripts: `cardiovascular_visualization.py`, `cardiovascular_visualization_complete.py`
- R implementation: `cardiovascular_visualization.R`
- Supporting documentation for comparisons and project summaries

## 🚀 Installation

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

```r
install.packages(c("ggplot2","dplyr","pROC","caret"))
```

## 🎯 Quick Start

```bash
python cardiovascular_visualization.py
python cardiovascular_visualization_complete.py
Rscript cardiovascular_visualization.R
jupyter notebook cardiovascular_prediction_visualization.ipynb
```

## 📁 Project Structure

```text
.
├── README.md
├── requirements.txt
├── cardiovascular_prediction_visualization.ipynb
├── cardiovascular_visualization.py
├── cardiovascular_visualization_complete.py
├── cardiovascular_visualization.R
└── VISUALIZATION_COMPARISON.md
```

## 💻 Usage

Run scripts for automated figure generation and use notebook mode for exploratory analysis.

## 🔬 Methodology

- Simulated-data-driven reproduction of reported risk metrics
- ROC/calibration/error visualization workflows
- Risk stratification and comparative plotting
- Multi-script robustness handling for stable outputs

## 📊 Results

Outputs include ROC curves, calibration plots, risk visualizations, and summary metrics.

## 🛠️ Contributing

Contributions are welcome through issues and pull requests.

## 📜 License

MIT License. See project license file.

## 📖 Citation

Please cite this repository and foundational retinal-risk prediction literature.

## 📞 Contact

Open a GitHub issue for support or collaboration.

