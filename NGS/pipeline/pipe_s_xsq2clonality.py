#!/usr/bin/python

import sys, os, getopt
from glob import glob

import mypipe, mybasic, mysetting

def register_modules(moduleL):
	homeDir = os.popen('echo $HOME','r').read().rstrip()
	for module in moduleL:
		sys.path.append('%s/JK1/%s' % (homeDir, module))

def genSpec(baseDir, server='smc1', genome='hg19'):
	register_modules(['NGS/mutation'])
	import	mut_clonality_batch

	return [ ## PARAMETERS
		{
		'name': 'determine mutation clonality',
		'desc': 'mutect -> mutect_cl.dat',
		'fun': mut_clonality_batch.main,
		'paramL': (baseDir, baseDir, mysetting.cnaBaseDir, False, server),
		'paramH': {},
		'logPostFix': '.mutect_cl.log',
		'logExistsFn': lambda x: len(x)==0,
		'outFilePostFix': ['mutect_cl.dat'],
		'clean': False,
		'rerun': False
		},

		]

if __name__ == '__main__':

	optL, argL = getopt.getopt(sys.argv[1:],'i:n:p:c:s:',[])

	optH = mybasic.parseParam(optL)
	pathL = optH['-i']
#	cnPathL = optH['-k']
	sN = optH['-n']
	pN = optH['-p']
	clean = optH['-c']
	server = optH['-s']
	
#	mypipe.main(inputFilePathL=glob(pathL)+glob(cnPathL), genSpecFn=genSpec, sampN=sN, projectN=pN, clean=clean, server=server)
	mypipe.main(inputFilePathL=glob(pathL), genSpecFn=genSpec, sampN=sN, projectN=pN, clean=clean, server=server)
