#!/usr/bin/python

import os, sys, re
from multiprocessing import Pool

def doWork(cmd):
	print cmd
	os.system(cmd)
	return(0)

def merge(inDir1, inDir2, outDir, moreInDirL=[]):
	inFileL1 = filter(lambda x: 'fastq.gz' in x, os.listdir(inDir1))
	inFileL2 = filter(lambda x: 'fastq.gz' in x, os.listdir(inDir2))

	common = list(set(inFileL1).intersection(inFileL2))
	for dir in moreInDirL:
		fileL = filter(lambda x: 'fastq.gz' in x, os.listdir(dir))
		common = list(set(common).intersection(fileL))

	if len(common) < 1:
		print "ERROR: no common file!"
		sys.exit(1)
	
	cmdL = []
	for file in common:
		prefix = re.match('(.*).fastq.gz', file).group(1)
		outName = prefix + '_merged.fastq.gz'

		cmd = 'zcat %s/%s; zcat %s/%s' % (inDir1,file, inDir2,file)
		for dir in moreInDirL:
			cmd = '%s; zcat %s/%s' % (cmd, dir,file)
		cmd = '(%s) | gzip -c > %s/%s' % (cmd, outDir,outName)
		cmdL.append(cmd)
		if os.path.isfile(outDir + '/' + outName):
			print '!!!!'
	
	for cmd in cmdL:
		print cmd
	pool = Pool(processes = 8)
	pool.map(doWork, cmdL)


if __name__ == '__main__':
#	merge('/EQL2/SGI_20140617/WXS/fastq', '/EQL2/SGI_20140703/WXS/fastq', '/EQL2/SGI_20140617/WXS/fastq')
#	merge('/EQL2/SGI_20140625/WXS/fastq', '/EQL2/SGI_20140718/WXS/fastq', '/EQL2/SGI_20140625/WXS/fastq')
#	merge('/EQL2/SGI_20140625/WXS/fastq', '/EQL2/SGI_20140804/WXS/fastq', '/EQL2/SGI_20140625/WXS/fastq')
#	merge('/EQL2/SGI_20140710/RNASeq/fastq', '/EQL2/SGI_20140804/RNASeq/fastq', '/EQL2/SGI_20140710/RNASeq/fastq')
#	merge('/EQL2/SGI_20140723/RNASeq/fastq', '/EQL2/SGI_20140804/RNASeq/fastq', '/EQL2/SGI_20140723/RNASeq/fastq')
#	merge('/EQL2/SGI_20140728/WXS/fastq', '/EQL2/SGI_20140807/WXS/fastq', '/EQL2/SGI_20140728/WXS/fastq')
#	merge('/EQL2/SGI_20140710/RNASeq/fastq', '/EQL2/SGI_20140807/RNASeq/fastq', '/EQL2/SGI_20140710/RNASeq/fastq')
#	merge('/EQL2/SGI_20140728/WXS/fastq', '/EQL2/SGI_20140818/WXS/fastq', '/EQL2/SGI_20140728/WXS/fastq')
#	merge('/EQL2/SGI_20140625/WXS/fastq', '/EQL2/SGI_20140718/WXS/fastq', '/EQL2/SGI_20140625/WXS/fastq', moreInDirL=['/EQL2/SGI_20140827/WXS/fastq'])
#	merge('/EQL2/SGI_20140825/WXS/fastq', '/EQL2/SGI_20140828/WXS/fastq', '/EQL2/SGI_20140825/WXS/fastq')
#	merge('/EQL2/SGI_20140825/WXS/fastq', '/EQL2/SGI_20140904/WXS/fastq', '/EQL2/SGI_20140825/WXS/fastq')
	merge('/EQL2/SGI_20150121/RNASeq/fastq', '/EQL2/SGI_20150121_2/RNASeq/fastq', '/EQL2/SGI_20150121/RNASeq/fastq')
