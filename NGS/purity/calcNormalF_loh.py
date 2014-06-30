#!/usr/bin/python

import sys, getopt, math
import mybasic

def main(inFileName, lohFileName, outFileName):

	inFile = open(inFileName)
	lohFile = open(lohFileName)

	outFile = open(outFileName,'w')
	outFile.write('chr\tpos\taf\ttype\tfrac\n')

	lohFile.readline()
	lohFileL = [line[:-1].split('\t') for line in lohFile]

	inFile.readline()
	
	for line in inFile:

		dataL = line[:-1].split('\t')

		chr = dataL[0]
		pos = int(dataL[1])

		aF = float(dataL[3])

		for tokL in lohFileL:

			(id, chrom, start, end, type, cn) = tokL

			if chrom != chr:
				continue

			if int(start) <= pos <= int(end):
				if type == 'LOH':
					frac = (1/aF)-1
				elif type == 'CNLOH':
					frac = 2*(1-aF)
				else:
					continue
					# type == 'gain' or 'NA'
			else:
				continue

			outFile.write('%s\t%s\t%.4f\t%s\t%.4f\n' %(chr,pos,aF,type,frac))

optL, argL = getopt.getopt(sys.argv[1:],'i:l:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:
	main(optH['-i'],optH['-l'],optH['-o'])

