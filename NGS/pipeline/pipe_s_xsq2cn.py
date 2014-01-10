#!/usr/bin/python

import sys, os, getopt
from glob import glob

import mypipe, mybasic, mysetting

def genSpec(baseDir, server='smc1', genome='hg19'):

	moduleL = ['NGS/coverage', 'NGS/expression', 'NGS/copynumber'] ## DIRECTORY
	homeDir = os.popen('echo $HOME','r').read().rstrip()

	for module in moduleL:
		sys.path.append('%s/JK1/%s' % (homeDir,module))

	import bam2sortedBed_batch, degSeq_batch, rpkm2cn_batch, prb2seg_batch, seg2gene_batch ## MODULES
	
	return [ ## PARAMETERS
		{
		'name': 'Formet Conversion and sorting',
		'desc': 'bam -> sort -> sorted.bed',
		'fun': bam2sortedBed_batch.sam2bed_batch,
		'paramL': (baseDir, baseDir, False),
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
		'name': 'Calculate a log rpkm ratio for all exons',
		'desc': 'log2(tumor rpkm/normal rpkm)',
		'fun': rpkm2cn_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.cn.log',
		'logExistsFn': lambda x: len(x)==0,
		'outFilePostFix': ['copynumber'],
		'clean': False,
		'rerun': False
		},
		
		{
		'name': 'Segmenation',
		'desc': 'copynumber -> seg',
		'fun': prb2seg_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.seg.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'array has repeated maploc positions' in x[-2],
		'outFilePostFix': ['copyNumber.seg'],
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

	optL, argL = getopt.getopt(sys.argv[1:],'i:j:n:p:c:s:g:',[])

	optH = mybasic.parseParam(optL)

	pathL = optH['-i']
	nPathL = optH['-j']
	sN = optH['-n']
	pN = optH['-p']
	clean = optH['-c']
	server = optH['-s']
	genome = optH['-g']

	#mypipe.main(inputFilePathL=glob('/EQL1/NSL/exome_bam/sortedBam_link/S023_T_SS.sorted.bam')+glob('/EQL1/NSL/exome_bam/sortedBam_link/S140_B_SS.sorted.bam'), genSpecFn=genSpec, sampN='S023_T_SS', projectN='test_xsq2cn', clean=False, server='smc1', genome='hg19')
	mypipe.main(inputFilePathL=glob(pathL)+glob(nPathL), genSpecFn=genSpec, sampN=sN, projectN=pN, clean=clean, server=server, genome=genome)
