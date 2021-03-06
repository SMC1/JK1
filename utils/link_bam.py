#!/usr/bin/python

import sys, os, re


def link(dirName,outDirName,filePattern,tag=''):

	inputFilePL = os.popen('find %s -name "*.recal.bam"' % dirName,'r')

	for fileP in inputFilePL:

		fileP = fileP[:-1]

		fileN = fileP.split('/')[-1]
		
		if 'bam_link' in fileN:
			continue

		ro = re.match(filePattern, fileN)
		sId = ro.group(1)

		seqT = ''

		if 'Kinome' in fileN:
			seqT = 'KN'
		elif 'trueSeq' in fileN:
			seqT = 'TS'
		else:
			seqT = 'SS'
		
		sampT = ''

		if '_N' in fileN or '_B' in fileN and not '_Br' in fileN:
			sampT = 'B'
		elif '_Br' in fileN:
			sampT = 'X'
		else:
			sampT = 'T'

		print 'ln -s %s %s/S%s_%s_%s.recal.bam' % (fileP, outDirName, sId, sampT, seqT)
		os.system('ln -s %s %s/S%s_%s_%s.recal.bam' % (fileP, outDirName, sId, sampT, seqT))
		bai = fileP.replace('.bam','.bai')
		if os.path.isfile(bai):
			print 'cp %s %s/S%s_%s_%s.recal.bai' % (bai, outDirName, sId, sampT, seqT)
			os.system('cp %s %s/S%s_%s_%s.recal.bai' % (bai, outDirName, sId, sampT, seqT))
#
#		fileP = fileP.replace('(','\(').replace(')','\)').replace(' ','\ ')
#
#		if ro:
#			os.system('ln -s %s %s/%s_%s.txt' % (fileP, outDirName,ro.group(2),ro.group(1).replace('(','\(').replace(')','\)')))


#link('/data1/IRCR/CGH/raw/GBM_8paired/CGH', '/data1/IRCR/CGH/fe', '(.*Sep09).*\((.*)\).*\.txt')
#link('/data1/IRCR/CGH/raw/CGH_matched_PrimXeno', '/data1/IRCR/CGH/fe', '(US.*).([0-9]{3}).Prim\.txt')
#link('/data1/IRCR/CGH/raw/CGH_matched_PrimXeno', '/data1/IRCR/CGH/fe', '(US.*).([0-9]{3}).Prim\.txt')
#link('/data1/IRCR/CGH/raw/11th_sector/Array\ CGH/Glioblastoma\ array\ CGH', '/data1/IRCR/CGH/fe', '(.*([0-9]{3}).*).txt')

link('/EQL1/NSL/exome_bam', '/EQL1/NSL/exome_bam/bam_link', '.*([0-9]{3}).*')
#link('/EQL1/NSL/exome_bam/mutation', '/EQL1/NSL/exome_bam/mutation/link', '(.*)_([0-9]{3})\.txt')
