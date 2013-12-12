#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(inDirName,outDirName,pbs=False):

	inFileNameL = filter(lambda x: re.match('(.*)_splice_exonSkip_normal\.gsnap', x), os.listdir(inDirName))
	sampNameS = set([re.match('(.*)_splice_exonSkip_normal\.gsnap', x).group(1) for x in inFileNameL])

	sampNameL = list(sampNameS)
	sampNameL.sort()
	
	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

		if pbs:
			os.system('echo "~/JK1/NGS/splice_gsnap/skipping/exonSkip_sort.py -i %s/%s_splice_exonSkip_normal.gsnap -r %s/%s_splice_exonSkip_normal_report.txt -s %s" \
				| qsub -N %s -o %s/%s.sort_normal.qlog -j oe' % (inDirName,sampN, outDirName,sampN, sampN, sampN, outDirName,sampN))
		else:
			os.system('(~/JK1/NGS/splice_gsnap/skipping/exonSkip_sort.py -i %s/%s_splice_exonSkip_normal.gsnap -r %s/%s_splice_exonSkip_normal_report.txt -s %s) \
				&> %s/%s.sort_normal.qlog' % (inDirName,sampN, outDirName,sampN, sampN, outDirName,sampN))


if __name__ == '__main__':

	main('/EQL2/TCGA/LUAD/RNASeq/skipping','/EQL2/TCGA/LUAD/RNASeq/skipping',False)
#optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])
#
#optH = mybasic.parseParam(optL)
#
#inDirName = optH['-i']
#
#if '-o' in optH:
#	outDirName = optH['-o']
#else:
#	outDirName = optH['-i']
#
#main(inDirName,outDirName)
