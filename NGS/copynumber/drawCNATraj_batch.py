#!/usr/bin/python

import sys, getopt, math, re, os
import mybasic, mygenome
from glob import glob

def main(inDirName, outDirName, assembly='hg19', sampL=[]):
	inputFileNL = glob('%s/*_T*_*S' % inDirName)
	print inputFileNL
	for inputFileN in inputFileNL:
		if os.path.isdir(inputFileN):
			prefix = inputFileN.split('/')[-1]
			(sid, postfix) = re.match('(.*)_([XCT].{,2})_.*', prefix).groups()
			if postfix != 'T':
				sampN = sid + '_' + postfix
			else:
				sampN = sid
			if sampL != [] and sampN not in sampL:
				continue
			segFile = '%s/%s.ngCGH.seg' % (inputFileN, prefix)
			if not os.path.isfile(segFile): ## cancerscan
				segFile = '%s/%s.copynumber' % (inputFileN, prefix)
			for format in ['png', 'pdf']:
				outFile = '%s/%s.Xsq_CNA_traj.%s' % (outDirName, prefix, format)
#				cmd = 'R --no-save --no-restore --args %s %s %s %s < ~/JK1/NGS/copynumber/draw_CNA_traj.R' % (sampN, prbFile, segFile, outFile)
				cmd = 'R --no-save --no-restore --args %s %s %s < ~/JK1/NGS/copynumber/draw_CNA_traj.simple.R' % (sampN, segFile, outFile)
				if not os.path.isfile(outFile):
					print sampN,segFile
					os.system(cmd)

def batch(inDirName, outDirName, assembly='hg19'):
	segFileL = glob('%s/*.ngCGH.seg' % inDirName) + glob('%s/*.copynumber' % inDirName)
	for segFile in segFileL:
		if segFile[-3:] == 'seg':
			prefix = re.match('(.*)\.ngCGH\.seg$', os.path.basename(segFile)).group(1)
		else:
			prefix = re.match('(.*)\.copynumber$', os.path.basename(segFile)).group(1)
		(sid, postfix) = re.match('(.*)_([XCT].{,2})_.*', prefix).groups()
		if postfix != 'T':
			sampN = sid + '_' + postfix
		else:
			sampN = sid
		for format in ['png', 'pdf']:
			outFile = '%s/%s.Xsq_CNA_traj.%s' % (outDirName, prefix, format)
			cmd = 'R --no-save --no-restore --args %s %s %s < ~/JK1/NGS/copynumber/draw_CNA_traj.simple.R' % (sampN, segFile, outFile)
			if not os.path.isfile(outFile):
				print sampN, outFile
				os.system(cmd)

def main2(inDirName, outDirName, assembly='hg19', sampL=[]):
	inputFileNL = glob('%s/*_T*_*S' % inDirName)
	for inputFileN in inputFileNL:
		if os.path.isdir(inputFileN):
			prefix = inputFileN.split('/')[-1]
			(sid, postfix) = re.match('(.*)_([XCT].{,2})_.*', prefix).groups()
			if postfix != 'T':
				sampN = sid + '_' + postfix
			else:
				sampN = sid
			if sampL != [] and sampN not in sampL:
				continue
			xSegFile = '%s/%s.ngCGH.seg' % (inputFileN, prefix)
			datFile = '%s/%s.cn_gene.dat' % (inputFileN, prefix)
			aSegFile = '/data1/IRCR/CGH/seg/seg/link/%s.seg' % sampN
			if os.path.isfile(aSegFile):
				for format in ['png', 'pdf']:
					outFile = '%s/%s.Xsq_CNA_traj_2pl.%s' % (outDirName, prefix, format)
					cmd = 'R --no-save --no-restore --args %s %s %s %s %s < ~/JK1/NGS/copynumber/draw_CNA_traj_2pl.R' % (aSegFile, xSegFile, sampN, datFile, outFile)
					print cmd
#					if not os.path.isfile(outFile):
#						os.system(cmd)

def chromwise(inDirName, outDirName, sampL=[]):
	inputFileNL = glob('%s/*_T*_*S' % inDirName)
	for inputFileN in inputFileNL:
		if os.path.isdir(inputFileN):
			prefix = inputFileN.split('/')[-1]
			(sid, postfix) = re.match('(.*)_([XCT].{,2})_.*', prefix).groups()
			if postfix != 'T':
				sampN = sid + '_' + postfix
			else:
				sampN = sid

			if sampL != [] and sampN not in sampL:
				continue

			prbFile = '%s/%s.ngCGH' % (inputFileN, prefix)
			outFile = '%s/%s.Xsq_CNA_traj_chromwise.pdf' % (outDirName, prefix)
			cmd = 'R --no-save --no-restore --args %s %s %s < ~/JK1/NGS/copynumber/draw_CNA_traj.chromwise.R' % (sampN, prbFile, outFile)
			print cmd
			if not os.path.isfile(outFile):
				os.system(cmd)

if __name__ == '__main__':
#	batch('/EQL3/pipeline/CNA/IRCR_GBM10_038_T_SS', '/EQL1/NSL/WXS/results/CNA')
#	batch('/EQL3/pipeline/CNA/IRCR_GBM12_199_T_SS', '/EQL1/NSL/WXS/results/CNA')
#	sampL = ['IRCR_GBM_352_TL','IRCR_GBM_352_TR']
#	sampL = ['IRCR_GBM_363_TD','IRCR_GBM_363_TM','S317_2']
#	sampL = ['S317','S317_2','S316']
#	sampL = ['S189','S189_2']
#	main('/EQL3/pipeline/CNA', '/EQL1/NSL/WXS/results/CNA', sampL=sampL)
#	chromwise('/EQL3/pipeline/CNA', '/EQL1/NSL/WXS/results/CNA', sampL=[])
#	main2('/EQL3/pipeline/CNA', '/EQL1/NSL/WXS/results/CNA', sampL=sampL)
#	main('/EQL3/pipeline/CNA', '/EQL1/NSL/WXS/results/CNA')
	main('/EQL5/pipeline/CS_CNA', '/EQL1/NSL/WXS/results/CNA')
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
