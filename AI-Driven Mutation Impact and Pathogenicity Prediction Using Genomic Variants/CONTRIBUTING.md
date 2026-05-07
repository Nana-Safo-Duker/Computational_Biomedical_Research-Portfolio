# Contributing to Mutation Impact and Pathogenicity Prediction

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion for improvement, please open an issue on GitHub with:

- A clear, descriptive title
- Detailed description of the issue or suggestion
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Environment details (OS, Python/R versions, etc.)

### Contributing Code

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/mutation-impact-prediction.git
   cd mutation-impact-prediction
   ```

3. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes** following the coding standards

5. **Test your changes**:
   ```bash
   # Python tests
   python -m pytest tests/
   
   # R tests (if applicable)
   Rscript tests/test_models.R
   ```

6. **Commit your changes** with clear messages:
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

7. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request** on GitHub

## Coding Standards

### Python

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions focused and single-purpose
- Use meaningful variable names

Example:
```python
def encode_sequences(sequences: List[str], method: str = 'onehot') -> np.ndarray:
    """
    Encode DNA sequences to numerical features.
    
    Args:
        sequences: List of DNA sequences
        method: Encoding method ('onehot', 'kmer', 'numerical')
        
    Returns:
        Encoded sequences as numpy array
    """
    # Implementation
    pass
```

### R

- Follow Google R Style Guide
- Use meaningful variable names
- Add comments for complex logic
- Document functions with roxygen2-style comments

Example:
```r
#' Encode DNA sequences
#' 
#' @param sequences Vector of DNA sequences
#' @param method Encoding method ('onehot', 'kmer', 'numerical')
#' @return Matrix of encoded sequences
encode_sequences <- function(sequences, method = 'onehot') {
  # Implementation
}
```

## Testing

- Write unit tests for new features
- Ensure all tests pass before submitting PR
- Aim for high code coverage
- Test edge cases and error handling

## Documentation

- Update README.md if adding new features
- Add docstrings/comments to code
- Update this CONTRIBUTING.md if needed
- Include examples in documentation

## Pull Request Process

1. Ensure your code follows the coding standards
2. Update documentation as needed
3. Add tests for new features
4. Ensure all tests pass
5. Update CHANGELOG.md (if applicable)
6. Request review from maintainers

## Questions?

If you have questions, please open an issue or contact the maintainers.

Thank you for contributing!


