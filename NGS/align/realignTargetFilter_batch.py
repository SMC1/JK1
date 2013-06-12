#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(inputDirN, outputDirN, pbs=False):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('(.*)\.RG.bam', x),inputFileNL)
	
	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.RG.bam',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	print 'Samples: %s' % sampNL, len(sampNL)

	for sampN in sampNL:

#		if sampN not in ['047T_N','047T','464T','464T_N','626T','626T_N']:
#			continue

		if pbs:

			print sampN

			os.system('echo "samtools index %s/%s.RG.bam; \
				java -jar /home/tools/GATK/GenomeAnalysisTK.jar -T RealignerTargetCreator -R /data1/Sequence/ucsc_hg19/hg19.fa -I %s/%s.RG.bam -o %s/%s.realigner.intervals -known /data1/Sequence/ucsc_hg19/annot/dbsnp_135.hg19.sort.vcf; \
				python ~/JK1/NGS/align/realignTargetFilter.py < %s/%s.realigner.intervals > %s/%s.realigner_ft.intervals" | \
				qsub -N %s -o %s/%s.interval.qlog -j oe' % \
				(inputDirN,sampN, inputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))

		else:

			print sampN

			os.system('(samtools index %s/%s.RG.bam; \
				java -jar /home/tools/GATK/GenomeAnalysisTK.jar -T RealignerTargetCreator -R /data1/Sequence/ucsc_hg19/hg19.fa -I %s/%s.RG.bam -o %s/%s.realigner.intervals -known /data1/Sequence/ucsc_hg19/annot/dbsnp_135.hg19.sort.vcf; \
				python ~/JK1/NGS/align/realignTargetFilter.py < %s/%s.realigner.intervals > %s/%s.realigner_ft.intervals) &> %s/%s.interval.qlog' % \
				(inputDirN,sampN, inputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN))

if __name__ == '__main__':

	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

	main('/Z/NSL/RNASeq/align/splice/gatk_test', '/Z/NSL/RNASeq/align/splice/gatk_test', True)
