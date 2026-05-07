# Updating R on Windows

## Method 1: Download and Install New Version (Recommended)

### Step 1: Download R 4.5.2

1. Go to the [CRAN website](https://cran.r-project.org/)
2. Click on "Download R for Windows"
3. Click on "base"
4. Download "Download R 4.5.2 for Windows" (or latest version)
5. Run the installer

### Step 2: Install R 4.5.2

1. Run the downloaded installer (`.exe` file)
2. Follow the installation wizard
3. **Important**: Choose the same installation directory as your current R installation (usually `C:\Program Files\R\R-4.x.x`)
4. The installer will detect the old version and offer to update it

### Step 3: Update RStudio (if using)

1. Open RStudio
2. Go to **Help** → **Check for Updates**
3. If an update is available, download and install it
4. RStudio will automatically detect the new R version

### Step 4: Verify Installation

Open R or RStudio and check the version:

```r
R.version.string
# Should show: "R version 4.5.2 (YYYY-MM-DD)"
```

### Step 5: Reinstall Packages

After updating R, you'll need to reinstall your packages. Here are options:

#### Option A: Manual Reinstallation

```r
# Install required packages for this project
install.packages(c("dplyr", "ggplot2", "gridExtra", "corrplot", "stringr", "rmarkdown"))
```

#### Option B: Use installr Package (Automated)

```r
# Install installr package
install.packages("installr")

# Load library
library(installr)

# Update R (this will guide you through the process)
updateR()

# After R is updated, reinstall packages
installr::install.packages(c("dplyr", "ggplot2", "gridExtra", "corrplot", "stringr", "rmarkdown"))
```

#### Option C: Migrate Packages (Advanced)

If you want to copy packages from the old version:

1. Find your old R library location:
   ```r
   .libPaths()
   # Usually: "C:/Users/YourName/Documents/R/win-library/4.5"
   ```

2. Copy packages to new library location, or use:
   ```r
   # In OLD R version
   old.packages <- installed.packages()
   save(old.packages, file = "old_packages.RData")
   
   # In NEW R version
   load("old_packages.RData")
   install.packages(old.packages[, "Package"])
   ```

## Method 2: Using installr Package (Easier)

This method automates the update process:

```r
# Install installr if not already installed
if (!requireNamespace("installr", quietly = TRUE)) {
  install.packages("installr")
}

# Load installr
library(installr)

# Update R (interactive process)
updateR()

# After update, reinstall packages
installr::install.packages(c("dplyr", "ggplot2", "gridExtra", "corrplot", "stringr", "rmarkdown"))
```

## After Updating

1. **Verify R version**:
   ```r
   R.version.string
   ```

2. **Reinstall project packages**:
   ```r
   install.packages(c("dplyr", "ggplot2", "gridExtra", "corrplot", "stringr", "rmarkdown"))
   ```

3. **Test the project**:
   ```r
   source("src/variant_identification.R")
   source("src/variant_analysis.R")
   ```

## Troubleshooting

### Issue: RStudio doesn't detect new R version

**Solution**:
1. Open RStudio
2. Go to **Tools** → **Global Options** → **General**
3. Under "R version", click "Change"
4. Select the new R installation directory
5. Click "OK" and restart RStudio

### Issue: Packages not found after update

**Solution**: Reinstall all packages (see Step 5 above)

### Issue: Old R version still running

**Solution**:
1. Close all R and RStudio windows
2. Restart RStudio
3. Check version with `R.version.string`

## Notes

- **Backup**: Consider backing up your `.Rprofile` and `.Renviron` files before updating
- **Library Location**: Your user library is usually at `C:\Users\YourName\Documents\R\win-library\4.x`
- **Multiple Versions**: You can have multiple R versions installed side-by-side, but RStudio will use one at a time

## Current Project Requirements

This project requires:
- **R version**: 4.0+ (4.5.2 recommended)
- **Required packages**: dplyr, ggplot2, gridExtra, corrplot, stringr, rmarkdown
- **Optional packages**: Biostrings (via BiocManager)

