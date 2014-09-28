#!/usr/bin/python

import sys, os, re, getopt, glob
import mybasic, mysetting


def main(inDirName,outDirName, ref='/data1/Sequence/ucsc_hg19/hg19.fasta', pbs=False):

	fileNameL = glob.glob('%s/*.recal.bam' % inDirName)

	print 'Files: %s (%s)' % (fileNameL, len(fileNameL))

	sampNameL = list(set([re.search('\/([^/]*)\.recal\.bam', inputFileN).group(1) for inputFileN in fileNameL]))
	sampNameL.sort()

	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

		print sampN

		cmd = '/usr/bin/python %s/NGS/mutation/procPileup_split.py -i %s/%s.recal.bam -r %s -o %s -q 15' % (mysetting.SRC_HOME, inDirName,sampN, ref, outDirName)

		log = '%s/%s.pileup_proc.log' % (outDirName,sampN)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))
		else:
			os.system('(%s) 2> %s' % (cmd, log))


#optL, argL = getopt.getopt(sys.argv[1:],'i:e:o:l:',[])
#
#optH = mybasic.parseParam(optL)
#
#if '-i' in optH and '-o' in optH:
#
#	main(optH['-i'], '', optH['-o'], '-t' in optH)

if __name__ == '__main__':
#	main('/pipeline/ExomeSeq_20130723/S437_T_SS', '/pipeline/ExomeSeq_20130723/S437_T_SS', False)
#	main('/EQL3/pipeline/SGI20140617_xsq2mut/IRCR_GBM13_300_T_SS', '/EQL3/pipeline/SGI20140617_xsq2mut/IRCR_GBM13_300_T_SS', False)
	main('/EQL3/pipeline/SGI20140611_xsq2mut/IRCR_GBM10_038_T_SS', '/EQL4/pipeline')
