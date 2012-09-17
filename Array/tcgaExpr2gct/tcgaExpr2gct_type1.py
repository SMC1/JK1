#!/usr/bin/python_epd

import sys, os, re, getopt
import mybasic


def tcgaExpr2gct(inputDirN):

	fileNameL = os.listdir(inputDirN)

	dupCkL = []
	dataH = {}

	fileIdx = 0

	for fileName in fileNameL:

		rm = re.search('TCGA.{11}', fileName)
		sampleN = rm.group(0)

		if sampleN in dupCkL or sampleN[-2:] in mytcga.normalSampleCodeL:
			continue

		dupCkL.append(sampleN)

		dataFile = open('%s/%s' % (inputDirN,fileName))
		dataFile.readline()

		for line in dataFile:

			(indivId,geneName,value) = line[:-1].split('\t')

			if fileIdx == 0:
				dataH[geneName] = {indivId: value}
			else:
				dataH[geneName][indivId] = value

		fileIdx +=1

	geneNameL = dataH.keys()

	print '#1.2'

	indivIdL = dataH[geneNameL[0]].keys()

	print '%s\t%s' % (len(geneNameL),len(indivIdL))

	sys.stdout.write('NAME\tDescription')

	for indivId in indivIdL:
		sys.stdout.write('\t%s' % indivId[:12])

	sys.stdout.write('\n')

	for geneName in geneNameL:

		sys.stdout.write('%s\t' % (geneName))

		for indivId in indivIdL:
			sys.stdout.write('\t%s' % dataH[geneName][indivId])

		sys.stdout.write('\n')


optL, argL = getopt.getopt(sys.argv[1:],'i:',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH):

	print 'Usage: tcgaExpr2gct.py -i [input file dir]'
	sys.exit(0)

tcgaExpr2gct(optH['-i'])
