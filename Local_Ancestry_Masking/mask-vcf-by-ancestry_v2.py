"""
authors: S.G.M.M & C.B.J
Mask VCF by local ancestry. Masked genotypes are encoded as missing values.
Usage:
    python mask-vcf-by-ancestry.py <ANC> <vcf> <lai> <output>

Args:
    ANC: Ancestry code, see the first line of input <lai> file.
    vcf: VCF file
    lai: Local ancestry file (gnomix *.msp output)
    output: output name for masked vcf file
    
NOTES:
    * It has to be run per chromosome
    * -1 indicates a missing genotype
    * See imports for required pacakges
"""


import pandas as pd
import numpy as np
from cyvcf2 import VCF, Writer
import sys

ANC, vcf, lai, output = sys.argv[1:]


lai = pd.read_csv(lai, sep='\t', skiprows=[0])

vcf = VCF(vcf)
index_to_sample_name = {x: y for (x, y) in enumerate(vcf.samples)}


ranges = [(row['spos'], row['epos']) for _, row in lai.iterrows()]


def retrieve_lai_at(pos, chrom):
    """
    Get the local ancestry of the given range
    """

    lai_pos = lai[(lai.spos <= pos) & (lai.epos >= pos)]
    lai_pos = lai_pos[lai_pos['#chm'].map(str) == str(chrom)]

    # If position if not in any range 
    # Find the nearest local ancestry range to the current position

    if lai_pos.shape[0] < 1:
        # encontrar el índice donde se debe insertar pos para mantener el orden
        idx = np.searchsorted(lai['spos'], pos)

        # encontrar el rango más cercano
        if idx == 0:
            nearest_range = lai.iloc[[0],:]
        elif idx == len(lai):
            nearest_range = lai.iloc[[-1],:]
        else:
            # comparar el rango en el índice idx y el índice anterior
            if abs(lai.loc[idx, 'spos'] - pos) < abs(lai.loc[idx-1, 'epos'] - pos):
                nearest_range = lai.loc[[idx],:]
            else:
                nearest_range = lai.loc[[idx-1],:]
        lai_pos=nearest_range
    
    if lai_pos.shape[0] > 1: 
        print(lai_pos)
        raise Exception(f'position {pos} is in multiple ranges')

    return lai_pos


def sample_ancestry_at(lai_pos, sample_index):
    """
    Get the ancestry of the given sample (index in the vcf)
    at lai_pos
    """
    sample_hap_0 = f'{index_to_sample_name[sample_index]}.0'
    sample_hap_1 = f'{index_to_sample_name[sample_index]}.1'

    anc_hap_0 = lai_pos[sample_hap_0].to_list()[0]
    anc_hap_1 = lai_pos[sample_hap_1].to_list()[0]

    return (anc_hap_0, anc_hap_1)


w = Writer(output, vcf)

i = 0
for variant in vcf:
    # c_: current
    c_pos = variant.POS
    chrom = variant.CHROM
    c_lai = retrieve_lai_at(c_pos, chrom)

 #   if (i % 1000 == 0):
 #       print(f'masking variant {i} ...')
 #   i += 1

    for (sample_index, _) in enumerate(variant.genotypes):

        anc_h0, anc_h1 = sample_ancestry_at(c_lai, sample_index)
       # print(f'sample: hap0 = {anc_h0}, hap1 = {anc_h1}')
	# Conver to str to have avoid python reading one as numeric and other as character and showing false when true
        if str(anc_h0) != str(ANC):
          #  print(f'{anc_h0} = {ANC} ?')
            variant.genotypes[sample_index][0] = -1

        if str(anc_h1) != str(ANC):
           # print(f'{anc_h1} = {ANC} ?')
            variant.genotypes[sample_index][1] = -1

    variant.genotypes = variant.genotypes
    w.write_record(variant)

w.close()
vcf.close()
