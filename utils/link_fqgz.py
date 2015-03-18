#!/usr/bin/python

import sys, os, re

def link_cs(dirName, outDirName, listFilename):
	inFile = open(listFilename, 'r')
	for line in inFile:
		colL = line.rstrip().split('\t')
		prefix=colL[0]
		if len(prefix.split('_')) == 3: #IRCR_***_[0-9]{3}
			prefix = prefix + '_T'
		
		fname=os.path.basename(colL[3])
		if fname[-2:] != 'gz':
			fname += '.gz'
		num=0
		if 'R2' in fname:
			num=2
		elif 'R1' in fname:
			num=1
		if os.path.isfile('%s/%s' % (dirName,fname)):
			cmd = 'ln -s %s/%s %s/%s_CS.%s.fq.gz' % (dirName,fname, outDirName,prefix,num)
			print cmd
			os.system(cmd)
#		fname=fname.replace('R1.fastq.gz','R2.fastq.gz')
#		if os.path.isfile('%s/%s' % (dirName,fname)):
#			cmd = 'ln -s %s/%s %s/%s_CS.2.fq.gz' % (dirName,fname, outDirName,prefix)
#			print cmd
#			os.system(cmd)

def link_fq(dirName, outDirName, filePatternL, prefix='IRCR.GBM', sid='', tag='', dType='T', sType='SS'):
	inputFilePL = os.popen('find %s -maxdepth 1 -name "*.fastq.gz"' % dirName, 'r')
	for fileP in inputFilePL:
		fileP = fileP[:-1]
		fileN = fileP.split('/')[-1]
		for filePattern in filePatternL:
			ro = re.match(filePattern, fileN)
			fileP = fileP.replace('(','\(').replace(')','\)').replace(' ','\ ')
			if ro:
				if sid == '':
					sid = ro.group(1)
				for i in range(3-len(sid)):
					sid = '0'+sid
				idx = ro.group(2).replace('(','\(').replace(')','\)')
				tail = tag
				if dType == 'S': #single-cell
					tail = tag + ro.group(1)
				outName = '%s_%s_%s%s_%s' % (prefix, sid, dType, tail, sType)
				os.system('ln -s %s %s/%s.%s.fq.gz' % (fileP, outDirName, outName, idx))


def link_l(dirName,outDirName,filePatternL,tag='',RSQ=False, normalL=[], prefix='S'):
	inputFilePL = os.popen('find %s -maxdepth 1 -name "*.fastq.gz"' % dirName, 'r')
	for fileP in inputFilePL:
		fileP = fileP[:-1]
		fileN = fileP.split('/')[-1]
		for filePattern in filePatternL:
			ro = re.match(filePattern, fileN)
			fileP = fileP.replace('(','\(').replace(')','\)').replace(' ','\ ')
			print '[%s]' % fileP
			if ro:
				if RSQ:
					os.system('ln -s %s %s/%s%s_RSq.%s.fq.gz' % (fileP, outDirName,prefix,ro.group(1),ro.group(2).replace('(','\(').replace(')','\)')))
				else:
					sid = ro.group(1)
					idx = ro.group(2).replace('(','\(').replace(')','\)')
					if sid in normalL:
						os.system('ln -s %s %s/%s%s_B_SS.%s.fq.gz' % (fileP, outDirName,prefix,sid,idx))
					else:
						print '%s%s_T_SS' % (prefix,sid)
						os.system('ln -s %s %s/%s%s_T_SS.%s.fq.gz' % (fileP, outDirName,prefix,sid,idx))

def link_fqgz_old(dirName, outDirName, patFileName):
	inFile = open(patFileName)
	for line in inFile:
		if line[0] == '#':
			continue
		colL = line.rstrip().split('\t')
		sType = colL[0]
		fName = colL[1]
		sid = colL[2]
		localFile = dirName + '/' + os.path.basename(fName)
		sNum = re.match('.*_R([12]).fastq.gz', os.path.basename(fName)).group(1)
		if os.path.isfile(localFile):
			if sType == 'RNA':
				os.system('ln -s %s %s/%s_RSq.%s.fq.gz' % (localFile, outDirName,sid,sNum))
			elif sType == 'DNA':
				os.system('ln -s %s %s/%s_SS.%s.fq.gz' % (localFile, outDirName,sid,sNum))

def link_fqgz(dirName, outDirName, patFileName, isCS=False):
	if not os.path.isdir(outDirName):
		os.system('mkdir %s' % outDirName)
	inFile = open(patFileName)
	for line in inFile:
		if line[0] == '#':
			continue
		colL = line.rstrip().split('\t')
		sid = colL[0]
		sType = colL[1]
		fName = colL[2]
#		fbase = re.match('(.*)_R[12].*.fastq.gz', os.path.basename(fName)).group(1)
#		fName2 = os.path.basename(fName).replace('_R1', '_R*').replace('_R2','_R*')
		fbase = re.match('(.*)_[R]{,1}[12].*.fastq.gz', os.path.basename(fName)).group(1)
		fName2 = os.path.basename(fName).replace('_R1', '_R*').replace('_R2','_R*').replace('_1','_*').replace('_2','_*')
		fileL = map(lambda x: os.path.basename(x.rstrip()), filter(lambda x: fbase in x, os.popen('ls %s/%s' % (dirName, fName2)).readlines()))
		if fileL != []:
			print sid, sType, fName, fbase
			for file in fileL:
