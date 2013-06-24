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
			java -jar /home/tools/GATK/GenomeAnalysisTK.jar -T RealignerTargetCreator -R /data1/Sequence/ucsc_hg19/hg19.fa -I %s/%s.RG.bam -o %s/%s_realigner.intervals -known /home/heejin/dbsnp_135.hg19.sort.vcf; \
			java -jar /home/tools/GATK/GenomeAnalysisTK.jar -T IndelRealigner -R /data1/Sequence/ucsc_hg19/hg19.fa -I %s/%s.RG.bam -targetIntervals %s/%s_realigner.intervals -o %s/%s.realign.bam; \
			java -jar /home/tools/GATK/GenomeAnalysisTK.jar -T BaseRecalibrator -R /data1/Sequence/ucsc_hg19/hg19.fa -I %s/%s.realign.bam -o %s/%s.grp -knownSites /home/heejin/dbsnp_135.hg19.sort.vcf; \
			java -jar /home/tools/GATK/GenomeAnalysisTK.jar -T PrintReads -R /data1/Sequence/ucsc_hg19/hg19.fa -I %s/%s.realign.bam -BQSR %s/%s.grp -o %s/%s.recal.bam" | \
			qsub -N %s -o %s/%s.realign.qlog -j oe' % (inputDirN,sampN, inputDirN,sampN, outputDirN,sampN, inputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))


		else:

			print sampN

			os.system('(samtools index %s/%s.RG.bam; \
			java -jar /home/tools/GATK/GenomeAnalysisTK.jar -T RealignerTargetCreator -R /data1/Sequence/ucsc_hg19/hg19.fa -I %s/%s.RG.bam -o %s/%s_realigner.intervals -known /home/heejin/dbsnp_135.hg19.sort.vcf; \
			java -jar /home/tools/GATK/GenomeAnalysisTK.jar -T IndelRealigner -R /data1/Sequence/ucsc_hg19/hg19.fa -I %s/%s.RG.bam -targetIntervals %s/%s_realigner.intervals -o %s/%s.realign.bam; \
			java -jar /home/tools/GATK/GenomeAnalysisTK.jar -T BaseRecalibrator -R /data1/Sequence/ucsc_hg19/hg19.fa -I %s/%s.realign.bam -o %s/%s.grp -knownSites /home/heejin/dbsnp_135.hg19.sort.vcf; \
			java -jar /home/tools/GATK/GenomeAnalysisTK.jar -T PrintReads -R /data1/Sequence/ucsc_hg19/hg19.fa -I %s/%s.realign.bam -BQSR %s/%s.grp -o %s/%s.recal.bam) &> %s/%s.realign.qlog' % \
			(inputDirN,sampN, inputDirN,sampN, outputDirN,sampN, inputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN))


if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

	main('/EQL1/NSL/Exome/bwa', '/EQL1/NSL/exome_bam', True)
