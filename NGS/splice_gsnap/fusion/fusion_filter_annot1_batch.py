#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(inDirName,outDirName,pbs=False):

	sampNameL = [re.match('.*\/([^/]*)_splice_transloc.gsnap', x).group(1) for x in os.popen('ls -l %s/*_splice_transloc.gsnap' % inDirName)]

	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

#		if sampN in ['G17663.TCGA-19-2619-01A-01R-1850-01.2','G17814.TCGA-06-5411-01A-01R-1849-01.4']:
#			continue

		print '[%s]' % sampN
		iprefix = '%s/%s' % (inDirName,sampN)
		oprefix = '%s/%s' % (outDirName,sampN)
		cmd = '~/JK1/NGS/splice_gsnap/fusion/fusion_filter_annot1.py -i %s_splice_transloc.gsnap -o %s_splice_transloc_annot1.gsnap' % (iprefix, oprefix)
		log = '%s.annot.qlog' % (oprefix)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))

		else:
			os.system('(%s) &> %s' % (cmd, log))



if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

	if '-i' in optH and '-o' in optH:
		main(optH['-i'], optH['-o'], False)
#	main('/home/heejin/practice/pipeline/fusion','/home/heejin/practice/pipeline/fusion',False)
