#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mygenome


def main(inFileName,outFileName,pileupDir):

	inFile = open(inFileName)
	outFile = open(outFileName,'w')

	outFile.write(inFile.readline())

	for line in inFile:

		tokL = line[:-1].split('\t')

		if tokL[-1]==tokL[-2]=='0':
			flag = 0 # Recur
		elif tokL[-3]==tokL[-4]=='0':
			flag = 1 # Prim
		else:
			outFile.write(line)
			continue
			
		rm = re.match('(chr[^:]*):([0-9]*)~([0-9]*)',tokL[2])
		(chrom,chrSta,chrEnd) = rm.groups()

		if int(chrEnd)-int(chrEnd)!=0:
			outFile.write(line)
			continue

		refAllele = tokL[3]
		altAllele = tokL[4]

		#print tokL[1], tokL[2], refAllele, '>', altAllele, tokL[-4:],

		sId = tokL[1].split('-')[1-flag]

		result = mygenome.lookupPileup([pileupDir,],sId,chrom,chrSta,refAllele,altAllele)
		
		if result:

			tokL[-1-flag*2] = str(result[1])
			tokL[-2-flag*2] = str(result[0])
			outFile.write('\t'.join(tokL)+'\n')

		else:

			outFile.write(line)

	outFile.close()


#optL, argL = getopt.getopt(sys.argv[1:],'i:o:l:',[])
#
#optH = mybasic.parseParam(optL)
#
#if '-i' in optH and '-o' in optH and '-l' in optH:
#
#	main(optH['-i'], optH['-o'], int(optH['-l']))

main('/EQL1/PrimRecur/signif/signif_mutation_pre.txt','/EQL1/PrimRecur/signif/signif_mutation.txt','/EQL1/NSL/WXS/exome_20130529/')
