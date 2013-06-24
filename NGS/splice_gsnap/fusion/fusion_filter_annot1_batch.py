#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(inDirName,outDirName,pbs=False):

	sampNameL = [re.match('.*\/([^/]*)_splice_transloc.gsnap', x).group(1) for x in os.popen('ls -l %s/*_splice_transloc.gsnap' % inDirName)]

	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

#		if sampN in ['G17663.TCGA-19-2619-01A-01R-1850-01.2','G17814.TCGA-06-5411-01A-01R-1849-01.4']:
#			continue
		if pbs:
			print '[%s]' % sampN

			os.system('echo "~/JK1/NGS/splice_gsnap/fusion/fusion_filter_annot1.py -i %s/%s_splice_transloc.gsnap -o %s/%s_splice_transloc_annot1.gsnap" | \
				qsub -N %s -o %s/%s.annot.qlog -j oe' % (inDirName,sampN, outDirName,sampN, sampN, outDirName,sampN))

		else:
			print '[%s]' % sampN

			os.system('(~/JK1/NGS/splice_gsnap/fusion/fusion_filter_annot1.py -i %s/%s_splice_transloc.gsnap -o %s/%s_splice_transloc_annot1.gsnap) &> \
				%s/%s.annot.qlog' % (inDirName,sampN, outDirName,sampN, outDirName,sampN))


if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

	main('/home/heejin/practice/pipeline/fusion','/home/heejin/practice/pipeline/fusion',False)
