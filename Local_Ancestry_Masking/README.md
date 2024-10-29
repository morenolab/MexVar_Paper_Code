# Mask VCF by local ancestry

This program masks genotypes in a VCF file based on local ancestry information, which is provided in a .msp file format. Masked genotypes are encoded as missing values.

Made By Santiago Medina Muñoz and Carmina Barberena Jonas

## Usage

``` 
python mask-vcf-by-ancestry.py <ANC> <vcf> <lai> <output>
```

### Arguments

- `ANC`: Ancestry code, see the first line of input `<lai>` file.
- `vcf`: VCF file
- `lai`: Local ancestry file (gnomix *.msp output)
- `output`: Output name for masked vcf file

### mask-vcf-by-ancestry_v2.vcf

If a site is not in the MSP, it is masked with the value of the closest range of sites. 

The use is the same 


Important note: Please note that this masking script works only if the "rephasing" option in Gnomix is set to "FALSE". Additionally, it is crucial to use the same phased VCF file that was used for generating the LAI file in Gnomix. If the phased VCF file and/or refasing option differ from those used in Gnomix, the masking script may produce incorrect results. Therefore, it is highly recommended to use caution and verify that the input files and options match those used in Gnomix before running the masking script.

### Notes

- `-1` indicates a missing genotype.
- Toy examples are provided in the files Toy.vcf and Toy.msp.


