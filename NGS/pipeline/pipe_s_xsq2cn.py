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
	import ngCGH_batch, cgh2seg_batch, seg2gene_batch

	return [ ## PARAMETERS
		{
		'name': 'run ngCGH for pairs of bam',
		'desc': 'bam -> .ngCGH',
		'fun': ngCGH_batch.main,
		'paramL': (baseDir, baseDir, 1000, False),
		'paramH': {},
		'logPostFix': '.cn_ngCGH.log',
		'logExistsFn': lambda x: len(x)>0 and 'finalizers' in x[-1],
		'outFilePostFix': ['ngCGH'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'Segmenation',
		'desc': 'ngCGH -> seg',
		'fun': cgh2seg_batch.cgh2seg,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.seg.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Centrality parameter' in x[-1],
		'outFilePostFix': ['ngCGH.seg'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'Calculate gene copy number from segments',
		'desc': 'seg -> cn_gene.dat',
		'fun': seg2gene_batch.main,
		'paramL': (baseDir, baseDir, mysetting.refFlatH[server][genome],[],False),
		'paramH': {},
		'logPostFix': '.cn_gene.log',
		'logExistsFn': lambda x: len(x)>0 and 'ZZZ3' in x[-1],
		'outFilePostFix': ['cn_gene.dat'],
		'clean': False,
		'rerun': False
		},

		]

if __name__ == '__main__':

	optL, argL = getopt.getopt(sys.argv[1:],'i:j:n:p:c:s:g:',['use_pool_dlink','use_pool_sgi'])

	optH = mybasic.parseParam(optL)
	pathL = optH['-i']
	sN = optH['-n']
	pN = optH['-p']
	clean = optH['-c']
	server = optH['-s']
	genome = optH['-g']
	if '--use_pool_dlink' in optH: ## use pooled blood/normal from DNA link
		nPathL = mysetting.poolB_DLink_bam
	elif '--use_pool_sgi' in optH: ## use pooled blood/normal from SGI
		nPathL = mysetting.poolB_SGI_bam
	elif '-j' in optH: ## use matched blood/normal
		nPathL = optH['-j']
	mypipe.main(inputFilePathL=glob(pathL)+glob(nPathL), genSpecFn=genSpec, sampN=sN, projectN=pN, clean=clean, server=server, genome=genome)
