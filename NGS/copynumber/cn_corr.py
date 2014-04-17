#!/usr/bin/python

import sys, os, getopt, math, re
import mybasic

def main(inFileName,outFileName,tFrac):

	inFile = open(inFileName)

	try:
		p = float(tFrac)/100
	except:
		sys.exit()
	
	outFile = open(outFileName,'w')

	for line in inFile:
	
		(chrom,sta,end,n,t,log) = line[:-1].split('\t')

		value = (2**float(log)) * 2
		cn = (value - 2*(1-p))/p
		if cn < 0:
			cn_re = -10.0
		else:
			cn_re = math.log(cn/2,2)	
		
		outFile.write('%s\t%s\t%s\t%s\t%s\t%.4f\n' %(chrom,sta,end,n,t,cn_re))
	outFile.flush()
	outFile.close()

optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' and '-p' in optH:
    main(optH['-i'],optH['-o'],optH['-p'])
