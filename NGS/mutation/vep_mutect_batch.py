#!/usr/bin/python

import sys, os
import vep_mutect

def main(inDirNameL):
	inFileL = []
	for inDirName in inDirNameL:
		inFileL += map(lambda x: x.rstrip(), os.popen('find %s -name S*.mutect' % inDirName).readlines())
	
	for inFile in inFileL:
		outDir = '/'.join(inFile.split('/')[:-1])
		print inFile, outDir
		vep_mutect.vep_mutect(inFile, outDir)
	
if __name__ == '__main__':
#	main(['/EQL1/NSL/exome_bam/mutation', '/EQL1/NSL/WXS/exome_20130529'])
	main(['/EQL3/pipeline/somatic_mutect'])
