# Data Directory

Place your `genomics_data.csv` file in this directory.

## Data Format

The CSV file should have the following structure:

```csv
Sequences,Labels
CCGAGGGCTATGGTTTGGAAGTTAGAACCCTGGGGCTTCTCGCGGACACC,0
GAGTTTATATGGCGCGAGCCTAGTGGTTTTTGTACTTGTTTGTCGCGTCG,0
GTCCACGACCGAACTCCCACCTTGACCGCAGAGGTACCACCAGAGCCCTG,1
...
```

### Columns:
- **Sequences**: DNA sequences (typically 50 nucleotides long)
- **Labels**: Binary labels (0 = no TF binding, 1 = TF binding)

## Dataset License

Please refer to the main README.md for dataset license information and attribution requirements.

