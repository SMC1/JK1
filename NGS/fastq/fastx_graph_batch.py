#!/usr/bin/python

import sys, os, re

if len(sys.argv) < 2:

	print 'Usage: fastx_graph_run.py [input file directory] [input file regular expression pattern; optional]'
	sys.exit(0)

inputDirName = sys.argv[1]

if len(sys.argv) < 3:
	inputFilePattern = '.*quality\.txt'
else:
	inputFilePattern = sys.argv[2]

inputFileNameL = os.listdir(inputDirName)
inputFileNameL = filter(lambda x: re.match(inputFilePattern,x), inputFileNameL)

analysisNameL = [('boxplot','fastq_quality_boxplot_graph.sh'),('ntDist','fastx_nucleotide_distribution_graph.sh')]

print 'Files: %s' % inputFileNameL

for inputFileName in inputFileNameL:

	dataName = inputFileName.split('_quality')[0]

	for (graphName,programName) in analysisNameL:

		print '/usr/local/bin/%s -t "%s" -i %s/%s -o %s/%s_%s.png' % \
			(programName, dataName, inputDirName,inputFileName, inputDirName,dataName, graphName )
		os.system('/usr/local/bin/%s -t "%s" -i %s/%s -o %s/%s_%s.png' % \
			(programName, dataName, inputDirName,inputFileName, inputDirName,dataName, graphName ))

		print '/usr/local/bin/%s -p -t "%s" -i %s/%s -o %s/%s_%s.ps' % \
			(programName, dataName, inputDirName,inputFileName, inputDirName,dataName, graphName )
		os.system('/usr/local/bin/%s -p -t "%s" -i %s/%s -o %s/%s_%s.ps' % \
			(programName, dataName, inputDirName,inputFileName, inputDirName,dataName, graphName ))
