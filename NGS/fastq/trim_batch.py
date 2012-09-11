#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def trim_batch(inDirName,fileNamePattern,outDirName,trimLen):

	fileNameL = os.listdir(inDirName)
	fileNameL = filter(lambda x: re.match(fileNamePattern, x), fileNameL)

	print 'Files: %s (%s)' % (fileNameL, len(fileNameL))

	sampNameL = list(set([re.match(fileNamePattern,inputFileN).group(1) for inputFileN in fileNameL]))
	sampNameL.sort()

	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL[2:3]:

		print sampN

		os.system('./trim.py -i %s/%s.1.fastq -o %s/%s.1 -l %s &' % (inDirName,sampN, outDirName,sampN, trimLen))
		os.system('./trim.py -i %s/%s.2.fastq -o %s/%s.2 -l %s' % (inDirName,sampN, outDirName,sampN, trimLen))


#optL, argL = getopt.getopt(sys.argv[1:],'i:e:o:l:',[])
#
#optH = mybasic.parseParam(optL)
#
#if '-i' in optH and '-o' in optH:
#
#	trim_batch(optH['-i'], '', optH['-o'], '-t' in optH)

trim_batch('/EQL1/TCGA/GBM/WXS/fastq', '(.*)\.[12]\.fastq', '/EQL1/TCGA/GBM/WXS/fastq/30nt', 30)
