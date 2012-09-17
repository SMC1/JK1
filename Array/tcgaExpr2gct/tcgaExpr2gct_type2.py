#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mytcga

#ex. COAD Agilent
#fileName: US82800149_251976013160_S01_GE2_105_Dec08.txt_lmean.out.logratio.gene.tcga_level3.data.txt
#Hybridization REF   TCGA-A6-2679-11A-01R-1758-07
#Composite Element REF   log2 lowess normalized (cy5/cy3) collapsed by gene symbol
#ELMO2   -0.875083333333333
#CREB3L1 1.558
#RPS11   0.87875
#...

def tcgaExpr2gct_type2(inputDirN,regex):

	fileNameL = os.listdir(inputDirN)

	dupCkL = []
	dataH = {}

	fileIdx = 0

	for fileName in fileNameL:

		if not re.search(regex,fileName):
			continue

		dataFile = open('%s/%s' % (inputDirN,fileName))
		header = dataFile.readline()
		dataFile.readline()

		rm = re.search('TCGA.{11}', header)
		sampleN = rm.group(0)
		indivId = sampleN[:-3]

		if indivId in dupCkL or sampleN[-2:] in mytcga.normalSampleCodeL:
			continue

		dupCkL.append(indivId)

		for line in dataFile:

			(geneName,value) = line[:-1].split('\t')

			if fileIdx == 0:
				dataH[geneName] = {indivId: value}
			else:
				dataH[geneName][indivId] = value

		fileIdx +=1

	geneNameL = dataH.keys()
	geneNameL.sort()

	print '#1.2'

	indivIdL = dataH[geneNameL[0]].keys()
	indivIdL.sort()

	print '%s\t%s' % (len(geneNameL),len(indivIdL))

	sys.stdout.write('NAME\tDescription')

	for indivId in indivIdL:
		sys.stdout.write('\t%s' % indivId)

	sys.stdout.write('\n')

	for geneName in geneNameL:

		sys.stdout.write('%s\t' % (geneName))

		for indivId in indivIdL:
			sys.stdout.write('\t%s' % dataH[geneName][indivId])

		sys.stdout.write('\n')


optL, argL = getopt.getopt(sys.argv[1:],'i:e:',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH):

	print 'Usage: tcgaExpr2gct_type2.py -i (input file dir) [-e (pattern)]'
	sys.exit(0)

if '-e' in optH:
	regex = optH['-e']
else:
	regex = '.*'

tcgaExpr2gct_type2(optH['-i'],regex)
