#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(inDirName,outDirName):

	inFileNameL = filter(lambda x: re.match('(.*)_splice_exonSkip_normal\.gsnap', x), os.listdir(inDirName))
	sampNameS = set([re.match('(.*)_splice_exonSkip_normal\.gsnap', x).group(1) for x in inFileNameL])

	sampNameL = list(sampNameS)
	sampNameL.sort()
	
	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL[:1]:

		os.system('echo "/home/jinkuk/JK1/NGS/splice_gsnap/skipping/exonSkip_sort.py -i %s/%s_splice_exonSkip_normal.gsnap -r %s/%s_splice_exonSkip_report.txt -s %s" \
			| qsub -N %s -o %s/%s.sort.qlog -j oe' % (inDirName,sampN, outDirName,sampN, sampN, sampN, outDirName,sampN))

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

inDirName = optH['-i']

if '-o' in optH:
	outDirName = optH['-o']
else:
	outDirName = optH['-i']

main(inDirName,outDirName)
