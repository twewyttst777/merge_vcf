#!/bin/bash


mkdir -p matching
mkdir -p unmatching

for FILE in [your_path]/*.HC_All.vcf;
do
	PREFIX=${FILE%%.*}
	NOPATH="${PREFIX##*/}"
	echo $NOPATH
	FILE_MUTECT="${PREFIX}_MuTect_All_Filtered.vcf"
	FILE_SNVS="${PREFIX}.strelka.passed.somatic.snvs.vcf"
	FILE_INDELS="${PREFIX}.strelka.passed.somatic.indels.vcf"
	python3 main.py -i $FILE_SNVS -m $FILE_MUTECT -o "${NOPATH}.MuTect_Strelka-snvs.vcf" 
	python3 main.py -i $FILE_INDELS -m $FILE_MUTECT -o "${NOPATH}.MuTect_Strelka-indels.vcf" 
done


