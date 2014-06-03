#!/usr/bin/python

import sys, getopt, re, os
import mybasic
from glob import glob

def main(inDirName, outDirName, outFileName, platform):

	inFileNL = os.listdir(inDirName)
	inLogRNL = filter(lambda x: re.match('TCGA.*.Paired_LogR.txt', x), inFileNL)
	inBafNL = filter(lambda x: re.match('TCGA.*.B_Allele_Freq.txt', x), inFileNL)

	logRSampNS = set([re.match('(.*).hudsonalpha.org_GBM.HumanHap550.*', x).group(1) for x in inLogRNL])
	BafSampNS = set([re.match('(.*).hudsonalpha.org_GBM.HumanHap550.*', x).group(1) for x in inBafNL])

	sampNS = logRSampNS.intersection(BafSampNS)

	sampNameL = list(sampNS)
	sampNameL.sort()

	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	outFile = open(outFileName,'w')
	outFile.write('sampleID\tfraction\tploidy\n')

	for sampN in sampNameL:

		print sampN

		logRFileN = glob(inDirName+'/'+sampN+'.*.Paired_LogR.txt')[0]
		BafFileN = glob(inDirName+'/'+sampN+'.*.B_Allele_Freq.txt')[0]
		
		os.system('Rscript ~/JK1/Array/purity/runAscat.r %s %s %s %s %s %s &>> %s/ascat_error_log.txt' % (outDirName,sampN,logRFileN,BafFileN,outFileName,platform, outDirName))


#optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])
#
#optH = mybasic.parseParam(optL)
#
#if '-i' in optH and '-o' in optH:
#	main(optH['-i'],optH['-o'])

main('/EQL1/TCGA/GBM/array_cn/CNV_SNP_Array/HAIB__HumanHap550/Level_2','/EQL1/TCGA/GBM/array_cn/ascat/results','/EQL1/TCGA/GBM/array_cn/ascat/results/results_summary.txt','Illumina610k')
