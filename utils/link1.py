#!/usr/bin/python

import sys, os, re


def link(dirName,outDirName,filePattern,tag=''):

	inputFilePL = os.popen('find %s -name "*.tdf"' % dirName,'r')

	for fileP in inputFilePL:

		fileP = fileP[:-1]

		fileN = fileP.split('/')[-1]
		
		ro = re.match(filePattern, fileN)

		if ro:
			#os.system('ln -s %s %s/T%s_%s.tdf' % (fileP, outDirName,ro.group(2),ro.group(1)))
			os.system('ln -s %s %s/T%s.tdf' % (fileP, outDirName,ro.group(2)))
			#os.system('ln -s %s %s/%s_%s_%s.tdf' % (fileP, outDirName,ro.group(2),tag,ro.group(1)))


#link('/data1/IRCR/CGH/raw/GBM_8paired/CGH', '/data1/IRCR/CGH/fe', '(.*Sep09).*\((.*)\).*\.txt')
#link('/data1/IRCR/CGH/raw/CGH_matched_PrimXeno', '/data1/IRCR/CGH/fe', '(US.*).([0-9]{3}).Prim\.txt')
#link('/data1/IRCR/CGH/raw/CGH_matched_PrimXeno', '/data1/IRCR/CGH/fe', '(US.*).([0-9]{3}).Prim\.txt')
#link('/data1/IRCR/CGH/raw/11th_sector/Array\ CGH/Glioblastoma\ array\ CGH', '/data1/IRCR/CGH/fe', '(.*([0-9]{3}).*).txt')

#link('/EQL1/NSL/CGH/raw/Array_CGH/CGH_SCRI', '/data1/IRCR/CGH/fe/test', '(.*)\(([0-9]{3})\)\.txt')
#link('/EQL1/NSL/CGH/raw/Array_CGH/CGH_SCRI', '/data1/IRCR/CGH/fe/test', '(.*)_([0-9]{3})\.txt')

#link('/EQL1/NSL/WXS/coverage', '/EQL1/NSL/Exome/coverage/tdf', '(.*([0-9]{3}).*)\.tdf','WXS')
#link('/EQL1/NSL/WXS_trueSeq/coverage', '/EQL1/NSL/Exome/coverage/tdf', '(.*([0-9]{3}).*)\.tdf','WXSts')
#link('/EQL1/NSL/Kinome/coverage', '/EQL1/NSL/Exome/coverage/tdf', '(.*([0-9]{3}).*)\.tdf','KN')

#link('/EQL2/TCGA/GBM/RNASeq/coverage/tdf', '/EQL2/TCGA/GBM/RNASeq/coverage/tdf/link', '.*(TCGA-..-(....).*)_30nt_z.\.tdf','')
#link('/EQL1/NSL/RNASeq/coverage/tdf', '/EQL1/NSL/RNASeq/coverage/tdf/link', '(.*([0-9]{3}).*)\.tdf','')

link('/EQL4/TCGA/GBM/WXS/coverage/tdf', '/EQL4/TCGA/GBM/WXS/coverage/tdf/link3', '(.*TCGA-..-([0-9]{4}).*)\.tdf','')

