#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(inDirName,outDirName,pbs=False):

	inFileNameL = filter(lambda x: re.match('(.*)_splice\.gsnap', x), os.listdir(inDirName))
	sampNameS = set([re.match('(.*)_splice\.gsnap', x).group(1) for x in inFileNameL])

	excSampNameS = set([re.match('.*/(.*).ei.qlog:Finished.*',line).group(1) for line in os.popen('grep Finished %s/*.ei.qlog' % outDirName)])
#	excSampNameS = set([re.search('([^/ ]+)_splice_transloc_annot1.report.txt',line).group(1) for line in os.popen('ls -l %s/*_transloc_annot1.report.txt' % inDirName)])
	sampNameS = sampNameS.difference(excSampNameS)

	sampNameL = list(sampNameS)
	sampNameL.sort()
	
	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

#		if int(sampN[13:15]) >= 10:
#			continue

		print sampN 

		if pbs:
			os.system('echo "~/JK1/NGS/splice_gsnap/ei_junc/ei_junc_EGFR.py -i %s/%s_splice.gsnap -o %s/%s_ei_EGFR.dat -s %s" \
				| qsub -N %s -o %s/%s.ei.qlog -j oe' % (inDirName,sampN, outDirName,sampN, sampN, sampN, outDirName,sampN))
		else:
			os.system('(~/JK1/NGS/splice_gsnap/ei_junc/ei_junc_EGFR.py -i %s/%s_splice.gsnap -o %s/%s_ei_EGFR.dat -s %s) &> \
				%s/%s.ei.qlog' % (inDirName,sampN, outDirName,sampN, sampN, outDirName,sampN))

if __name__ == '__main__':
	
	main('/EQL2/TCGA/LUAD/RNASeq/alignment/splice_EGFR/link','/EQL2/TCGA/LUAD/RNASeq/ei_junc',False)

#	optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])
#
#	optH = mybasic.parseParam(optL)
#
#	if '-i' in optH:
#
#		if '-o' in optH:
#			main(optH['-i'],optH['-o'])
#		else:
#			main(optH['-i'],optH['-i'])
