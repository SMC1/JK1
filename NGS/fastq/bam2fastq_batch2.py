#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mysetting
from glob import glob

def bam2fastq_batch2(inDirName,outDirName,outGzDirName,fileNamePattern):

#	fileNameL = os.listdir(inDirName)
#	fileNameL = filter(lambda x: re.match(fileNamePattern, x), fileNameL)
#
#	nameL = list([(inputFileN, re.match(fileNamePattern,inputFileN).group(1)) for inputFileN in fileNameL])
#	
#	print 'Samples: %s (%s)' % (nameL, len(nameL))

	print 'Samples: %s (%s)' % (inDirName, len(inDirName))

	procFileNameL = os.listdir(outGzDirName)
	procFileNameL = filter(lambda x: re.match('(.*)\.1\.fastq.gz', x), procFileNameL)
	procNameL = list([re.match('(.*)\.1\.fastq.gz',procFileN).group(1) for procFileN in procFileNameL])

	print procNameL, len(procNameL)

	for inputFN in inDirName:

		name = inputFN.split('/')[-1]
		name = re.match(fileNamePattern,name).group(1)

		if name in procNameL:
			continue

		print name

		os.system('echo "/usr/bin/python %s/NGS/fastq/bam2fastq.py -i %s -o %s/%s; \
			gzip %s/%s.*.fastq" | qsub -N %s -o %s/%s.qlog -j oe' % (mysetting.SRC_HOME, inputFN, outDirName,name, outDirName,name, name, outDirName,name))

#		os.system('./bam2fastq.py -i %s -o %s/%s; \
#			gzip %s/%s.*.fastq' % (inputFN, outDirName,name, outDirName,name))


if __name__ == '__main__':

	pattern1 = '(.*-[0-9]{2}\.[0-9])\.bam'
	pattern2 = 'UNCID_[0-9]{7}\.(.*)\.sorted_genome_alignments.bam'
	pattern3 = '(.*)\.bam'

	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

	optH = mybasic.parseParam(optL)

	bam2fastq_batch2(glob('/EQL2/TCGA/LUAD/RNASeq/raw/*/*.bam'),'/EQL2/TCGA/LUAD/RNASeq/fastq','/EQL2/TCGA/LUAD/RNASeq/fastq/fqgz',pattern2)
