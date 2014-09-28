#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def align(inputDirN, outputDirN, filePattern, thread, memory, pbs=False, refN='/data1/Sequence/ucsc_hg19/hg19.fa', compressed=True):

	if compressed:
		cat_command = 'zcat'
		extension = '.gz'
	else:
		cat_command = 'cat'
		extension = ''

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match(filePattern, x),inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match(filePattern,inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

#		if sampN not in ['047T_N','464T_N','626T_N']:
#			continue

		print sampN

		sai1 = '%s/%s.1.sai' % (outputDirN, sampN)
		sai2 = '%s/%s.2.sai' % (outputDirN, sampN)
		fq1 = '%s/%s.1.fq%s' % (inputDirN, sampN, extension)
		fq2 = '%s/%s.2.fq%s' % (inputDirN, sampN, extension)

		cmd = 'bwa aln -t %s %s %s > %s; bwa aln -t %s %s %s > %s;' % (thread,refN,fq1,sai1, thread,refN,fq2,sai2)
		cmd = '%s bwa sampe -n 1 -N 1 -r "@RG\tID:%s\tSM:%s\tPL:Illumina" -P %s %s %s %s %s' % (cmd, sampN,sampN, refN, sai1,sai2,fq1,fq2)
		cmd = '%s | samtools view -Sb - | samtools sort -m %s - %s/%s.sorted' % (cmd, memory, outputDirN,sampN)

		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s/%s.bwa.qlog -j oe' % (cmd, sampN, outputDirN,sampN))
		else:
			os.system('(%s) 2> %s/%s.bwa.qlog' % (cmd, outputDirN,sampN))


if __name__ == '__main__':

	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

	defaultPattern = '(.*)\.[12]\.fq\.gz'

	#align('/EQL1/NSL/WXS_trueSeq/fastq/link', '/EQL1/NSL/WXS_trueSeq/alignment/bwa', defaultPattern, 10, 40000000000) # WXS_trueSeq
	align('/EQL1/NSL/WXS/fastq', '/EQL1/NSL/WXS/bwa', '(.*)\.[12]\.fq\.gz', 10, 40000000000, False) # WXS
	#align('/EQL1/NSL/Kinome/fastq/link', '/EQL1/NSL/Kinome/bwa', '(.*)\.[12]\.fq\.gz', 15, 60000000000, False) # Kinome
