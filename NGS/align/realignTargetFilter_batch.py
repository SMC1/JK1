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

		print sampN
		iprefix = '%s/%s' % (inputDirN,sampN)
		oprefix = '%s/%s' % (outputDirN,sampN)
		cmd = 'samtools index %s.RG.bam' % (iprefix)
		cmd = '%s; java -jar /home/tools/GATK/GenomeAnalysisTK.jar -T RealignerTargetCreator -R %s -I %s.RG.bam -o %s.realigner.intervals -known %s' % (cmd, ref, iprefix, oprefix, dbsnp)
		cmd = '%s; python ~/JK1/NGS/align/realignTargetFilter.py < %s.realigner.intervals > %s.realigner_ft.intervals' % (cmd, oprefix, oprefix)
		log = '%s.interval.qlog' % (oprefix)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))


		else:
			os.system('(%s) &> %s' % (cmd, log))

if __name__ == '__main__':

	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])

	optH = mybasic.parseParam(optL)

	main('/Z/NSL/RNASeq/align/splice/gatk_test', '/Z/NSL/RNASeq/align/splice/gatk_test', True)
