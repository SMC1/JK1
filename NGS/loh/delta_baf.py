#!/usr/bin/python

import sys, getopt, math
import mybasic

def main(inFileName, outFileName):

	inFile = open(inFileName)
	outFile = open(outFileName,'w')
	
	outFile.write('chrom\tloc.start\tvalue\taf\n')

	inFile.readline()
	
	for line in inFile:

		dataL = line[:-1].split('\t')

		chr = dataL[0]
		start = dataL[1]
		ref = dataL[2]
		obs = dataL[3]

		nr1 = int(dataL[4])
		nr2 = int(dataL[5])
		tr1 = int(dataL[8])
		tr2 = int(dataL[9])
		
		type = dataL[12]

		minF = min(float(nr1)/float(nr1+nr2), float(nr2)/float(nr1+nr2))

		# heterozygous
		if minF < 0.4:
			continue

		if nr1+nr2 < 10:
			continue
		
		if tr1+tr2 < 10:
			continue

		Naf = float(nr2)/float(nr1+nr2)
		Taf = float(tr2)/float(tr1+tr2)

		#delta = math.fabs(Taf-0.5)
		delta = math.fabs(Taf-Naf)

		if Taf >= 0.5:
			af = Taf
		else:
			af = 1-Taf

		outFile.write('%s\t%s\t%.4f\t%.4f\n' %(chr[3:],start,delta,af))

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:
	main(optH['-i'],optH['-o'])

main('/EQL1/NSL/exome_bam/mutation/S140_T_SS.snp','/EQL1/NSL/exome_bam/purity/S140_T_SS.dbaf.txt')