#				sNum = re.match('.*_R([12]).*.fastq.gz', file).group(1)
				sNum = re.match('.*_[R]{,1}([12]).*.fastq.gz', file).group(1)
				print sNum, file
				if sType == 'RNA':
					os.system('ln -s %s/%s %s/%s_RSq.%s.fq.gz' % (dirName,file, outDirName,sid,sNum))
				elif sType == 'DNA':
					if isCS:
						os.system('ln -s %s/%s %s/%s_CS.%s.fq.gz' % (dirName,file, outDirName,sid,sNum))
					else:
						os.system('ln -s %s/%s %s/%s_SS.%s.fq.gz' % (dirName,file, outDirName,sid,sNum))

def link(dirName,outDirName,filePattern,tag='',RSQ=False, normalL=[]):

	inputFilePL = os.popen('find %s -maxdepth 1 -name "*.fastq.gz"' % dirName, 'r')

	for fileP in inputFilePL:

		fileP = fileP[:-1]

		fileN = fileP.split('/')[-1]
		
		ro = re.match(filePattern, fileN)

		fileP = fileP.replace('(','\(').replace(')','\)').replace(' ','\ ')

		print '[%s]' % fileP

		if ro:
			if RSQ:
				os.system('ln -s %s %s/S%s_RSq.%s.fq.gz' % (fileP, outDirName,ro.group(1),ro.group(2).replace('(','\(').replace(')','\)')))
			else:
				sid = ro.group(1)
				idx = ro.group(2).replace('(','\(').replace(')','\)')
				if sid in normalL:
					os.system('ln -s %s %s/S%s_B_SS.%s.fq.gz' % (fileP, outDirName,sid,idx))
				else:
					os.system('ln -s %s %s/S%s_T_SS.%s.fq.gz' % (fileP, outDirName,sid,idx))


#link('/data1/IRCR/CGH/raw/GBM_8paired/CGH', '/data1/IRCR/CGH/fe', '(.*Sep09).*\((.*)\).*\.txt')
#link('/data1/IRCR/CGH/raw/CGH_matched_PrimXeno', '/data1/IRCR/CGH/fe', '(US.*).([0-9]{3}).Prim\.txt')
#link('/data1/IRCR/CGH/raw/CGH_matched_PrimXeno', '/data1/IRCR/CGH/fe', '(US.*).([0-9]{3}).Prim\.txt')
#link('/data1/IRCR/CGH/raw/11th_sector/Array\ CGH/Glioblastoma\ array\ CGH', '/data1/IRCR/CGH/fe', '(.*([0-9]{3}).*).txt')

#link('/EQL1/NSL/CGH/raw/Array_CGH/CGH_SCRI', '/data1/IRCR/CGH/fe/test', '(.*)\(([0-9]{3})\)\.txt')
#link('/EQL1/NSL/CGH/raw/Array_CGH/CGH_SCRI', '/data1/IRCR/CGH/fe/test', '(.*)_([0-9]{3})\.txt')

