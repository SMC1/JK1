#!/usr/bin/python

import sys, re

def main(sampNamePat=('(.*)',''),geneList=[]):
	inFile = sys.stdin

	for line in inFile:
		valueL = line[:-1].split('\t')
		sampN = valueL[0]

		sid = re.match(sampNamePat[0], sampN).group(1)

		if '_X_' in sampN and sid[-2:] != '_X':
			sid = sid + '_X'
		if '_B_' in sampN:
			continue
		if '6A' in sampN or '6B' in sampN: ## make sure to ignore sample with very poor-quality blood sample
			continue

		chrom = valueL[1]
		chrSta = valueL[2]
		chrEnd = valueL[3]

		ref = valueL[4]
		alt = valueL[5]

		n_nReads_ref = valueL[6]
		n_nReads_alt = valueL[7]
		nReads_ref = valueL[8]
		nReads_alt = valueL[9]


		if int(nReads_alt) < 2:
			continue

		strand = valueL[10]
		geneN = valueL[11]
		if len(geneN) < 1:
			geneN = '-'

		ch_dna = valueL[12]
		ch_aa = valueL[13]
		ch_type = valueL[14]

#		if ch_type == 'Substitution - coding silent' or ch_type == 'synonymous_variant' or ch_type == 'stop_retained_variant' or ch_type == 'stop_retained_variant,synonymous_variant':
#			continue

		cosmic = ''
		mutsig = ''

		sys.stdout.write('S%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
			(sid, chrom,chrSta,chrEnd, ref,alt, n_nReads_ref, n_nReads_alt, nReads_ref, nReads_alt, strand, \
			geneN, ch_dna, ch_aa, ch_type, cosmic, mutsig))

main(('.{1}(.*)_[BNTX]_[KNST]{2}',''),[])
