#!/usr/bin/python

import os, sys
from mysetting import SGI_DIR_PREFIX, SGI_PATH

def mount_dir():
	for i in SGI_PATH.keys():
		os.system('mount -t nfs %s %s' % (SGI_PATH[i], SGI_DIR_PREFIX[i]))

def umount_dir():
	for i in SGI_PATH.keys():
		os.system('umount %s' % SGI_DIR_PREFIX[i])

def get_files(listFN, outDirN):
	listF = open(listFN, 'r')

	for line in listF:
		if line[0] == '#':
			continue
		colL = line.rstrip().split('\t')
		dType = colL[1]
		file = colL[2]

		if 'hiseq1' in file:
			fileN = '/BiO/' + '/'.join(file.split('/')[2:])
			fileN = fileN.replace('_R1', '_R*').replace('_R2', '_R*')
		elif 'hiseq2' in file:
			fileN = '/SGI2/' + '/'.join(file.split('/')[2:])
			fileN = fileN.replace('_R1', '_R*').replace('_R2', '_R*')
		else:
			fileN = file.replace('_R1', '_R*').replace('_R2', '_R*')

		dest = ''
		if dType == 'RNA':
			dest = outDirN + '/RNASeq/fastq'
			if not os.path.isdir(outDirN + '/RNASeq'):
				os.system('mkdir %s/RNASeq' % outDirN)
				os.system('mkdir %s/RNASeq/fastq' % outDirN)
			elif not os.path.isdir(dest):
				os.system('mkdir %s' % dest)
		elif dType == 'DNA':
			dest = outDirN + '/WXS/fastq'
			if not os.path.isdir(outDirN + '/WXS'):
				os.system('mkdir %s/WXS' % outDirN)
				os.system('mkdir %s/WXS/fastq' % outDirN)
			elif not os.path.isdir(dest):
				os.system('mkdir %s' % dest)
		else:
			dest = outDirN + '/fastq'
			if not os.path.isdir(outDirN + '/fastq'):
				os.system('mkdir %s/fastq' % outDirN)
		if dest != '':
#			sys.stdout.write('cd %s; sshpass -p myfastq sftp fastq@119.5.134.125:%s' % (dest, fileN))
#			sys.stdout.write('\n')
			if fileN[:4] == 'http':
				os.system('cd %s; wget %s' % (dest, fileN))
				os.system('cd %s; wget %s' % (dest, fileN.replace('_1.fastq.gz','_2.fastq.gz')))
			else:
				os.system('cd %s; sshpass -p myfastq sftp fastq@119.5.134.125:%s' % (dest, fileN))

