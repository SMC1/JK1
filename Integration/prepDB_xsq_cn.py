#!/usr/bin/python

import sys, getopt, re
import mybasic

def main(inFileN='', outFileN='', geneList=[]):
	inFile = sys.stdin
	if inFileN != '':
		inFile = open(inFileN, 'r')
	outFile = sys.stdout
	if outFileN != '':
		outFile = open(outFileN, 'w')
	
	for line in inFile:
		dataL = line[:-1].split('\t')
		if dataL[0] == 'S6A' or dataL[0] == 'S6B':
			continue
		if geneList==[] or dataL[1] in geneList:
			outFile.write(line)
	outFile.flush()
	outFile.close()
	inFile.close()

if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:t',[])
	optH = mybasic.parseParam(optL)

	inFile = ''
	if '-i' in optH:
		inFile = optH['-i']
	outFile = ''
	if '-o' in optH:
		outFile = optH['-o']

	main(inFile, outFile, [])
