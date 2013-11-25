#!/usr/bin/python

import sys, os, getopt
from glob import glob

import mypipe, mybasic, mysetting

def genSpec(baseDir, server='smc1', genome='hg19'):

	moduleL = ['NGS/fastq','NGS/align','NGS/mutation'] ## DIRECTORY
	homeDir = os.popen('echo $HOME','r').read().rstrip()

	for module in moduleL:
		sys.path.append('%s/JK1/%s' % (homeDir,module))

	import fastqc_batch, gsnap_splice_bam_batch, gsnap_splice_bam_sort_batch, markDuplicates_batch, realignTargetFilter_batch, realignWithFtTarget_batch, unifiedGeno_batch, vcf2mutScan_batch, mutscan_snp_cosmic_batch, annotate_mutscan_batch, annotate_join_cosmic_batch ## MODULES

	specL = [ ## PARAMETERS
		{
		'name': 'Align',
		'desc': '.fq.gz -> .bam',
		'fun': gsnap_splice_bam_batch.align,
		'paramL': (baseDir, baseDir, False, genome),
		'paramH': {},
		'logPostFix': '.gsnap.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Processed' in x[-1],
		'outFilePostFix': ['splice.bam'],
		'clean': False,
		'rerun': False 
		},

		{
		'name': 'Sort',
		'desc': 'bam -> sorted.bam',
		'fun': gsnap_splice_bam_sort_batch.main,
		'paramL': (baseDir, baseDir, 10000000000),
		'paramH': {},
		'logPostFix': '_splice.sort.qlog',
		'logExistsFn': lambda x: len(x)<1 or 'merging' in x[-1],
		'outFilePostFix': ['sorted.bam'],
		'clean': False,
		'rerun': False 
		},

		{
		'name': 'MarkDuplicate/ReadGroup',
		'desc': 'sorted.bam -> dedup.bam -> RG.bam',
		'fun': markDuplicates_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '_splice.dedup.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'totalMemory()' in x[-1],
		'outFilePostFix': ['dedup.bam', 'RG.bam'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'RealignTarget',
		'desc': 'RG.bam -> realigner.intervals -> realigner_ft.intervals',
		'fun': realignTargetFilter_batch.main,
		'paramL': (baseDir, baseDir, False, mysetting.ucscRefH[server][genome], mysetting.dbsnpH[server][genome]),
		'paramH': {},
		'logPostFix': '_splice.interval.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Uploaded run' in x[-1],
		'outFilePostFix': ['realigner.intervals','realigner_ft.intervals'],
		'clean': False,
		'rerun': False
		},
		
		{
		'name': 'Realign/Recalibrate',
		'desc': 'RG.bam -> realign.bam -> recal.bam',
		'fun': realignWithFtTarget_batch.main,
		'paramL': (baseDir, baseDir, False, mysetting.ucscRefH[server][genome], mysetting.dbsnpH[server][genome]),
		'paramH': {},
		'logPostFix': '_splice.realign.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Uploaded run' in x[-1],
		'outFilePostFix': ['realign.bam', 'recal.bam'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'UnifiedGenotype',
		'desc': 'recal.bam -> vcf',
		'fun': unifiedGeno_batch.main,
		'paramL': (baseDir, baseDir, False, mysetting.ucscRefH[server][genome], mysetting.dbsnpH[server][genome]),
		'paramH': {},
		'logPostFix': '_splice.gatk.log',
		'logExistsFn': lambda x: len(x)>0 and 'Uploaded run' in x[-1],
		'outFilePostFix': ['vcf'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'MutScan',
		'desc': 'vcf -> mutscan',
		'fun': vcf2mutScan_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '_splice.mutscan.log',
		'logExistsFn': lambda x: len(x)==0,
		'outFilePostFix': ['_splice.mutscan'],
		'clean': False,
		'rerun': False
		},

### annotate mutscan using VEP
#		{
#		'name': 'VEP annotation',
#		'desc': 'Annotate mutscan output',
#		'fun': annotate_mutscan_batch.annotate_mutscan_batch,
#		'paramL': (baseDir, '(.*)\.mutscan$', baseDir),
#		'paramH': {},
#		'logPostFix': '_splice.vep.log',
#		'logExistsFn': lambda x: len(x)>0 and 'Finished!' in x[-1],
#		'outFilePostFix': ['vep'],
#		'clean': False,
#		'rerun': False
#		},

## join cosmic
#		{
#		'name': 'Join Cosmic',
#		'desc': 'Join annotated mutscan output with COSMIC',
#		'fun': annotate_join_cosmic_batch.main,
#		'paramL': (baseDir, '(.*)\.vep$', baseDir),
#		'paramH': {},
#		'logPostFix': '_splice.mutscan.cosmic.log',
#		'logExistsFn': lambda x: len(x)==0,
#		'outFilePostFix': ['_cosmic.dat'],
#		'clean': False,
#		'rerun': False
#		},

#		{ ## old joinCosmic
#		'name': 'JoinCosmic',
#		'desc': 'mutscan -> cosmic.dat',
#		'fun': mutscan_snp_cosmic_batch.main,
#		'paramL': (baseDir,),
#		'paramH': {},
#		'logPostFix': '_splice.cosmic.log',
#		'logExistsFn': lambda x: len(x)==0,
#		'outFilePostFix': ['dat'],
#		'clean': False,
#		'rerun': False 
#		},

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

#	if server == 'smc2':
#		return specL[-1]
#	else:
#		return specL
	return specL

if __name__ == '__main__':
	
	optL, argL = getopt.getopt(sys.argv[1:],'i:n:p:c:s:g:',[])

	optH = mybasic.parseParam(optL)
	
	pathL = optH['-i']
	sN = optH['-n']
	pN = optH['-p']
	clean = optH['-c']
	server = optH['-s']
	genome = optH['-g']

	mypipe.main(inputFilePathL=glob(pathL), genSpecFn=genSpec, sampN=sN, projectN=pN, clean=clean, server=server, genome=genome)

	#mypipe.main(inputFilePathL=glob('/home/heejin/practice/gatk/pipe_test/*.bam'), genSpecFn=genSpec, sampN='S647_splice', projectN='rsq_pipe_test2', clean=False)
