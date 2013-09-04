#!/usr/bin/python

import sys, os, re


def link(dirName,outDirName,filePattern,tag=''):

	inputFilePL = os.popen('find %s -name "*.txt"' % dirName,'r')
	
	for fileP in inputFilePL:

		fileP = fileP[:-1]
		
		if 'QCStats' in fileP or 'Metastatic' in fileP or 'Colorectal' in fileP or 'Breast' in fileP or 'Ovarian' in fileP or 'Gastric' in fileP or 'Bladder' in fileP or 'Pancreatic' in fileP or 'Gene expression' in fileP:
			continue

		fileN = fileP.split('/')[-1]
		
		ro = re.match(filePattern, fileN)

		fileP = fileP.replace('(','\(').replace(')','\)').replace(' ','\ ')

		if ro:
			os.system('ln -s %s %s/%s_%s' % (fileP, outDirName,ro.group(2),ro.group(1).replace('(','\(').replace(')','\)').replace(' ','\ ')))
		else:
			os.system('ln -s %s %s/%s' % (fileP, outDirName,fileN))


#link('/data1/IRCR/CGH/raw/GBM_8paired/CGH', '/data1/IRCR/CGH/fe', '(.*Sep09).*\((.*)\).*\.txt')
#link('/data1/IRCR/CGH/raw/CGH_matched_PrimXeno', '/data1/IRCR/CGH/fe', '(US.*).([0-9]{3}).Prim\.txt')
#link('/data1/IRCR/CGH/raw/CGH_matched_PrimXeno', '/data1/IRCR/CGH/fe', '(US.*).([0-9]{3}).Prim\.txt')
#link('/data1/IRCR/CGH/raw/11th_sector/Array\ CGH/Glioblastoma\ array\ CGH', '/data1/IRCR/CGH/fe', '(.*([0-9]{3}).*).txt')

link('/EQL1/NSL/CGH/raw/', '/EQL1/NSL/CGH/fe/link', '(.*([0-9]{3})[^\_^0-9].*)')
#link('/EQL1/NSL/CGH/raw/', '/EQL1/NSL/CGH/fe', '(.*)\(([0-9]{3})\)\.txt')
#link('/EQL1/NSL/CGH/raw/Array_CGH/CGH_SCRI', '/data1/IRCR/CGH/fe/test', '(.*)\(([0-9]{3})\)\.txt')
#link('/EQL1/NSL/CGH/raw/Array_CGH/CGH_SCRI', '/data1/IRCR/CGH/fe/test', '(.*)_([0-9]{3})\.txt')
