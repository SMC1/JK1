#!/usr/bin/python

import sys, os, re, getopt, glob
import mybasic, mysetting


def main(inDirName):

	fileNameL = glob.glob('%s/*.depth' % inDirName)

	print 'Files: %s (%s)' % (fileNameL, len(fileNameL))

	sampNameL = list(set([re.match('.*\/([^/]*)\.depth',inputFileN).group(1) for inputFileN in fileNameL]))
	sampNameL.sort()

	print 'Samples: %s (%s)' % (sampNameL, len(sampNameL))

	for sampN in sampNameL:

		print sampN
		os.system('Rscript %s/NGS/quality/distribution.r %s %s &> %s/%s.distr.qlog' % (mysetting.SRC_HOME, inDirName,sampN,inDirName,sampN))


if __name__ == '__main__':

	#optL, argL = getopt.getopt(sys.argv[1:],'i:e:o:l:',[])
	#optH = mybasic.parseParam(optL)
	
	main('/EQL1/NSL/Exome/mutation')
