#!/usr/bin/python

import sys, os, re


def link(dirName,outDirName,filePattern,tag=''):

	inputFilePL = os.popen('find %s -name "*.fastq.gz"' % dirName,'r')

	for fileP in inputFilePL:

		fileP = fileP[:-1]

		fileN = fileP.split('/')[-1]
				
		ro = re.match(filePattern, fileN)
		sId = ro.group(1)

		seqT = ''

		if 'Kinome' in fileN:
			seqT = 'KN'
		elif 'trueSeq' in fileN:
			seqT = 'TS'
		else:
			seqT = 'SS'
		
		sampT = 'T'

		normal = ['.*_N[^S].*','.*_B[^r].*','N_.*','.*_normal_.*','.*[0-9]{3}N.*']

		for x in normal:
			if re.match(x,fileN):
				sampT = 'B'

		if '_Br' in fileN:
			sampT='T'
		
		newDirN = 'S' + sId +'_'+ sampT +'_'+ seqT
		new_dir = outDirName + '/' + newDirN

		if newDirN in os.listdir(outDirName):
			pass	
		else:
			os.system('mkdir %s' % new_dir)

		if 'R1' in fileN:
			os.system('ln -s %s %s/S%s_%s_%s.1.fq.gz' % (fileP, new_dir, sId, sampT, seqT))
		
		if 'R2' in fileN:
			os.system('ln -s %s %s/S%s_%s_%s.2.fq.gz' % (fileP, new_dir, sId, sampT, seqT))


if __name__ == '__main__':
	#link('/data1/IRCR/CGH/raw/GBM_8paired/CGH', '/data1/IRCR/CGH/fe', '(.*Sep09).*\((.*)\).*\.txt')
	#link('/data1/IRCR/CGH/raw/CGH_matched_PrimXeno', '/data1/IRCR/CGH/fe', '(US.*).([0-9]{3}).Prim\.txt')
	#link('/data1/IRCR/CGH/raw/CGH_matched_PrimXeno', '/data1/IRCR/CGH/fe', '(US.*).([0-9]{3}).Prim\.txt')
	#link('/data1/IRCR/CGH/raw/11th_sector/Array\ CGH/Glioblastoma\ array\ CGH', '/data1/IRCR/CGH/fe', '(.*([0-9]{3}).*).txt')

	link('/EQL1/NSL/WXS/fastq/20130719', '/EQL1/NSL/WXS/fastq/20130719', '.*([0-9]{3})[ITN].*')
	#link('/EQL1/NSL/exome_bam/mutation', '/EQL1/NSL/exome_bam/mutation/link', '(.*)_([0-9]{3})\.txt')
