#!/usr/bin/python

import sys, getopt, math, re, os
import mybasic, mygenome

def main(inDirName, outDirName, assembly='hg19'):
	inputFileNL = os.listdir(inDirName)
	for inputFileN in inputFileNL:
		if os.path.isdir(inDirName + '/' + inputFileN):
			sampN = re.match('(.*)_T_.*', inputFileN).group(1)
			print sampN, inputFileN
			prbFile = '%s/%s/%s.copynumber' % (inDirName, inputFileN, inputFileN)
			segFile = '%s/%s/%s.copyNumber.seg' % (inDirName, inputFileN, inputFileN)
			for format in ['png', 'pdf']:
				outFile = '%s/%s.Xsq_CNA_traj.%s' % (outDirName, inputFileN, format)
#				cmd = 'R --no-save --no-restore --args %s %s %s %s < ~/JK1/NGS/copynumber/draw_CNA_traj.R' % (sampN, prbFile, segFile, outFile)
				cmd = 'R --no-save --no-restore --args %s %s %s < ~/JK1/NGS/copynumber/draw_CNA_traj.simple.R' % (sampN, segFile, outFile)
				os.system(cmd)

def main2(inDirName, outDirName, assembly='hg19'):
	inputFileNL = os.listdir(inDirName)
	for inputFileN in inputFileNL:
		if os.path.isdir(inDirName + '/' + inputFileN):
			sampN = re.match('(.*)_T_.*', inputFileN).group(1)
			print sampN, inputFileN
			xSegFile = '%s/%s/%s.copyNumber.seg' % (inDirName, inputFileN, inputFileN)
			datFile = '%s/%s/%s.cn_gene.dat' % (inDirName, inputFileN, inputFileN)
			aSegFile = '/data1/IRCR/CGH/seg/seg/link/%s.seg' % sampN
			if os.path.isfile(aSegFile):
				for format in ['png', 'pdf']:
					outFile = '%s/%s.Xsq_CNA_traj_2pl.%s' % (outDirName, inputFileN, format)
					cmd = 'R --no-save --no-restore --args %s %s %s %s %s < ~/JK1/NGS/copynumber/draw_CNA_traj_2pl.R' % (aSegFile, xSegFile, sampN, datFile, outFile)
					os.system(cmd)

if __name__ == '__main__':
	main('/EQL3/pipeline/CNA', '/EQL1/NSL/WXS/results/CNA')
	main2('/EQL3/pipeline/CNA', '/EQL1/NSL/WXS/results/CNA')
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
