#!/usr/bin/python

import sys, os, getopt
from glob import glob

import mypipe, mybasic, mysetting

def genSpec_single(baseDir, server='smc1', genome='hg19'):
	mybasic.add_module_path(['NGS/mutation'])
	import mutect_batch, somaticindeldetector_batch

	return [ ## PARAMETERS
		{
		'name': 'Run MuTect (single)',
		'desc': '.recal.bam -> .mutect, mutect_single_filter.vcf',
		'fun': mutect_batch.mutect_PON,
		'paramL': (baseDir, genome, server, False),
		'paramH': {},
		'logPostFix': '.mutect_single.log',
		'logExistsFn': lambda x: 'done' in x[-9],
		'outFilePostFix': ['mutect_single_filter.vcf'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'somaticindeldetector',
		'desc': '.recal.bam -> indels_single_filter.vcf',
		'fun': somaticindeldetector_batch.single_mode,
		'paramL': (baseDir, baseDir, 'SS', genome, server, False),
		'paramH': {},
		'logPostFix': '.somaticindeldetector_single.log',
		'logExistsFn': lambda x: ('chrX' in x[-1] or 'chrX' in x[-2]),
		'outFilePostFix': ['indels_single_filter.vcf','indels_single_filter.out'],
		'clean': False,
		'rerun': False
		},
	]

def genSpec(baseDir, server='smc1', genome='hg19'):
	mybasic.add_module_path(['NGS/mutation'])
	import mutect_batch, somaticindeldetector_batch

	return [ ## PARAMTERS
		{
		'name': 'Run MuTect',
		'desc': '.recal.bam -> .mutect, mutect.vcf',
		'fun': mutect_batch.mutect_pair,
		'paramL': (baseDir, baseDir, genome, server, False),
		'paramH': {},
		'logPostFix': '.mutect_pair.log',
		'logExistsFn': lambda x: 'done' in x[-9],
		'outFilePostFix': ['.mutect','.mutect_pair.vcf'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'somaticindeldetector',
		'desc': '.recal.bam -> indels_filter.vcf',
		'fun': somaticindeldetector_batch.paired_mode,
		'paramL': (baseDir, baseDir, 'SS', genome, server, False),
		'paramH': {},
		'logPostFix': '.somaticindeldetector_pair.log',
		'logExistsFn': lambda x: ('chrX' in x[-1] or 'chrX' in x[-2]),
		'outFilePostFix': ['indels_pair_filter.vcf','indels_pair_filter.out'],
		'clean': False,
		'rerun': False
		},
	]

if __name__ == '__main__':

	optL, argL = getopt.getopt(sys.argv[1:],'i:j:n:p:c:s:g:')

	optH = mybasic.parseParam(optL)
	pathL = optH['-i']
	sN = optH['-n']
	pN = optH['-p']
	clean = optH['-c']
	server = optH['-s']
	genome = optH['-g']

	if '-j' not in optH: # single mode
		genSpecFN = genSpec_single
		inputL = glob(optH['-i'])
	else: # paired mode
		genSpecFN = genSpec
		inputL = glob(optH['-i']) + glob(optH['-j'])

	if inputL != []:
		mypipe.main(inputFilePathL=inputL, genSpecFn=genSpecFN, sampN=sN, projectN=pN, clean=clean, server=server, genome=genome)
