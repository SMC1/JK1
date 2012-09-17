#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def bam2fastq(inDirName,fileNamePattern,outDirName):

	file = os.popen('samtools view %s')

	file

optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH and '-p' in optH:
#
#	bam2fastq(optH['-i'], optH['-p'], optH['-o'])
#
#else:

pattern1 = '(.*-[0-9]{2}\.[0-9])\.bam'
pattern2 = 'UNCID_[0-9]{7}\.(.*)\.sorted_.*'
pattern3 = '(.*)\.bam'

bam2fastq('/EQL1/TCGA/NTRK1-outlier/alignment/sortedByName',pattern3,'/EQL1/TCGA/NTRK1-outlier/fastq')
