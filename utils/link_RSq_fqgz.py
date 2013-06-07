#!/usr/bin/python

import sys, os, re


def link(dirName,outDirName,filePattern,tag=''):

	inputFilePL = os.popen('find %s -name "*.fastq.gz"' % dirName,'r')

	for fileP in inputFilePL:

		fileP = fileP[:-1]
		fileN = fileP.split('/')[-1]
		
		ro = re.match(filePattern, fileN)
		sId = ro.group(1)
		idx = ro.group(2)

		os.system('ln -s %s %s/S%s_RSq.%s.fq.gz' % (fileP, outDirName, sId, idx))


#link('/data1/IRCR/CGH/raw/GBM_8paired/CGH', '/data1/IRCR/CGH/fe', '(.*Sep09).*\((.*)\).*\.txt')
#link('/data1/IRCR/CGH/raw/CGH_matched_PrimXeno', '/data1/IRCR/CGH/fe', '(US.*).([0-9]{3}).Prim\.txt')
#link('/data1/IRCR/CGH/raw/CGH_matched_PrimXeno', '/data1/IRCR/CGH/fe', '(US.*).([0-9]{3}).Prim\.txt')
#link('/data1/IRCR/CGH/raw/11th_sector/Array\ CGH/Glioblastoma\ array\ CGH', '/data1/IRCR/CGH/fe', '(.*([0-9]{3}).*).txt')

#link('/EQL1/NSL/exome_bam/mutation', '/EQL1/NSL/exome_bam/mutation/link', '.*([0-9]{3}).*')
#link('/EQL1/NSL/exome_bam/mutation', '/EQL1/NSL/exome_bam/mutation/link', '(.*)_([0-9]{3})\.txt')
link('/EQL1/NSL/RNASeq/fastq', '/EQL1/NSL/RNASeq/fastq/link41', '.*([0-9]{3})T.*R([12]).*')
