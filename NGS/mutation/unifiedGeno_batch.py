#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mysetting


def main(inputDirN, outputDirN, server='smc1', genome='hg19', pbs=False):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('(.*)\.recal.bam', x),inputFileNL)
	

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.recal.bam',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	ref = mysetting.ucscRefH[server][genome]
	dbsnp = mysetting.dbsnpH[server][genome]
	kgpf = mysetting.all_1kgH[server][genome]
	espf = mysetting.espH[server][genome]

	print 'Samples: %s' % sampNL, len(sampNL)

	for sampN in sampNL:

#		if sampN not in ['047T_N','047T','464T','464T_N','626T','626T_N']:
#			continue

		print sampN
		iprefix = '%s/%s' % (inputDirN,sampN)
		oprefix = '%s/%s' % (outputDirN,sampN)
		command = "java -Xmx8g -jar /home/tools/GATK/GenomeAnalysisTK.jar -T UnifiedGenotyper -R %s --dbsnp %s -stand_call_conf 15 -I %s.recal.bam -o %s.vcf -glm BOTH --comp:KGPF %s --comp:ESPF %s -dcov 50000 -A BaseQualityRankSumTest -A FisherStrand -A MappingQualityRankSumTest -A LowMQ -A RMSMappingQuality -A TandemRepeatAnnotator" % (ref, dbsnp, iprefix, oprefix, kgpf, espf)
		log = '%s.gatk.log' % (oprefix)

		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (command, sampN, log))

		else:
			os.system('(%s) &> %s' % (command, log))

if __name__ == '__main__':

#	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p:',[])
#
#	optH = mybasic.parseParam(optL)
#
#	main('/Z/NSL/RNASeq/align/splice/gatk_test', '/Z/NSL/RNASeq/align/splice/gatk_test', True)
#	main('/EQL8/pipeline/SGI20140204_rsq2mut/IRCR_GBM_352_TR_RSq', '/EQL8/pipeline/SGI20140204_rsq2mut/IRCR_GBM_352_TR_RSq', False)
#	main('/EQL8/pipeline/SGI20140204_rsq2mut/IRCR_GBM_352_TL_RSq', '/EQL8/pipeline/SGI20140204_rsq2mut/IRCR_GBM_352_TL_RSq', False)
#	main('/EQL6/pipeline/SCS20140203_rsq2mut/IRCR.GBM-363-SD_Bulk_RSq', '/EQL6/pipeline/SCS20140203_rsq2mut/IRCR.GBM-363-SD_Bulk_RSq', False)
#	main('/EQL6/pipeline/SCS20140203_rsq2mut/IRCR.GBM-363-SM_Bulk_RSq', '/EQL6/pipeline/SCS20140203_rsq2mut/IRCR.GBM-363-SM_Bulk_RSq', False)
	main('/EQL8/pipeline/SGI20140804_rsq2mut/IRCR_GBM14_508_RSq', '/EQL8/pipeline/SGI20140804_rsq2mut/IRCR_GBM14_508_RSq', pbs=False)
