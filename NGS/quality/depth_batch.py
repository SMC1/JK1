#!/usr/bin/python

import sys, os, re, getopt, glob
import mybasic, mysetting


def main(inDirName,outDirName):

	fileNameL = map(lambda x: x.rstrip(), os.popen('find %s -maxdepth 2 -name "*.pileup" | grep -v "_KN"' % inDirName, 'r').readlines())
	fileNameL += map(lambda x: x.rstrip(), os.popen('find %s -maxdepth 2 -name "*.pileup.gz" | grep -v "_KN"' % inDirName, 'r').readlines())

	for fileName in fileNameL:
		sampN = re.match('.*\/([^/]*)\.pileup[\.gz]*',fileName).group(1)

		print sampN

		cmd = 'echo "%s/NGS/quality/depth.py -i %s -o %s/%s.depth" | qsub -N depth_%s -o %s/%s.depth.qlog -j oe' % (mysetting.SRC_HOME, fileName, outDirName,sampN, sampN, outDirName,sampN)
		if not os.path.isfile('%s/%s.depth.qlog' % (outDirName,sampN)):
			os.system(cmd)

if __name__ == '__main__':

	#optL, argL = getopt.getopt(sys.argv[1:],'i:e:o:l:',[])
	#optH = mybasic.parseParam(optL)
	
#	main('/EQL1/NSL/Exome/mutation','/EQL1/NSL/Exome/mutation')

#	dirL = ['/EQL1/NSL/WXS/exome_20130529/','/EQL1/NSL/exome_bam/mutation/pileup_link/','/EQL1/pipeline/ExomeSeq_20130723/', '/EQL3/pipeline/SGI20131031_xsq2mut', '/EQL3/pipeline/SGI20131119_xsq2mut', '/EQL3/pipeline/SGI20131212_xsq2mut', '/EQL3/pipeline/SGI20131216_xsq2mut']
	dirL = ['/EQL2/pipeline/SGI20140204_xsq2mut']
	for dir in dirL:
		main(dir, '/EQL4/pipeline/dcov')
