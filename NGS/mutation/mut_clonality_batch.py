#!/usr/bin/python

import sys, os, re, getopt
import mybasic

def main(inDir, outDir, cnDir, purity, pbs=False):

	inFileNL = os.listdir(inDir)
	inFileNL = filter(lambda x: re.match('(.*)\.mutect', x), inFileNL)

	print 'Files: %s' % inFileNL

	sampNL = list(set([re.match('(.*)\.mutect', inFileN).group(1) for inFileN in inFileNL]))
	sampNL.sort()

	print 'Samples: %s' % sampNL, len(sampNL)

	for sampN in sampNL:

		print sampN

		iprefix = '%s/%s' % (inDir,sampN)
		oprefix = '%s/%s' % (outDir,sampN)
		cmd = '/usr/bin/python ~/JK1/NGS/mutation/mut_clonality.py -s %s/%s.ngCGH.seg -i %s.mutect -o %s.mutect_cl.dat -p %s' % (cnDir,sampN, iprefix, oprefix, purity)
		log = '%s.mutect_cl.log' % oprefix
		print cmd
		
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))
		else:
			os.system('(%s) &> %s' % (cmd, log))

if __name__ == '__main__':
	pass
