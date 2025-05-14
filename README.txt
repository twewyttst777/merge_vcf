# VCF Position Matcher / Merger (specifically designed for Mutect2 and Strelka VCF merging)

Author: Timothy Okitsu  
Lab: Chih-Lin Hsieh  
Associated Study: *High-depth Whole Genome Sequencing of Single Human Colon Crypts Uncovers New View on Crypt Clonality*  

## Overview

This Python script is designed to facilitate comparison and filtering of genomic variant call files (VCFs) generated from single colon crypt sequencing data. It performs two major functions:

1. **VCF Position Matching**: Identifies variants with shared chromosome and position entries across two VCF files. Outputs both matched and unmatched records.
2. **CSV Variant Table Merging**: Merges annotated variant tables
from CSV or MAF files (e.g., from Strelka and MuTect2 workflows) into a
unified table for downstream analysis. Outputs only matched records.

---

## Table of Contents

- [Usage](#usage)
- [Modes](#modes)
- [Output](#output)
- [Installation](#installation)
- [Directory Structure](#directory-structure)
- [Batch Processing](#batch-processing)
- [License](#license)

---

## Usage

```bash
python3 main.py -i FILE_1.vcf -m FILE_2.vcf -o OUTPUT.vcf
```

This will compare `FILE_1.vcf` against `FILE_2.vcf` and:
- Write **matched variants** to `matching/OUTPUT.vcf`
- Write **unmatched variants** to `unmatching/OUTPUT.vcf`
- Print match statistics as fractions of each file's size

To merge annotated variant tables from TSV/CSV:
```bash
python3 main.py -i FILE_1.tsv -m FILE_2.tsv -o MERGED_OUTPUT.tsv -c
```

---

## Modes

### VCF Matching Mode (Default)

- Compares VCF files by chromosome and position.
- Ignores records with filters except for `HighDepth`.
- Writes matched and unmatched records to separate output files.
- Provides summary statistics on overlap between the two files.

### CSV Merge Mode (`-c` flag)

- Performs inner join on `Chromosome` and `Start_Position` fields, outputting
  the union of the two fields.
- Requires header rows starting from row 2 (i.e., `header=1` in `pandas.read_csv`).
- Output is a tab-separated file for integrated variant comparison.

---

## Output

| File Location           | Content Description                            |
|-------------------------|-------------------------------------------------|
| `matching/OUTPUT.vcf`   | Variants present in both input VCFs             |
| `unmatching/OUTPUT.vcf` | Variants unique to the first input VCF          |
| `MERGED_OUTPUT.tsv`     | Merged variant table (CSV mode)                 |

---

## Installation

It is recommended to use a Python virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Required packages (as defined in `requirements.txt`) include:
- `PyVCF`
- `pandas`
- `matplotlib`
- `numpy`

---

## Directory Structure

Before running, ensure the following subdirectories exist:
```
project/
├── main.py
├── matching/
├── unmatching/
├── example.sh
├── requirements.txt
```

You can create missing folders with:
```bash
mkdir -p matching unmatching
```

---

## Batch Processing

The included `example.sh` script automates comparisons over a directory of VCF files. It assumes filenames are formatted in a consistent way (e.g., to distinguish SNVs and indels). You may need to customize this script for your dataset structure.

If variants are filtered into separate files (e.g., SNVs and indels), results may be merged using tools such as [`bcftools merge`](https://samtools.github.io/bcftools/bcftools.html).

---

## License

This code is intended for academic research use and is provided without warranty. Please cite the associated manuscript if used in published work.
