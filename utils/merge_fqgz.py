#!/usr/bin/python

import os, sys, re
from multiprocessing import Pool

def doWork(cmd):
	print cmd
	os.system(cmd)
	return(0)

def merge(inDir1, inDir2, outDir):
	inFileL1 = filter(lambda x: 'fastq.gz' in x, os.listdir(inDir1))
	inFileL2 = filter(lambda x: 'fastq.gz' in x, os.listdir(inDir2))

	common = list(set(inFileL1).intersection(inFileL2))

	if len(common) < 1:
		print "ERROR: no common file!"
		sys.exit(1)
	
	cmdL = []
	for file in common:
		prefix = re.match('(.*).fastq.gz', file).group(1)
		outName = prefix + '_merged.fastq.gz'

		cmd = '(zcat %s/%s; zcat %s/%s) | gzip -c > %s/%s' % (inDir1,file, inDir2,file, outDir,outName)
		cmdL.append(cmd)
	
	pool = Pool(processes = 4)
	pool.map(doWork, cmdL)


if __name__ == '__main__':
#	merge('/EQL2/SGI_20140617/WXS/fastq', '/EQL2/SGI_20140703/WXS/fastq', '/EQL2/SGI_20140617/WXS/fastq')
#	merge('/EQL2/SGI_20140625/WXS/fastq', '/EQL2/SGI_20140718/WXS/fastq', '/EQL2/SGI_20140625/WXS/fastq')
	merge('/EQL2/SGI_20140625/WXS/fastq', '/EQL2/SGI_20140804/WXS/fastq', '/EQL2/SGI_20140625/WXS/fastq')
	merge('/EQL2/SGI_20140710/RNASeq/fastq', '/EQL2/SGI_20140804/RNASeq/fastq', '/EQL2/SGI_20140710/RNASeq/fastq')
