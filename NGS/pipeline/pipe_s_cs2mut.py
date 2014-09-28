#!/usr/bin/python

import sys, os, getopt
from glob import glob

import mypipe, mysetting, mybasic

def genSpec(baseDir, server='smc1', genome='hg19'):

	mybasic.add_module_path(['NGS/fastq','NGS/align','NGS/mutation'])
	import bwa_batch, markDuplicates_batch, realign_batch, procPileup_split_batch, mutScan_batch ## MODULES
	import fastqc_batch, vep_mutect_batch, mutect_batch, somaticindeldetector_batch

	return [ ## PARAMETERS
		{
		'name': 'FastQC',
		'desc': 'QC for fastq',
		'fun': fastqc_batch.fastqc_batch,
		'paramL': (baseDir, '(.*)\.[12]\.fq\.gz', baseDir, baseDir),
		'paramH': {},
		'logPostFix': '.fastqc.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Analysis complete' in x[-1],
		'outFilePostFix': ['_fastqc.zip'],
		'outLinkPostFix': ['_fastqc/fastqc_report.html'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'BWA',
		'desc': 'fq -> sam -> bam -> sorted.bam',
		'fun': bwa_batch.align,
		'paramL': (baseDir, baseDir, '(.*)\.[12]\.fq.gz', 10, 5000000000, False, mysetting.bwaIndexH[server][genome], True),
		'paramH': {},
		'logPostFix': '.bwa.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'bam_sort_core' in x[-1],
		'outFilePostFix': ['sorted.bam'],
		'clean': True,
		'rerun': False
		},

		{
		'name': 'MarkDuplicate/ReadGroup',
		'desc': 'sorted.bam -> dedup.bam',
		'fun': markDuplicates_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.dedup.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'totalMemory()' in x[-1],
		'outFilePostFix': ['dedup.bam'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'Realign',
		'desc': 'dedup.bam -> realign.bam -> recal.bam',
		'fun': realign_batch.main,
		'paramL': (baseDir, baseDir, False, mysetting.ucscRefH[server][genome], mysetting.dbsnpH[server][genome]),
		'paramH': {},
		'logPostFix': '.realign.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Uploaded run' in x[-1],
		'outFilePostFix': ['recal.bam'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'MuTect',
		'desc': 'recal.bam -> .vcf',
		'fun': mutect_batch.mutect_PON,
		'paramL': (baseDir, genome, server, False),
		'paramH': {},
		'logPostFix': '.mutect_single.log',
		'logExistsFn': lambda x: 'done' in x[-9],
		'outFilePostFix': ['_mutect.vcf','.mutect'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'SomaticIndelDetector',
		'desc': 'recal.bam -> indels.vcf -> indels_filter.vcf',
		'fun': somaticindeldetector_batch.single_mode,
		'paramL': (baseDir, baseDir, 'CS', genome, server, False),
		'paramH': {},
		'logPostFix': '.somaticindeldetector.log',
		'logExistsFn': lambda x: ('chrX' in x[-1] or 'chrX' in x[-2]),
		'outFilePostFix': ['indels_filter.vcf','indels_filter.out'],
		'clean': False,
		'rerun': False
		},

#		{ ## keep dying while trying to fork (when using PBS, even with --fork 2). It's better to annotate in a single batch (take it to post- pipeline?)
#		'name': 'VEP',
#		'desc': '.vcf -> .dat',
#		'fun': vep_mutect_batch.main,
#		'paramL': ([baseDir], False),
#		'paramH': {},
#		'logPostFix': 'mutect_vep.log',
#		'logExistsFn': lambda x: len(x) > 0 and 'Finished!' in x[-1],
#		'outFilePostFix': ['_vep.dat'],
#		'clean': False,
#		'rerun': False
#		}

#		{
#		'name': 'Cleanup',
#		'desc': 'remove all, but logs and designated result file',
#		'fun': cleanup.main,
#		'paramL': (baseDir,),
#		'paramH': {},
#		'logPostFix': 'cleanup.qlog',
#		'logExistsFn': lambda x: False,
#		'outFilePostFix': ['pileup']
#		},

		]

if __name__ == '__main__':

	optL, argL = getopt.getopt(sys.argv[1:],'i:n:p:c:s:g:',[])

	optH = dict(optL)

	pathL = optH['-i']
	sN = optH['-n']
	pN = optH['-p']
	clean = optH['-c']
	server = optH['-s']
	genome = optH['-g']

	mypipe.main(inputFilePathL=glob(pathL), genSpecFn=genSpec, sampN=sN, projectN=pN, clean=clean, server=server, genome=genome)

#	mypipe.main(inputFilePathL=glob('/home/yenakim/YN/linked_fq/S780_T_SS/S780_T_SS.*.fq'), genSpecFn=genSpec, sampN='S780_T_SS', projectN='test_yn', clean=False)
