#!/usr/bin/python

import sys, os, re

def rename_sid(dirName, old_ID, new_ID):
	inputL=filter(lambda x: old_ID in x, os.listdir(dirName))
	for input in inputL:
		if os.path.isdir('%s/%s' % (dirName,input)):
			for ifile in os.listdir('%s/%s' % (dirName, input)):
				ro = re.match('%s(.*)' % old_ID, ifile)
				if ro:
					surfix = ro.group(1)
					ofile = '%s%s' % (new_ID, surfix)
					cmd = 'mv %s/%s/%s %s/%s/%s' % (dirName,input,ifile, dirName,input,ofile)
					print cmd
					os.system(cmd)
				else:
					print ifile
		ro = re.match('%s(.*)' % old_ID, input)
		if ro:
			surfix = ro.group(1)
			output = '%s%s' % (new_ID,surfix)
			cmd = 'mv %s/%s %s/%s' % (dirName,input, dirName,output)
			print cmd
			os.system(cmd)
		else:
			print input
	

def rename(dirName,outDirName,filePattern,tag):

	inputFileNL = os.listdir(dirName)

	for fileN in inputFileNL:

		ro = re.match(filePattern, fileN)

		if ro:
			os.system('mv -f %s/%s %s/%s.fastq' % (dirName,fileN, outDirName,ro.group(1)))


#rename('/EQL3/TCGA/GBM/RNASeq/alignment/splice/ei_junc', '/EQL3/TCGA/GBM/RNASeq/alignment/splice/ei_junc', '(.*)_EGFR.dat','')
#rename('/EQL1/NSL/RNASeq/fastq', '/EQL1/NSL/RNASeq/fastq', '(.*).fastq.gz.N.fastq','')
#rename_sid('/EQL3/pipeline/SGI20140103_xsq2mut', 'S633', 'S633B')
#rename_sid('/EQL2/pipeline/SGI20140128_xsq2mut', 'S633', 'S633A')
rename_sid('/EQL3/pipeline/SGI20131226_rsq2expr', 'S633', 'S633B')
rename_sid('/EQL3/pipeline/SGI20131226_rsq2mut', 'S633', 'S633B')
rename_sid('/EQL3/pipeline/SGI20131226_rsq2eiJunc', 'S633', 'S633B')
rename_sid('/EQL3/pipeline/SGI20131226_rsq2fusion', 'S633', 'S633B')
rename_sid('/EQL3/pipeline/SGI20131226_rsq2skip', 'S633', 'S633B')
