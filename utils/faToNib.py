#!/usr/bin/python

import sys
import os

seqGroupName = ['seedLib_55k','pombe', 'tair9', 'ucsc_hg19']
seqName = [['array_55k_seq_final'],['chr1','chr2','chr3'], ['Chr%s' % s for s in range(1,6)+['C','M']], ['chr%s' % s for s in range(1,23)+['X','Y','M']]]

for i in [-1]: #range(len(seqGroupName)):

	for seqN in seqName[i]:

		os.system('faToNib ./%s/%s.fa ./%s/%s.nib' % (seqGroupName[i],seqN,seqGroupName[i],seqN))
