"""
Setup script for AI-Enhanced Ultrasound Imaging for Liver Disease Diagnosis
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name="ai-liver-ultrasound",
    version="1.0.0",
    author="Research Team",
    author_email="research@example.com",
    description="AI-enhanced ultrasound imaging for improved diagnosis of liver diseases",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/ai-liver-ultrasound",
    packages=find_packages(exclude=['tests', 'docs', 'data', 'notebooks']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scipy>=1.7.0",
        "torch>=1.12.0",
        "torchvision>=0.13.0",
        "opencv-python>=4.5.0",
        "Pillow>=9.0.0",
        "scikit-learn>=1.0.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "jupyter>=1.0.0",
        "tqdm>=4.63.0",
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
        ],
        'medical': [
            'pydicom>=2.3.0',
            'nibabel>=3.2.0',
            'SimpleITK>=2.2.0',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

