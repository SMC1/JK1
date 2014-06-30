#!/usr/bin/python

import sys, os
import vep_mutect

def main(inDirNameL):
	inFileL = []
	for inDirName in inDirNameL:
		inFileL += filter(lambda x: 'backup' not in x, map(lambda x: x.rstrip(), os.popen('find %s -name *S.mutect' % inDirName).readlines()))
	
	for inFile in inFileL:
		print inFile
		outDir = '/'.join(inFile.split('/')[:-1])
		vepOut = outDir + '/' + inFile.split('/')[-1] + '_vep.dat'
		if not os.path.isfile(vepOut):
			print inFile, outDir, vepOut
			vep_mutect.vep_mutect(inFile, outDir)
	
if __name__ == '__main__':
#	main(['/EQL1/NSL/exome_bam/mutation', '/EQL1/NSL/WXS/exome_20130529'])
	main(['/EQL3/pipeline/somatic_mutect'])
