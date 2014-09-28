#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mysetting


def main(inDirName,outDirName,pbs=False):

	inFileNameL = filter(lambda x: re.match('(.*)_splice_exonSkip\.gsnap', x), os.listdir(inDirName))
	sampNameS = set([re.match('(.*)_splice_exonSkip\.gsnap', x).group(1) for x in inFileNameL])

	sampNameL = list(sampNameS)
	sampNameL.sort()
	
	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:
	
		iprefix = '%s/%s' % (inDirName,sampN)
		oprefix = '%s/%s' % (outDirName,sampN)
		cmd = '%s/NGS/splice_gsnap/skipping/exonSkip_sort.py -i %s_splice_exonSkip.gsnap -r %s_splice_exonSkip_report.txt -s %s' % (mysetting.SRC_HOME, iprefix, oprefix, sampN)
		log = '%s.sort.qlog' % (oprefix)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))
		else:
			os.system('(%s) &> %s' % (cmd, log))


if __name__ == '__main__':

	main('/EQL2/TCGA/LUAD/RNASeq/skipping/exonskip','/EQL2/TCGA/LUAD/RNASeq/skipping/exonskip',False)

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
