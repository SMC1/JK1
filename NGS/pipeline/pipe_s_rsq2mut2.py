#!/usr/bin/python

import sys, os
from glob import glob

import mypipe

def genSpec(baseDir):

	moduleL = ['NGS/align','NGS/mutation'] ## DIRECTORY
	homeDir = os.popen('echo $HOME','r').read().rstrip()

	for module in moduleL:
		sys.path.append('%s/JK1/%s' % (homeDir,module))

	import bwa_batch, markDuplicates_batch, realign_batch, pileup_batch ## MODULES

	return [ ## PARAMETERS
		{
		'name': 'BWA',
		'desc': 'fq -> sam -> bam -> sorted.bam',
		'fun': bwa_batch.align,
		'paramL': (baseDir, baseDir, '(.*)\.[12]\.fq', 10, 40000000000, False, 'hg19', False),
		'paramH': {},
		'logPostFix': 'bwa.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Real time:' in x[-1],
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
		'outFilePostFix': ['RG.bam']
		},

		{
		'name': 'Realign',
		'desc': 'RG.bam -> realign.bam -> recal.bam',
		'fun': realign_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': 'realign.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Uploaded run' in x[-1],
		'outFilePostFix': ['recal.bam']
		},

		{
		'name': 'Pileup',
		'desc': 'recal.bam -> pileup',
		'fun': pileup_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': 'pileup.log',
		'logExistsFn': lambda x: len(x)>0 and 'Set max' in x[-1],
		'outFilePostFix': ['pileup']
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
	mypipe.main(inputFilePathL=glob('/home/yenakim/YN/linked_fq/S780_T_SS/S780_T_SS.*.fq'), genSpecFn=genSpec, sampN='S780_T_SS', projectN='test', clean=False)
