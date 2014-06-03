#!/usr/bin/python

import sys, os, re, getopt
import mybasic
from glob import glob

def bam2fastq_batch1(inDirName,fileNamePattern,outDirName):

#	fileNameL = os.listdir(inDirName)
#	fileNameL = filter(lambda x: re.match(fileNamePattern, x), fileNameL)
#
#	nameL = list([(inputFileN, re.match(fileNamePattern,inputFileN).group(1)) for inputFileN in fileNameL])

	print 'Samples: %s (%s)' % (inDirName, len(inDirName))

	for inputFN in inDirName[1:]:

	#	if not name[1] in ['C282.TCGA-32-2638-01A-01W-0922-08.1']:
	#		continue

		name = inputFN.split('/')[-1]
		name = re.match(fileNamePattern,name).group(1)

		os.system('echo "java -jar /home/tools/picard-tools-1.73/SamToFastq.jar VALIDATION_STRINGENCY=SILENT INPUT=%s FASTQ=%s/%s.1.fastq SECOND_END_FASTQ=%s/%s.2.fastq QUIET=true" \
			| qsub -N %s -o %s/%s.qlog -j oe' % (inputFN, outDirName,name, outDirName,name, name, outDirName,name))
#		os.system('java -jar /home/tools/picard-tools-1.73/SamToFastq.jar VALIDATION_STRINGENCY=SILENT INPUT=%s FASTQ=%s/%s.1.fastq SECOND_END_FASTQ=%s/%s.2.fastq QUIET=true' % \
			(inputFN, outDirName,name, outDirName,name))


pattern1 = '(.*-[0-9]{2}\.[0-9])\.bam' # GBM
pattern2 = 'UNCID_[0-9]{7}\.(.*)\.sorted_genome_alignments.bam'
pattern3 = '(TCGA.{24})\.bam' # pre-sorted (BRCA, KIRC, UCEC)
pattern4 = '(.*)_rnaseq.bam' # OV
pattern5 = '(.*).bam'

optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

bam2fastq_batch1(glob('/EQL2/TCGA/LUAD/RNASeq/raw/*/*.bam'),pattern2,'/EQL2/TCGA/LUAD/RNASeq/fastq')
