#!/usr/bin/python

import sys, os, re

fileNameL_pre = ['/Data2/%s' % s for s in os.listdir('/Data2')] + \
	['/Data1/Data2_RNASeq_result/%s' % s for s in os.listdir('/Data1/Data2_RNASeq_result')] + \
	['/Data2/GH/%s' % s for s in os.listdir('/Data2/GH')]

fileNameL = []

for fileName in fileNameL_pre:

	if re.match('.*/RNASeq_SMC[0-9]*_S[0-9]*_result.txt', fileName):
	#if re.match('.*/GH.txt', fileName):
		fileNameL.append(fileName)

for fileName in fileNameL:

	os.system('./gsnap_stats.py %s' % fileName)
