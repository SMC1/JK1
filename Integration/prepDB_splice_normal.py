#!/usr/bin/python

import sys, getopt, re
import mybasic


def main(sampNamePat, inFileN='', outFileN=''):

	inFile = sys.stdin
	if inFileN != '':
		inFile = open(inFileN, 'r')
	outFile = sys.stdout
	if outFileN != '':
		outFile = open(outFileN, 'w')

	for line in inFile:

		dataL = line[:-1].split('\t')

		(sampN,loc1,loc2,exon1,exon2,nReads,nPos) = (dataL[0],dataL[1],dataL[2],dataL[3],dataL[4],dataL[5],dataL[7])

		sampN = re.match(sampNamePat[0],sampN).group(1).replace('.','_').replace('-','_')

		outFile.write('%s%s\t%s\t%s\t%s\t%s\n' % (sampNamePat[1],sampN,loc1,loc2,nReads,nPos))
	outFile.flush()
	outFile.close()


if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

	optH = mybasic.parseParam(optL)

	#if '-i' in optH and '-o' in optH:
	#	main(optH['-i'], optH['-o'])

	#main(('.*([0-9]{3}).*','S'))
	#main(('.*(TCGA-..-....).*',''))
	#main(('.*(TCGA-..-....-...).*',''))
	#main(('.*([0-9]{3}).*','S'))
	main(('.{1}(.*)_RSq','S'))
