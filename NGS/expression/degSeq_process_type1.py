#!/usr/bin/python

import sys, os, re, getopt
import mybasic

# degSeq_geneName 

def degSeq_process_type1(inputDirN, outputFileN, regex):

	fileNameL = os.listdir(inputDirN)

	dataH = {}

	fileIdx = 0

	for fileName in fileNameL:

		if not re.search(regex,fileName):
			continue

		print '%s\t%s' % (fileIdx+1,fileName)

		rm = re.search('TCGA.{24}', fileName)
		sampleN = rm.group(0)

		dataFile = open('%s/%s' % (inputDirN,fileName))
		dataFile.readline()

		for line in dataFile:

			(gene,rawCount,rpkm,allReads,length) = line[:-1].split('\t')

			geneName = gene

			if fileIdx == 0:
				dataH[geneName] = {sampleN: rpkm}
			else:
				dataH[geneName][sampleN] = rpkm 

		fileIdx +=1

	geneNameL = dataH.keys()
	geneNameL.sort()

	outputFile = open(outputFileN, 'w')

	outputFile.write('#1.2\n')

	sampleNL = dataH[geneNameL[0]].keys()
	sampleNL.sort()

	outputFile.write('%s\t%s\n' % (len(geneNameL),len(sampleNL)))

	outputFile.write('NAME\tDescription')

	for sampleN in sampleNL:
		outputFile.write('\t%s' % sampleN)

	outputFile.write('\n')

	for geneName in geneNameL:

		outputFile.write('%s\t' % (geneName))

		for sampleN in sampleNL:
			outputFile.write('\t%s' % dataH[geneName][sampleN])

		outputFile.write('\n')


optL, argL = getopt.getopt(sys.argv[1:],'i:o:e:',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH and '-o' in optH):

	print 'Usage: degSeq_process_type1.py -i (input file dir) -o (output file name) -e (regex for filename)'
	sys.exit(0)

if '-e' in optH:

	regex = optH['-e']

degSeq_process_type1(optH['-i'], optH['-o'], regex)
