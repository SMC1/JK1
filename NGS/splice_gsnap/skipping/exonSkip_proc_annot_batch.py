#!/usr/bin/python

import sys, os, re, getopt, time
import mybasic


def exonSkip_proc_annot_batch(inDirName,outDirName,cnaFilePath=None, pbs=False):

#	sampNameS = set([re.match('.*/(.*).qlog:Processed.*',line).group(1).replace('.gsnap','') for line in os.popen('grep -H Processed %s/*.qlog' % inDirName)])
	sampNameL = [re.match('.*\/(.*)_splice_exonSkip_report.txt', x).group(1) for x in os.popen('ls -l %s/*_splice_exonSkip_report.txt' % inDirName,'r')]

#	excSampNameS = set([re.search('([^/ ]+)_splice_transloc_annot1.report.txt',line).group(1) for line in os.popen('ls -l %s/*_transloc_annot1.report.txt' % inDirName)])
#	sampNameS = sampNameS.difference(excSampNameS)
#	sampNameL = list(sampNameS)

	sampNameL.sort()
	
	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

#		if sampN not in ['G17792.TCGA-28-5204-01A-01R-1850-01.4']:
#			continue

		print sampN 

		iprefix = '%s/%s' % (inDirName,sampN)
		oprefix = '%s/%s' % (outDirName,sampN)
		if cnaFilePath:
			cna = '-c %s' % (cnaFilePath)
		else:
			cna = ''
		cmd = '~/JK1/NGS/splice_gsnap/skipping/exonSkip_proc_annot.py -i %s_splice_exonSkip_report.txt -o %s_splice_exonSkip_report_annot.txt %s' % (iprefix, oprefix, cna)
		log = '%s.skip_annot.qlog' % (oprefix)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))
		
		else:
			os.system('(%s) &> %s' % (cmd, log))

if __name__ == '__main__':
	
	exonSkip_proc_annot_batch('/home/heejin/practice/pipeline/skipping','/home/heejin/practice/pipeline/skipping',None,False)

#	optL, argL = getopt.getopt(sys.argv[1:],'i:o:c:',[])
#
#	optH = mybasic.parseParam(optL)
#
#	inFileName = optH['-i']
#
#	if '-o' in optH:
#		outFileName = optH['-o']
#	else:
#		outFileName = inFileName
#
#	if '-c' in optH:
#		exonSkip_proc_annot_batch(inFileName,outFileName,optH['-c'])
#	else:
#		exonSkip_proc_annot_batch(inFileName,outFileName)
