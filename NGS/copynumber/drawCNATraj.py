#!/usr/bin/python

import sys, getopt, math, re, os
import mybasic, mygenome, mysetting
from glob import glob

def main(inDirName, outDirName):
	inFileNL = filter(lambda x: re.match('(.*)\.corr\.ngCGH\.seg', x), os.listdir(inDirName))

	for inFileN in inFileNL:
		(sid, postfix) = re.match('(.*)_([XCT].{,2})_.*corr.ngCGH.seg', inFileN).groups()
		if postfix != 'T':
			sampN = sid + '_' + postfix
		else:
			sampN = sid

		prefix = re.match('(.*)\.corr\.ngCGH\.seg', inFileN).group(1)

		segFile = '%s/%s' % (inDirName, inFileN)
		for format in ['png', 'pdf']:
			outFile = '%s/%s.%s' % (outDirName, inFileN, format)
			cmd = 'Rscript %s/NGS/copynumber/draw_CNA_traj.simple.R %s %s %s' % (mysetting.SRC_HOME, sampN, segFile, outFile)
			log = '%s/%s.traj_plot.log' % (inDirName,prefix)
			if not os.path.isfile(outFile):
				os.system('(%s) &> %s' % (cmd, log))

if __name__ == '__main__':
	sampL = []
	main('/EQL3/pipeline/CNA', '/EQL1/NSL/WXS/results/CNA', sampL=sampL)
	main2('/EQL3/pipeline/CNA', '/EQL1/NSL/WXS/results/CNA', sampL=sampL)
#	main('/EQL3/pipeline/CNA', '/EQL1/NSL/WXS/results/CNA')
#	main2('/EQL3/pipeline/CNA', '/EQL1/NSL/WXS/results/CNA')
#	optL, argL = getopt.getopt(sys.argv[1:],'i:r:o:g:a:',[])
#
#	optH = mybasic.parseParam(optL)
#
#	if '-i' in optH and '-o' in optH:
#
#		if '-g' in optH:
#			geneNameL = geneNames.split(',')
#		else:
#			geneNameL = [] 
#
#	main(optH['-i'],optH['-r'],optH['-o'],geneNameL,optH['-a'])
