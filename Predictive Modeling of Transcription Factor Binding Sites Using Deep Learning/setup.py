"""
Setup script for Transcription Factor Binding Prediction project.
This script helps set up the project environment and verify data.
"""

import os
import sys

def create_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        'data',
        'scripts/python',
        'scripts/r',
        'notebooks/python',
        'notebooks/r',
        'models',
        'results',
        'docs'
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            if os.path.exists(directory):
                print(f"✓ Directory exists: {directory}")
        except OSError as e:
            if e.errno != 17:  # File exists error
                print(f"✗ Error creating directory {directory}: {e}")
            else:
                print(f"✓ Directory exists: {directory}")

def check_data_file():
    """Check if data file exists."""
    data_path = 'data/genomics_data.csv'
    if os.path.exists(data_path):
        print(f"✓ Data file found: {data_path}")
        return True
    else:
        print(f"✗ Data file not found: {data_path}")
        print("  Please place your genomics_data.csv file in the data/ directory")
        return False

def check_dependencies():
    """Check if required Python packages are installed."""
    required_packages = [
        'numpy', 'pandas', 'scikit-learn', 'xgboost',
        'tensorflow', 'matplotlib', 'seaborn'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install them using: pip install -r requirements.txt")
        return False
    return True

def main():
    """Main setup function."""
    print("=" * 60)
    print("Transcription Factor Binding Prediction - Setup")
    print("=" * 60)
    print()
    
    print("1. Creating directories...")
    create_directories()
    print()
    
    print("2. Checking data file...")
    data_exists = check_data_file()
    print()
    
    print("3. Checking dependencies...")
    deps_ok = check_dependencies()
    print()
    
    print("=" * 60)
    if data_exists and deps_ok:
        print("✓ Setup complete! You can now run the scripts.")
    else:
        print("⚠ Setup incomplete. Please address the issues above.")
    print("=" * 60)

if __name__ == '__main__':
    main()

