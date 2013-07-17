#/usr/bin/python

import sys, os, re, getopt
import mybasic

# degSeq_geneName 

def rpkm_process(inputDirN, filePattern, sampRegex, outputFileN):

	filePathL = os.popen('find %s -name "%s"' % (inputDirN,filePattern))

	dataH = {}

	fileIdx = 0

	for filePath in filePathL:

		filePath = filePath.rstrip()
		print '%s\t%s' % (fileIdx+1,filePath)

		rm = re.search(sampRegex, filePath.split('/')[-1])
		sampleN = rm.group(1)
		
		dataFile = open(filePath)
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
		outputFile.write('\tS%s' % sampleN)

	outputFile.write('\n')

	for geneName in geneNameL:

		outputFile.write('%s\t' % (geneName))

		for sampleN in sampleNL:
			outputFile.write('\t%s' % dataH[geneName][sampleN])

		outputFile.write('\n')


#optL, argL = getopt.getopt(sys.argv[1:],'i:o:e:',[])
#
#optH = mybasic.parseParam(optL)
#
#if not ('-i' in optH and '-o' in optH):
#
#	print 'Usage: rpkm_process.py -i (input file dir) -o (output file name) -e (regex for filename)'
#	sys.exit(0)
#
#if '-e' in optH:
#
#	regex = optH['-e']

#rpkm_process('/EQL1/NSL/RNASeq/results/expression', '/EQL1/NSL/RNASeq/results/expression/NSL_RPKM_43.gct', 'rpkm', '[0-9]{3}')
#rpkm_process('/EQL1/NSL/RNASeq/expression', '/EQL1/NSL/RNASeq/expression/NSL_RPKM_41.gct', 'rpkm', '([0-9]{3})')
rpkm_process('/pipeline/WY_RNASeq_expr', '*.rpkm', '([^.]+).rpkm', '/EQL6/NSL/WY/expression/U87MG_rpkm_3.gct')
