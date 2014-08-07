#!/usr/bin/python

import sys, os, getopt
from glob import glob

import mypipe, mysetting

def genSpec(baseDir, server='smc1', genome='hg19'):

	moduleL = ['NGS/fastq','NGS/align','NGS/mutation'] ## DIRECTORY
	homeDir = os.popen('echo $HOME','r').read().rstrip()

	for module in moduleL:
		sys.path.append('%s/JK1/%s' % (homeDir,module))

	import bwa_batch, markDuplicates_batch, realign_batch, pileup_batch, procPileup_split_batch, mutScan_batch, mutscan_snp_cosmic_batch ## MODULES
	import fastqc_batch, annotate_mutscan_batch, annotate_join_cosmic_batch, vep_mutscan_batch

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
		'desc': 'sorted.bam -> dedup.bam -> RG.bam',
		'fun': markDuplicates_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.dedup.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'totalMemory()' in x[-1],
		'outFilePostFix': ['RG.bam'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'Realign',
		'desc': 'RG.bam -> realign.bam -> recal.bam',
		'fun': realign_batch.main,
		'paramL': (baseDir, baseDir, False, mysetting.ucscRefH[server][genome], mysetting.dbsnpH[server][genome]),
		'paramH': {},
		'logPostFix': '.realign.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Uploaded run' in x[-1],
		'outFilePostFix': ['recal.bam'],
		'clean': False,
		'rerun': False
		},

#		{
#		'name': 'Pileup',
#		'desc': 'recal.bam -> pileup',
#		'fun': pileup_batch.main,
#		'paramL': (baseDir, baseDir, False, mysetting.ucscRefH[server][genome]),
#		'paramH': {},
#		'logPostFix': '.pileup.log',
#		'logExistsFn': lambda x: len(x)>0 and 'Set max' in x[-1],
#		'outFilePostFix': ['pileup'],
#		'clean': False,
#		'rerun': False
#		},

		{
		'name': 'Pileup_proc',
		'desc': 'recal.bam -> pileup -> pileup_proc',
		'fun': procPileup_split_batch.main,
		'paramL': (baseDir, baseDir, mysetting.ucscRefH[server][genome], False),
		'paramH': {},
		'logPostFix': '.pileup_proc.log',
		'logExistsFn': lambda x: len(x)>0 and 'Success' in x[-1],
		'outFilePostFix': ['pileup_proc','pileup.gz'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'MutScan',
		'desc': 'pileup_proc -> mutscan',
		'fun': mutScan_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.mutscan.log',
		'logExistsFn': lambda x: len(x)>0 and 'Success' in x[-1],
		'outFilePostFix': ['mutscan'],
		'clean': False,
		'rerun': False
		},
#
#		{## old cosmic join
#		'name': 'mutscan_snp_cosmic',
#		'desc': 'mutscan -> cosmic.dat',
#		'fun': mutscan_snp_cosmic_batch.main,
#		'paramL': (baseDir, server),
#		'paramH': {},
#		'logPostFix': '.cosmic.log',
#		'logExistsFn': lambda x: len(x) == 0,
#		'outFilePostFix': ['cosmic.dat'],
#		'clean': False,
#		'rerun': False
#		},
#
#		{
#		'name': 'VEP annotation',
#		'desc': 'Annotate mutscan output',
#		'fun': vep_mutscan_batch.main,
#		'paramL': ([baseDir]),
#		'paramH': {},
#		'logPostFix': '.mutscan_vep.log',
#		'logExistsFn': lambda x: len(x)>0 and 'Finished!' in x[-1],
#		'outFilePostFix': ['mutscan_vep_out.vcf'],
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
