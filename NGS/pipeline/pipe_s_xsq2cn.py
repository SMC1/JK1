#!/usr/bin/python

import sys, os, getopt
from glob import glob

import mypipe, mybasic, mysetting

def register_modules(moduleL):
	homeDir = os.popen('echo $HOME','r').read().rstrip()
	for module in moduleL:
		sys.path.append('%s/JK1/%s' % (homeDir, module))

def genSpec_CS(baseDir, server='smc1', genome='hg19'):
	register_modules(['NGS/coverage','NGS/expression','NGS/copynumber'])
	import bam2sortedBed_batch, degSeq_batch, rpkm2cn_batch, exon2gene_batch

	return [ ## PARAMTERS
		{
		'name': 'Format Conversion and sorting',
		'desc': 'bam -> sort -> sorted.bed',
		'fun': bam2sortedBed_batch.sam2bed_batch,
		'paramL': (baseDir, baseDir, 'recal', False),
		'paramH': {},
		'logPostFix': '.sorted.bed.qlog',
		'logExistsFn': lambda x: len(x)==0,
		'outFilePostFix': ['sorted.bed'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'RPKMgen',
		'desc': 'sorted.bed -> rpkm',
		'fun': degSeq_batch.main,
		'paramL': (baseDir, baseDir, '/data1/Sequence/ucsc_hg19/annot/refFlat_exon.txt', False),
		'paramH': {},
		'logPostFix': '.degSeq.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'omitted' in x[-1],
		'outFilePostFix': ['rpkm'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'Calculate a log2 rpkm ratio for all exons',
		'desc': 'log2(tumor rpkm/normal rpkm',
		'fun': rpkm2cn_batch.main_pool,
		'paramL': (baseDir, baseDir, 10, mysetting.poolB_CS_rpkm, False),
		'paramH': {},
		'logPostFix': '.cn.log',
		'logExistsFn': lambda x: len(x)==0,
		'outFilePostFix': ['copynumber'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'Calculate gene copy number from log2 rpkm ratios',
		'desc': 'copynumber -> cn_gene.dat',
		'fun': exon2gene_batch.main,
		'paramL': (baseDir, baseDir, mysetting.refFlatH[server][genome],mysetting.cs_gene,False),
		'paramH': {},
		'logPostFix': '.cn_gene.log',
		'logExistsFn': lambda x: len(x)>0 and 'VHL' in x[-1],
		'outFilePostFix': ['cn_gene.dat'],
		'clean': False,
		'rerun': False
		},
	]

def genSpec(baseDir, server='smc1', genome='hg19'):
	register_modules(['NGS/copynumber'])
	import ngCGH_batch, cgh2seg_batch, seg2gene_batch, drawCNATraj_batch

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

		{
		'name': 'Draw Plot',
		'desc': 'seg->plot',
		'fun' : drawCNATraj_batch.batch,
		'paramL': (baseDir, '/EQL1/NSL/WXS/results/CNA',genome),
		'paramH': {},
		'logPostFix': '',
		'logExistsFn': lambda x: True,
		'outFilePostFix': [],
		'clean': False,
		'rerun': False
		},

		]

if __name__ == '__main__':

	optL, argL = getopt.getopt(sys.argv[1:],'i:j:n:p:c:s:g:',['use_pool_dlink','use_pool_sgi','cancerscan'])

	optH = mybasic.parseParam(optL)
	pathL = optH['-i']
	sN = optH['-n']
	pN = optH['-p']
	clean = optH['-c']
	server = optH['-s']
	genome = optH['-g']
	genSpecFN = genSpec
	inputL = []
	if '--cancerscan' in optH: ## cancerscan sample
#		nPathL = mysetting.poolB_CS_bam
		genSpecFN = genSpec_CS
		inputL = glob(pathL)

	else:
		if '--use_pool_dlink' in optH: ## use pooled blood/normal from DNA link
			nPathL = mysetting.poolB_DLink_bam
		elif '--use_pool_sgi' in optH: ## use pooled blood/normal from SGI
			nPathL = mysetting.poolB_SGI_bam
		elif '-j' in optH: ## use matched blood/normal
			nPathL = optH['-j']
		inputL = glob(pathL) + glob(nPathL)
	
	if inputL != []:
		mypipe.main(inputFilePathL=inputL, genSpecFn=genSpecFN, sampN=sN, projectN=pN, clean=clean, server=server, genome=genome)
