#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def gsnap_filtProc_batch(inDirName,outDirName):

	sampNameL = list(set([re.match('.*/(.*).qlog:Processed.*',line).group(1) for line in os.popen('grep -H Processed %s/*.qlog' % inDirName)]))
	sampNameL.sort()

	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

#		if sampN in ['G17663.TCGA-19-2619-01A-01R-1850-01.2','G17814.TCGA-06-5411-01A-01R-1849-01.4']:
#			continue

		print '[%s]' % sampN

		print '\tRunning ./gsnap_filter_transloc.py'
		os.system('./gsnap_filter_transloc.py -i %s/%s_splice.gsnap -o %s/%s_splice_transloc.gsnap' % (inDirName,sampN, outDirName,sampN))
		print '\tRunning ./gsnap_filter_annot1.py'
		os.system('./gsnap_filter_annot1.py -i %s/%s_splice_transloc.gsnap -o %s/%s_splice_transloc_annot1.gsnap' % (inDirName,sampN, outDirName,sampN))
		print '\tRunning ./gsnap_splice_process.py'
		os.system('./gsnap_splice_process.py -i %s/%s_splice_transloc_annot1.gsnap -o %s/%s_splice_transloc_annot1.sorted.gsnap -r %s/%s_splice_transloc_annot1.report.txt -s %s' % \
			(inDirName,sampN, outDirName,sampN, outDirName,sampN,sampN))

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH:

	if '-o' in optH:
		gsnap_filtProc_batch(optH['-i'],optH['-o'])
	else:
		gsnap_filtProc_batch(optH['-i'],optH['-i'])
