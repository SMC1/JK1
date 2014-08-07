#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(inputDirN, outputDirN, pbs=False):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('(.*)\.sorted.bam', x),inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.sorted.bam',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	print 'Samples: %s' % sampNL, len(sampNL)

	for sampN in sampNL:

#		if sampN not in ['047T_N','047T','464T','464T_N','626T','626T_N']:
#			continue

		print sampN
		iprefix = '%s/%s' % (inputDirN,sampN)
		oprefix = '%s/%s' % (outputDirN,sampN)
		cmd = 'java -jar /home/tools/picard/MarkDuplicates.jar I=%s.sorted.bam O=%s.dedup.bam METRICS_FILE=%s.PCR_duplicates REMOVE_DUPLICATES=true ASSUME_SORTED=true VALIDATION_STRINGENCY=LENIENT CREATE_INDEX=true' % (iprefix, oprefix, oprefix)
# done during 'bwa sampe'
#		cmd = '%s; java -jar /home/tools/picard/AddOrReplaceReadGroups.jar I=%s.dedup.bam O=%s.RG.bam SORT_ORDER=coordinate RGID=%s RGLB=%s RGPL=illumina RGPU=ex RGSM=%s VALIDATION_STRINGENCY=LENIENT' % (cmd, oprefix, oprefix, sampN, sampN, sampN)
		log = '%s.dedup.qlog' % (oprefix)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))


		else:
			os.system('(%s) 2> %s' % (cmd, log))


if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

	#main('/EQL1/NSL/WXS/bwa', '/EQL1/NSL/Exome/bwa', True)
	#main('/EQL1/NSL/Exome/bwa', '/EQL1/NSL/Exome/bwa', True)
	main('/Z/NSL/RNASeq/align/splice/gatk_test', '/Z/NSL/RNASeq/align/splice/gatk_test', True)
