#!/bin/bash
# Author: Carmina Barberena Jonas
# Description:
# This script calculates allele frequencies and performs Generalized Linear Model (GLM) analysis for biomedical variants across all chromosomes (1-22) using PLINK and an R script. It processes PLINK data with population-specific clustering information to compute allele frequencies, and subsequently applies GLM analysis to identify significant associations. The script combines all chromosome-specific results into a single output file for comprehensive analysis.


# Path to PLINK files (update according to data location)
plink_data_dir="ALl_Bioemdical_maf"

# Directory containing per-individual clustering files by chromosome
clusters_dir="../Ejemplos_puntuales/clusters_MXB_perindividual"

# Base name for output files
output_base="ALl_Bioemdical_Freq_Int"

# Loop through chromosomes 1 to 22
for chrom in {1..22}
do
  # Generate output filename for the current chromosome
  output_file="temp${output_base}_chr${chrom}"
  
   # Run PLINK to calculate allele frequencies
  plink --bfile "$plink_data_dir" \
        --chr $chrom \
        --within "$clusters_dir" \
        --freq \
        --out "$output_file"
done

# Execute the R script to calculate GLM results for each chromosome

# Loop to run the R script with different chromosome frequency files as input

for i in {1..22}
do
   # Build the filename for the frequency file
  frq_strat_file="tempALl_Bioemdical_Freq_Int_chr${i}.frq.strat"
  
   # Set output filename for the GLM results
  output_file="Gml_results_biomedical_chr${i}.csv"
  
   # Run the R script with the frequency file and output file as arguments
  Rscript ../../Scrips/glm_analysis.R $frq_strat_file $output_file &
  
done
# Combine all chromosome-specific GLM results into a single CSV file
 cat Gml_results_biomedical_chr*.csv >Gml_results_biomedical_allchr.csv


