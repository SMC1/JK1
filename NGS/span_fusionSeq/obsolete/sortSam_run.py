#!/usr/bin/python

import os

dataDir = '/data2/FusionSeq'

i = '03'

os.system('sort -r %s/RNASeq_SMC1_S%s_result.sam > %s/RNASeq_SMC1_S%s_result_sorted.sam' % (dataDir,i,dataDir,i))

#os.system('rm %s/RNASeq_SMC1_S%s_result.sam' % (dataDir,i))
