#!/usr/bin/python

import sys, os, getopt
from glob import glob

import mypipe, mybasic

def genSpec(baseDir, server='smc1', genome='hg19'):

	moduleL = ['NGS/align','NGS/splice_gsnap/fusion'] ## DIRECTORY
	homeDir = os.popen('echo $HOME','r').read().rstrip()

	for module in moduleL:
		sys.path.append('%s/JK1/%s' % (homeDir,module))

	import gsnap_splice_batch, fusion_filter_transloc_batch, fusion_filter_annot1_batch, fusion_proc_sort_batch, fusion_proc_annot_batch ## MODULES

	return [ ## PARAMETERS
#		{
#		'name': 'Align',
#		'desc': 'fastq -> splice.gsnap',
#		'fun': gsnap_splice_batch.align,
#		'paramL':(baseDir, baseDir, 6, False),
#		'paramH': {},
#		'logPostFix': '.gsnap.qlog',
#		'logExistsFn': lambda x: len(x)>0 and 'Processed' in x[-1],
#		'outFilePostFix': ['splice.gsnap'],
#		'clean': False,
#		'rerun': False
#		},
#
		{
		'name': 'Filter transloc',
		'desc': 'splice.gsnap.gz -> splice_transloc.gsnap',
		'fun': fusion_filter_transloc_batch.fusion_filter_batch,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.ft_tloc.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Results' in x[-1],
		'outFilePostFix': ['splice_transloc.gsnap'],
		'clean': False,
		'rerun': False 
		},

		{
		'name': 'annotate',
		'desc': 'splice_transloc.gsnap -> splice_transloc_annot1.gsnap',
		'fun': fusion_filter_annot1_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.annot.qlog',
		'logExistsFn': lambda x: len(x)>1 and 'Results' in x[-1],
		'outFilePostFix': ['splice_transloc_annot1.gsnap'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'sort',
		'desc': 'splice_transloc_annot1.gsnap -> splice_transloc_annot1.sorted.gsnap and gnerate report.txt',
		'fun': fusion_proc_sort_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.sort.qlog',
		'logExistsFn': lambda x: len(x)==0,
		'outFilePostFix': ['splice_transloc_annot1.sorted.gsnap','splice_transloc_annot1.report.txt'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'annotate report',
		'desc': 'report.txt -> report_annot.txt',
		'fun': fusion_proc_annot_batch.fusion_proc_annot_batch,
		'paramL': (baseDir, baseDir, None, False),
		'paramH': {},
		'logPostFix': '.report_annot.qlog',
		'logExistsFn': lambda x: len(x)==0,
		'outFilePostFix': ['splice_transloc_annot1.report_annot.txt'],
		'clean': False,
		'rerun': False
		},
		
#		{
#		'name': 'Summarize',
#		'desc': '',
#		'fun': ,
#		'paramL': (baseDir, baseDir, False),
#		'paramH': {},
#		'logPostFix': 'realign.qlog',
#		'logExistsFn': lambda x: len(x)>0 and 'Uploaded run' in x[-1],
#		'outFilePostFix': ['realign.bam', 'recal.bam'],
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

#	mypipe.main(inputFilePathL=glob('/EQL2/TCGA/LUAD/RNASeq/raw/a83dc51f-66f4-411e-9e5c-079ad215607d/UNCID_1098753.0ddf256d-70a4-4dfc-ade0-1f51a4c115a3.sorted_genome_alignments.bam'), genSpecFn=genSpec, sampN='', projectN='rsq_pipe_test2', clean=False)
