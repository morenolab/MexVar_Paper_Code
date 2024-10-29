# Author: Carmina Barberena Jonas 
#Code to calculate glm incorporation Indigenous and African Ancestry
#For MexVar 

# Load required libraries
library(data.table)  # For efficient handling of large datasets
library(dplyr)       # For data manipulation (selecting, filtering, joining)
library(purrr)       # For functional programming and handling lists
library(broom)       # For tidying up model output into data frames
library(tibble)      # For advanced data frame manipulation

# Read command-line arguments for input and output files
args <- commandArgs(trailingOnly = TRUE)

# Check that both input and output filenames are provided
if (length(args) != 2) {
  cat("Uso: Rscript procesamiento.R <nombre_archivo_entrada> <nombre_archivo_salida>\n")
  quit(status = 1)
}
# Assign filenames to variables
nombre_archivo_entrada <- args[1]
nombre_archivo_salida <- args[2]

# Load data from the specified files

File_freq <- fread(nombre_archivo_entrada)  # Frequency data of variants (SNPs) from the input file
Global_Ancestry <- fread("/data/users/carbarjon/PhD/MXB_Freq/Data/MXB_K4_Global_Ancestry_from_gnomix.csv") # Global ancestry data
MXB_LL <- fread("/data/projects/mxb_popstructure/data/external/23-10-11-MXB-Metadata/mxb_metadata.csv")  # Metadata from the Mexican Biobank


# Data processing

File_freq <- rbind(File_freq, File_freq)

# Statistical modeling for each SNP

Resultados_modelo <- File_freq %>%
  group_by(SNP) %>%
  mutate(genotype = ifelse(MAC == 2, 1, ifelse(MAC == 0, 0, c(0, 1)))) %>%  # Genotype coding based on minor allele count
  rename("ind" = "CLST") %>%
  left_join(Global_Ancestry) %>%
  left_join(MXB_LL, by = c("ind" = "sample_id")) %>%
  mutate(across(c("Indigenous","Africa", "latitud", "longitud"), scale)) %>%
  group_by(SNP) %>%
  # Run logistic regression model with ancestry and geographic variables
  do(model = glm(genotype ~ Indigenous +Africa + longitud + latitud, family = binomial, data = .)) %>%
  # Clean up model results into a tidy data frame format
  deframe() %>%
  purrr::map_df(broom::tidy, .id = "SNP")

# Save processed results to the specified output file
write.csv(Resultados_modelo, file = nombre_archivo_salida)
