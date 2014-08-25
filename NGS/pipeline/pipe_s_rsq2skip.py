#!/usr/bin/python

import sys, os, getopt
from glob import glob

import mypipe, mybasic

def genSpec(baseDir, server='smc1', genome='hg19'):

	mybasic.add_module_path(['NGS/align','NGS/splice_gsnap/skipping'])
	import gsnap_splice_batch, exonSkip_filter_batch, exonSkip_filter_normal_batch, exonSkip_sort_batch, exonSkip_normal_sort_batch, exonSkip_proc_annot_batch ## MODULES

	return [ ## PARAMETERS
#		{
#		'name': 'Align',
#		'desc': 'fastq -> splice.gsnap',
#		'fun': gsnap_splice_batch.align,
#		'paramL':(baseDir, baseDir, 6, False),
#		'paramH': {},
#		'logPostFix': 'gsnap.qlog',
#		'logExistsFn': lambda x: len(x)>0 and 'Processed' in x[-1],
#		'outFilePostFix': ['splice.gsnap'],
#		'clean': False,
#		'rerun': False
#		},

		{
		'name': 'Filter exonskip',
		'desc': 'splice.gsnap.gz -> splice_exonSkip.gsnap',
		'fun': exonSkip_filter_batch.exonSkip_filter_batch,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.exonSkip.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Results' in x[-1],
		'outFilePostFix': ['splice_exonSkip.gsnap'],
		'clean': False,
		'rerun': False 
		},

		{
		'name': 'Filter normal exonskip',
		'desc': 'splice.gsnap -> splice_exonSkip_normal.gsnap.gz',
		'fun': exonSkip_filter_normal_batch.exonSkip_filter_batch,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.exonSkip_normal.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Results' in x[-1],
		'outFilePostFix': ['splice_exonSkip_normal.gsnap.gz'],
		'clean': False,
		'rerun': False 
		},

		{
		'name': 'sort',
		'desc': 'splice_exonSkip.gsnap -> splice_exonSkip_report.txt',
		'fun': exonSkip_sort_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.sort.qlog',
		'logExistsFn': lambda x: len(x)==0,
		'outFilePostFix': ['splice_exonSkip_report.txt'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'sort-normal',
		'desc': 'splice_exonSkip_normal.gsnap.gz -> splice_exonSkip_normal_report.txt',
		'fun': exonSkip_normal_sort_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.sort_normal.qlog',
		'logExistsFn': lambda x: len(x)==0,
		'outFilePostFix': ['splice_exonSkip_normal_report.txt'],
		'clean': False,
		'rerun': False
		},
		
		{
		'name': 'annotate report',
		'desc': 'report.txt -> report_annot.txt',
		'fun': exonSkip_proc_annot_batch.exonSkip_proc_annot_batch,
		'paramL': (baseDir, baseDir, None, False),
		'paramH': {},
		'logPostFix': '.skip_annot.qlog',
		'logExistsFn': lambda x: len(x)==0,
		'outFilePostFix': ['splice_exonSkip_report_annot.txt'],
		'clean': False,
		'rerun': False
		},

#		{
#		'name': 'link',
#		'desc': 'put all report_annot.txt files in a directory',
#		'fun': exonSkip_link.link,
#		'paramL': (baseDir, '/EQL1/NSL/RNASeq/results/exonSkip'),
#		'paramH': {},
#		'logPostFix': 'link.qlog',
#		'logExistsFn': lambda x: len(x)==0,
#		'outFilePostFix': ['splice_exonSkip_report_annot.txt'],
#		'clean': False,
#		'rerun': False
#		},
#
#		{
#		'name': 'link-normal',
#		'desc': 'put all report_normal.txt files in a directory',
#		'fun': exonSkip_link_normal.link,
#		'paramL': (baseDir, '/EQL1/NSL/RNASeq/results/exonSkip_normal'),
#		'paramH': {},
#		'logPostFix': 'link_normal.qlog',
#		'logExistsFn': lambda x: len(x)==0,
#		'outFilePostFix': ['splice_exonSkip_normal_report.txt'],
#		'clean': False,
#		'rerun': False
#		},

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
