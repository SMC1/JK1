#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(inDirName,outDirName,pbs=False):

	inFileNameL = filter(lambda x: re.match('(.*)_splice_exonSkip_normal\.gsnap\.gz', x), os.listdir(inDirName))
	sampNameS = set([re.match('(.*)_splice_exonSkip_normal\.gsnap\.gz', x).group(1) for x in inFileNameL])

	sampNameL = list(sampNameS)
	sampNameL.sort()
	
	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

		iprefix = '%s/%s' % (inDirName,sampN)
		oprefix = '%s/%s' % (outDirName,sampN)
		cmd = '~/JK1/NGS/splice_gsnap/skipping/exonSkip_sort.py -i %s_splice_exonSkip_normal.gsnap.gz -r %s_splice_exonSkip_normal_report.txt -s %s' % (iprefix, oprefix, sampN)
		log = '%s.sort_normal.qlog' % (oprefix)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))
		else:
			os.system('(%s) &> %s' % (cmd, log))


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
