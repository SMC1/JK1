#!/usr/bin/python

import sys, os, getopt
from glob import glob

import mypipe, mysetting

def genSpec(baseDir, server='smc1', genome='hg19'):

	moduleL = ['NGS/mutation','NGS/purity'] ## DIRECTORY
	homeDir = os.popen('echo $HOME','r').read().rstrip()

	for module in moduleL:
		sys.path.append('%s/JK1/%s' % (homeDir,module))

	import pileup2snp_pair_batch, delta_baf_batch, delta_baf_mutscan_batch, delta_baf_seg_batch, calcCN_LOH_batch, calcNormalF_loh_batch, peakFrac_batch, dbaf_cn_plot_batch ## MODULES

	return [ ## PARAMETERS
#		{
#		'name': 'VarScan',
#		'desc': 'pileup -> snp',
#		'fun': pileup2snp_pair_batch.main,
#		'paramL': (baseDir, baseDir, False),
#		'paramH': {},
#		'logPostFix': '.snp.qlog',
#		'logExistsFn': lambda x: len(x)>0 and 'Variant' in x[-1],
#		'outFilePostFix': ['snp'],
#		'clean': False,
#		'rerun': False
#		},
#		
#		{
#		'name': 'delta B-allele frequencies calculation',
#		'desc': 'calculate tumor delta BAF for all positions genotyped as heterozygous in the normal sample',
#		'fun': delta_baf_batch.main,
#		'paramL': (baseDir, baseDir, False),
#		'paramH': {},
#		'logPostFix': '.dbaf.log',
#		'logExistsFn': lambda x: len(x)==0,
#		'outFilePostFix': ['dbaf.txt'],
#		'clean': False,
#		'rerun': False
#		},
#		
		{
		'name': 'delta B-allele frequencies calculation',
		'desc': 'calculate tumor delta BAF for all positions genotyped as heterozygous in the normal sample',
		'fun': delta_baf_mutscan_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.dbaf.log',
		'logExistsFn': lambda x: len(x)==0,
		'outFilePostFix': ['dbaf.txt'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'delta BAF segmentation',
		'desc': 'segment delta BAF',
		'fun': delta_baf_seg_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.dbaf.seg.log',
		'logExistsFn': lambda x: len(x)>0 and 'Analyzing' in x[-1],
		'outFilePostFix': ['seg'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'Plotting',
		'desc': 'Generate deltaBAF/CN trajectory plot',
		'fun': dbaf_cn_plot_batch.main,
		'paramL': (baseDir, baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.traj_plot.log',
		'logExistsFn': lambda x: len(x)>0 and 'Done' in x[-1],
		'outFilePostFix': ['dBAF_CNA_traj.pdf'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'CNLOH/LOH determination',
		'desc': 'calculate average copy number of LOH segments to determine CNLOH/LOH',
		'fun': calcCN_LOH_batch.main,
		'paramL': (baseDir, baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.loh_cn.log',
		'logExistsFn': lambda x: len(x)>0 and 'Setting' in x[-1],
		'outFilePostFix': ['loh_cn.txt'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'Normal contamiation calculation',
		'desc': 'calculate normal contamination levels at heterozygous germline SNPs in LOH regions',
		'fun': calcNormalF_loh_batch.main,
		'paramL': (baseDir, baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.nfrac_all.log',
		'logExistsFn': lambda x: len(x)==0,
		'outFilePostFix': ['nFrac_all.txt'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'Tumor fraction estimation',
		'desc': 'estimate tumor fraction',
		'fun': peakFrac_batch.main,
		'paramL': (baseDir, baseDir,False),
		'paramH': {},
		'logPostFix': '.tfrac.log',
		'logExistsFn': lambda x: len(x)>0 and 'Done' in x[-1],
		'outFilePostFix': ['tumor_frac.txt'],
		'clean': False,
		'rerun': False
		},

		]

if __name__ == '__main__':

	optL, argL = getopt.getopt(sys.argv[1:],'i:j:k:n:p:c:s:g:',[])

	optH = dict(optL)

	pathL = optH['-i']
	nPathL = optH['-j']
	cnPathL = optH['-k']
	sN = optH['-n']
	pN = optH['-p']
	clean = optH['-c']
	server = optH['-s']
	genome = optH['-g']

#	mypipe.main(inputFilePathL=glob('/EQL1/NSL/exome_bam/mutation/mutscan/S647_T_SS.mutscan')+glob('/EQL1/NSL/exome_bam/mutation/mutscan/S586_B_SS.mutscan')+glob('/EQL3/pipeline/CNA/S647_T_SS/S647_T_SS.copyNumber.seg'), genSpecFn=genSpec, sampN='S647_T_SS', projectN='test_purity', clean=False, server='smc1', genome='hg19')
	mypipe.main(inputFilePathL=glob(pathL)+glob(nPathL)+glob(cnPathL), genSpecFn=genSpec, sampN=sN, projectN=pN, clean=clean, server=server, genome=genome)
