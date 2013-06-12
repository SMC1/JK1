#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(inputDirN, outputDirN, pbs=False):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('(.*)\.recal.bam', x),inputFileNL)
	

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.recal.bam',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	print 'Samples: %s' % sampNL, len(sampNL)

	for sampN in sampNL:

#		if sampN not in ['047T_N','047T','464T','464T_N','626T','626T_N']:
#			continue

		command = "java -jar /home/tools/GATK/GenomeAnalysisTK.jar -T UnifiedGenotyper \
			-R /data1/Sequence/ucsc_hg19/hg19.fa --dbsnp /data1/Sequence/ucsc_hg19/annot/dbsnp_135.hg19.sort.vcf \
			-I %s/%s.recal.bam -o %s/%s.vcf" % (inputDirN,sampN, outputDirN,sampN)

		if pbs:

			print sampN
			os.system('echo "%s" | qsub -N %s -o %s/%s.gatk.log -j oe' % (command, sampN, outputDirN,sampN))

		else:

			print sampN
			os.system('(%s) &> %s/%s.gatk.log' % (command, outputDirN,sampN))


if __name__ == '__main__':

	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

	main('/Z/NSL/RNASeq/align/splice/gatk_test', '/Z/NSL/RNASeq/align/splice/gatk_test', True)
