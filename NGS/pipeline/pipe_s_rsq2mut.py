#!/usr/bin/python

import sys, os, getopt
from glob import glob

import mypipe, mybasic

def genSpec(baseDir):

	moduleL = ['NGS/align','NGS/mutation'] ## DIRECTORY
	homeDir = os.popen('echo $HOME','r').read().rstrip()

	for module in moduleL:
		sys.path.append('%s/JK1/%s' % (homeDir,module))

	import gsnap_splice_bam_sort_batch, markDuplicates_batch, realignTargetFilter_batch, realignWithFtTarget_batch, unifiedGeno_batch, vcf2mutScan_batch, mutscan_snp_cosmic_batch ## MODULES

	return [ ## PARAMETERS
		{
		'name': 'Sort',
		'desc': 'bam -> sorted.bam',
		'fun': gsnap_splice_bam_sort_batch.main,
		'paramL': (baseDir, baseDir, 10000000000),
		'paramH': {},
		'logPostFix': 'sort.qlog',
		'logExistsFn': lambda x: len(x)==0,# and 'Real time:' in x[-1],
		'outFilePostFix': ['sorted.bam']
		},

		{
		'name': 'MarkDuplicate/ReadGroup',
		'desc': 'sorted.bam -> dedup.bam -> RG.bam',
		'fun': markDuplicates_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': 'dedup.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'totalMemory()' in x[-1],
		'outFilePostFix': ['dedup.bam', 'RG.bam']
		},

		{
		'name': 'RealignTarget',
		'desc': 'RG.bam -> realigner.intervals -> realigner_ft.intervals',
		'fun': realignTargetFilter_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': 'interval.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Uploaded run' in x[-1],
		'outFilePostFix': ['realigner.intervals','realigner_ft.intervals']
		},
		
		{
		'name': 'Realign/Recalibrate',
		'desc': 'RG.bam -> realign.bam -> recal.bam',
		'fun': realignWithFtTarget_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': 'realign.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Uploaded run' in x[-1],
		'outFilePostFix': ['realign.bam', 'recal.bam']
		},

		{
		'name': 'UnifiedGenotype',
		'desc': 'recal.bam -> vcf',
		'fun': unifiedGeno_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': 'gatk.log',
		'logExistsFn': lambda x: len(x)>0 and 'Uploaded run' in x[-1],
		'outFilePostFix': ['vcf']
		},

		{
		'name': 'MutScan',
		'desc': 'vcf -> mutscan',
		'fun': vcf2mutScan_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': 'mutscan.log',
		'logExistsFn': lambda x: len(x)==0,
		'outFilePostFix': ['mutscan']
		},

		{
		'name': 'JoinCosmic',
		'desc': 'mutscan -> cosmic.dat',
		'fun': mutscan_snp_cosmic_batch.main,
		'paramL': (baseDir,),
		'paramH': {},
		'logPostFix': 'cosmic.log',
		'logExistsFn': lambda x: len(x)==0,
		'outFilePostFix': ['dat']
		},

##		{
##		'name': 'Cleanup',
##		'desc': 'remove all, but logs and designated result file',
##		'fun': cleanup.main,
##		'paramL': (baseDir,),
##		'paramH': {},
##		'logPostFix': 'cleanup.qlog',
##		'logExistsFn': lambda x: False,
##		'outFilePostFix': ['pileup']
##		},

		]

if __name__ == '__main__':
	
	optL, argL = getopt.getopt(sys.argv[1:],'i:n:p:c:',[])

	optH = mybasic.parseParam(optL)
	
	pathL = optH['-i']
	sN = optH['-n']
	pN = optH['-p']
	clean = optH['-c']

	mypipe.main(inputFilePathL=glob(pathL), genSpecFn=genSpec, sampN=sN, projectN=pN, clean=clean)
	#mypipe.main(inputFilePathL=glob('/home/heejin/practice/gatk/pipe_test/*.bam'), genSpecFn=genSpec, sampN='S647_splice', projectN='rsq_pipe_test2', clean=False)
