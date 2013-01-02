#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def trim4x_batch(inDirName,fileNamePattern,outDirName,trimLen):

	fileNameL = os.listdir(inDirName)
	fileNameL = filter(lambda x: re.match(fileNamePattern, x), fileNameL)

	sampNameL = list(set([re.match(fileNamePattern,inputFileN).group(1) for inputFileN in fileNameL]))
	sampNameL.sort()

	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

#		if sampN not in ['C282.TCGA-32-2638-01A-01W-0922-08.1','C484.TCGA-12-5299-01A-02D-1486-08.6']:
		if sampN not in ['C484.TCGA-12-5299-01A-02D-1486-08.6']:
			continue

		print sampN

		os.system('cat %s/%s.*.fastq | ~jinkuk/Codes/NGS/fastq/trim4x.py -i stdin -o %s/%s_WXS_4x_%snt -l %s' \
			% (inDirName,sampN, outDirName,sampN,trimLen, trimLen))


optL, argL = getopt.getopt(sys.argv[1:],'i:e:o:l:',[])

optH = mybasic.parseParam(optL)

trim4x_batch('/EQL2/TCGA/GBM/WXS/fastq', '(.*)\.[12]\.fastq', '/EQL2/TCGA/GBM/WXS/fastq/4x_27nt', 27)
