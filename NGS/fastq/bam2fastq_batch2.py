#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def bam2fastq_batch2(inDirName,fileNamePattern,outDirName):

	fileNameL = os.listdir(inDirName)
	fileNameL = filter(lambda x: re.match(fileNamePattern, x), fileNameL)

	nameL = list([(inputFileN, re.match(fileNamePattern,inputFileN).group(1)) for inputFileN in fileNameL])
	
	print 'Samples: %s (%s)' % (nameL, len(nameL))

	for name in nameL[1:]:

		if not name[1] in ['C282.TCGA-32-2638-01A-01W-0922-08.1']:
			continue

		print name

		os.system('./bam2fastq.py -i %s/%s -o %s/%s' % (inDirName,name[0], outDirName,name[1]))


pattern1 = '(.*-[0-9]{2}\.[0-9])\.bam'
pattern2 = 'UNCID_[0-9]{7}\.(.*)\.sorted_.*'
pattern3 = '(.*)\.bam'

optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

bam2fastq_batch2('/EQL3/TCGA/GBM/WXS/alignment',pattern1,'/EQL3/TCGA/GBM/WXS/fastq')
