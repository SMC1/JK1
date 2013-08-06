#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def bam2fastq_batch1(inDirName,fileNamePattern,outDirName):

	fileNameL = os.listdir(inDirName)
	fileNameL = filter(lambda x: re.match(fileNamePattern, x), fileNameL)

	nameL = list([(inputFileN, re.match(fileNamePattern,inputFileN).group(1)) for inputFileN in fileNameL])
	
	print 'Samples: %s (%s)' % (nameL, len(nameL))

	for name in nameL:

		if not name[1] in ['C282.TCGA-32-2638-01A-01W-0922-08.1']:
			continue

		print name

		os.system('java -jar /home/tools/picard-tools-1.73/SamToFastq.jar INPUT=%s/%s FASTQ=%s/%s.1.fastq SECOND_END_FASTQ=%s/%s.2.fastq QUIET=true' % \
			(inDirName,name[0], outDirName,name[1], outDirName,name[1]))


pattern1 = '(.*-[0-9]{2}\.[0-9])\.bam' # GBM
pattern2 = 'UNCID_[0-9]{7}\.(.*)\.sorted_genome_alignments.bam'
pattern3 = '(TCGA.{24})\.bam' # pre-sorted (BRCA, KIRC, UCEC)
pattern4 = '(.*)_rnaseq.bam' # OV
pattern5 = '(.*).bam'

optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

bam2fastq_batch1('/EQL2/TCGA/LUAD/RNASeq/raw/fc0e023d-9052-469c-8028-c05a0fb1f6c3',pattern2,'/EQL2/TCGA/LUAD/RNASeq/fastq')
