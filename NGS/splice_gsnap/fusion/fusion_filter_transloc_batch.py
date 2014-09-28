#!/usr/bin/python

import sys, os, re, getopt, time
import mybasic, mysetting


def fusion_filter_batch(inDirName,outDirName, pbs=False):
	inFileNameL = filter(lambda x: re.match('(.*)_splice\.gsnap\.gz$', x), os.listdir(inDirName))
	sampNameS = set([re.match('(.*)_splice\.gsnap\.gz$', x).group(1) for x in inFileNameL])

#	excSampNameS = set([re.search('([^/ ]+)_splice_transloc_annot1.report.txt',line).group(1) for line in os.popen('ls -l %s/*_transloc_annot1.report.txt' % inDirName)])
#	sampNameS = sampNameS.difference(excSampNameS)

	sampNameL = list(sampNameS)
	sampNameL.sort()
	
	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

#		if sampN not in ['G17678.TCGA-06-5417-01A-01R-1849-01.2']:
#			continue
		print sampN 
		iprefix = '%s/%s' % (inDirName,sampN)
		oprefix = '%s/%s' % (outDirName,sampN)
		cmd = '%s/NGS/splice_gsnap/fusion/fusion_filter_transloc.py -i %s_splice.gsnap.gz -o %s_splice_transloc.gsnap' % (mysetting.SRC_HOME, iprefix, oprefix)
		log = '%s.ft_tloc.qlog' % (oprefix)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))
		
		else:
			os.system('(%s) &> %s' % (cmd, log))


if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

	optH = mybasic.parseParam(optL)

	if '-i' in optH:

		if '-o' in optH:
			fusion_filter_batch(optH['-i'],optH['-o'])
		else:
			fusion_filter_batch(optH['-i'],optH['-i'])
#	fusion_filter_batch('/home/heejin/practice/pipeline/fusion','/home/heejin/practice/pipeline/fusion',False)
