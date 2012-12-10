#!/usr/bin/python

import sys, os, re, getopt, time
import mybasic


def exonSkip_batch(inDirName,outDirName):

	sampNameS = set([re.match('.*/(.*).qlog:Processed.*',line).group(1) for line in os.popen('grep -H Processed %s/*.qlog' % inDirName)])
	excSampNameS = set([re.search('([^/ ]+)_splice_exonSkip_report.txt',line).group(1) for line in os.popen('ls -l %s/*_exonSkip_report.txt' % inDirName)])

	sampNameL = list(sampNameS.difference(excSampNameS))
	sampNameL.sort()
	
	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

#		if sampN not in ['G17197.TCGA-06-0211-01B-01R-1849-01.2']:
#			continue

		os.system('echo "~jinkuk/JK1/NGS/splice_gsnap/skipping/exonSkip_filter.py -i %s/%s_splice.gsnap -o %s/%s_splice_exonSkip.gsnap" \
			| qsub -N %s -o %s/exonSkip_filter_qlog/%s.qlog -j oe' % (inDirName,sampN, outDirName,sampN, sampN, outDirName,sampN))

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH:

	if '-o' in optH:
		exonSkip_batch(optH['-i'],optH['-o'])
	else:
		exonSkip_batch(optH['-i'],optH['-i'])
