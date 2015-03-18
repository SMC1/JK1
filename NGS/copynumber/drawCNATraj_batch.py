#!/usr/bin/python

import sys, getopt, math, re, os
import mybasic, mygenome, mysetting
from glob import glob

def draw_single(inDirN, outDirN, assembly='hg19'):
	prefix = os.path.basename(inDirN)
	(sid, postfix) = re.match('(.*)_([XCT].{,2})_.*', prefix).groups()
	if postfix != 'T':
		sampN = sid + '_' + postfix
	else:
		sampN = sid

	segFileNL = filter(lambda x: x.endswith("corr.ngCGH.seg"), os.listdir(inDirN))
	if segFileNL != []:
		for segFileN in segFileNL:
			for format in ['png', 'pdf']:
				outFileN = '%s/%s.%s' % (inDirN, segFileN, format)
				cmd = 'R --no-save --no-restore --args %s %s/%s %s < %s/NGS/copynumber/draw_CNA_traj.simple.R' % (sampN, inDirN,segFileN, outFileN, mysetting.SRC_HOME)
				if not os.path.isfile(outFileN):
					print outFileN
					os.system(cmd)
	else:
		segFileNL = filter(lambda x: x.endswith("ngCGH.seg"), os.listdir(inDirN)) + filter(lambda x: x.endswith("copynumber"), os.listdir(inDirN))
		for segFileN in segFileNL:
			for format in ['png', 'pdf']:
				outFileN = '%s/%s' % (outDirN, segFileN.replace('ngCGH.seg', 'Xsq_CNA_traj.%s' % format))
				cmd = 'R --no-save --no-restore --args %s %s/%s %s < %s/NGS/copynumber/draw_CNA_traj.simple.R' % (sampN, inDirN,segFileN, outFileN, mysetting.SRC_HOME)
				if not os.path.isfile(outFileN):
					print outFileN
					os.system(cmd)
	#if

	prbFileNL = filter(lambda x: x.endswith("corr.ngCGH"), os.listdir(inDirN))
	outFileN = '%s/%s.corr.Xsq_CNA_traj_chromwise.pdf' % (outDirN, prefix)
	if prbFileNL == []:
		prbFileNL = filter(lambda x: x.endswith("ngCGH"), os.listdir(inDirN))
		outFileN = '%s/%s.Xsq_CNA_traj_chromwise.pdf' % (outDirN,prefix)
	cmd = 'R --no-save --no-restore --args %s %s/%s %s < %s/NGS/copynumber/draw_CNA_traj.chromwise.R' % (sampN, inDirN,prbFileNL[0], outFileN, mysetting.SRC_HOME)
	if not os.path.isfile(outFileN):
		print outFileN
		os.system(cmd)

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
				cmd = 'R --no-save --no-restore --args %s %s %s < %s/NGS/copynumber/draw_CNA_traj.simple.R' % (sampN, segFile, outFile, mysetting.SRC_HOME)
				if not os.path.isfile(outFile):
					print sampN,segFile,outFile
#					os.system(cmd)
			prbFile = '%s/%s.corr.ngCGH' % (inputFileN, prefix)
			outFile = '%s/%s/%s.corr.Xsq_CNA_traj_chromwise.pdf' % (outDirName, prefix, prefix)
			if not os.path.isfile(prbFile): ## if initial xsq2cn run
				prbFile = '%s/%s.ngCGH' % (inputFileN, prefix)
				outFile = '%s/%s.Xsq_CNA_traj_chromwise.pdf' % (outDirName, prefix)
			cmd = 'R --no-save --no-restore --args %s %s %s < %s/NGS/copynumber/draw_CNA_traj.chromwise.R' % (sampN, prbFile, outFile, mysetting.SRC_HOME)
			if not os.path.isfile(outFile):
				print cmd
#				os.system(cmd)


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
			cmd = 'R --no-save --no-restore --args %s %s %s < %s/NGS/copynumber/draw_CNA_traj.simple.R' % (sampN, segFile, outFile, mysetting.SRC_HOME)
			if not os.path.isfile(outFile):
				print sampN, outFile
				os.system(cmd)

def acgh_batch():
	outDirN = '/EQL1/NSL/CGH/plots'
#	sidL = map(lambda x: x.rstrip(), os.popen('cat acgh_seg_list').readlines())
#	print sidL
	segFileL = glob('/EQL1/NSL/CGH/seg/seg/link/*seg')
	for segFile in segFileL:
		sid = re.match('(.*)\.seg$', os.path.basename(segFile)).group(1)
#		if sid not in sidL:
#			continue
		for format in ['png', 'pdf']:
			outFile = '%s/%s.CGH_CNA_traj.%s' % (outDirN, sid, format)
			cmd = 'R --no-save --no-restore --args %s %s %s < %s/NGS/copynumber/draw_CNA_traj.simple.R' % (sid, segFile, outFile, mysetting.SRC_HOME)
			if not os.path.isfile(outFile):
				print sid, outFile
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
					cmd = 'R --no-save --no-restore --args %s %s %s %s %s < %s/NGS/copynumber/draw_CNA_traj_2pl.R' % (aSegFile, xSegFile, sampN, datFile, outFile, mysetting.SRC_HOME)
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
			chromwise_s(prbFile, outDirName, prefix)

def chromwise_s(segFileN, outDirN, prefix):
	(sid, postfix) = re.match('(.*)_([XCT].{,2})_.*', prefix).groups()
	if postfix != 'T':
		sampN = sid + '_' + postfix
	else:
		sampN = sid
	outFile = '%s/%s.Xsq_CNA_traj_chromwise.pdf' % (outDirN, prefix)
	cmd = 'R --no-save --no-restore --args %s %s %s < %s/NGS/copynumber/draw_CNA_traj.chromwise.R' % (sampN, segFileN, outFile, mysetting.SRC_HOME)
	if not os.path.isfile(outFile):
		print cmd
#		os.system(cmd)

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
#	main('/EQL5/pipeline/CS_CNA', '/EQL1/NSL/WXS/results/CNA')

#	for dirN in glob('/EQL3/pipeline/CNA/*S'):
#		draw_single(dirN, '/EQL1/NSL/WXS/results/CNA')
	for dirN in glob('/EQL3/pipeline/CNA_corr/*S'):
		draw_single(dirN, dirN)

#	main2('/EQL3/pipeline/CNA', '/home/ihlee/352_cn', sampL=['IRCR_GBM_352_TL','IRCR_GBM_352_TR'])
#	main2('/EQL3/pipeline/CNA_corr/backup_CNA_corr_352_LR', '/home/ihlee/352_cn', sampL=['IRCR_GBM_352_TL','IRCR_GBM_352_TR'])
#	acgh_batch()

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
