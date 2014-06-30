#!/usr/bin/python

import sys, os, re, getopt
import mybasic

def fastqc_batch(inDirName, inFilePattern, outDirName, repDirName):
	fileNameL = os.listdir(inDirName)
	fileNameL = filter(lambda x: re.match(inFilePattern, x), fileNameL)

	print 'Files: %s (%s)' % (fileNameL, len(fileNameL))

	sampNameL = list(set([re.match(inFilePattern, inputFile).group(1) for inputFile in fileNameL]))
	sampNameL.sort()

	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:
		os.system('/home/tools/FastQC/fastqc --outdir %s %s/%s.1.fq.gz %s/%s.2.fq.gz &> %s/%s.fastqc.qlog' \
			% (repDirName, inDirName,sampN, inDirName,sampN, outDirName,sampN))

if __name__ == '__main__':
#	fastqc_batch('/EQL1/NSL/RNASeq/fastq/link', '(.*)\.[12]\.fq\.gz', '/home/ihlee/test_data/tttt')
	fastqc_batch('/home/ihlee/test_data', '(.*)\.[12]\.fq\.gz', '/home/ihlee/test_data/tttt')
