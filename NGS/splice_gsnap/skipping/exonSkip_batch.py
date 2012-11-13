#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def exonSkip_batch(inDirName,outDirName):

	sampNameL = list(set([re.match('.*/(.*).qlog:Processed.*',line).group(1) for line in os.popen('grep Processed %s/*.qlog' % inDirName)]))
	sampNameL.sort()

	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

#		if sampN in ['G17663.TCGA-19-2619-01A-01R-1850-01.2','G17814.TCGA-06-5411-01A-01R-1849-01.4']:
#			continue

		print '[%s]' % sampN

		print '\tRunning ./exonSkip_gsnap_filter_annot.py'
		os.system('./exonSkip_gsnap_filter_annot.py -i %s/%s_splice.gsnap -o %s/%s_splice_annot.gsnap' % (inDirName,sampN, outDirName,sampN))

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH:

	if '-o' in optH:
		exonSkip_batch(optH['-i'],optH['-o'])
	else:
		exonSkip_batch(optH['-i'],optH['-i'])
