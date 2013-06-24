#!/usr/bin/python

# for varscan output

import sys, getopt, re, os
import mybasic

def main(inTFileName,inNFileName,geneList=[]):

	sampIdL = []
	
	inFile = open(inNFileName)

	for line in inFile:

		valueL = line[:-1].split('\t')
		
		sampId = valueL[0]
		sampIdL.append(sampId)

		sys.stdout.write(line)

	inFile = open(inTFileName)

	for line in inFile:

		valueL = line[:-1].split('\t')

		sampN = valueL[0]

		if sampN in sampIdL:
			continue

		chrom = valueL[1]
		chrSta = valueL[2]
		chrEnd = valueL[3]

		ref = valueL[4]
		alt = valueL[5]

		nReads_ref = valueL[6]
		nReads_alt = valueL[7]
			
		n_count_ref = ''
		n_count_alt = ''

		strand = valueL[8]

		geneN = valueL[9]

		ch_dna = valueL[10]
		ch_aa = valueL[11]
		ch_type = valueL[12]

#		if 'silent' in ch_type:
#			continue
				
		cosmic = valueL[11]

		mutsig = ''

		sys.stdout.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
			(sampN, chrom,chrSta,chrEnd, ref,alt, n_count_ref,n_count_alt, nReads_ref, nReads_alt, strand, \
			geneN, ch_dna, ch_aa, ch_type, cosmic, mutsig))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#	main(optH['-i'], optH['-o'])

main('/EQL1/NSL/exome_bam/mutation/NSL_GBM_mutation_44.dat','/EQL1/NSL/exome_bam/mutation/NSL_GBM_N_mutation_13.dat',[])
