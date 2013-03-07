#!/usr/bin/python

# for firehose MAF data

import sys, getopt, re, numpy
import mybasic

def main(sampNamePat=('(.*)',''),geneList=[]):


	inFile = sys.stdin

#	headerL = inFile.readline()[:-1].split('\t')
#
#	idxH = dict([(x, headerL.index(x)) for x in nameL])

	for line in inFile:

		valueL = line[:-1].split('\t')

		sampN = valueL[0]

		if sampN in ['780T_B_WXS_trueSeq','GBM10_025T_Kinome','780T_Br2_WXS_trueSeq','NS09_780T_Kinome','671T_Br1_WXS_trueSeq']:
			continue

		sId = re.match(sampNamePat[0], sampN).group(1)

		chrom = valueL[1]
		chrSta = valueL[2]
		chrEnd = valueL[3]

		ref = valueL[4]
		alt = valueL[5]

		nReads_ref = valueL[6]
		nReads_alt = valueL[7]

		strand = valueL[8]

		geneN = valueL[9]

		ch_dna = valueL[10]
		ch_aa = valueL[11]
		ch_type = valueL[12]

		cosmic = valueL[11]

		mutsig = ''


		sys.stdout.write('S%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
			(sId, chrom,chrSta,chrEnd, ref,alt, nReads_ref, nReads_alt, strand, \
			geneN, ch_dna, ch_aa, ch_type, cosmic, mutsig))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#	main(optH['-i'], optH['-o'])

main(('.*([0-9]{3}).*',''),[])
