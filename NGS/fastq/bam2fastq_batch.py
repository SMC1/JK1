#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def batch_bam2fastq(inDirName,fileNamePattern,outDirName):

	fileNameL = os.listdir(inDirName)
	fileNameL = filter(lambda x: re.match(fileNamePattern, x), fileNameL)

	nameL = list([(inputFileN, re.match(fileNamePattern,inputFileN).group(1)) for inputFileN in fileNameL])
	
	print 'Samples: %s (%s)' % (nameL, len(nameL))

	for name in nameL:

		print name

		os.system('java -jar /home/tools/picard-tools-1.73/SamToFastq.jar INPUT=%s/%s FASTQ=%s/%s.1.fastq SECOND_END_FASTQ=%s/%s.2.fastq QUIET=true' % \
			(inDirName,name[0], outDirName,name[1], outDirName,name[1]))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH and '-p' in optH:
#
#	batch_bam2fastq(optH['-i'], optH['-p'], optH['-o'])
#
#else:

pattern1 = '(.*-[0-9]{2}\.[0-9])\.bam'
pattern2 = 'UNCID_[0-9]{7}\.(.*)\.sorted_.*'
pattern3 = '(.*)\.bam'

batch_bam2fastq('/EQL1/TCGA/NTRK1-outlier/alignment/sortedByName',pattern3,'/EQL1/TCGA/NTRK1-outlier/fastq')
