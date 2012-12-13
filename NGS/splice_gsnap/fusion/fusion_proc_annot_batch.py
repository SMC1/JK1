#!/usr/bin/python

import sys, os, re, getopt, time
import mybasic


def fusion_proc_annot_batch(inDirName,outDirName,cnaFilePath=None):

	sampNameS = set([re.match('.*/(.*).qlog:Processed.*',line).group(1) for line in os.popen('grep -H Processed %s/*.qlog' % inDirName)])

#	excSampNameS = set([re.search('([^/ ]+)_splice_transloc_annot1.report.txt',line).group(1) for line in os.popen('ls -l %s/*_transloc_annot1.report.txt' % inDirName)])
#	sampNameS = sampNameS.difference(excSampNameS)

	sampNameL = list(sampNameS)
	sampNameL.sort()
	
	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

		if sampN not in ['G17209.TCGA-06-0219-01A-01R-1849-01.2']:
			continue

		print sampN 

		if cnaFilePath:
			os.system('echo "~jinkuk/JK1/NGS/splice_gsnap/fusion/fusion_proc_annot.py -i %s/%s_splice_transloc_annot1.report.txt -o %s/%s_splice_transloc_annot1.report_annot.txt -c %s" \
				| qsub -N %s -o %s/fusion_qlog/%s.annot.qlog -j oe' % (inDirName,sampN, outDirName,sampN, cnaFilePath, sampN, outDirName,sampN))
		else:
			os.system('echo "~jinkuk/JK1/NGS/splice_gsnap/fusion/fusion_proc_annot.py -i %s/%s_splice_transloc_annot1.report.txt -o %s/%s_splice_transloc_annot1.report_annot.txt" \
				| qsub -N %s -o %s/fusion_qlog/%s.annot.qlog -j oe' % (inDirName,sampN, outDirName,sampN, sampN, outDirName,sampN))

optL, argL = getopt.getopt(sys.argv[1:],'i:o:c:',[])

optH = mybasic.parseParam(optL)

inFileName = optH['-i']

if '-o' in optH:
	outFileName = optH['-o']
else:
	outFileName = inFileName

if '-c' in optH:
	fusion_proc_annot_batch(inFileName,outFileName,optH['-c'])
else:
	fusion_proc_annot_batch(inFileName,outFileName)
