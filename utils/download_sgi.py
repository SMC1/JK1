#!/usr/bin/python

import os, sys
from mysetting import SGI_DIR_PREFIX, SGI_PATH

def mount_dir():
	for i in SGI_PATH.keys():
		os.system('mount -t nfs -o wsize=131072,rsize=131072 %s %s' % (SGI_PATH[i], SGI_DIR_PREFIX[i]))
		os.system('mount -t nfs %s %s' % (SGI_PATH[i], SGI_DIR_PREFIX[i]))

def umount_dir():
	for i in SGI_PATH.keys():
		os.system('umount %s' % SGI_DIR_PREFIX[i])

def get_files(listFN, outDN):
	mount_dir()
	listF = open(listFN, 'r')

	for line in listF:
		colL = line.rstrip().split('\t')
		dType = '-'
		if len(colL) > 1:
			dType = colL[0]
			file = colL[1]
		else:
			file = colL[0]
		server = file.split('/')[1]
		fileN = SGI_DIR_PREFIX[server]+'/'+'/'.join(file.split('/')[3:])
		print dType,file

		dest = ''
		if dType == 'RNA':
			dest = outDN + '/RNASeq/fastq'
			if not os.path.isdir(outDN + '/RNASeq'):
				os.system('mkdir %s/RNASeq' % outDN)
				os.system('mkdir %s/RNASeq/fastq' % outDN)
			elif not os.path.isdir(dest):
				os.system('mkdir %s' % dest)
		elif dType == 'DNA':
			dest = outDN + '/WXS/fastq'
			if not os.path.isdir(outDN + '/WXS'):
				os.system('mkdir %s/WXS' % outDN)
				os.system('mkdir %s/WXS/fastq' % outDN)
			elif not os.path.isdir(dest):
				os.system('mkdir %s' % dest)
		else:
			dest = outDN + '/fastq'
			if not os.path.isdir(outDN + '/fastq'):
				os.system('mkdir %s/fastq' % outDN)
		if dest != '':
			print 'cp %s %s' % (fileN, dest)
			os.system('cp %s %s' % (fileN, dest))
	umount_dir()

if __name__ == '__main__':
#	get_files('/EQL2/SGI_20131226/filelist.txt','/EQL2/SGI_20131226')
#	get_files('/EQL2/SGI_20140103/filelist.txt','/EQL2/SGI_20140103')
#	get_files('/EQL2/SGI_20140128/filelist.txt','/EQL2/SGI_20140128')
#	get_files('/EQL2/SGI_20140204/filelist.txt','/EQL2/SGI_20140204')
#	get_files('/EQL2/SGI_20140210/filelist.txt','/EQL2/SGI_20140210')
#	get_files('/EQL2/SGI_20140219/filelist.txt','/EQL2/SGI_20140219')
#	get_files('/EQL6/RC85_LC195/filelist.txt', '/EQL6/RC85_LC195')
#	get_files('/EQL2/SGI_20140331/filelist.txt','/EQL2/SGI_20140331')
#	get_files('/EQL2/SGI_20140410/filelist.txt','/EQL2/SGI_20140410')
#	get_files('/EQL2/SGI_20140411/filelist.txt','/EQL2/SGI_20140411')
#	get_files('/EQL2/SGI_20140422/filelist.txt','/EQL2/SGI_20140422')
#	get_files('/EQL6/SGI_20140422_singlecell/filelist.txt','/EQL6/SGI_20140422_singlecell')
#	get_files('/EQL6/RC85_LC195_WXS/filelist.txt','/EQL6/RC85_LC195_WXS')
	get_files('/EQL2/SGI_20140520/filelist.txt','/EQL2/SGI_20140520')
