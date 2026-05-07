# GitHub Repository Setup Guide

This guide explains how to set up and manage the GitHub repository for this project.

## Initial Repository Setup

### 1. Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name the repository (e.g., `mutation-impact-prediction`)
5. Choose visibility (public or private)
6. **Do NOT** initialize with README, .gitignore, or license (we already have these)
7. Click "Create repository"

### 2. Connect Local Repository to GitHub

```bash
# Navigate to project directory
cd "Mutation Impact and Pathogenicity Prediction"

# Initialize git (if not already done)
git init

# Add remote repository
git remote add origin https://github.com/your-username/mutation-impact-prediction.git

# Verify remote
git remote -v
```

### 3. Initial Commit and Push

```bash
# Add all files
git add .

# Commit
git commit -m "Initial commit: Mutation Impact and Pathogenicity Prediction project"

# Push to GitHub
git push -u origin main
```

**Note**: If your default branch is `master` instead of `main`:
```bash
# Rename branch to main
git branch -M main

# Push to main
git push -u origin main
```

## Repository Structure on GitHub

After pushing, your GitHub repository should have:

```
mutation-impact-prediction/
├── .gitignore
├── .gitattributes
├── LICENSE
├── README.md
├── CONTRIBUTING.md
├── SETUP_GUIDE.md
├── requirements.txt
├── environment.yml
├── R_requirements.R
├── data/
│   └── genomics_data.csv
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_loader.R
│   ├── models.py
│   ├── models.R
│   ├── main.py
│   └── main.R
├── notebooks/
│   ├── mutation_prediction_python.ipynb
│   └── mutation_prediction_R.ipynb
├── models/
├── results/
├── docs/
│   └── GITHUB_SETUP.md
└── tests/
```

## GitHub Repository Settings

### 1. Repository Description

Add a description: "Machine learning project for predicting functional impact of mutations in genomic sequences"

### 2. Topics

Add relevant topics:
- `machine-learning`
- `bioinformatics`
- `genomics`
- `mutation-prediction`
- `python`
- `r`
- `precision-medicine`

### 3. Website (Optional)

If you have a project website, add it in the repository settings.

### 4. Branch Protection (Recommended)

1. Go to Settings → Branches
2. Add rule for `main` branch
3. Enable:
   - Require pull request reviews
   - Require status checks to pass
   - Require branches to be up to date

## GitHub Actions (Optional)

Create `.github/workflows/ci.yml` for continuous integration:

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python -m pytest tests/
```

## Releases

### Creating a Release

1. Go to Releases → Draft a new release
2. Choose a tag (e.g., `v1.0.0`)
3. Add release title and description
4. Attach any relevant files
5. Publish release

### Version Tagging

```bash
# Create and push a tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

## Collaboration

### Adding Collaborators

1. Go to Settings → Collaborators
2. Add collaborators by username or email
3. Choose permission level (Read, Write, or Admin)

### Forking and Pull Requests

1. Fork the repository
2. Clone your fork
3. Create a branch for your changes
4. Make changes and commit
5. Push to your fork
6. Create a pull request on GitHub

## Documentation on GitHub

### README.md

The README.md file will be automatically displayed on the repository homepage.

### GitHub Pages (Optional)

1. Go to Settings → Pages
2. Select source branch (e.g., `main` or `docs`)
3. Choose folder (e.g., `/docs` or `/root`)
4. Save

## Best Practices

1. **Commit Messages**: Use clear, descriptive commit messages
2. **Branch Naming**: Use descriptive branch names (e.g., `feature/new-model`, `fix/data-loader`)
3. **Pull Requests**: Provide detailed descriptions in PRs
4. **Issues**: Use issues to track bugs and feature requests
5. **Labels**: Use labels to categorize issues and PRs
6. **Milestones**: Use milestones to track project progress

## Security

### Secrets Management

Never commit sensitive information:
- API keys
- Passwords
- Personal data
- Credentials

Use GitHub Secrets for sensitive data in workflows.

### .gitignore

Ensure `.gitignore` is properly configured to exclude:
- Virtual environments
- Model files (if large)
- Sensitive data
- IDE files
- OS files

## Maintenance

### Regular Updates

- Update dependencies regularly
- Keep documentation up to date
- Respond to issues and PRs
- Review and merge contributions

### Archive (If Needed)

If the project is no longer maintained:
1. Update README with archive notice
2. Archive the repository (Settings → Archive repository)

## Resources

- [GitHub Documentation](https://docs.github.com/)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Markdown Guide](https://guides.github.com/features/mastering-markdown/)

## Support

For questions about GitHub setup:
- Check [GitHub Help](https://help.github.com/)
- Open an issue on the repository
- Contact the repository maintainers


