# Contributing to AI-Enhanced Ultrasound Imaging for Liver Disease Diagnosis

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs. actual behavior
- Environment details (OS, Python version, etc.)

### Suggesting Enhancements

To suggest new features:
- Open an issue describing the enhancement
- Explain why it would be valuable
- Provide possible implementation approaches if available

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Write/update tests** for your changes
5. **Ensure code quality**:
   - Follow PEP 8 style guide for Python
   - Run `black` for code formatting
   - Run `flake8` for linting
   - Add docstrings to functions and classes
6. **Commit changes**: Use clear, descriptive commit messages
7. **Push to your fork**: `git push origin feature/your-feature-name`
8. **Create a Pull Request**

### Pull Request Process

1. Update documentation for any new features or changes
2. Ensure all tests pass
3. Get code review from maintainers
4. Address any feedback or requested changes

## Development Setup

```bash
# Clone the repository
git clone https://github.com/username/ai-liver-ultrasound.git
cd ai-liver-ultrasound

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -e ".[dev]"
```

## Coding Standards

### Python Style

- Follow PEP 8
- Maximum line length: 100 characters
- Use type hints where appropriate
- Write comprehensive docstrings

### Example:

```python
def process_ultrasound_image(
    image: np.ndarray,
    normalize: bool = True
) -> np.ndarray:
    """
    Process ultrasound image for AI analysis.
    
    Parameters:
    -----------
    image : np.ndarray
        Input ultrasound image
    normalize : bool
        Whether to normalize pixel values
        
    Returns:
    --------
    np.ndarray
        Processed image
    """
    # Implementation here
    pass
```

### Documentation

- Update README.md for user-facing changes
- Add docstrings to all public functions
- Include examples in docstrings where helpful

### Testing

- Write unit tests for new functionality
- Aim for >80% code coverage
- Use descriptive test names
- Test edge cases

## Research Ethics

When contributing medical imaging analysis code:
- Respect patient privacy and data confidentiality
- Follow HIPAA and GDPR guidelines
- Use only de-identified data for examples
- Clearly document data sources

## Questions?

Open an issue or contact the maintainers.

Thank you for contributing! 🎉

