#!/usr/bin/python

import sys, os, getopt
from glob import glob

import mypipe, mybasic, mysetting

def register_modules(moduleL):
	homeDir = os.popen('echo $HOME','r').read().rstrip()
	for module in moduleL:
		sys.path.append('%s/JK1/%s' % (homeDir, module))

def genSpec(baseDir, server='smc1', genome='hg19'):
	register_modules(['NGS/copynumber'])
	import	cn_corr_batch, corrcgh2seg_batch, drawCNATraj, corrseg2gene_batch

	return [ ## PARAMETERS
		{
		'name': 'copy number correction',
		'desc': 'ngCGH -> corr.ngCGH',
		'fun': cn_corr_batch.main,
		'paramL': (baseDir, baseDir, purity, False),
		'paramH': {},
		'logPostFix': '.cn_corr.qlog',
		'logExistsFn': lambda x: len(x)==0,
		'outFilePostFix': ['corr.ngCGH'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'Segmenation',
		'desc': 'corr.ngCGH -> corr.ngCGH.seg',
		'fun': corrcgh2seg_batch.cgh2seg,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.corr.seg.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Centrality parameter' in x[-1],
		'outFilePostFix': ['corr.ngCGH.seg'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'Plot corrected segmentation',
		'desc': 'Plot segmentations for corrected copy number profile',
		'fun': drawCNATraj.main,
		'paramL': (baseDir, baseDir),
		'paramH': {},
		'logPostFix': '.traj_plot.log',
		'logExistsFn': lambda x: len(x)==0,
		'outFilePostFix': ['seg.png','seg.pdf'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'Calculate gene copy number from segments',
		'desc': 'corr.seg -> corr.cn_gene.dat',
		'fun': corrseg2gene_batch.main,
		'paramL': (baseDir, baseDir, mysetting.refFlatH[server][genome],[],False),
		'paramH': {},
		'logPostFix': '.corr.cn_gene.log',
		'logExistsFn': lambda x: len(x)>0 and 'ZZZ3' in x[-1],
		'outFilePostFix': ['corr.cn_gene.dat'],
		'clean': False,
		'rerun': False
		},

		]

if __name__ == '__main__':

	optL, argL = getopt.getopt(sys.argv[1:],'i:t:n:p:c:s:g:')

	optH = mybasic.parseParam(optL)
	pathL = optH['-i']
	sN = optH['-n']
	pN = optH['-p']
	clean = optH['-c']
	server = optH['-s']
	genome = optH['-g']
	purity = optH['-t']

	mypipe.main(inputFilePathL=glob(pathL), genSpecFn=genSpec, sampN=sN, projectN=pN, clean=clean, server=server, genome=genome)
