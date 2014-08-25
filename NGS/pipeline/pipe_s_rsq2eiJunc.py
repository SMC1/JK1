#!/usr/bin/python

import sys, os, getopt
from glob import glob

import mypipe, mybasic

def genSpec(baseDir, server='smc1', genome='hg19'):

	mybasic.add_module_path(['NGS/fastq','NGS/align','NGS/splice_gsnap/ei_junc'])
	import bam2fastq_batch2, gsnap_splice_batch, ei_junc_batch## MODULES

	return [ ## PARAMETERS
#		{
#		'name': 'bam to fastq',
#		'desc': 'bam -> fastq',
#		'fun': bam2fastq_batch2.bam2fastq_batch2,
#		'paramL':(baseDir, baseDir, 'UNCID_[0-9]{7}\.(.*)\.sorted_.*'),
#		'paramH': {},
#		'logPostFix': 'fastq.log',
#		'logExistsFn': lambda x: len(x)>0 and 'Samples' in x[-1],
#		'outFilePostFix': ['fastq'],
#		'clean': False,
#		'rerun': False
#		},
#
#		{
#		'name': 'Align',
#		'desc': 'fastq -> splice.gsnap',
#		'fun': gsnap_splice_batch.align,
#		'paramL':(baseDir, baseDir, 6, False, False),
#		'paramH': {},
#		'logPostFix': 'gsnap.qlog',
#		'logExistsFn': lambda x: len(x)>0 and 'Processed' in x[-1],
#		'outFilePostFix': ['splice.gsnap'],
#		'clean': False,
#		'rerun': False
#		},

		{
		'name': 'Filter eiJunc',
		'desc': 'splice.gsnap.gz -> ei.dat',
		'fun': ei_junc_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.ei.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Finished' in x[-1],
		'outFilePostFix': ['ei.dat'],
		'clean': False,
		'rerun': False 
		},

		]

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

	#mypipe.main(inputFilePathL=glob('/pipeline/fusion_test/S436_RSq_test/*splice.gsnap'), genSpecFn=genSpec, sampN='S436_RSq_test_splice', projectN='test_skip', clean=False)
