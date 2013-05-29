#!/usr/bin/python

import sys, os, re


def rename(dirName,outDirName,filePattern,tag):

	inputFileNL = os.listdir(dirName)

	for fileN in inputFileNL:

		ro = re.match(filePattern, fileN)

		if ro:
			os.system('mv -f %s/%s %s/%s.fastq' % (dirName,fileN, outDirName,ro.group(1)))


#rename('/EQL3/TCGA/GBM/RNASeq/alignment/splice/ei_junc', '/EQL3/TCGA/GBM/RNASeq/alignment/splice/ei_junc', '(.*)_EGFR.dat','')
rename('/EQL1/NSL/RNASeq/fastq', '/EQL1/NSL/RNASeq/fastq', '(.*).fastq.gz.N.fastq','')
