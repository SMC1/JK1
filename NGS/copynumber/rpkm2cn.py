#!/usr/bin/python

import sys, getopt, math
import mybasic

def main(inFileName, inNFileName, sampN, outFileName):

	inFile = open(inFileName)
	inNFile = open(inNFileName)

	outFile = open(outFileName,'w')
	outFile.write('ID\tchrom\tloc.start\tloc.end\tnum.mark\tvalue\n')

	normalH = {}

	inNFile.readline()
	
	for line in inNFile:
		
		dataL = line[:-1].split('\t')

		id = dataL[0]

		rpkm = float(dataL[2])

		normalH[id] = rpkm

	inFile.readline()

	for line in inFile:

		dataL = line[:-1].split('\t')

		id = dataL[0]
		
		try:
			rpkmN = float(normalH[id])
		except:
			continue

		rpkm = float(dataL[2])

		logR = math.log((rpkm+1)/(rpkmN+1),2)

		chr = id.split(':')[0][3:]
		start = id.split(':')[1].split('-')[0]
		end = id.split(':')[1].split('-')[1]

		outFile.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (sampN,chr,start,end,"NA",logR))


optL, argL = getopt.getopt(sys.argv[1:],'i:n:s:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:
	main(optH['-i'],optH['-n'],optH['-s'],optH['-o'])

