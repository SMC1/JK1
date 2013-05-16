#!/usr/bin/python

import sys, os, re

redunH = {'460':'460_US91703680_252206016153_S01_CGH_107_Sep09_1_1_copyNumber.seg', '503':'503_NS08.503T_copyNumber.seg', '559':'559_US91703680_252206010876_S01_CGH_107_Sep09_1_2_copyNumber.seg', '585':'585_US91703680_252206011010_S01_CGH_107_Sep09_1_2_copyNumber.seg', '631':'631_NS09.631T_copyNumber.seg', '633':'633_NS09.633T_copyNumber.seg', '740':'740_NS09.740T_copyNumber.seg'}

def link(dirName,outDirName,filePattern,tag=''):

	inputFilePL = os.popen('find %s -name "*.seg"' % dirName,'r')

	for fileP in inputFilePL:

		fileP = fileP[:-1]

		fileN = fileP.split('/')[-1]
		
		ro = re.match(filePattern, fileN)

		if not ro:
			continue

		if ro.group(1) in redunH and redunH[ro.group(1)] != fileN:
			continue

		fileP = fileP.replace('(','\(').replace(')','\)').replace(' ','\ ')

		if ro:
			os.system('ln -s %s %s/S%s.seg' % (fileP, outDirName,ro.group(1)))


#link('/data1/IRCR/CGH/raw/GBM_8paired/CGH', '/data1/IRCR/CGH/fe', '(.*Sep09).*\((.*)\).*\.txt')
#link('/data1/IRCR/CGH/raw/CGH_matched_PrimXeno', '/data1/IRCR/CGH/fe', '(US.*).([0-9]{3}).Prim\.txt')
#link('/data1/IRCR/CGH/raw/CGH_matched_PrimXeno', '/data1/IRCR/CGH/fe', '(US.*).([0-9]{3}).Prim\.txt')
#link('/data1/IRCR/CGH/raw/11th_sector/Array\ CGH/Glioblastoma\ array\ CGH', '/data1/IRCR/CGH/fe', '(.*([0-9]{3}).*).txt')

#link('/EQL1/NSL/CGH/raw/Array_CGH/CGH_SCRI', '/data1/IRCR/CGH/fe/test', '(.*)\(([0-9]{3})\)\.txt')

link('/data1/IRCR/CGH/seg', '/data1/IRCR/CGH/seg/link', '([0-9]{3}).*\.seg')
