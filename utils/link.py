#!/usr/bin/python

import sys, os, re


def link(dirName,outDirName,filePattern,tag):

	inputFileNL = os.listdir(dirName)

	for fileN in inputFileNL:

		ro = re.match(filePattern, fileN)

		if ro:
			os.system('ln -s %s/%s %s/%s_%s.%s' % (dirName,fileN, outDirName,ro.group(1),tag,ro.group(2)))


#link('/EQL1/NSL/WXS/fastq', '(.*)_[ATGC]{6}_L005_R([12])_001\.fastq\.gz')
#link('/EQL1/NSL/Kinome/fastq', '(.*)_[ATGC]{6}_L008_R([12])_001\.fastq\.gz\.N\.fastq\.gz')
#link('/EQL1/NSL/WXS_trueSeq/fastq', '/EQL1/NSL/WXS_trueSeq/fastq/link', '(.*)_R([12])\.fq\.gz')
#link('/EQL1/NSL/RNASeq/fastq', '/EQL1/NSL/RNASeq/fastq/link', '(.*)_[ATGC]{6}_L008_R([12])_001\.fastq\.gz')
#link('/EQL1/NSL/RNASeq/fastq/screening', '/EQL1/NSL/RNASeq/fastq/link', '(.*)_[ATGC]{6}_L[0-9]{3}_R([12])_001\.fastq\.gz')

#link('/EQL1/NSL/WXS/coverage', '/EQL1/NSL/Exome/coverage', '(.*)\.(bedgraph)','WXS')
#link('/EQL1/NSL/WXS_trueSeq/coverage', '/EQL1/NSL/Exome/coverage', '(.*)\.(bedgraph)','WXS_trueSeq')
#link('/EQL1/NSL/Kinome/coverage', '/EQL1/NSL/Exome/coverage', '(.*)\.(bedgraph)','Kinome')

#link('/EQL1/NSL/Kinome/bwa', '/EQL1/NSL/Exome/bwa', '(.*)\.(sorted\.bam)','Kinome')
#link('/EQL1/NSL/WXS/bwa', '/EQL1/NSL/Exome/bwa', '(.*)\.(sorted\.bam)','WXS')
link('/EQL1/NSL/WXS_trueSeq/alignment/bwa', '/EQL1/NSL/Exome/bwa', '(.*)\.(sorted\.bam)','WXS_trueSeq')
