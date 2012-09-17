#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def sortByName_batch(inDirName,fileNamePattern,outDirName):

	fileNameL = os.listdir(inDirName)
	fileNameL = filter(lambda x: re.match(fileNamePattern, x), fileNameL)

	nameL = list([(inputFileN, re.match(fileNamePattern,inputFileN).group(1)) for inputFileN in fileNameL])
	
	print '%s (%s)' % (nameL, len(nameL))

	for name in nameL:

		print name
		os.system('samtools sort -n -m 100000000000 %s/%s %s/%s' % (inDirName,name[0], outDirName,name[1]))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

#if '-i' in optH and '-o' in optH and '-p' in optH:
#
#	sortByName_batch(optH['-i'], optH['-p'], optH['-o'])

pattern1 = '(.*-[0-9]{2}\.[0-9])\.bam'
pattern2 = 'UNCID_[0-9]{7}\.(.*)\.sorted_.*'

sortByName_batch('/EQL1/TCGA/NTRK1-outlier/alignment',pattern2,'/EQL1/TCGA/NTRK1-outlier/alignment/sortedByName')
