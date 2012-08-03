#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def batch_bam2fastq(inDirName,fileNamePattern,outDirName,test=False):

	fileNameL = os.listdir(inDirName)
	fileNameL = filter(lambda x: re.match(fileNamePattern, x), fileNameL)

	print 'Files: %s (%s)' % (fileNameL, len(fileNameL))

	sampNameL = list(set([re.match(fileNamePattern,inputFileN).group(1) for inputFileN in fileNameL]))
	sampNameL.sort()

	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

		if sampN == 'G17188.TCGA-02-0047-01A-01R-1849-01.2':
			continue

		print sampN

		os.system('java -jar /home/tools/picard-tools-1.73/SamToFastq.jar INPUT=%s/%s.bam FASTQ=%s/%s.1.fastq SECOND_END_FASTQ=%s/%s.2.fastq QUIET=true' % \
			(inDirName,sampN, outDirName,sampN, outDirName,sampN))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:t',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH:
#
#	batch_bam2fastq(optH['-i'], '', optH['-o'], '-t' in optH)

batch_bam2fastq('/EQL3/TCGA/GBM/RNASeq/bam','(.*-[0-9]{2}\.[0-9])\.bam','/EQL3/TCGA/GBM/RNASeq/fastq')
