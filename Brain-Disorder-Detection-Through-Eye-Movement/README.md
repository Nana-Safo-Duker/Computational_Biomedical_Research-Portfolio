# Brain Disorder Detection Through Eye Movement Analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![R 4.0+](https://img.shields.io/badge/R-4.0+-blue.svg)](https://www.r-project.org/)

A comprehensive research project for detecting neurological disorder signatures from eye movement features using machine learning and statistical analysis.

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

This repository uses eye movement trajectories as potential biomarkers for brain disorder screening tasks. It includes Python and R scripts plus a notebook workflow for reproducible analysis.

## ✨ Key Features

- Python script: `eye_movement_analysis.py`
- R script: `eye_movement_analysis.R`
- Notebook: `eye_movement_analysis.ipynb`
- Feature extraction, statistical testing, and classifier evaluation

## 🚀 Installation

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

```r
install.packages(c("dplyr","ggplot2","caret","randomForest","e1071","pROC"))
```

## 🎯 Quick Start

```bash
python eye_movement_analysis.py
Rscript eye_movement_analysis.R
jupyter notebook eye_movement_analysis.ipynb
```

## 📁 Project Structure

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

## 💻 Usage

Use scripts for automated runs and the notebook for exploratory analysis.

## 🔬 Methodology

- Time-series preprocessing of eye-position signals
- Feature extraction (velocity/acceleration and event proxies)
- Group comparisons and significance testing
- Classification model evaluation with standard metrics

## 📊 Results

Typical outputs include feature summaries, model metrics, and visual diagnostics.

## 🛠️ Contributing

Contributions are welcome through GitHub issues and pull requests.

## 📜 License

MIT License. See `LICENSE`.

## 📖 Citation

Please cite this repository and associated literature used in the project.

## 📞 Contact

Open an issue for support or collaboration.

