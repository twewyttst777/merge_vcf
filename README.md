# About

Script to output the union of two vcf files.

main.py can be run with command line arguments to combine two vcf files.

> python3 main.py -i FILE_1 -m FILE_2 -o OUTFILE

This will scan the contents of FILE_1 and output the entries in FILE_2 that share the same chromosomes and starting position.

merge_vcf.sh is a script for batch runs; pass a directory as input and it will run every file in it. Will require modification to run as desired.

NOTE: The bash script is set up to run twice; for a file filtered for indels and one filtered for SNVs. If your files are structured similarly, you may need to combine them using bcftools.

## Installation

> pip3 install -r requirements.txt

Will install required files. You should run this in a [virtual environment](https://docs.python.org/3/library/venv.html).
