#!/usr/bin/python

import sys, os, re, getopt
import mybasic

# for RNASeqV2

def tcgaExpr2gct_type4(inputDirN, outputFileN, regex):

	fileNameL = os.listdir(inputDirN)

	dataH = {}

	fileIdx = 0

	for fileName in fileNameL:

		if not re.search(regex,fileName):
			continue

		print '%s\t%s' % (fileIdx+1,fileName)

		rm = re.search('.{8}-.{4}-.{4}-.{4}-.{12}', fileName)
		uuid = rm.group(0)

		dataFile = open('%s/%s' % (inputDirN,fileName))
		dataFile.readline()

		for line in dataFile:

			(gene,rpkm) = line[:-1].split('\t')

			geneName = gene.split('|')[0]

			if geneName == '?':
				continue

			if fileIdx == 0:
				dataH[geneName] = {uuid: rpkm}
			else:
				dataH[geneName][uuid] = rpkm 

		fileIdx +=1

	geneNameL = dataH.keys()
	geneNameL.sort()

	outputFile = open(outputFileN, 'w')

	outputFile.write('#1.2\n')

	uuidL = dataH[geneNameL[0]].keys()
	uuidL.sort()

	outputFile.write('%s\t%s\n' % (len(geneNameL),len(uuidL)))

	outputFile.write('NAME\tDescription')

	for uuid in uuidL:
		outputFile.write('\t%s' % uuid)

	outputFile.write('\n')

	for geneName in geneNameL:

		outputFile.write('%s\t' % (geneName))

		for uuid in uuidL:
			outputFile.write('\t%s' % dataH[geneName][uuid])

		outputFile.write('\n')


optL, argL = getopt.getopt(sys.argv[1:],'i:o:e:',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH and '-o' in optH):

	print 'Usage: tcgaExpr2gct_type4.py -i (input file dir) -o (output file name) -e (regex for filename)'
	sys.exit(0)

if '-e' in optH:

	regex = optH['-e']

tcgaExpr2gct_type4(optH['-i'], optH['-o'], regex)
