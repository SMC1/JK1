#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(inputDirN, outputDirN, pbs=False, ref='/data1/Sequence/ucsc_hg19/hg19.fa'):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('(.*)\.recal\.bam', x),inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.recal\.bam',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

#		if sampN not in ['047T','047T_N','464T','464T_N','626T','626T_N']:
#			continue

		print sampN
		cmd = 'samtools mpileup -f %s %s/%s.recal.bam > %s/%s.pileup' % (ref, inputDirN,sampN, outputDirN,sampN)
		log = '%s/%s.pileup.log' % (outputDirN,sampN)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))

		else:
			os.system('(%s) 2> %s' % (cmd, log))



if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

	main('/Z/NSL/RNASeq/align/splice/gatk_test', '/Z/NSL/RNASeq/align/splice/gatk_test', True)
