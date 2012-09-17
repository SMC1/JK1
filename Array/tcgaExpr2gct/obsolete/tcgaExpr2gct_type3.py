#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mytcga


def tcgaExpr2gct_type3(inputDirN, outputFileN, regex):

	fileNameL = os.listdir(inputDirN)

	dupCkL = []
	dataH = {}

	fileIdx = 0

	for fileName in fileNameL:

		if not re.search(regex,fileName):
			continue

		print '%s\t%s' % (fileIdx+1,fileName)

		rm = re.search('TCGA.{11}', fileName)
		sampleN = rm.group(0)
		indivId = sampleN[:-3]

		if indivId in dupCkL or sampleN[-2:] in mytcga.normalSampleCodeL:
			continue

		dupCkL.append(indivId)

		dataFile = open('%s/%s' % (inputDirN,fileName))
		dataFile.readline()

		for line in dataFile:

			(gene,count1,count2,rpkm) = line[:-1].split('\t')

			geneName = gene.split('|')[0]

			if geneName == '?':
				continue

			if fileIdx == 0:
				dataH[geneName] = {indivId: rpkm}
			else:
				dataH[geneName][indivId] = rpkm 

		fileIdx +=1

	geneNameL = dataH.keys()
	geneNameL.sort()

	outputFile = open(outputFileN, 'w')

	outputFile.write('#1.2\n')

	indivIdL = dataH[geneNameL[0]].keys()
	indivIdL.sort()

	outputFile.write('%s\t%s\n' % (len(geneNameL),len(indivIdL)))

	outputFile.write('NAME\tDescription')

	for indivId in indivIdL:
		outputFile.write('\t%s' % indivId[:12])

	outputFile.write('\n')

	for geneName in geneNameL:

		outputFile.write('%s\t' % (geneName))

		for indivId in indivIdL:
			outputFile.write('\t%s' % dataH[geneName][indivId])

		outputFile.write('\n')


optL, argL = getopt.getopt(sys.argv[1:],'i:o:e:',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH and '-o' in optH):

	print 'Usage: tcgaExpr2gct_type3.py -i (input file dir) -o (output file name) [-e (regex for filename)]'
	sys.exit(0)

if '-e' in optH:

	regex = optH['-e']

tcgaExpr2gct_type3(optH['-i'], optH['-o'], regex)
