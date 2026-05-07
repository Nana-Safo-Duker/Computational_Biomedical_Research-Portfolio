"""
Mutation Impact and Pathogenicity Prediction Package
"""

from .data_loader import GenomicsDataLoader
from .models import MutationPredictor, ModelEnsemble

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    'GenomicsDataLoader',
    'MutationPredictor',
    'ModelEnsemble'
]


