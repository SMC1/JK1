#!/usr/bin/python

import sys, os, re

inDirName = '/EQL3/TCGA/GBM/RNASeq/fastq/30nt'
inFilePattern = '*.fastq'

outDirName = '/EQL3/TCGA/GBM/RNASeq/fastq/30nt'

file = os.popen('find %s -name "%s"' % (inDirName,inFilePattern))

for filePath in file:

	filePath = filePath[:-1]

	ro = re.search('(.*)\.([12])_30nt\.fastq', filePath.split('/')[-1])

	os.system('mv %s %s/%s_30nt.%s.fastq' % (filePath,outDirName,ro.group(1),ro.group(2)))
