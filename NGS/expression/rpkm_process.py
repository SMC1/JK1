#/usr/bin/python

import sys, os, re, getopt, numpy
import mybasic

# degSeq_geneName 

def rpkm_process(inputDirN, filePattern, sampRegex, outputFileN, avg=False):

	filePathL = os.popen('find %s -name "%s"' % (inputDirN,filePattern))

	dataH = {}

	fileIdx = 0

	for filePath in filePathL:

		filePath = filePath.rstrip()
		print '%s\t%s' % (fileIdx+1,filePath)

		rm = re.search(sampRegex, filePath.split('/')[-1])
		sampleN = rm.group(1).replace('.','_').replace('-','_')
		
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

	outputFile.write('%s\t%s\n' % (len(geneNameL),len(sampleNL)+1 if avg else len(sampleNL)))

	outputFile.write('NAME\tDescription')

	for sampleN in sampleNL:
		outputFile.write('\t%s' % sampleN)
		
	if avg:
		outputFile.write('\tAverage')

	outputFile.write('\n')

	for geneName in geneNameL:
		
		outputFile.write('%s\t' % (geneName))

		for sampleN in sampleNL:
			outputFile.write('\t%s' % dataH[geneName][sampleN])
	
		if avg:
			outputFile.write('\t%.4f' % numpy.mean(map(float,dataH[geneName].values())))

		outputFile.write('\n')


if __name__ == '__main__':
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

	#for SGI_20131031 samples
	#rpkm_process('/EQL1/pipeline/SGI20131031_rsq2expr', '*.rpkm', '([0-9]+[AB]*)', '/EQL2/SGI_20131031/RNASeq/results/expression/RPKM_30.gct')
	#rpkm_process('/EQL1/NSL/RNASeq/results/expression', '*.rpkm', '([0-9]{3})','/EQL1/NSL/RNASeq/results/expression/NSL_RPKM_45.gct')
	#rpkm_process('/EQL1/NSL/RNASeq/expression', '/EQL1/NSL/RNASeq/expression/NSL_RPKM_41.gct', 'rpkm', '([0-9]{3})')
	#rpkm_process('/pipeline/WY_RNASeq_expr', '*.rpkm', '([^.]+).rpkm', '/EQL6/NSL/WY/expression/U87MG_rpkm_3.gct')
	#rpkm_process('/EQL1/pipeline/SGI20131119_rsq2expr', '*.rpkm', '([0-9]{3})', '/EQL1/NSL/RNASeq/results/expression/SGI20131119_6.gct')
#	rpkm_process('/EQL1/pipeline/SGI20131212_rsq2expr', '*.rpkm', '([0-9]{3})', '/EQL1/NSL/RNASeq/results/expression/SGI20131212_6.gct')
#	rpkm_process('/EQL1/NSL/WXS/WXS_B_SS/copynumber', '*.rpkm', '([0-9]{3})','/EQL1/NSL/WXS/WXS_B_SS/copynumber/NSL_CN_B_12.gct',avg=True)
	rpkm_process('/EQL6/pipeline/SCS20140104_rsq2expr', '*.rpkm', 'IRCR.GBM-[0-9]{3}-S(.*)_RSq', '/EQL6/pipeline/SCS20140104_rsq2expr/SCS20140104_rsq2expr.gct')
