#!/usr/bin/python

import sys, os, getopt
from glob import glob

import mypipe, mybasic, mysetting

def genSpec(baseDir, server='smc1', genome='hg19'):
	mybasic.add_module_path(['NGS/phylotree'])
	import merge_count, make_phylotree

	return [
		{
		'name': 'merge counts',
		'desc': 'merge mutation loci and allele counts',
		'fun': merge_count.merge_count,
		'paramL': (baseDir, baseDir, 5, 0.05, 5),
#		'paramL': (baseDir, baseDir, 20, 0.2, 5),
		'paramH': {},
		'logPostFix': '.merge_count.log',
		'logExistsFn': lambda x: 'done' in x[-1],
		'outFilePostFix': ['.mutations','.filtered'],
		'clean': False,
		'rerun': False
		},

		{
		'name': 'build tree',
		'desc': 'make phylogenetic tree',
		'fun': make_phylotree.main,
		'paramL': (baseDir, baseDir),
		'paramH': {},
		'logPostFix': '.make_phylotree.log',
		'logExistsFn': lambda x: 'done' in x[-1],
		'outFilePostFix': ['.infile', '.outfile','.tree','.pars_tree.pdf','.outfile_report.txt'],
		'clean': False,
		'rerun': False
		},
	]

if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:], 'i:n:p:c:s:g:')

	optH = mybasic.parseParam(optL)
	pathL = optH['-i'].split(',')
	sN = optH['-n']
	pN = optH['-p']
	clean = optH['-c']
	server = optH['-s']
	genome = optH['-g']
	genSpecFN = genSpec

	if pathL != []:
		mypipe.main(inputFilePathL=pathL, genSpecFn=genSpecFN, sampN=sN, projectN=pN, clean=clean, server=server, genome=genome)
