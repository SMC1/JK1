#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def exonSkip_filter_batch(inDirName,outDirName, pbs=False):

	inFileNameL = filter(lambda x: re.match('(.*)_splice\.gsnap', x), os.listdir(inDirName))
	sampNameS = set([re.match('(.*)_splice\.gsnap', x).group(1) for x in inFileNameL])

#	sampNameS = set([re.match('.*/(.*).qlog:Processed.*',line).group(1).replace('.gsnap','') for line in os.popen('grep -H Processed %s/*.qlog' % inDirName)])
#	excSampNameS = set([re.search('([^/ ]+)_splice_exonSkip_report.txt',line).group(1) for line in os.popen('ls -l %s/*_exonSkip_report.txt' % inDirName)])
#	sampNameS = sampNameS.difference(excSampNameS)

	sampNameL = list(sampNameS)
	sampNameL.sort()
	
	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

#		if sampN not in ['G17678.TCGA-06-5417-01A-01R-1849-01.2']:
#			continue

		if pbs:
			os.system('echo "~/JK1/NGS/splice_gsnap/skipping/exonSkip_filter.py -i %s/%s_splice.gsnap -o %s/%s_splice_exonSkip.gsnap" \
				| qsub -N %s -o %s/%s.exonSkip.qlog -j oe' % (inDirName,sampN, outDirName,sampN, sampN, outDirName,sampN))
		else:
			os.system('(~/JK1/NGS/splice_gsnap/skipping/exonSkip_filter.py -i %s/%s_splice.gsnap -o %s/%s_splice_exonSkip.gsnap) &> \
				%s/%s.exonSkip.qlog' % (inDirName,sampN, outDirName,sampN,outDirName,sampN))


if __name__ == '__main__':

	exonSkip_filter_batch('/pipeline/test_skip/S436_RSq_test_splice','/home/heejin/practice/pipeline/skipping',False)

#optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])
#
#optH = mybasic.parseParam(optL)
#
#inputDirN = optH['-i']
#
#if '-o' in optH:
#	exonSkip_filter_batch(inputDirN,optH['-o'])
#else:
#	exonSkip_filter_batch(inputDirN,inputDirN)
