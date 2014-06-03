#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(inDirName,outDirName,pbs=False):

	inFileNameL = filter(lambda x: re.match('(.*)_splice\.gsnap\.gz', x), os.listdir(inDirName))
	sampNameS = set([re.match('(.*)_splice\.gsnap\.gz', x).group(1) for x in inFileNameL])

#	excSampNameS = set([re.search('([^/ ]+)_splice_transloc_annot1.report.txt',line).group(1) for line in os.popen('ls -l %s/*_transloc_annot1.report.txt' % inDirName)])
#	sampNameS = sampNameS.difference(excSampNameS)

	sampNameL = list(sampNameS)
	sampNameL.sort()
	
	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

#		if sampN not in ['G17678.TCGA-06-5417-01A-01R-1849-01.2']:
#			continue

		print sampN 

		iprefix = '%s/%s' % (inDirName,sampN)
		oprefix = '%s/%s' % (outDirName,sampN)
		cmd = '~/JK1/NGS/splice_gsnap/ei_junc/ei_junc.py -i %s_splice.gsnap.gz -o %s_ei.dat -s %s' % (iprefix, oprefix, sampN)
		log = '%s.ei.qlog' % (oprefix)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))
		else:
			os.system('(%s) &> %s' % (cmd, log))

if __name__ == '__main__':
	
#	main('/EQL2/TCGA/LUAD/RNASeq/align','/EQL2/TCGA/LUAD/RNASeq/eijunc',False)

	optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

	optH = mybasic.parseParam(optL)

	if '-i' in optH:

		if '-o' in optH:
			main(optH['-i'],optH['-o'])
		else:
			main(optH['-i'],optH['-i'])
