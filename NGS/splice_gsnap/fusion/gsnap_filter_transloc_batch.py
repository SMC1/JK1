#!/usr/bin/python

import sys, os, re, getopt, time
import mybasic


def fusion_filter_batch(inDirName,outDirName):

	sampNameS = set([re.match('.*/(.*).qlog:Processed.*',line).group(1) for line in os.popen('grep -H Processed %s/*.qlog' % inDirName)])

#	excSampNameS = set([re.search('([^/ ]+)_splice_transloc_annot1.report.txt',line).group(1) for line in os.popen('ls -l %s/*_transloc_annot1.report.txt' % inDirName)])
#	sampNameS = sampNameS.difference(excSampNameS)

	sampNameL = list(sampNameS)
	sampNameL.sort()
	
#	sampNameL = ['G17188.TCGA-02-0047-01A-01R-1849-01.2'] + sampNameL

	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

#		if sampN not in ['G17197.TCGA-06-0211-01B-01R-1849-01.2']:
#			continue

		os.system('echo "~jinkuk/JK1/NGS/splice_gsnap/fusion/gsnap_filter_transloc.py -i %s/%s_splice.gsnap -o %s/%s_splice_transloc.gsnap" \
			| qsub -N %s -o %s/fusion_filter_qlog/%s.qlog -j oe' % (inDirName,sampN, outDirName,sampN, sampN, outDirName,sampN))

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH:

	if '-o' in optH:
		fusion_filter_batch(optH['-i'],optH['-o'])
	else:
		fusion_filter_batch(optH['-i'],optH['-i'])
