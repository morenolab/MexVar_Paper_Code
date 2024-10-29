# MexVar Paper Code
This repository contains custom-make code used in the analysis and creation of the paper: MexVar database for expanding Latin American precision medicine illustrates striking clinical genetic variation in the Mexican Biobank. Authored by Carmina Barberena-Jonas, PhD student at MorenoLab. Currently under review. 

## Code available 

This repository provides the following code resources:

- GLM Analysis: A set of scripts to perform Generalized Linear Model (GLM) analysis. This includes:

  -  An R script (glm_analysis.R) to run the GLM on a specified SNP.
  -  A shell script (run_glm.sh) to parallelize the process and execute the GLM analysis across all SNPs.
    
- Local Ancestry Masking: A script that masks genotypes in a VCF file based on local ancestry information, encoding masked genotypes as missing values. This is used for ancestry-specific analyses, allowing for accurate allele frequency calculations within defined ancestry segments.
 
## Contact Information 

For any questions or further information, please contact Carmina Barberena-Jonas at carmina.barberena@cinvestav.mx.



