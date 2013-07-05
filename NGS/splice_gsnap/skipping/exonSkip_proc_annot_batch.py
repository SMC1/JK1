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

		if pbs:
			if cnaFilePath:
				os.system('echo "~/JK1/NGS/splice_gsnap/skipping/exonSkip_proc_annot.py -i %s/%s_splice_exonSkip_report.txt -o %s/%s_splice_exonSkip_report_annot.txt -c %s" \
					| qsub -N %s -o %s/%s.skip_annot.qlog -j oe' % (inDirName,sampN, outDirName,sampN, cnaFilePath, sampN, outDirName,sampN))
			else:
				os.system('echo "~/JK1/NGS/splice_gsnap/skipping/exonSkip_proc_annot.py -i %s/%s_splice_exonSkip_report.txt -o %s/%s_splice_exonSkip_report_annot.txt" \
					| qsub -N %s -o %s/%s.skip_annot.qlog -j oe' % (inDirName,sampN, outDirName,sampN, sampN, outDirName,sampN))
		
		else:
			if cnaFilePath:
				os.system('(~/JK1/NGS/splice_gsnap/skipping/exonSkip_proc_annot.py -i %s/%s_splice_exonSkip_report.txt -o %s/%s_splice_exonSkip_report_annot.txt -c %s) &> \
					%s/%s.skip_annot.qlog' % (inDirName,sampN, outDirName,sampN, cnaFilePath, outDirName,sampN))
			else:
				os.system('(~/JK1/NGS/splice_gsnap/skipping/exonSkip_proc_annot.py -i %s/%s_splice_exonSkip_report.txt -o %s/%s_splice_exonSkip_report_annot.txt) &> \
					%s/%s.skip_annot.qlog' % (inDirName,sampN, outDirName,sampN, outDirName,sampN))

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
