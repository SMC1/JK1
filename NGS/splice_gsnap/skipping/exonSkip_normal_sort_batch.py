#!/usr/bin/python

import sys, os, re, getopt, time
import mybasic


def exonSkip_batch(inDirName,outDirName,cnaFilePath=None):

#	sampNameS = set([re.match('.*/(.*).qlog:Processed.*',line).group(1).replace('.gsnap','') for line in os.popen('grep -H Processed %s/*.qlog' % inDirName)])
	sampNameL = [re.match('.*\/([S0-9]+)_splice_exonSkip_normal.gsnap', x).group(1) for x in os.popen('ls -l %s/*_splice_exonSkip_normal.gsnap' % inDirName,'r')]

#	excSampNameS = set([re.search('([^/ ]+)_splice_exonSkip_report.txt',line).group(1) for line in os.popen('ls -l %s/*_exonSkip_report.txt' % inDirName)])
#	sampNameS = sampNameS.difference(excSampNameS))
#	sampNameL = list(sampNameS)

	sampNameL.sort()
	
	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL[:1]:

#		if sampN not in ['G17197.TCGA-06-0211-01B-01R-1849-01.2']:
#			continue

		#print '[%s]' % sampN

		initTime = time.time()

#		print '\tRunning exonSkip_filter.py, %s' % time.strftime('%m/%d %H:%M:%S')
#		os.system('./exonSkip_filter.py -i %s/%s_splice.gsnap -o %s/%s_splice_exonSkip.gsnap' % (inDirName,sampN, outDirName,sampN))

		#print '\tRunning exonSkip_sort.py'
		os.system('echo "/home/jinkuk/JK1/NGS/splice_gsnap/skipping/exonSkip_sort.py -i %s/%s_splice_exonSkip_normal.gsnap -r %s/%s_splice_exonSkip_normal_report.txt -s %s" \
			| qsub -N %s -o %s/%s.sort.qlog -j oe' % (inDirName,sampN, outDirName,sampN, sampN, sampN, outDirName,sampN))

#		print '\tRunning exonSkip_proc_sort.py, %s' % time.strftime('%m/%d %H:%M:%S')
#		os.system('./exonSkip_proc_sort.py -i %s/%s_splice_exonSkip.gsnap -o %s/%s_splice_exonSkip_sort.gsnap -r %s/%s_splice_exonSkip_report.txt -s %s' % \
#			(inDirName,sampN, outDirName,sampN, outDirName,sampN, sampN))

#		print '\tRunning exonSkip_proc_annot.py, %s' % time.strftime('%m/%d %H:%M:%S')
#		if cnaFilePath:
#			os.system('./exonSkip_proc_annot.py -i %s/%s_splice_exonSkip_report.txt -o %s/%s_splice_exonSkip_report_annot.txt -c %s' % \
#				(inDirName,sampN, outDirName,sampN, cnaFilePath))
#		else:
#			os.system('./exonSkip_proc_annot.py -i %s/%s_splice_exonSkip_report.txt -o %s/%s_splice_exonSkip_report_annot.txt' % \
#				(inDirName,sampN, outDirName,sampN))

		#print '\tFinished, %s, duration: %.1fmin' % (time.strftime('%m/%d %H:%M:%S'),(time.time()-initTime)/60)

optL, argL = getopt.getopt(sys.argv[1:],'i:o:c:',[])

optH = mybasic.parseParam(optL)

inFileName = optH['-i']

if '-o' in optH:
	outFileName = optH['-o']
else:
	outFileName = optH['-i']

if '-c' in optH:
	exonSkip_batch(inFileName,outFileName,optH['-c'])
else:
	exonSkip_batch(inFileName,outFileName)
