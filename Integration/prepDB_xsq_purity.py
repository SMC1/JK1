#!/usr/bin/python

import sys, getopt, re
import mybasic

def main(sampPattern='(.*)', inFileN='', outFileN=''):
	inFile = sys.stdin
	if inFileN != '':
		inFile = open(inFileN, 'r')
	outFile = sys.stdout
	if outFileN != '':
		outFile = open(outFileN, 'w')
	
	for line in inFile:
		dataL = line[:-1].split('\t')
		sampN = re.match(sampPattern, dataL[0]).group(1)
		if float(dataL[1]) < 0:
			outFile.write('S%s\tND\tND\n' % sampN)
		else:
			outFile.write('S%s\t%s\t%s\n' % (sampN, int(float(dataL[1])*100), int(float(dataL[2])*100)))
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

	main('.{1}(.*)_[BNTX]_[NSKT]{2}', inFile, outFile)
