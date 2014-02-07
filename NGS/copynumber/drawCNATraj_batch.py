#!/usr/bin/python

import sys, getopt, math, re, os
import mybasic, mygenome
from glob import glob

def main(inDirName, outDirName, assembly='hg19', sampL=[]):
	inputFileNL = glob('%s/*_T_*S' % inDirName)
	for inputFileN in inputFileNL:
		if os.path.isdir(inputFileN):
			prefix = inputFileN.split('/')[-1]
			sampN = re.match('(.*)_T_.*', prefix).group(1)
			if sampL != [] and sampN not in sampL:
				continue
			prbFile = '%s/%s.copynumber' % (inputFileN, prefix)
			segFile = '%s/%s.copyNumber.seg' % (inputFileN, prefix)
			for format in ['png', 'pdf']:
				outFile = '%s/%s.Xsq_CNA_traj.%s' % (outDirName, prefix, format)
#				cmd = 'R --no-save --no-restore --args %s %s %s %s < ~/JK1/NGS/copynumber/draw_CNA_traj.R' % (sampN, prbFile, segFile, outFile)
				cmd = 'R --no-save --no-restore --args %s %s %s < ~/JK1/NGS/copynumber/draw_CNA_traj.simple.R' % (sampN, segFile, outFile)
				os.system(cmd)

def main2(inDirName, outDirName, assembly='hg19', sampL=[]):
	inputFileNL = glob('%s/*_T_*S' % inDirName)
	for inputFileN in inputFileNL:
		if os.path.isdir(inputFileN):
			prefix = inputFileN.split('/')[-1]
			sampN = re.match('(.*)_T_.*', prefix).group(1)
			if sampL != [] and sampN not in sampL:
				continue
			xSegFile = '%s/%s.copyNumber.seg' % (inputFileN, prefix)
			datFile = '%s/%s.cn_gene.dat' % (inputFileN, prefix)
			aSegFile = '/data1/IRCR/CGH/seg/seg/link/%s.seg' % sampN
			if os.path.isfile(aSegFile):
				for format in ['png', 'pdf']:
					outFile = '%s/%s.Xsq_CNA_traj_2pl.%s' % (outDirName, prefix, format)
					cmd = 'R --no-save --no-restore --args %s %s %s %s %s < ~/JK1/NGS/copynumber/draw_CNA_traj_2pl.R' % (aSegFile, xSegFile, sampN, datFile, outFile)
					os.system(cmd)

if __name__ == '__main__':
	sampL=['S723','S015','S202','S386','S421']
	main('/EQL3/pipeline/CNA', '/EQL1/NSL/WXS/results/CNA', sampL=sampL)
	main2('/EQL3/pipeline/CNA', '/EQL1/NSL/WXS/results/CNA', sampL=sampL)
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
