#!/usr/bin/python

import sys, os, re, getopt, time
import mybasic


def main(inDirName,outDirName):

	sampNameS = set([re.match('.*/(.*).gsnap.qlog:Processed.*',line).group(1).replace('.gsnap','') for line in os.popen('grep -H Processed %s/*.gsnap.qlog' % inDirName)])

#	excSampNameS = set([re.search('([^/ ]+)_splice_transloc_annot1.report.txt',line).group(1) for line in os.popen('ls -l %s/*_transloc_annot1.report.txt' % inDirName)])
#	sampNameS = sampNameS.difference(excSampNameS)

	sampNameL = list(sampNameS)
	sampNameL.sort()
	
	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

#		if sampN not in ['G17678.TCGA-06-5417-01A-01R-1849-01.2']:
#			continue

		print sampN 

		os.system('echo "~jinkuk/JK1/NGS/splice_gsnap/ei_junc/ei_junc.py -i %s/%s_splice.gsnap -o %s/%s_ei_RTK1.dat -s %s" \
			| qsub -N %s -o %s/%s.ei_RTK1.qlog -j oe' % (inDirName,sampN, outDirName,sampN, sampN, sampN, outDirName,sampN))

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH:

	if '-o' in optH:
		main(optH['-i'],optH['-o'])
	else:
		main(optH['-i'],optH['-i'])
