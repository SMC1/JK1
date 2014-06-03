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
		dataL = line.rstrip().split('\t')
#		sampN = re.match(sampPattern, dataL[0]).group(1)
		(sid, postfix) = re.match(sampPattern, dataL[0]).groups()
		if postfix != 'T':
			sampN = sid + '_' + postfix
		else:
			sampN = sid
		outFile.write('%s\t%s\n' % (sampN, '\t'.join(dataL[1:])))
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

	main('(.*)_([TXC].{,2})_[NSKT]{2}', inFile, outFile)
