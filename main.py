from collections import Counter
from statistics import median
import vcf, sys
import argparse
import matplotlib.pyplot as plt 
import random
import numpy as np
import pandas as pd
import os.path
import csv
import re, sys

af_filter_level = .1

#TODO: Can I make this more pythony?

def double_genotype(f_record):
    #TODO: Check this one liner
    #Probably not worth it, this is pretty fast anyways.
    #return Counter(for sample in f_record.samples).values().count(2) == 0
    gt = []
    for sample in f_record.samples:
        if sample['GT'] in gt:
            return 0
        if sample['GT'] == './.':
            return 0
        gt.append(sample['GT'])
    return 1

def af_filter(f_record):
    for sample in f_record.samples:
        if sample['DP'] and sample['AD'][1]/sample['DP'] < af_filter_level:
            return 0
    return 1

def double_filter(f_record):
    return double_genotype(f_record) and af_filter(f_record)

def filter_str_builder(gq, dp):
    #TODO: Make this more expandable
    filter_str = "MIN(FMT/GQ) >= {0} && MIN(FMT/DP) > {1}".format(gq, dp)
    print(filter_str)
    return filter_str

def custom_filters(ifile, ofile):
    #We use pyvcf to get an iterable for the file
    #    and then use itertools filter to filter them
    #Albeit, perhaps this should've just been using the pyvcf filter tool anyways.
    #TODO: Test performance of this
    #       Addendum: Performance is very good, it's just the io that sucks
    #       But I'm bad at IO unfortunately
    vcf_reader = vcf.Reader(filename=ifile)
    #Is an iterator
    filtered_vcf = filter(double_filter, vcf_reader)
    reader_template = vcf.Reader(filename='out.vcf')
    vcf_writer = vcf.Writer(open(ofile, 'w'), reader_template)
    i = 0
    for record in filtered_vcf:
        #This is the bottleneck
        vcf_writer.write_record(record)
        if i == 500:
            vcf_writer.flush()
            i=0
        i += 1
    vcf_writer.close()

def match_positions(input_vcf1, input_vcf2, outfile, write_out):

    vcf_reader_1=vcf.Reader(filename=input_vcf1)
    vcf_reader_2=vcf.Reader(filename=input_vcf2)


    print("Begin matching.")
    print("Reading File 2")

    pos_mem_2 = []

    for record in vcf_reader_2:
        if (record.FILTER == [] or record.FILTER == ["HighDepth"]) and record.POS not in pos_mem_2:
            pos_mem_2.append([record.POS,record.CHROM])
    print(str(len(pos_mem_2)))

    reader_template = vcf.Reader(filename=input_vcf1)
    matching_file = 'matching/' + outfile
    unmatching_file = 'unmatching/' + outfile
    if write_out:
        vcf_writer = vcf.Writer(open(matching_file, 'w'), reader_template)
        vcf_writer2 = vcf.Writer(open(unmatching_file, 'w'), reader_template)
    
    matching_num = 0
    i = 0
    j = 0

    print("Reading File 1")

    pos_mem_1 = 0

    for record in vcf_reader_1:
        pos_mem_1 += 1
        if ([record.POS, record.CHROM]) in pos_mem_2 and (record.FILTER == [] or record.FILTER ==["HighDepth"]):
            if write_out:
                vcf_writer.write_record(record)
                if i == 500:
                    vcf_writer.flush()
                    i = 0
                i += 1
            matching_num+=1
        else:
            if write_out:
                vcf_writer2.write_record(record)
                if j == 500:
                    vcf_writer2.flush()
                    j = 0
                j += 1
    if write_out:
        vcf_writer.close()
        vcf_writer2.close()
    matching_data = {
        "percent_1":  matching_num/pos_mem_1,
        "percent_2":  matching_num/len(pos_mem_2)
    }

    return matching_data

def default_mode(input_file, output_file, matching_file):
    matching_data = match_positions(input_file, matching_file, output_file, True)
    print("Match %1: {0}\nMatch %2: {1}".format(matching_data['percent_1'], matching_data['percent_2']))

def calculate_af(t_alt, t_depth, reflect_graph):
    #if t_alt < 15 or t_depth < 15:
    #    return 0 
    if not reflect_graph:
        return t_alt/t_depth
    AF = t_alt/t_depth
    print(str(t_depth))
    if AF == 0 or AF == 1:
        return 1
    if AF > .5:
        return 1 - AF
    return AF

def merge_csvs(input_file1, input_file2, output_file):
    on_list = ['Chromosome', 'Start_Position']
    df1 = pd.read_csv(input_file1, header=1, sep='\t')
    df2 = pd.read_csv(input_file2, header=1, sep='\t')

    df1_len = len(df1)
    df2_len = len(df2)

    df1['Start_Position'] = df1.Start_Position.astype(str, errors='raise')
    df2['Start_Position'] = df2.Start_Position.astype(str, errors='raise')

    merged_df = pd.merge(df1, df2, how='inner', on=on_list, suffixes = ["_Dragen","_MuTect"])
    merged_df.drop_duplicates(subset=on_list, keep='first')

    combined_len = len(merged_df) 

    merged_df.to_csv(output_file, sep='\t', index=False)

    print(f'{output_file},{df1_len},{df2_len},{combined_len}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input_file", help="Input File")
    #parser.add_argument("-j", "--input_file_graph", help="Temporary Input File for graphing")
    parser.add_argument("-o", "--output_file", help="Intermediary output file") #Set this flag only if you need to do the same type haplo filter again
    parser.add_argument("-m", "--matching_file", help="File to compare to")
    parser.add_argument("-c", "--merge_csv", action="store_true", help="Run with csvs instead of vcf")

    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    matching_file = args.matching_file
    merge_csv = args.merge_csv

    if merge_csv:
        merge_csvs(input_file, matching_file, output_file)
        exit()
            
    
    default_mode(input_file, output_file, matching_file)
