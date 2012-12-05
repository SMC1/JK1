#!/usr/bin/python

import sys, os, re, getopt, time
import mybasic


def exonSkip_batch(inDirName,outDirName):

	while 1:

		sampNameS = set([re.match('.*/(.*).qlog:Processed.*',line).group(1) for line in os.popen('grep -H Processed %s/*.qlog' % inDirName)])
		excSampNameS = set([re.search('([^/ ]+)_splice_exonSkip_report.txt',line).group(1) for line in os.popen('ls -l %s/*_exonSkip_report.txt' % inDirName)])

		print sampNameS
		print excSampNameS

		sampNameL = list(sampNameS.difference(excSampNameS))

		print sampNameL

		if len(sampNameL) == 0:
			break

		sampNameL.sort()

		sampN = sampNameL[0]

		outLogFile = open('%s/%s_splice_exonSkip.log' % (outDirName,sampN),'w')

		outLogFile.write('[%s]\n' % sampN)

		initTime = time.time()

		outLogFile.write('\tRunning exonSkip_filter.py, %s\n' % time.strftime('%m/%d %H:%M:%S')); outLogFile.flush()
		
		if os.system('./exonSkip_filter.py -i %s/%s_splice.gsnap -o %s/%s_splice_exonSkip.gsnap' % \
				(inDirName,sampN, outDirName,sampN)) != 0:
			break

		outLogFile.write('\tRunning exonSkip_proc_sort.py, %s\n' % time.strftime('%m/%d %H:%M:%S')); outLogFile.flush()

		if os.system('./exonSkip_proc_sort.py -i %s/%s_splice_exonSkip.gsnap -o %s/%s_splice_exonSkip_sort.gsnap \
				-r %s/%s_splice_exonSkip_report.txt -s %s' % (inDirName,sampN, outDirName,sampN, outDirName,sampN, sampN)) != 0:
			break

		outLogFile.write('\tRunning exonSkip_proc_annot.py, %s\n' % time.strftime('%m/%d %H:%M:%S')); outLogFile.flush()

		if os.system('./exonSkip_proc_annot.py -i %s/%s_splice_exonSkip_report.txt -o %s/%s_splice_exonSkip_report_annot.txt' % \
				(inDirName,sampN, outDirName,sampN)) != 0:
			break

		outLogFile.write('\tFinished, %s, duration: %.1fmin\n' % (time.strftime('%m/%d %H:%M:%S'),(time.time()-initTime)/60))

		outLogFile.close()

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH:

	if '-o' in optH:
		exonSkip_batch(optH['-i'],optH['-o'])
	else:
		exonSkip_batch(optH['-i'],optH['-i'])
