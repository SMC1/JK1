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

		if pbs:

			print sampN

			os.system('echo "java -jar /home/tools/picard/MarkDuplicates.jar I=%s/%s.sorted.bam O=%s/%s.dedup.bam \
			METRICS_FILE=%s/%s.PCR_duplicates REMOVE_DUPLICATES=true ASSUME_SORTED=true VALIDATION_STRINGENCY=LENIENT; \
			java -jar /home/tools/picard/AddOrReplaceReadGroups.jar I=%s/%s.dedup.bam O=%s/%s.RG.bam \
			SORT_ORDER=coordinate RGID=%s RGLB=%s RGPL=illumina RGPU=ex RGSM=%s VALIDATION_STRINGENCY=LENIENT" | \
			qsub -N %s -o %s/%s.dedup.qlog -j oe' \
			% (inputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, sampN,sampN,sampN, sampN, outputDirN,sampN))

		else:

			print sampN

			os.system('java -jar /home/tools/picard/MarkDuplicates.jar I=%s/%s.sorted.bam O=%s/%s.dedup.bam \
			METRICS_FILE=%s/%s.PCR_duplicates REMOVE_DUPLICATES=true ASSUME_SORTED=true VALIDATION_STRINGENCY=LENIENT; \
			java -jar /home/tools/picard/AddOrReplaceReadGroups.jar I=%s/%s.dedup.bam O=%s/%s.RG.bam \
			SORT_ORDER=coordinate RGID=%s RGLB=%s RGPL=illumina RGPU=ex RGSM=%s VALIDATION_STRINGENCY=LENIENT 2> %s/%s.dedup.qlog'\
			% (inputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, sampN,sampN,sampN, outputDirN,sampN))

#			os.system('java -jar /home/tools/VarScan/VarScan.v2.3.3.jar pileup2snp %s/%s.pileup > %s/%s.snp 2> %s/%s.snp.qlog' % \
#				(inputDirN,sampN, outputDirN,sampN, outputDirN,sampN))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

optH = mybasic.parseParam(optL)

#main('/EQL1/NSL/WXS/bwa', '/EQL1/NSL/Exome/bwa', True)
#main('/EQL1/NSL/Exome/bwa', '/EQL1/NSL/Exome/bwa', True)
main('/Z/NSL/RNASeq/align/splice/gatk_test', '/Z/NSL/RNASeq/align/splice/gatk_test', True)