def get_files_old(listFN, outDN):
#	mount_dir()
	listF = open(listFN, 'r')

	for line in listF:
		if line[0] == '#':
			continue
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
#	umount_dir()

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
#	get_files('/EQL2/SGI_20140520/filelist.txt','/EQL2/SGI_20140520')
#	get_files('/EQL2/SGI_20140526/filelist.txt','/EQL2/SGI_20140526')
#	get_files('/EQL2/SGI_20140428/filelist.txt','/EQL2/SGI_20140428')
#	get_files('/EQL2/SGI_20140526/filelist2.txt','/EQL2/SGI_20140526')
#	get_files('/EQL2/SGI_20140529/filelist.txt','/EQL2/SGI_20140529')
#	get_files('/EQL2/SGI_20140602/filelist.txt','/EQL2/SGI_20140602')
#	get_files('/EQL2/SGI_20140611/filelist.txt','/EQL2/SGI_20140611')
#	get_files('/EQL2/SGI_20140617/filelist.txt','/EQL2/SGI_20140617')
#	get_files('/EQL2/SGI_20140620/filelist.txt','/EQL2/SGI_20140620')
#	get_files('/EQL2/CS_20140623/filelist.txt','/EQL2/CS_20140623')
#	get_files('/EQL2/SGI_20140625/filelist.txt','/EQL2/SGI_20140625')
#	get_files('/EQL2/CS_20140702/filelist.txt','/EQL2/CS_20140702')
#	get_files('/EQL2/SGI_20140702/filelist.txt','/EQL2/SGI_20140702')
#	get_files('/EQL2/SGI_20140703/filelist.txt','/EQL2/SGI_20140703')
#	get_files('/EQL2/SGI_20140707/filelist.txt','/EQL2/SGI_20140707')
#	get_files('/EQL2/SGI_20140710/filelist.txt','/EQL2/SGI_20140710')
#	get_files('/EQL2/SGI_20140714/filelist.txt','/EQL2/SGI_20140714')
#	get_files('/EQL2/CS_20140714/filelist.txt','/EQL2/CS_20140714')
#	get_files('/EQL2/SGI_20140716/filelist.txt','/EQL2/SGI_20140716')
#	get_files('/EQL2/SGI_20140718/filelist.txt','/EQL2/SGI_20140718')
#	get_files('/EQL2/SGI_20140721/filelist.txt','/EQL2/SGI_20140721')
#	get_files('/EQL2/SGI_20140723/filelist.txt','/EQL2/SGI_20140723')
#	get_files('/EQL2/CS_20140728/filelist.txt','/EQL2/CS_20140728')
#	get_files('/EQL2/SGI_20140728/filelist.txt','/EQL2/SGI_20140728')
#	get_files('/EQL2/SGI_20140804/filelist.txt','/EQL2/SGI_20140804')
#	get_files('/EQL2/CS_20140805/filelist.txt','/EQL2/CS_20140805')
##	get_files('/EQL2/SGI_20140807/filelist.txt','/EQL2/SGI_20140807')
##	get_files('/EQL2/SGI_20140811/filelist.txt','/EQL2/SGI_20140811')
##	get_files('/EQL2/SGI_20140813/filelist.txt','/EQL2/SGI_20140813')
#	get_files('/EQL2/SGI_20140818/filelist.txt','/EQL2/SGI_20140818')
#	get_files('/EQL2/CS_20140819/filelist.txt','/EQL2/CS_20140819')
#	get_files('/EQL2/SGI_20140821/filelist.txt','/EQL2/SGI_20140821')
#	get_files('/EQL2/SGI_20140825/filelist.txt','/EQL2/SGI_20140825')
#	get_files('/EQL2/SGI_20140827/filelist.txt','/EQL2/SGI_20140827')
#	get_files('/EQL2/SGI_20140828/filelist.txt','/EQL2/SGI_20140828')
#	get_files('/EQL2/SGI_20140829/filelist.txt','/EQL2/SGI_20140829')
#	get_files('/EQL2/SGI_20140901/filelist.txt','/EQL2/SGI_20140901')
#	get_files('/EQL2/CS_20140828/filelist.txt','/EQL2/CS_20140828')
#	get_files('/EQL2/SGI_20140904/filelist.txt','/EQL2/SGI_20140904')
#	get_files('/EQL2/CS_20140904/filelist.txt','/EQL2/CS_20140904')
#	get_files('/EQL6/SGI_20140915_singlecell/filelist.txt','/EQL6/SGI_20140915_singlecell')
#	get_files('/EQL2/SGI_20140917/filelist.txt','/EQL2/SGI_20140917')
#	get_files('/EQL2/SGI_20140922/filelist.txt','/EQL2/SGI_20140922')
#	get_files('/EQL2/CS_20140924/filelist.txt','/EQL2/CS_20140924')
#	get_files('/EQL2/SGI_20140930_NSC/filelist.txt','/EQL2/SGI_20140930_NSC')
#	get_files('/EQL2/SGI_20140930/filelist.txt','/EQL2/SGI_20140930')
#	get_files('/EQL2/SGI_20141001/filelist.txt','/EQL2/SGI_20141001')
#	get_files('/EQL2/CS_20141007/filelist.txt','/EQL2/CS_20141007')
#	get_files('/EQL2/SGI_20141008/filelist.txt','/EQL2/SGI_20141008')
#	get_files('/EQL2/SGI_20141013/filelist.txt','/EQL2/SGI_20141013')
#	get_files('/EQL2/CS_20141015/filelist.txt','/EQL2/CS_20141015')
#	get_files('/EQL2/CS_20141022/filelist.txt','/EQL2/CS_20141022')
#	get_files('/EQL2/SGI_20141021/filelist.txt','/EQL2/SGI_20141021')
#	get_files('/EQL2/SGI_20141027/filelist.txt','/EQL2/SGI_20141027')
#	get_files('/EQL2/SGI_20141031/filelist.txt','/EQL2/SGI_20141031')
#	get_files('/EQL2/CS_20141030/filelist.txt','/EQL2/CS_20141030')
#	get_files('/EQL2/SGI_20141103/filelist.txt','/EQL2/SGI_20141103')
#	get_files('/EQL2/SGI_20141110/filelist.txt','/EQL2/SGI_20141110')
#	get_files('/EQL2/SGI_20141112/filelist.txt','/EQL2/SGI_20141112')
#	get_files('/EQL2/CS_20141112/filelist.txt','/EQL2/CS_20141112')
#	get_files('/EQL2/SGI_20141117/filelist.txt','/EQL2/SGI_20141117')
#	get_files('/EQL2/CS_20141126/filelist.txt','/EQL2/CS_20141126')
#	get_files('/EQL2/SGI_20141126/filelist.txt','/EQL2/SGI_20141126')
#	get_files('/EQL2/SGI_20141202/filelist.txt','/EQL2/SGI_20141202')
#	get_files('/EQL2/SGI_20141203/filelist.txt','/EQL2/SGI_20141203')
#	get_files('/EQL2/CS_20141210/filelist.txt','/EQL2/CS_20141210')
#	get_files('/EQL2/SGI_20141210/filelist.txt','/EQL2/SGI_20141210')
#	get_files('/EQL2/SGI_20141211/filelist.txt','/EQL2/SGI_20141211')
#	get_files('/EQL2/CS_20141217/filelist.txt','/EQL2/CS_20141217')
#	get_files('/EQL2/SGI_20141218/filelist.txt','/EQL2/SGI_20141218')
#	get_files('/EQL2/SGI_20141222/filelist.txt','/EQL2/SGI_20141222')
#	get_files('/EQL2/CS_20141231/filelist.txt','/EQL2/CS_20141231')
#	get_files('/EQL2/CS_20150107/filelist.txt','/EQL2/CS_20150107')
#	get_files('/EQL2/SGI_20150102/filelist.txt','/EQL2/SGI_20150102')
#	get_files('/EQL2/SGI_20150112/filelist.txt','/EQL2/SGI_20150112')
#	get_files('/EQL2/CS_20150115/filelist.txt','/EQL2/CS_20150115')
#	get_files('/EQL2/SGI_20150115/filelist.txt','/EQL2/SGI_20150115')
#	get_files('/EQL2/SGI_20150121/filelist.txt','/EQL2/SGI_20150121')
#	get_files('/EQL2/SGI_20150121_2/filelist.txt','/EQL2/SGI_20150121_2')
#	get_files('/EQL2/SGI_20150123/filelist.txt','/EQL2/SGI_20150123')
#	get_files('/EQL2/SGI_20150128/filelist.txt','/EQL2/SGI_20150128')
#	get_files('/EQL2/CS_20150128/filelist.txt','/EQL2/CS_20150128')
#	get_files('/EQL2/CS_20150204/filelist.txt','/EQL2/CS_20150204')
#	get_files('/EQL2/SGI_20150206/filelist.txt','/EQL2/SGI_20150206')
#	get_files('/EQL2/CS_20150211/filelist.txt','/EQL2/CS_20150211')
	get_files('/EQL2/SGI_20150223/filelist.txt','/EQL2/SGI_20150223')
