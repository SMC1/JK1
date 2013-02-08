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

	for sampN in sampNameL:

		print sampN

		os.system('zcat %s/%s.1.fq.gz | ./trim.py -i stdin -o stdout -l %s > %s/%s.1.fq &' % (inDirName,sampN, trimLen, outDirName,sampN))
		os.system('zcat %s/%s.2.fq.gz | ./trim.py -i stdin -o stdout -l %s > %s/%s.2.fq' % (inDirName,sampN, trimLen, outDirName,sampN))


#optL, argL = getopt.getopt(sys.argv[1:],'i:e:o:l:',[])
#
#optH = mybasic.parseParam(optL)
#
#if '-i' in optH and '-o' in optH:
#
#	trim_batch(optH['-i'], '', optH['-o'], '-t' in optH)

#trim_batch('/EQL1/TCGA/GBM/WXS/fastq', '(.*5411-10.*)\.[12]\.fastq', '/EQL1/TCGA/GBM/WXS/fastq/30nt', 30)
trim_batch('/EQL1/NSL/RNASeq/fastq/link2/renamed', '(.*)\.[12]\.fq\.gz', '/EQL1/NSL/RNASeq/fastq/30nt/new', 30)
