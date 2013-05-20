#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def fusion_proc_batch(inDirName,outDirName,cnaFilePath=None):

#	sampNameL = list(set([re.match('.*/(.*).qlog:Processed.*',line).group(1).replace('.gsnap','') for line in os.popen('grep -H Processed %s/*.qlog' % inDirName)]))
#	sampNameL.sort()

	sampNameL = [re.match('.*\/([^/]*)_splice_transloc.gsnap', x).group(1) for x in os.popen('ls -l %s/*_splice_transloc.gsnap' % inDirName)]

	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

#		if sampN in ['G17663.TCGA-19-2619-01A-01R-1850-01.2','G17814.TCGA-06-5411-01A-01R-1849-01.4']:
#			continue

		print '[%s]' % sampN

#		print '\tRunning ./fusion_filter_transloc.py'
#		os.system('./fusion_filter_transloc.py -i %s/%s_splice.gsnap -o %s/%s_splice_transloc.gsnap' % (inDirName,sampN, outDirName,sampN))

		print '\tRunning ./fusion_filter_annot1.py'
		os.system('./fusion_filter_annot1.py -i %s/%s_splice_transloc.gsnap -o %s/%s_splice_transloc_annot1.gsnap' % (inDirName,sampN, outDirName,sampN))

		print '\tRunning ./fusion_proc_sort.py'
		os.system('./fusion_proc_sort.py -i %s/%s_splice_transloc_annot1.gsnap -o %s/%s_splice_transloc_annot1.sorted.gsnap -r %s/%s_splice_transloc_annot1.report.txt -s %s' % \
			(inDirName,sampN, outDirName,sampN, outDirName,sampN,sampN))

#		print '\tRunning ./fusion_proc_annot.py'
#
#		if cnaFilePath:
#			os.system('./fusion_proc_annot.py -i %s/%s_splice_transloc_annot1.report.txt -o %s/%s_splice_transloc_annot1.report_annot.txt -c %s' % \
#				(inDirName,sampN, outDirName,sampN, cnaFilePath))
#		else:
#			os.system('./fusion_proc_annot.py -i %s/%s_splice_transloc_annot1.report.txt -o %s/%s_splice_transloc_annot1.report_annot.txt' % \
#				(inDirName,sampN, outDirName,sampN))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:c:',[])

optH = mybasic.parseParam(optL)

print optH

inFileName = optH['-i']

if '-o' in optH:
	outFileName = optH['-o']
else:
	outFileName = optH['-i']

if '-c' in optH:
	fusion_proc_batch(inFileName,outFileName,optH['-c'])
else:
	fusion_proc_batch(inFileName,outFileName)
