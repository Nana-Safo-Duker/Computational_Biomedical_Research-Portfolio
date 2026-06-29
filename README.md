# AI/ML Computational Biomedical Research Portfolio

Multi-project laboratory of computational biomedical analytics created by Nana Safo-Duker. Each folder is a self-contained workflow that combines statistical modeling, explainable ML, and deep learning for healthcare AI: neurological eye-movement analytics, retinal cardiovascular risk, DNA-sequence gene expression, cancer genomics and radiomics, ultrasound-based liver diagnosis, cell phenotyping from imaging, drug-target and cancer-target discovery, and computational treatment modeling and optimization.

This README provides the cross-project narrative by documenting structure, shared tooling, reproducibility workflow, and expected deliverables.

## Table of Contents
- [About](#about)
- [Portfolio Overview](#portfolio-overview)
- [Repository Layout](#repository-layout)
- [Technology Stack and Tooling Matrix](#technology-stack-and-tooling-matrix)
- [Shared Setup Workflow](#shared-setup-workflow)
- [Workflow Blueprint](#workflow-blueprint)
- [Project Capsules](#project-capsules)
- [Data Sources and Governance](#data-sources-and-governance)
- [Testing and Validation Hooks](#testing-and-validation-hooks)
- [Extensibility Playbook](#extensibility-playbook)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [Contact](#contact)

## About
**Description:** AI/ML computational biomedical portfolio spanning neurology and eye tracking, retinal and medical imaging (including radiomics and ultrasound), cancer genomics and oncology analytics, sequence-based gene expression, cell phenotyping, drug and cancer-target discovery, and treatment optimization workflows.  
**Website:** https://nana-safo-duker.github.io/  
**Topics:** biomedical-ai, healthcare-analytics, brain-disorders, eye-tracking, retinal-imaging, radiomics, ultrasound, liver-disease, cardiovascular-risk, genomics, cancer-genomics, oncology, gene-expression, cell-phenotyping, drug-discovery, bioinformatics, deep-learning, precision-medicine.

## Portfolio Overview
- **Disciplines represented:** digital neurology, medical signal analysis, ophthalmic and radiological image analytics, cardiovascular risk stratification, ultrasound-based hepatology, cancer genomics and multi-omics learning, DNA-sequence models for expression, microscopy/cell phenotyping, drug-target discovery, and computational cancer treatment optimization.
- **Languages and runtimes:** Python 3.10+, R 4.x, Jupyter Notebooks, pip/requirements, Conda where provided.
- **Learning paradigms:** supervised ML (RF, SVM, boosting), statistical hypothesis testing, feature engineering, deep learning (CNN/LSTM and sequence models), and explainability-oriented evaluation.
- **Deliverables:** reproducible notebooks, reusable scripts, trained model artifacts, diagnostics plots, and project-level technical documentation.
- **Operational footprint:** consolidated multi-project repository with standalone folders, each preserving original code structure and commit lineage through subtree imports.

## Repository Layout
Top-level directories (each is an independent project; names match the repository exactly, including spaces where present):

```text
Computational_Biomedical_Research-Portfolio/
├── AI-cancer target identification-drug-discovery/
├── AI-enhanced ultrasound imaging for improved diagnosis of liver diseases/
├── Brain-Disorder-Detection-Through-Eye-Movement/
├── Cardiovascular-Risk-Prediction-from-Retinal-Images/
├── Computational approaches to modelling and optimizing cancer treatment/
├── Deep learning in cancer genomics/
├── Image-based cell phenotyping with deep learning/
├── Machine Learning for Drug Target Identification in Bioinformatics/
├── Predicting cancer outcomes with radiomics and artificial intelligence in radiology/
├── Predicting-Gene-Expression-from-DNA-Sequence-Using-Deep-Learning-Models/
└── README.md
```

Each project generally follows a consistent pattern:
- `data/` or sample-data placeholders (replace for production/research deployment)
- `notebooks/` for exploratory and step-by-step analysis
- `scripts/` or root scripts for repeatable CLI execution
- `results/`, `figures/`, and/or `models/` for experiment outputs and checkpoints
- domain documentation (`README.md`, quick-start files, or methodology notes)

## Technology Stack and Tooling Matrix
| Layer | Tooling | Where Used |
|---|---|---|
| Languages | Python, R | Cross-project implementation and reproducibility |
| Environments | `requirements.txt`, virtual environments, optional Conda | Deterministic setup by project |
| Notebooks | Jupyter (`.ipynb`) | Interactive analysis and experiment walkthroughs |
| ML/DL Libraries | scikit-learn, TensorFlow/Keras, XGBoost/boosting variants, R ML packages | Classification, risk prediction, and sequence modeling |
| Visualization | matplotlib, seaborn, ggplot2, confusion matrix and ROC exports | Diagnostic reporting and model comparison |
| Serialization | `.pkl`, `.h5`, notebook outputs, CSV metrics | Reusable model artifacts and experiment records |
| QA | Repeatable scripts/notebooks, baseline metrics, manual model validation | Regression checks and reproducibility confirmation |

## Shared Setup Workflow
Clone once to access all projects:

```bash
git clone https://github.com/Nana-Safo-Duker/Computational_Biomedical_Research-Portfolio.git
cd Computational_Biomedical_Research-Portfolio
```

Then:
1. Select a project folder and read its local `README.md`.
2. Create an environment (`python -m venv venv` or project-specific setup).
3. Install dependencies from `requirements.txt` or equivalent files.
4. Run notebooks (`jupyter notebook`) or scripts (`python ...`, `Rscript ...`).
5. Store generated outputs in project `results/`/`models/` locations.

> Note: Demo/sample datasets may be synthetic or placeholders. Use licensed, governance-approved datasets for publication or clinical-facing workflows.

## Workflow Blueprint
- **Discovery:** choose a project aligned with your biomedical question (e.g. neurology, cardiovascular or retinal imaging, radiomics, ultrasound, oncology genomics, gene expression from sequence, cell imaging, pharmacology/target ID, treatment optimization).
- **Environment provisioning:** recreate dependencies locally using project lock/setup files.
- **Notebook rehearsal:** execute notebooks end-to-end to validate assumptions and outputs.
- **Script automation:** move to script-based execution for repeatable training and evaluation.
- **Model management:** persist trained artifacts under `models/` and diagnostics under `results/`.
- **Reporting prep:** export core metrics and visual artifacts for reports, papers, or stakeholder review.

## Project Capsules

### 1) Brain-Disorder-Detection-Through-Eye-Movement
**Problem statement:** detect and monitor brain-disorder signals using wearable eye-movement data and statistical/ML pipelines.  
**Highlights:** Python + R implementations, feature extraction for movement dynamics, statistical tests, dimensionality reduction, and classification workflows.  
**Use cases:** neurological screening research, digital biomarker prototyping, longitudinal monitoring studies.

### 2) Cardiovascular-Risk-Prediction-from-Retinal-Images
**Problem statement:** infer cardiovascular risk from retinal image patterns using AI-based visual feature learning.  
**Highlights:** image-centric preprocessing and modeling pipeline, risk classification support, reproducible script/notebook workflow, clinically interpretable evaluation outputs.  
**Use cases:** non-invasive risk stratification research, ophthalmic screening augmentation, preventive cardiology analytics.

### 3) Predicting-Gene-Expression-from-DNA-Sequence-Using-Deep-Learning-Models
**Problem statement:** predict gene expression signatures directly from DNA sequence context using deep learning.  
**Highlights:** sequence encoding pipeline, deep architecture experimentation, performance diagnostics across biological targets, exportable model artifacts.  
**Use cases:** regulatory genomics research, promoter/enhancer signal modeling, precision medicine hypothesis generation.

### 4) AI-cancer target identification-drug-discovery
**Problem statement:** support AI-guided cancer target identification workflows for therapeutic and drug-discovery research.  
**Highlights:** blog-style synthesis plus Python, R, and Jupyter workflows for reproducible analysis.  
**Use cases:** target discovery prototyping, oncology research communication, coursework and transparent methodology demos.

### 5) AI-enhanced ultrasound imaging for improved diagnosis of liver diseases
**Problem statement:** apply ML to ultrasound-derived signals and tasks relevant to liver disease diagnosis (e.g., steatosis grading, fibrosis staging, lesion analysis).  
**Highlights:** multi-algorithm modeling, statistical validation, Python and R implementations, documented methodology.  
**Use cases:** hepatology imaging research, non-invasive diagnostics education, benchmarking ML against conventional readouts.

### 6) Computational approaches to modelling and optimizing cancer treatment
**Problem statement:** model treatment response, dosing, and comparative effectiveness using computational and statistical methods.  
**Highlights:** treatment response prediction motifs, dosing optimization narratives, genomic/clinical visualization, combined ML and pharmacokinetic-style framing.  
**Use cases:** precision oncology methods exploration, simulation-oriented teaching, treatment analytics prototypes.

### 7) Deep learning in cancer genomics
**Problem statement:** analyze cancer genomics with deep learning and classical ML across classification, biomarker discovery, survival, and multi-omics angles.  
**Highlights:** PyTorch/TensorFlow alongside R, preprocessing through evaluation pipelines, linkage to literature (e.g., *Genome Medicine* deep-learning genomics discourse).  
**Use cases:** pan-cancer genomics benchmarking, biomarker discovery exercises, reproducible oncology ML coursework.

### 8) Image-based cell phenotyping with deep learning
**Problem statement:** study deep learning approaches to image-based single-cell or cellular phenotyping.  
**Highlights:** publication-oriented layout with notebooks and scripts in Python and R.  
**Use cases:** computational microscopy tutorials, phenotype classification experiments, open science documentation.

### 9) Machine Learning for Drug Target Identification in Bioinformatics
**Problem statement:** identify and prioritize therapeutic targets using ML on bioinformatics-style features and workflows.  
**Highlights:** end-to-end script and notebook workflows in Python/R with reproducibility-oriented repository hygiene.  
**Use cases:** target discovery education, comparative ML baselines for omics-derived targets.

### 10) Predicting cancer outcomes with radiomics and artificial intelligence in radiology
**Problem statement:** predict cancer patient outcomes from quantitative imaging (radiomics) combined with AI.  
**Highlights:** radiomic feature extraction, statistical testing, predictive modeling, bilingual Python/R analysis paths.  
**Use cases:** radiology AI research, outcome modeling from imaging cohorts, feature interpretability exercises.

## Data Sources and Governance
- Use only datasets with clear licensing and reuse rights.
- Keep PHI/PII and sensitive clinical data outside the repository.
- Store secrets/paths in `.env` or secure config files (gitignored).
- Document provenance, cohort definitions, and preprocessing decisions per project.
- Follow institutional IRB and applicable HIPAA/GDPR requirements where relevant.

## Testing and Validation Hooks
- Re-run core notebooks/scripts with fixed seeds when possible.
- Track baseline metrics (AUC, F1, precision/recall, MAE/RMSE where relevant).
- Version diagnostic outputs (ROC curves, confusion matrices, residual/error plots).
- Add smoke tests for data loading and training/inference pipeline integrity.

## Extensibility Playbook
- Add new biomedical modalities by reusing the existing folder contract (`data`, `notebooks`, `scripts`, `results`, `docs`).
- Factor common preprocessing/evaluation helpers into a shared `common/` package when overlap grows.
- Add model cards and dataset cards for transparency and reproducibility.
- Introduce CI checks for linting, notebook smoke tests, and dependency validation.

## Contributing
1. Create a feature branch: `git checkout -b feature/<feature-name>`
2. Keep changes scoped to a single project unless introducing shared utilities.
3. Update both project-level docs and this root README when scope changes.
4. Validate with notebooks/scripts and include key metrics in PR notes.
5. Submit a pull request with methods, data assumptions, and evaluation summary.

## Roadmap
- Standardize setup files and environment reproducibility across projects.
- Add consistent evaluation report templates for cross-project comparison.
- Introduce lightweight GitHub Actions checks for scripts/notebook execution.
- Expand documentation on data governance and clinical translation boundaries.
- Publish themed releases for neurology, cardiovascular and radiology imaging, oncology genomics, and therapeutic-discovery workflows.

## Contact
Questions, collaboration requests, or demo inquiries: open an issue or connect via https://nana-safo-duker.github.io/.

Also see related repositories under Nana Safo-Duker's profile for companion climate/energy and health analytics portfolios.

**Last Updated**: August 2025.

