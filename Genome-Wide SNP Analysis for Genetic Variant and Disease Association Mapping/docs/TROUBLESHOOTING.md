# Troubleshooting Guide

## Common Issues and Solutions

### R Package Loading Messages

#### Message: "The following objects are masked from 'package:stats': filter, lag"

**Problem**: This is NOT an error - it's a normal informational message.

**Explanation**: When `dplyr` loads, it provides functions with the same names as some base R functions. The message is just informing you that `dplyr`'s versions will be used by default.

**Solutions**:
- **No action needed** - this is expected behavior
- If you need the original functions, use package prefixes:
  ```r
  stats::filter()  # Original stats::filter()
  dplyr::filter()  # dplyr's filter() (default)
  ```

### R Markdown / Pandoc Issues

#### Error: "pandoc version 1.12.3 or higher is required and was not found"

**Problem**: Pandoc is not installed or not found in your system PATH.

**Solutions**:

1. **Install Pandoc**:
   - **Windows**: 
     - Download from [Pandoc Releases](https://github.com/jgm/pandoc/releases/latest)
     - Install the `.msi` installer
     - Restart R/RStudio after installation
   
   - **macOS**:
     ```bash
     brew install pandoc
     ```
     Or download from the releases page.
   
   - **Linux (Ubuntu/Debian)**:
     ```bash
     sudo apt-get install pandoc
     ```
   
   - **Linux (Fedora/RHEL)**:
     ```bash
     sudo dnf install pandoc
     ```

2. **Verify Installation**:
   ```r
   rmarkdown::pandoc_available()
   rmarkdown::pandoc_version()
   ```

3. **Alternative**: Use R scripts directly instead of R Markdown:
   ```r
   # Run R scripts directly (no Pandoc needed)
   source("src/variant_identification.R")
   source("src/variant_analysis.R")
   main()
   ```

### Python Import Errors

#### Error: "ModuleNotFoundError: No module named 'variant_identification'"

**Problem**: Python can't find the module because the path is incorrect.

**Solutions**:

1. **Run from project root directory**:
   ```bash
   cd "Genetic Variants and Disease Association_(SNPs)"
   python src/variant_analysis.py
   ```

2. **In Jupyter Notebook**, ensure the path is correct:
   ```python
   import sys
   sys.path.append('../src')  # Adjust path if needed
   ```

3. **Install package in development mode** (optional):
   ```bash
   pip install -e .
   ```

### R Source File Errors

#### Error: "cannot open file 'src/variant_identification.R'"

**Problem**: Working directory is incorrect.

**Solutions**:

1. **Set working directory in R**:
   ```r
   setwd("path/to/Genetic Variants and Disease Association_(SNPs)")
   ```

2. **Use absolute paths**:
   ```r
   source("C:/full/path/to/src/variant_identification.R")
   ```

3. **Run from project root**:
   ```bash
   cd "Genetic Variants and Disease Association_(SNPs)"
   Rscript src/variant_analysis.R
   ```

### Data File Not Found

#### Error: "FileNotFoundError: data/genomics_data.csv"

**Problem**: Data file is missing or path is incorrect.

**Solutions**:

1. **Verify data file exists**:
   ```bash
   ls data/genomics_data.csv  # Linux/Mac
   dir data\genomics_data.csv  # Windows
   ```

2. **Check working directory**:
   - Ensure you're running scripts from the project root
   - Or update paths in the scripts to match your location

3. **Verify file was moved correctly**:
   - The file should be in `data/genomics_data.csv`
   - If it's still in the root, move it: `mv genomics_data.csv data/`

### Memory Issues with Large Datasets

**Problem**: Running out of memory when processing large datasets.

**Solutions**:

1. **Process in batches**:
   - Modify the code to process sequences in chunks
   - Save intermediate results

2. **Use more efficient data structures**:
   - Consider using generators in Python
   - Use data.table in R for large datasets

3. **Increase available memory**:
   - Close other applications
   - Use a machine with more RAM

### Visualization Errors

#### Error: "Figure size too large" or display issues

**Solutions**:

1. **Adjust figure size**:
   ```python
   plt.figure(figsize=(10, 6))  # Smaller size
   ```

2. **Save instead of displaying**:
   ```python
   plt.savefig('output.png', dpi=150, bbox_inches='tight')
   plt.close()  # Free memory
   ```

### Package Installation Issues

#### Python: "pip install fails"

**Solutions**:

1. **Update pip**:
   ```bash
   python -m pip install --upgrade pip
   ```

2. **Use virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

#### R: "Package installation fails"

**Solutions**:

1. **Update R packages**:
   ```r
   update.packages()
   ```

2. **Install from CRAN**:
   ```r
   install.packages("package_name", repos="https://cran.rstudio.com/")
   ```

3. **Check R version** (should be 4.0+, 4.5.2 recommended):
   ```r
   R.version
   R.version.string
   ```
   
   **To update R**: See [UPDATE_R.md](UPDATE_R.md) for detailed update instructions.

### Git Issues

#### Error: "fatal: not a git repository"

**Solution**:
```bash
git init
git add .
git commit -m "Initial commit"
```

### Path Issues on Windows

**Problem**: Path separators and spaces in directory names cause issues.

**Solutions**:

1. **Use raw strings in Python**:
   ```python
   path = r"C:\Users\fresh\Desktop\AI-ML BIOINFORMATICS_&_PRECISION MEDCINE\..."
   ```

2. **Use forward slashes** (works on Windows too):
   ```python
   path = "data/genomics_data.csv"
   ```

3. **Quote paths with spaces**:
   ```bash
   cd "Genetic Variants and Disease Association_(SNPs)"
   ```

## Getting Help

If you encounter issues not covered here:

1. Check the error message carefully
2. Verify all dependencies are installed
3. Ensure you're in the correct directory
4. Check file paths and permissions
5. Review the README.md for usage instructions
6. Open an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - System information (OS, Python/R versions)
   - Relevant code snippets

