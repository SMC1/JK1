#!/usr/bin/python

import sys, os, getopt
from glob import glob

import mypipe, mybasic

def genSpec(baseDir):

	moduleL = ['NGS/align','NGS/splice_gsnap/ei_junc'] ## DIRECTORY
	homeDir = os.popen('echo $HOME','r').read().rstrip()

	for module in moduleL:
		sys.path.append('%s/JK1/%s' % (homeDir,module))

	import gsnap_splice_batch, ei_junc_batch## MODULES

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
		'desc': 'splice.gsnap -> ei.dat',
		'fun': ei_junc_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': 'ei.qlog',
		'logExistsFn': lambda x: len(x)>0 and 'Finished' in x[-1],
		'outFilePostFix': ['ei.dat'],
		'clean': False,
		'rerun': False 
		},

		]

if __name__ == '__main__':
	
	optL, argL = getopt.getopt(sys.argv[1:],'i:n:p:c:',[])

	optH = mybasic.parseParam(optL)
		
	pathL = optH['-i']
	sN = optH['-n']
	pN = optH['-p']
	clean = optH['-c']
	 
	mypipe.main(inputFilePathL=glob(pathL), genSpecFn=genSpec, sampN=sN, projectN=pN, clean=clean)

	#mypipe.main(inputFilePathL=glob('/pipeline/fusion_test/S436_RSq_test/*splice.gsnap'), genSpecFn=genSpec, sampN='S436_RSq_test_splice', projectN='test_skip', clean=False)
