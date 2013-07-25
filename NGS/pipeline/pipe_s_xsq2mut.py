#!/usr/bin/python

import sys, os, getopt
from glob import glob

import mypipe

def genSpec(baseDir):

	moduleL = ['NGS/align','NGS/mutation'] ## DIRECTORY
	homeDir = os.popen('echo $HOME','r').read().rstrip()

	for module in moduleL:
		sys.path.append('%s/JK1/%s' % (homeDir,module))

	import bwa_batch, markDuplicates_batch, realign_batch, pileup_batch, procPileup_split_batch, mutscan_batch ## MODULES

	return [ ## PARAMETERS
		{
		'name': 'BWA',
		'desc': 'fq -> sam -> bam -> sorted.bam',
		'fun': bwa_batch.align,
		'paramL': (baseDir, baseDir, '(.*)\.[12]\.fq.gz', 10, 40000000000, False, 'hg19', True),
		'paramH': {},
		'logPostFix': 'bwa.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Real time:' in x[-1],
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
		'logPostFix': 'dedup.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'totalMemory()' in x[-1],
		'outFilePostFix': ['RG.bam'],
		'clean': False,
		'rerun': False

		},

		{
		'name': 'Realign',
		'desc': 'RG.bam -> realign.bam -> recal.bam',
		'fun': realign_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': 'realign.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Uploaded run' in x[-1],
		'outFilePostFix': ['recal.bam'],
		'clean': False,
		'rerun': False

		},

		{
		'name': 'Pileup',
		'desc': 'recal.bam -> pileup',
		'fun': pileup_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': 'pileup.log',
		'logExistsFn': lambda x: len(x)>0 and 'Set max' in x[-1],
		'outFilePostFix': ['pileup'],
		'clean': False,
		'rerun': False

		},

		{
		'name': 'Pileup_proc',
		'desc': 'pileup -> pileup_proc',
		'fun': procPileup_split_batch.main,
		'paramL': (baseDir, baseDir,'(.*)\.pileup',False),
		'paramH': {},
		'logPostFix': 'pileup_proc.log',
		'logExistsFn': lambda x: len(x)==0,
		'outFilePostFix': ['pileup_proc'],
		'clean': False,
		'rerun': False

		},

		{
		'name': 'MutScan',
		'desc': 'pileup_proc -> mutscan',
		'fun': mutScan_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': 'mutscan.log',
		'logExistsFn': lambda x: len(x)==0,
		'outFilePostFix': ['mutscan'],
		'clean': False,
		'rerun': False

		},

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

	optL, argL = getopt.getopt(sys.argv[1:],'i:n:p:c:',[])

	optH = dict(optL)

	pathL = optH['-i']
	sN = optH['-n']
	pN = optH['-p']
	clean = optH['-c']

	mypipe.main(inputFilePathL=glob(pathL), genSpecFn=genSpec, sampN=sN, projectN=pN, clean=clean)

#	mypipe.main(inputFilePathL=glob('/home/yenakim/YN/linked_fq/S780_T_SS/S780_T_SS.*.fq'), genSpecFn=genSpec, sampN='S780_T_SS', projectN='test_yn', clean=False)
