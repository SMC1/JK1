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

		if pbs:

			print sampN

			os.system('echo "samtools index %s/%s.RG.bam; \
			java -jar /home/tools/GATK/GenomeAnalysisTK.jar -T RealignerTargetCreator -R /data1/Sequence/ucsc_hg19/hg19.fa -I %s/%s.RG.bam -o %s/%s_realigner.intervals -known /home/heejin/dbsnp_135.hg19.sort.vcf; \
			java -jar /home/tools/GATK/GenomeAnalysisTK.jar -T IndelRealigner -R /data1/Sequence/ucsc_hg19/hg19.fa -I %s/%s.RG.bam -targetIntervals %s/%s_realigner.intervals -o %s/%s.realign.bam; \
			java -jar /home/tools/GATK/GenomeAnalysisTK.jar -T BaseRecalibrator -R /data1/Sequence/ucsc_hg19/hg19.fa -I %s/%s.realign.bam -o %s/%s.grp -knownSites /home/heejin/dbsnp_135.hg19.sort.vcf; \
			java -jar /home/tools/GATK/GenomeAnalysisTK.jar -T PrintReads -R /data1/Sequence/ucsc_hg19/hg19.fa -I %s/%s.realign.bam -BQSR %s/%s.grp -o %s/%s.recal.bam" | \
			qsub -N %s -o %s/%s.qlog -j oe' % (inputDirN,sampN, inputDirN,sampN, outputDirN,sampN, inputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))

#			os.system('echo "java -jar /home/tools/VarScan/VarScan.v2.3.3.jar pileup2snp %s/%s.pileup > %s/%s.snp 2> /dev/null" | \
#				qsub -N %s -o %s/%s.snp.qlog -j oe' % \
#				(inputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))
#
		else:

			print sampN

			os.system('samtools index %s/%s.RG.bam; \
			java -jar /home/tools/GATK/GenomeAnalysisTK.jar -T RealignerTargetCreator -R /data1/Sequence/ucsc_hg19/hg19.fa -I %s/%s.RG.bam -o %s/%s_realigner.intervals -known /home/heejin/dbsnp_135.hg19.sort.vcf; \
			java -jar /home/tools/GATK/GenomeAnalysisTK.jar -T IndelRealigner -R /data1/Sequence/ucsc_hg19/hg19.fa -I %s/%s.RG.bam -targetIntervals %s/%s_realigner.intervals -o %s/%s.realign.bam; \
			java -jar /home/tools/GATK/GenomeAnalysisTK.jar -T BaseRecalibrator -R /data1/Sequence/ucsc_hg19/hg19.fa -I %s/%s.realign.bam -o %s/%s.grp -knownSites /home/heejin/dbsnp_135.hg19.sort.vcf; \
			java -jar /home/tools/GATK/GenomeAnalysisTK.jar -T PrintReads -R /data1/Sequence/ucsc_hg19/hg19.fa -I %s/%s.realign.bam -BQSR %s/%s.grp -o %s/%s.recal.bam' % \
			(inputDirN,sampN, inputDirN,sampN, outputDirN,sampN, inputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN, outputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))

#
#			os.system('java -jar /home/tools/VarScan/VarScan.v2.3.3.jar pileup2snp %s/%s.pileup > %s/%s.snp 2> /dev/null' % \
#				(inputDirN,sampN, outputDirN,sampN, outputDirN,sampN))
#			os.system('java -jar /home/tools/VarScan/VarScan.v2.3.3.jar pileup2snp %s/%s.pileup > %s/%s.snp 2> %s/%s.snp.qlog' % \
#				(inputDirN,sampN, outputDirN,sampN, outputDirN,sampN))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

optH = mybasic.parseParam(optL)

main('/EQL1/NSL/Exome/bwa', '/data1/IRCR/exome_bam', True)
