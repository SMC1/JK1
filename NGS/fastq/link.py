#!/usr/bin/python

import sys, os, re


def link(dirName,filePattern):

	inputFileNL = os.listdir(dirName)

	for fileN in inputFileNL:

		ro = re.match(filePattern, fileN)

		if ro:
			os.system('ln -s %s/%s %s/%s.%s.fq.gz' % (dirName,fileN, dirName,ro.group(1),ro.group(2)))


#link('/EQL1/NSL/WXS/fastq', '(.*)_[ATGC]{6}_L005_R([12])_001\.fastq\.gz')
#link('/EQL1/NSL/Kinome/fastq', '(.*)_[ATGC]{6}_L008_R([12])_001\.fastq\.gz\.N\.fastq\.gz')
link('/EQL1/NSL/WXS_trueSeq/fastq', '(.*)_R([12])\.fq')
