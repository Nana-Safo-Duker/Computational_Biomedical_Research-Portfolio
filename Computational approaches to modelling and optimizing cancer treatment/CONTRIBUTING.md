# Contributing to Cancer Treatment Optimization

Thank you for your interest in contributing to this project! We welcome contributions from the community.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the issue tracker
2. Create a new issue with a clear title and description
3. Include steps to reproduce the issue (if applicable)
4. Attach relevant code or data (if appropriate)

### Contributing Code

1. **Fork the repository** to your GitHub account

2. **Create a branch** from the main branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**:
   - Follow the coding standards (see below)
   - Write clear, commented code
   - Add tests if applicable
   - Update documentation

4. **Commit your changes**:
   ```bash
   git commit -m "Add: Description of your feature"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

### Coding Standards

#### Python

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Maximum line length: 100 characters
- Use type hints where appropriate

Example:
```python
def calculate_score(data: pd.DataFrame, weights: dict) -> float:
    """
    Calculate weighted score from data.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Input data with features
    weights : dict
        Weights for each feature
        
    Returns:
    --------
    float
        Weighted score
    """
    return (data * weights).sum()
```

#### R

- Follow the tidyverse style guide
- Use clear, descriptive variable names
- Add comments for complex logic
- Use consistent indentation (2 spaces)

Example:
```r
#' Calculate treatment response rate
#'
#' @param data Data frame with treatment outcomes
#' @return Numeric response rate
calculate_response_rate <- function(data) {
  return(sum(data$responder) / nrow(data))
}
```

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Welcome newcomers and help them learn

### Review Process

1. Pull requests will be reviewed by maintainers
2. We may request changes or ask questions
3. Once approved, your changes will be merged
4. Thank you for contributing!

## Areas for Contribution

We're particularly interested in contributions to:

- **New machine learning models**: Additional algorithms for treatment prediction
- **Optimization methods**: Improved dosing optimization algorithms
- **Statistical methods**: Additional analysis techniques
- **Visualizations**: Better plots and interactive displays
- **Documentation**: Tutorials, guides, and examples
- **Testing**: Unit tests and integration tests
- **Performance**: Code optimization and speed improvements

## Questions?

If you have questions about contributing:
- Open an issue with the "question" label
- Check existing documentation
- Review closed issues for similar questions

---

**Thank you for contributing to the Cancer Treatment Optimization project!**

