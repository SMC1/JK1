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
#	mount_dir()
	listF = open(listFN, 'r')

	for line in listF:
		if line[0] == '#':
			continue
		colL = line.rstrip().split('\t')
		dType = '-'
		if len(colL) > 1:
			dType = colL[2]
			file = colL[3]
		else:
			file = colL[0]
		server = file.split('/')[1]
		if server == 'EQL2':
			fileN = file
		else:
			fileN = SGI_DIR_PREFIX[server]+'/'+'/'.join(file.split('/')[3:])
		fileN = fileN.replace('R1', 'R*')
		print dType,file,fileN

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
#	umount_dir()

if __name__ == '__main__':
#	get_files('/EQL2/CS_20140327/filelist.txt','/EQL2/CS_20140327')
#	get_files('/EQL2/CS_20140430/filelist.txt','/EQL2/CS_20140430')
#	get_files('/EQL2/CS_20140512/filelist.txt','/EQL2/CS_20140512')
#	get_files('/EQL2/CS_20140613/filelist.txt','/EQL2/CS_20140613')
	get_files('/EQL2/CS_20140618/filelist.txt','/EQL2/CS_20140618')
