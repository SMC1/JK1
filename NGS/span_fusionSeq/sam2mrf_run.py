#!/usr/bin/python

import os

dataDir = '/data2/FusionSeq'

i = '03'

os.system('/home/tools/RSEQtools-0.6/sam2mrf < %s/RNASeq_SMC1_S%s_result.sam > %s/RNASeq_SMC1_S%s_result.mrf' % (dataDir,i,dataDir,i))
