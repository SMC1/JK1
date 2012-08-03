#!/usr/bin/python

import sys, os

dataDir = '/data1/RNASeq_LymphNK/00_Sequence_fastq/SMC1/fastx'

if len(sys.argv) == 1 or sys.argv[1] not in ('png','ps'):
	imageFormat = 'png'
else:
	imageFormat = sys.argv[1]

if imageFormat == 'png':
	flag = ''
else: # 'ps'
	flag = '-p'

i = '03'

os.system('/usr/local/bin/fastq_quality_boxplot_graph.sh %s -t "%s" \
	-i %s/S%s_sequence_R1_quality.txt -o %s/S%s_sequence_R1_boxplot.%s' % \
	(flag, dataDir,i, dataDir,i, imageFormat))
