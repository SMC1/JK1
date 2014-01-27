#!/usr/bin/python

import sys, getopt, numpy
import mybasic

def main(inFileName, lohFileName, outFileName, cnlohCutoff, lohCutoff):

	inFile = open(inFileName)
	outFile = open(outFileName,'w')

	cnH = {}

	outFile.write('chr\tpos\taf\tcn\ttype\tnormalF\n')

	inFile.readline()

	for line in inFile:

		valueL = line[:-1].split('\t')

		chr = valueL[1]
		start = int(valueL[2])
		end = int(valueL[3])

		loc = 'chr%s:%d-%d' % (chr,start,end)

		value = float(valueL[5])

		cnH[loc] = value

	lohFile = open(lohFileName)
	
	lohH = {}

	for line in lohFile:
		
		valueL = line[:-1].split('\t')

		chr_B = valueL[0]
		pos = int(valueL[1])
		af = float(valueL[6])

		for loc in cnH:
			chr = loc.split(':')[0]
			start = int(loc.split(':')[1].split('-')[0])
			end = int(loc.split(':')[1].split('-')[1])
			value = cnH[loc]
			
			if chr_B != chr:
				continue
			
			if start < pos <= end:
				#lohH['%s-%s' % (chr_B,pos)] = (af,value)
				mybasic.addHash(lohH,('%s-%s' % (chr_B,pos), af), value)
	
	for key in lohH:
		
		(loc, af) = key	

		cn = numpy.mean(lohH[key]) 
		
		chr = loc.split('-')[0]
		pos = loc.split('-')[1]

		if abs(float(cn)) < float(cnlohCutoff):
			type = 'CNLOH'
			nf = 2*(1-af)
		elif float(cn) <= float(lohCutoff):
			type = 'LOH'
			nf = (1/af) - 1
		else:
			type = 'NA'
			nf = 'NA'


		outFile.write('%s\t%s\t%.4f\t%.4f\t%s\t%s\n' % (chr,pos,af,cn,type,nf))

optL, argL = getopt.getopt(sys.argv[1:],'i:f:o:c:l:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-f' in optH and '-o' in optH:
	main(optH['-i'],optH['-f'],optH['-o'],optH['-c'],optH['-l'])

