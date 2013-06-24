#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mygenome


def align(inputDirN, outputDirN, filePattern, thread, memory, pbs=False, assemCode='hg19', compressed=True):

	assemblyH = {'hg18':'/data1/Sequence/ucsc_hg18/hg18.fa', 'hg19':'/data1/Sequence/ucsc_hg19/hg19.fa'}
	assemFN = assemblyH[assemCode] #mygenome.assemblyH[assemCode]

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

#		if pbs:
#			os.system('echo "bwa aln -t %s %s %s/%s_R1.fq > %s/%s.1.sai; bwa aln -t %s %s %s/%s_R2.fq > %s/%s.2.sai; \
#				bwa sampe -n 1 -N 1 -P %s %s/%s.1.sai %s/%s.2.sai %s/%s_R1.fq %s/%s_R2.fq | \
#				samtools view -Sb - | samtools sort -m %s - %s/%s.sorted" | qsub -N %s -o %s/%s.bwa.qlog -j oe' % \
#				(thread,assemFN,inputDirN,sampN,outputDirN,sampN, thread,assemFN,inputDirN,sampN,outputDirN,sampN, \
#				assemFN, outputDirN,sampN, outputDirN,sampN, inputDirN,sampN, inputDirN,sampN, \
#				memory, outputDirN,sampN, sampN, outputDirN,sampN))

		print sampN

		os.system('(%s %s/%s.1.fq%s | bwa aln -t %s %s - > %s/%s.1.sai; \
			%s %s/%s.2.fq%s | bwa aln -t %s %s - > %s/%s.2.sai; \
			bwa sampe -n 1 -N 1 -P %s %s/%s.1.sai %s/%s.2.sai %s/%s.1.fq%s %s/%s.2.fq%s | \
			samtools view -Sb - | samtools sort -m %s - %s/%s.sorted) 2> %s/%s.bwa.qlog' % \
			(cat_command,inputDirN,sampN,extension,thread,assemFN,outputDirN,sampN, \
			cat_command,inputDirN,sampN,extension,thread,assemFN,outputDirN,sampN, \
			assemFN, outputDirN,sampN, outputDirN,sampN, inputDirN,sampN,extension, inputDirN,sampN,extension, \
			memory, outputDirN,sampN, outputDirN,sampN))


if __name__ == '__main__':

	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

	defaultPattern = '(.*)\.[12]\.fq\.gz'

	#align('/EQL1/NSL/WXS_trueSeq/fastq/link', '/EQL1/NSL/WXS_trueSeq/alignment/bwa', defaultPattern, 10, 40000000000) # WXS_trueSeq
	align('/EQL1/NSL/WXS/fastq', '/EQL1/NSL/WXS/bwa', '(.*)\.[12]\.fq\.gz', 10, 40000000000, False) # WXS
	#align('/EQL1/NSL/Kinome/fastq/link', '/EQL1/NSL/Kinome/bwa', '(.*)\.[12]\.fq\.gz', 15, 60000000000, False) # Kinome
