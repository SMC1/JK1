#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mysetting


def exonSkip_filter_batch(inDirName,outDirName, pbs=False):

	inFileNameL = filter(lambda x: re.match('(.*)_splice\.gsnap\.gz', x), os.listdir(inDirName))
	sampNameS = set([re.match('(.*)_splice\.gsnap\.gz', x).group(1) for x in inFileNameL])

#   sampNameS = set([re.match('.*/(.*).qlog:Processed.*',line).group(1).replace('.gsnap','') for line in os.popen('grep -H Processed %s/*.qlog' % inDirName)])
#	excSampNameS = set([re.search('([^/ ]+)_splice_exonSkip_report.txt',line).group(1) for line in os.popen('ls -l %s/*_exonSkip_report.txt' % inDirName)])
#	sampNameS = sampNameS.difference(excSampNameS)

	if len(os.popen('ls %s/*exonSkip_normal.qlog' % outDirName).readlines()) > 0:
		excSampNameS = set([re.match('.*/(.*)\.exonSkip_normal.qlog:Results.*',line).group(1).replace('_splice.gsnap','') for line in os.popen('grep -H Results %s/*.qlog' % outDirName)])
		sampNameS = sampNameS.difference(excSampNameS)

	sampNameL = list(sampNameS)
	sampNameL.sort()
	
	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

#		if sampN not in ['G17678.TCGA-06-5417-01A-01R-1849-01.2']:
#			continue

		iprefix = '%s/%s' % (inDirName,sampN)
		oprefix = '%s/%s' % (outDirName,sampN)
		cmd = '%s/NGS/splice_gsnap/skipping/exonSkip_filter_normal.py -i %s_splice.gsnap.gz -o %s_splice_exonSkip_normal.gsnap.gz' % (mysetting.SRC_HOME, iprefix, oprefix)
		log = '%s.exonSkip_normal.qlog' % (oprefix)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))
		else:
			os.system('(%s) &> %s' % (cmd, log))


if __name__ == '__main__':

#	exonSkip_filter_batch('/pipeline/fusion_test/S436_RSq_test','/home/heejin/practice/pipeline/skipping',False)

	optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

	optH = mybasic.parseParam(optL)

	inputDirN = optH['-i']

	if '-o' in optH:
		exonSkip_filter_batch(inputDirN,optH['-o'])
	else:
		exonSkip_filter_batch(inputDirN,inputDirN)
