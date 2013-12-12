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

		if sampN not in ['TCGA-91-6840-01A-11R-1949-07','TCGA-L4-A4E6-01A-11R-A24H-07']:
			continue

		if pbs:
			os.system('echo "~/JK1/NGS/splice_gsnap/skipping/exonSkip_filter.py -i %s/%s_splice.gsnap -o %s/%s_splice_exonSkip.gsnap" \
				| qsub -N %s -o %s/%s.exonSkip.qlog -j oe' % (inDirName,sampN, outDirName,sampN, sampN, outDirName,sampN))
		else:
			os.system('(~/JK1/NGS/splice_gsnap/skipping/exonSkip_filter.py -i %s/%s_splice.gsnap -o %s/%s_splice_exonSkip.gsnap) &> \
				%s/%s.exonSkip.qlog' % (inDirName,sampN, outDirName,sampN,outDirName,sampN))


if __name__ == '__main__':

	exonSkip_filter_batch('/EQL2/TCGA/LUAD/RNASeq/alignment/splice_EGFR/link','/EQL2/TCGA/LUAD/RNASeq/skipping/exonskip',False)

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
