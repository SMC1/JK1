#!/usr/bin/python

import os

dataDir = '/data1/RNASeq_LymphNK/00_Sequence_fastq/SMC1'

i = '03'

os.system('gsnap --db=hg19 --batch=5 --nthreads=30 --npath=1 -A sam \
	%s/S%s_sequence_R1.txt %s/S%s_sequence_R2.txt \
	> /data2/FusionSeq/RNASeq_SMC1_S%s_result.sam \
	2> /data2/FusionSeq/RNASeq_SMC1_S%s_result_log.txt' \
	% (dataDir,i,dataDir,i, i,i))