#link('/EQL1/NSL/RNASeq/fastq', '/EQL1/NSL/RNASeq/fastq/link3', '.*(568|050|047|022|460)T.*R([12])_001\.fastq.gz')
##SGI 20131031 samples
#link_l('/EQL2/SGI_20131031/RNASeq/fastq','/EQL2/SGI_20131031/RNASeq/fastq/link',['([0-9]{1,2}[AB]).*R([12]).fastq.gz', '.*([0-9]{3})T.*R([12]).fastq.gz'], RSQ=True)
#link('/EQL2/SGI_20131031/WXS/fastq','/EQL2/SGI_20131031/WXS/fastq/link','([0-9]{1,2}C).*R([12]).fastq.gz', normalL=['10C','11C','12C','3C','7C','9C'])
##SGI 20131119 samples
#link('/EQL2/SGI_20131119/RNASeq/fastq','/EQL2/SGI_20131119/RNASeq/fastq/link','.*-([0-9]{3}).*_[ACGT]{6}_R([12]).fastq.gz',RSQ=True)
#link_l('/EQL2/SGI_20131119/WXS/fastq','/EQL2/SGI_20131119/WXS/fastq/link',['([0-9]{1,2}[ABC])_[ACGT]{6}_R([12]).*.fastq.gz','.*([0-9]{3}).*_[ACGT]{6}_R([12]).fastq.gz'], normalL=['14C','8C','5C'])
##SGI 20131212 samples
#link_l('/EQL2/SGI_20131212/WXS/fastq', '/EQL2/SGI_20131212/WXS/fastq/link',['([0-9]{1,2}[ABC])_[ACGT]{6}_R([12]).*.fastq.gz','.*([0-9]{3}).*_[ACGT]{6}_R([12]).fastq.gz'], normalL=['4C','6C','208'])
#link_l('/EQL2/SGI_20131212/RNASeq/fastq', '/EQL2/SGI_20131212/RNASeq/fastq/link', ['NS[0-9]{2}([0-9]{3}).*_[ACGT]{6}_R([12]).fastq.gz','GBM[0-9]{2}([0-9]{3}).*_[ACGT]{6}_R([12]).fastq.gz'], RSQ=True)
#link_l('/EQL2/SGI_20131216/WXS/fastq','/EQL2/SGI_20131216/WXS/fastq/link',['.*([0-9]{3}).*[ACGT]{6}_R([12]).fastq.gz'])
#link_l('/EQL2/SGI_20131226/RNASeq/fastq','/EQL2/SGI_20131226/RNASeq/fastq/link',['([0-9][AB]).*_[ACGT]{6}_R([12]).fastq.gz','IRCR_GBM[0-9]{2}_([0-9]{3}).*_[ACGT]{6}_R([12]).fastq.gz','NS[0-9]{2}_([0-9]{3}).*_[ACGT]{6}_R([12]).fastq.gz'],RSQ=True)
#link_l('/EQL2/SGI_20140103/WXS/fastq','/EQL2/SGI_20140103/WXS/fastq/link',['NS[0-9]{2}_([0-9]{3}).*_[ACGT]{6}_R([12]).*.fastq.gz'])
#link_l('/EQL2/SGI_20140103/WXS/fastq','/EQL2/SGI_20140103/WXS/fastq/link',['NS[0-9]{2}_B_([0-9]{3}).*_[ACGT]{6}_R([12]).*.fastq.gz'], normalL=['796'])
#link_fq('/EQL6/SGI_20140104_singlecell/RNASeq/fastq', '/EQL6/SGI_20140104_singlecell/RNASeq/fastq/link',['GBM1_(.*)_[ACGT]{8}-[ACGT]{8}_R([12]).fastq.gz'], prefix='IRCR.GBM', sid='352', tag='1_', dType='S', sType='RSq')
#link_fq('/EQL6/SGI_20140104_singlecell/RNASeq/fastq', '/EQL6/SGI_20140104_singlecell/RNASeq/fastq/link',['GBM2_(.*)_[ACGT]{8}-[ACGT]{8}_R([12]).fastq.gz'], prefix='IRCR.GBM', sid='352', tag='2_', dType='S', sType='RSq')
#link_l('/EQL2/SGI_20140128/WXS/fastq','/EQL2/SGI_20140128/WXS/fastq/link',['.*_([0-9]{3}).*_[ACGT]{6}_R([12]).fastq.gz'], normalL=['015','386','676','723'])
#link_fq('/EQL6/SGI_20140203_singlecell/RNASeq/fastq', '/EQL6/SGI_20140203_singlecell/RNASeq/fastq/link', ['GBM363_T1_(.*)_[ACGT]{8}-[ACGT]{8}_R([12]).fastq.gz'], prefix='IRCR.GBM', sid='363', tag='M_', dType='S', sType='RSq')
#link_fq('/EQL6/SGI_20140203_singlecell/RNASeq/fastq', '/EQL6/SGI_20140203_singlecell/RNASeq/fastq/link', ['GBM363_T2_(.*)_[ACGT]{8}-[ACGT]{8}_R([12]).fastq.gz'], prefix='IRCR.GBM', sid='363', tag='D_', dType='S', sType='RSq')
#link_l('/EQL2/SGI_20140204/RNASeq/fastq', '/EQL2/SGI_20140204/RNASeq/fastq/link', ['NS04_(.*)_[ACGT]{6}_R([12])_.*.fastq.gz'], RSQ=True) ## 079
#link_fq('/EQL2/SGI_20140204/RNASeq/fastq', '/EQL2/SGI_20140204/RNASeq/fastq/link', ['NS07_(.*)T_.*_R([12])_.*.fastq.gz'], prefix='NS_GBM', tag='01', dType='C', sType='RSq')
#link_fq('/EQL2/SGI_20140204/RNASeq/fastq', '/EQL2/SGI_20140204/RNASeq/fastq/link', ['NS01_(.*)T_.*_R([12])_.*.fastq.gz'], prefix='NS_GBM', tag='01', dType='C', sType='RSq')
#link_fq('/EQL2/SGI_20140204/RNASeq/fastq', '/EQL2/SGI_20140204/RNASeq/fastq/link', ['NS08_(.*)T_.*_R([12])_.*.fastq.gz'], prefix='NS_GBM', tag='01', dType='C', sType='RSq') #559
#link_fq('/EQL2/SGI_20140204/RNASeq/fastq', '/EQL2/SGI_20140204/RNASeq/fastq/link', ['IRCR.*_(.*)T1_.*_R([12]).fastq.gz'], prefix='IRCR_GBM', tag='L', dType='T', sType='RSq') #352
#link_fq('/EQL2/SGI_20140204/RNASeq/fastq', '/EQL2/SGI_20140204/RNASeq/fastq/link', ['IRCR.*_(.*)T2_.*_R([12]).fastq.gz'], prefix='IRCR_GBM', tag='R', dType='T', sType='RSq') #352
#link_fq('/EQL2/SGI_20140204/WXS/fastq', '/EQL2/SGI_20140204/WXS/fastq/link', ['IRCR_GBM.*_(.*)T1_.*_R([12]).fastq.gz'], prefix='IRCR_GBM', tag='L', dType='T', sType='SS')
#link_fq('/EQL2/SGI_20140204/WXS/fastq', '/EQL2/SGI_20140204/WXS/fastq/link', ['IRCR_GBM.*_(.*)T2_.*_R([12]).fastq.gz'], prefix='IRCR_GBM', tag='R', dType='T', sType='SS')
#link_l('/EQL2/SGI_20140204/WXS/fastq', '/EQL2/SGI_20140204/WXS/fastq/link', ['IRCR_B_GBM.*_(.*)_[ACGT]{6}_R([12]).fastq.gz'], normalL=['352'])
#link_l('/EQL2/SGI_20140210/WXS/fastq', '/EQL2/SGI_20140210/WXS/fastq/link', ['(.{2})_[ACGT]{6}_R([12]).fastq.gz','B_NS.{2}_(.*)T_[ACGT]{6}_R([12]).fastq.gz','IRCR_B_GBM.{2}_(.*)T_[ACGT]{6}_R([12]).fastq.gz'], normalL=['320','388','470','585','783','334','335'])
#link_l('/EQL2/SGI_20140219/RNASeq/fastq','/EQL2/SGI_20140219/RNASeq/fastq/link', ['.*_([0-9]{3})[TAB]+_[ACGT]{6}_R([12]).fastq.gz'], RSQ=True)
#link_l('/EQL2/SGI_20140219/WXS/fastq','/EQL2/SGI_20140219/WXS/fastq/link', ['B_.+_(.*)T_.*_R([12]).fastq.gz'], normalL=['503','633','750'])
#link_l('/EQL2/SGI_20140219/WXS/fastq','/EQL2/SGI_20140219/WXS/fastq/link',['IRCR_GBM13_(.*)T_[ACGT]{6}_R([12]).fastq.gz','NS0._([0-9]{3}).*_[ACGT]{6}_R([12]).fastq.gz'])
#link_fq('/EQL6/RC85_LC195/fastq/SCS_RM', '/EQL6/RC85_LC195/fastq/SCS_RM/link', ['RM1(.*)_[ACGT]{8}-[ACGT]{8}_R([12]).fastq.gz'], prefix='LC', sid='195', tag='1', dType='S', sType='RSq')
#link_fq('/EQL6/RC85_LC195/fastq/SCS_RM', '/EQL6/RC85_LC195/fastq/SCS_RM/link', ['RM2(.*)_[ACGT]{8}-[ACGT]{8}_R([12]).fastq.gz'], prefix='LC', sid='195', tag='2', dType='S', sType='RSq')
#link_fq('/EQL6/RC85_LC195/fastq/SCS_RMX', '/EQL6/RC85_LC195/fastq/SCS_RMX/link', ['RMX_(.*)_[ACGT]{8}-[ACGT]{8}_R([12]).fastq.gz'], prefix='LC', sid='195', tag='X_', dType='S', sType='RSq')
#link_fq('/EQL6/RC85_LC195/fastq/SCS_RX', '/EQL6/RC85_LC195/fastq/SCS_RX/link', ['RX_(.*)_[ACGT]{8}-[ACGT]{8}_R([12]).fastq.gz'], prefix='RCC', sid='085', tag='X_', dType='S', sType='RSq')
#link_l('/EQL2/SGI_20140331/WXS/fastq','/EQL2/SGI_20140331/WXS/fastq/link', ['IRCR_B_GBM13_(.*)T_[ACGT]{6}_R([12]).fastq.gz'], normalL=['316','317','363'])
#link_l('/EQL2/SGI_20140331/WXS/fastq','/EQL2/SGI_20140331/WXS/fastq/link', ['IRCR_GBM13_(.*)T_[ACGT]{6}_R([12]).fastq.gz'])
#link_l('/EQL2/SGI_20140331/RNASeq/fastq','/EQL2/SGI_20140331/RNASeq/fastq/link', ['IRCR_GBM13_(.*)T2_[ACGT]{6}_R([12]).fastq.gz'], RSQ=True)
#link_l('/EQL2/SGI_20140410/WXS/fastq','/EQL2/SGI_20140410/WXS/fastq/link', ['(.*)_T2.*_R([12]).fastq.gz'])
#link_cs('/EQL2/CS_20140327/WXS/fastq','/EQL2/CS_20140327/WXS/fastq/link', '/EQL2/CS_20140327/filelist.txt')
#link_l('/EQL2/SGI_20140411/WXS/fastq','/EQL2/SGI_20140411/WXS/fastq/link', ['IRCR_GBM13_(.*)T_.*R([12])_merged.fastq.gz'])
#link_fq('/EQL6/SGI_20140422_singlecell/RNASeq/fastq','/EQL6/SGI_20140422_singlecell/RNASeq/fastq/link', ['GBM412T_(.*)_[ACGT]{8}-[ACGT]{8}_R([12]).fastq.gz'], prefix='IRCR_GBM', sid='412', tag='1_', dType='S', sType='RSq')
#link_cs('/EQL2/CS_20140430/WXS/fastq','/EQL2/CS_20140430/WXS/fastq/link', '/EQL2/CS_20140430/filelist.txt')
#link_cs('/EQL2/CS_20140512/WXS/fastq','/EQL2/CS_20140512/WXS/fastq/link', '/EQL2/CS_20140512/filelist.txt')
#link_cs('/EQL2/CS_20140513/WXS/fastq','/EQL2/CS_20140513/WXS/fastq/link', '/EQL2/CS_20140513/filelist.txt')
#link_cs('/EQL2/CS_20140519/WXS/fastq','/EQL2/CS_20140519/WXS/fastq/link', '/EQL2/CS_20140519/filelist.txt')
#link_l('/EQL2/SGI_20140520/RNASeq/fastq','/EQL2/SGI_20140520/RNASeq/fastq/link',['(.*)T_[ACGT]{6}_R([12]).fastq.gz'],RSQ=True, prefix='')
#sidL = map(lambda x: 'CS11_14_00%03d' % int(x), range(93,113))
#link_l('/EQL2/CS_HAPMAP/WXS/fastq','/EQL2/CS_HAPMAP/WXS/fastq/link',['(.*)_[ACGT]{8}_R([12]).fastq.gz'],prefix='',normalL=sidL)
#link_fqgz('/EQL2/SGI_20140526/WXS/fastq','/EQL2/SGI_20140526/WXS/fastq/link',patFileName='/EQL2/SGI_20140526/filelist.txt')
#link_fqgz('/EQL2/SGI_20140526/RNASeq/fastq','/EQL2/SGI_20140526/RNASeq/fastq/link',patFileName='/EQL2/SGI_20140526/filelist.txt')
#link_fqgz('/EQL2/SGI_20140428/WXS/fastq', '/EQL2/SGI_20140428/WXS/fastq/link',patFileName='/EQL2/SGI_20140428/filelist.txt')
#link_cs('/EQL2/CS_20140526/WXS/fastq','/EQL2/CS_20140526/WXS/fastq/link','/EQL2/CS_20140526/filelist.txt')
#link_fqgz('/EQL2/SGI_20140526/RNASeq/fastq','/EQL2/SGI_20140526/RNASeq/fastq/link',patFileName='/EQL2/SGI_20140526/filelist2.txt')
#link_fqgz('/EQL2/SGI_20140529/WXS/fastq','/EQL2/SGI_20140529/WXS/fastq/link',patFileName='/EQL2/SGI_20140529/filelist.txt')
#link_fqgz('/EQL2/SGI_20140602/RNASeq/fastq', '/EQL2/SGI_20140602/RNASeq/fastq/link',patFileName='/EQL2/SGI_20140602/filelist.txt')
#link_fqgz('/EQL2/SGI_20140602/WXS/fastq', '/EQL2/SGI_20140602/WXS/fastq/link',patFileName='/EQL2/SGI_20140602/filelist.txt')
#link_fqgz('/EQL2/SGI_20140611/WXS/fastq', '/EQL2/SGI_20140611/WXS/fastq/link',patFileName='/EQL2/SGI_20140611/filelist.txt')
#link_cs('/EQL2/CS_20140613/WXS/fastq', '/EQL2/CS_20140613/WXS/fastq/link','/EQL2/CS_20140613/filelist.txt')
#link_fqgz('/EQL2/SGI_20140617/WXS/fastq', '/EQL2/SGI_20140617/WXS/fastq/link', patFileName='/EQL2/SGI_20140617/filelist.txt')
#link_cs('/EQL2/CS_20140618/WXS/fastq', '/EQL2/CS_20140618/WXS/fastq/link','/EQL2/CS_20140618/filelist.txt')
#link_fqgz('/EQL2/SGI_20140620/RNASeq/fastq', '/EQL2/SGI_20140620/RNASeq/fastq/link', patFileName='/EQL2/SGI_20140620/filelist.txt', isCS=False)
#link_fqgz('/EQL2/CS_20140623/WXS/fastq', '/EQL2/CS_20140623/WXS/fastq/link',patFileName='/EQL2/CS_20140623/filelist.txt',isCS=True)
#link_fqgz('/EQL2/SGI_20140625/WXS/fastq', '/EQL2/SGI_20140625/WXS/fastq/link',patFileName='/EQL2/SGI_20140625/filelist.txt',isCS=False)
#link_fqgz('/EQL2/CS_20140702/WXS/fastq', '/EQL2/CS_20140702/WXS/fastq/link',patFileName='/EQL2/CS_20140702/filelist.txt',isCS=True)
#link_fqgz('/EQL2/SGI_20140702/RNASeq/fastq', '/EQL2/SGI_20140702/RNASeq/fastq/link',patFileName='/EQL2/SGI_20140702/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20140707/WXS/fastq', '/EQL2/SGI_20140707/WXS/fastq/link',patFileName='/EQL2/SGI_20140707/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20140710/RNASeq/fastq', '/EQL2/SGI_20140710/RNASeq/fastq/link',patFileName='/EQL2/SGI_20140710/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20140714/WXS/fastq', '/EQL2/SGI_20140714/WXS/fastq/link',patFileName='/EQL2/SGI_20140714/filelist.txt',isCS=False)
#link_fqgz('/EQL2/CS_20140714/WXS/fastq', '/EQL2/CS_20140714/WXS/fastq/link',patFileName='/EQL2/CS_20140714/filelist.txt',isCS=True)
#link_fqgz('/EQL2/SGI_20140716/RNASeq/fastq', '/EQL2/SGI_20140716/RNASeq/fastq/link',patFileName='/EQL2/SGI_20140716/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20140721/WXS/fastq', '/EQL2/SGI_20140721/WXS/fastq/link',patFileName='/EQL2/SGI_20140721/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20140723/RNASeq/fastq', '/EQL2/SGI_20140723/RNASeq/fastq/link',patFileName='/EQL2/SGI_20140723/filelist.txt',isCS=False)
#link_fqgz('/EQL2/CS_20140728/WXS/fastq', '/EQL2/CS_20140728/WXS/fastq/link',patFileName='/EQL2/CS_20140728/filelist.txt',isCS=True)
#link_fqgz('/EQL2/SGI_20140728/WXS/fastq', '/EQL2/SGI_20140728/WXS/fastq/link',patFileName='/EQL2/SGI_20140728/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20140804/WXS/fastq', '/EQL2/SGI_20140804/WXS/fastq/link',patFileName='/EQL2/SGI_20140804/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20140804/RNASeq/fastq', '/EQL2/SGI_20140804/RNASeq/fastq/link',patFileName='/EQL2/SGI_20140804/filelist.txt',isCS=False)
#link_fqgz('/EQL2/CS_20140805/WXS/fastq', '/EQL2/CS_20140805/WXS/fastq/link',patFileName='/EQL2/CS_20140805/filelist.txt',isCS=True)
#link_fqgz('/EQL2/SGI_20140807/WXS/fastq', '/EQL2/SGI_20140807/WXS/fastq/link',patFileName='/EQL2/SGI_20140807/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20140811/WXS/fastq', '/EQL2/SGI_20140811/WXS/fastq/link',patFileName='/EQL2/SGI_20140811/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20140811/RNASeq/fastq', '/EQL2/SGI_20140811/RNASeq/fastq/link',patFileName='/EQL2/SGI_20140811/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20140813/WXS/fastq', '/EQL2/SGI_20140813/WXS/fastq/link',patFileName='/EQL2/SGI_20140813/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20140818/WXS/fastq', '/EQL2/SGI_20140818/WXS/fastq/link',patFileName='/EQL2/SGI_20140818/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20140818/RNASeq/fastq', '/EQL2/SGI_20140818/RNASeq/fastq/link',patFileName='/EQL2/SGI_20140818/filelist.txt',isCS=False)
#link_fqgz('/EQL2/CS_20140819/WXS/fastq', '/EQL2/CS_20140819/WXS/fastq/link',patFileName='/EQL2/CS_20140819/filelist.txt',isCS=True)
#link_fqgz('/EQL2/SGI_20140821/RNASeq/fastq', '/EQL2/SGI_20140821/RNASeq/fastq/link',patFileName='/EQL2/SGI_20140821/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20140825/WXS/fastq', '/EQL2/SGI_20140825/WXS/fastq/link',patFileName='/EQL2/SGI_20140825/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20140827/WXS/fastq', '/EQL2/SGI_20140827/WXS/fastq/link',patFileName='/EQL2/SGI_20140827/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20140829/RNASeq/fastq', '/EQL2/SGI_20140829/RNASeq/fastq/link',patFileName='/EQL2/SGI_20140829/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20140901/WXS/fastq', '/EQL2/SGI_20140901/WXS/fastq/link',patFileName='/EQL2/SGI_20140901/filelist.txt',isCS=False)
#link_fqgz('/EQL2/CS_20140828/WXS/fastq', '/EQL2/CS_20140828/WXS/fastq/link',patFileName='/EQL2/CS_20140828/filelist.txt',isCS=True)
#link_fqgz('/EQL2/SGI_20140904/WXS/fastq', '/EQL2/SGI_20140904/WXS/fastq/link',patFileName='/EQL2/SGI_20140904/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20140904/RNASeq/fastq', '/EQL2/SGI_20140904/RNASeq/fastq/link',patFileName='/EQL2/SGI_20140904/filelist.txt',isCS=False)
#link_fqgz('/EQL2/CS_20140904/WXS/fastq', '/EQL2/CS_20140904/WXS/fastq/link',patFileName='/EQL2/CS_20140904/filelist.txt',isCS=True)
#link_fqgz('/EQL2/SGI_20140917/WXS/fastq', '/EQL2/SGI_20140917/WXS/fastq/link',patFileName='/EQL2/SGI_20140917/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20140922/RNASeq/fastq', '/EQL2/SGI_20140922/RNASeq/fastq/link',patFileName='/EQL2/SGI_20140922/filelist.txt',isCS=False)
#link_fqgz('/EQL2/CS_20140924/WXS/fastq', '/EQL2/CS_20140924/WXS/fastq/link',patFileName='/EQL2/CS_20140924/filelist.txt',isCS=True)
#link_fqgz('/EQL10/SignetRingCell_WTS', '/EQL10/SignetRingCell_WTS/link',patFileName='/EQL10/SignetRingCell_WTS/f', isCS=False)
#link_fqgz('/EQL10/Young_CRC_WTS', '/EQL10/Young_CRC_WTS/link',patFileName='/EQL10/Young_CRC_WTS/f', isCS=False)
#link_fqgz('/EQL2/SGI_20140930/RNASeq/fastq', '/EQL2/SGI_20140930/RNASeq/fastq/link',patFileName='/EQL2/SGI_20140930/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20140930/WXS/fastq', '/EQL2/SGI_20140930/WXS/fastq/link',patFileName='/EQL2/SGI_20140930/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20140930_NSC/WXS/fastq', '/EQL2/SGI_20140930_NSC/WXS/fastq/link',patFileName='/EQL2/SGI_20140930_NSC/filelist.txt',isCS=False)
#link_fqgz('/EQL2/CS_20141007/WXS/fastq', '/EQL2/CS_20141007/WXS/fastq/link',patFileName='/EQL2/CS_20141007/filelist.txt',isCS=True)
#link_fqgz('/EQL2/SGI_20141001/WXS/fastq', '/EQL2/SGI_20141001/WXS/fastq/link',patFileName='/EQL2/SGI_20141001/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20141008/WXS/fastq', '/EQL2/SGI_20141008/WXS/fastq/link',patFileName='/EQL2/SGI_20141008/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20141013/RNASeq/fastq', '/EQL2/SGI_20141013/RNASeq/fastq/link',patFileName='/EQL2/SGI_20141013/filelist.txt',isCS=False)
#link_fqgz('/EQL2/CS_20141015/WXS/fastq', '/EQL2/CS_20141015/WXS/fastq/link',patFileName='/EQL2/CS_20141015/filelist.txt',isCS=True)
#link_fqgz('/EQL2/SGI_20141021/RNASeq/fastq', '/EQL2/SGI_20141021/RNASeq/fastq/link',patFileName='/EQL2/SGI_20141021/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20141021/WXS/fastq', '/EQL2/SGI_20141021/WXS/fastq/link',patFileName='/EQL2/SGI_20141021/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20141027/RNASeq/fastq', '/EQL2/SGI_20141027/RNASeq/fastq/link',patFileName='/EQL2/SGI_20141027/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20141027/WXS/fastq', '/EQL2/SGI_20141027/WXS/fastq/link',patFileName='/EQL2/SGI_20141027/filelist.txt',isCS=False)
#link_fqgz('/EQL2/CS_20141030/WXS/fastq', '/EQL2/CS_20141030/WXS/fastq/link',patFileName='/EQL2/CS_20141030/filelist.txt',isCS=True)
#link_fqgz('/EQL2/SGI_20141031/RNASeq/fastq', '/EQL2/SGI_20141031/RNASeq/fastq/link',patFileName='/EQL2/SGI_20141031/filelist.txt',isCS=False)
#link_fqgz('/EQL2/CS_20141022/WXS/fastq', '/EQL2/CS_20141022/WXS/fastq/link',patFileName='/EQL2/CS_20141022/filelist.txt',isCS=True)
#link_fqgz('/EQL2/SGI_20141103/RNASeq/fastq', '/EQL2/SGI_20141103/RNASeq/fastq/link',patFileName='/EQL2/SGI_20141103/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20141103/WXS/fastq', '/EQL2/SGI_20141103/WXS/fastq/link',patFileName='/EQL2/SGI_20141103/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20141110/WXS/fastq', '/EQL2/SGI_20141110/WXS/fastq/link',patFileName='/EQL2/SGI_20141110/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20141112/WXS/fastq', '/EQL2/SGI_20141112/WXS/fastq/link',patFileName='/EQL2/SGI_20141112/filelist.txt',isCS=False)
#link_fqgz('/EQL2/CS_20141112/WXS/fastq', '/EQL2/CS_20141112/WXS/fastq/link',patFileName='/EQL2/CS_20141112/filelist.txt',isCS=True)
#link_fqgz('/EQL2/SGI_20141117/RNASeq/fastq', '/EQL2/SGI_20141117/RNASeq/fastq/link',patFileName='/EQL2/SGI_20141117/filelist.txt',isCS=False)
#link_fqgz('/EQL2/CS_20141126/WXS/fastq', '/EQL2/CS_20141126/WXS/fastq/link',patFileName='/EQL2/CS_20141126/filelist.txt',isCS=True)
#link_fqgz('/EQL2/SGI_20141126/WXS/fastq', '/EQL2/SGI_20141126/WXS/fastq/link',patFileName='/EQL2/SGI_20141126/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20141126/RNASeq/fastq', '/EQL2/SGI_20141126/RNASeq/fastq/link',patFileName='/EQL2/SGI_20141126/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20141202/WXS/fastq', '/EQL2/SGI_20141202/WXS/fastq/link',patFileName='/EQL2/SGI_20141202/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20141202/RNASeq/fastq', '/EQL2/SGI_20141202/RNASeq/fastq/link',patFileName='/EQL2/SGI_20141202/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20141203/RNASeq/fastq', '/EQL2/SGI_20141203/RNASeq/fastq/link',patFileName='/EQL2/SGI_20141203/filelist.txt',isCS=False)
#link_fqgz('/EQL2/CS_20141210/WXS/fastq', '/EQL2/CS_20141210/WXS/fastq/link',patFileName='/EQL2/CS_20141210/filelist.txt',isCS=True)
#link_fqgz('/EQL2/SGI_20141210/WXS/fastq', '/EQL2/SGI_20141210/WXS/fastq/link',patFileName='/EQL2/SGI_20141210/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20141211/RNASeq/fastq', '/EQL2/SGI_20141211/RNASeq/fastq/link',patFileName='/EQL2/SGI_20141211/filelist.txt',isCS=False)
#link_fqgz('/EQL2/CS_20141217/WXS/fastq', '/EQL2/CS_20141217/WXS/fastq/link',patFileName='/EQL2/CS_20141217/filelist.txt',isCS=True)
#link_fqgz('/EQL2/SGI_20141218/WXS/fastq', '/EQL2/SGI_20141218/WXS/fastq/link',patFileName='/EQL2/SGI_20141218/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20141218/RNASeq/fastq', '/EQL2/SGI_20141218/RNASeq/fastq/link',patFileName='/EQL2/SGI_20141218/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20141222/RNASeq/fastq', '/EQL2/SGI_20141222/RNASeq/fastq/link',patFileName='/EQL2/SGI_20141222/filelist.txt',isCS=False)
#link_fqgz('/EQL2/CS_20141231/WXS/fastq', '/EQL2/CS_20141231/WXS/fastq/link',patFileName='/EQL2/CS_20141231/filelist.txt',isCS=True)
#link_fqgz('/EQL2/CS_20150107/WXS/fastq', '/EQL2/CS_20150107/WXS/fastq/link',patFileName='/EQL2/CS_20150107/filelist.txt',isCS=True)
#link_fqgz('/EQL2/CS_20150115/WXS/fastq', '/EQL2/CS_20150115/WXS/fastq/link',patFileName='/EQL2/CS_20150115/filelist.txt',isCS=True)
#link_fqgz('/EQL2/SGI_20150102/RNASeq/fastq', '/EQL2/SGI_20150102/RNASeq/fastq/link',patFileName='/EQL2/SGI_20150102/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20150102/WXS/fastq', '/EQL2/SGI_20150102/WXS/fastq/link',patFileName='/EQL2/SGI_20150102/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20150112/WXS/fastq', '/EQL2/SGI_20150112/WXS/fastq/link',patFileName='/EQL2/SGI_20150112/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20150115/WXS/fastq', '/EQL2/SGI_20150115/WXS/fastq/link',patFileName='/EQL2/SGI_20150115/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20150121/WXS/fastq', '/EQL2/SGI_20150121/WXS/fastq/link',patFileName='/EQL2/SGI_20150121/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20150121/RNASeq/fastq', '/EQL2/SGI_20150121/RNASeq/fastq/link',patFileName='/EQL2/SGI_20150121/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20150123/WXS/fastq', '/EQL2/SGI_20150123/WXS/fastq/link',patFileName='/EQL2/SGI_20150123/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20150128/WXS/fastq', '/EQL2/SGI_20150128/WXS/fastq/link',patFileName='/EQL2/SGI_20150128/filelist.txt',isCS=False)
#link_fqgz('/EQL2/CS_20150128/WXS/fastq', '/EQL2/CS_20150128/WXS/fastq/link',patFileName='/EQL2/CS_20150128/filelist.txt',isCS=True)
#link_fqgz('/EQL2/CS_20150204/WXS/fastq', '/EQL2/CS_20150204/WXS/fastq/link',patFileName='/EQL2/CS_20150204/filelist.txt',isCS=True)
#link_fqgz('/EQL2/SGI_20150206/WXS/fastq', '/EQL2/SGI_20150206/WXS/fastq/link',patFileName='/EQL2/SGI_20150206/filelist.txt',isCS=False)
#link_fqgz('/EQL2/SGI_20150206/RNASeq/fastq', '/EQL2/SGI_20150206/RNASeq/fastq/link',patFileName='/EQL2/SGI_20150206/filelist.txt',isCS=False)
#link_fqgz('/EQL2/CS_20150211/WXS/fastq', '/EQL2/CS_20150211/WXS/fastq/link',patFileName='/EQL2/CS_20150211/filelist.txt',isCS=True)
#link_fqgz('/EQL2/SGI_20150223/WXS/fastq', '/EQL2/SGI_20150223/WXS/fastq/link',patFileName='/EQL2/SGI_20150223/filelist.txt',isCS=False)
link_fqgz('/EQL2/SGI_20150306/RNASeq/fastq', '/EQL2/SGI_20150306/RNASeq/fastq/link',patFileName='/EQL2/SGI_20150306/filelist.txt',isCS=False)
link_fqgz('/EQL2/SGI_20150309/RNASeq/fastq', '/EQL2/SGI_20150309/RNASeq/fastq/link',patFileName='/EQL2/SGI_20150309/filelist.txt',isCS=False)
