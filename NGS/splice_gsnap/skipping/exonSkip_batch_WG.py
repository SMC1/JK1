#!/usr/bin/python

import sys, os, re, getopt, time
import mybasic


def exonSkip_batch(inDirName,outDirName):

	sampNameL = list(set([re.match('.*/(.*).qlog:Processed.*',line).group(1) for line in os.popen('grep Processed %s/*.qlog' % inDirName)]))
	sampNameL.sort()

	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

		if sampN not in ['G17197.TCGA-06-0211-01B-01R-1849-01.2']:
			continue

		outLogFile = open('%s/%s.proc.log' % (outDirName,sampN),'w')

		outLogFile.write('[%s]\n' % sampN)

		initTime = time.time()

		outLogFile.write('\tRunning exonSkip_filter_annot.py, %s\n' % time.strftime('%m/%d %H:%M:%S')); outLogFile.flush()
		os.system('./exonSkip_filter_annot.py -i %s/%s_splice.gsnap -o %s/%s_splice_exonSkip.gsnap' % (inDirName,sampN, outDirName,sampN))

		outLogFile.write('\tRunning exonSkip_proc_sort.py, %s\n' % time.strftime('%m/%d %H:%M:%S')); outLogFile.flush()
		os.system('./exonSkip_proc_sort.py -i %s/%s_splice_exonSkip.gsnap -o %s/%s_splice_exonSkip_sort.gsnap -r %s/%s_splice_exonSkip_report.txt -s %s' % \
			(inDirName,sampN, outDirName,sampN, outDirName,sampN, sampN))

		outLogFile.write('\tRunning exonSkip_proc_annot.py, %s\n' % time.strftime('%m/%d %H:%M:%S')); outLogFile.flush()
		os.system('./exonSkip_proc_annot.py -i %s/%s_splice_exonSkip_report.txt -o %s/%s_splice_exonSkip_report_annot.txt' % \
			(inDirName,sampN, outDirName,sampN))

		outLogFile.write('\tFinished, %s, duration: %.1fmin\n' % (time.strftime('%m/%d %H:%M:%S'),(time.time()-initTime)/60))

		outLogFile.close()

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH:

	if '-o' in optH:
		exonSkip_batch(optH['-i'],optH['-o'])
	else:
		exonSkip_batch(optH['-i'],optH['-i'])
