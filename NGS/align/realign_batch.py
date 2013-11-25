#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def main(inputDirN, outputDirN, pbs=False, ref='/data1/Sequence/ucsc_hg19/hg19.fa', dbsnp='/data1/Sequence/ucsc_hg19/annot/dbsnp_135.hg19.sort.vcf'):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('(.*)\.RG.bam', x),inputFileNL)
	

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.RG.bam',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	print 'Samples: %s' % sampNL, len(sampNL)

	for sampN in sampNL:

#		if sampN not in ['047T_N','047T','464T','464T_N','626T','626T_N']:
#			continue

		gatk='/home/tools/GATK/GenomeAnalysisTK.jar'
		rg='%s/%s.RG.bam' % (inputDirN,sampN)
		realign='%s/%s.realign.bam' % (outputDirN,sampN)
		recal='%s/%s.recal.bam' % (outputDirN,sampN)
		intervals='%s/%s_realigner.intervals' % (outputDirN,sampN)
		grp='%s/%s.grp' % (outputDirN,sampN)

		cmd = 'samtools index %s' % (rg)
		cmd = '%s; java -jar %s -T RealignerTargetCreator -R %s -I %s -o %s -known %s' % (cmd, gatk, ref, rg, intervals, dbsnp)
		cmd = '%s; java -jar %s -T IndelRealigner -R %s -I %s -targetIntervals %s -o %s' % (cmd, gatk, ref, rg, intervals, realign)
		cmd = '%s; java -jar %s -T BaseRecalibrator -R %s -I %s -o %s -knownSites %s' % (cmd, gatk, ref, realign, grp, dbsnp)
		cmd = '%s; java -jar %s -T PrintReads -R %s -I %s -BQSR %s -o %s' % (cmd, gatk, ref, realign, grp, recal)

		if pbs:

			print sampN

			os.system('echo "%s" | qsub -N %s -o %s/%s.realign.qlog -j oe' % (cmd, sampN, outputDirN,sampN))

		else:

			print sampN

			os.system('(%s) &> %s/%s.realign.qlog' % (cmd, outputDirN,sampN))


if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

	main('/EQL1/NSL/Exome/bwa', '/EQL1/NSL/exome_bam', True)
