#!/usr/bin/python

import sys, os
from glob import glob

def genSpec(baseDir):

	moduleL = ['NGS/align','NGS/mutation'] ## DIRECTORY
	homeDir = os.popen('echo $HOME','r').read().rstrip()

	for module in moduleL:
		sys.path.append('%s/JK1/%s' % (homeDir,module))

	import bwa_batch, markDuplicates_batch, realign_batch, pileup_batch ## MODULES

	return [ ## PARAMETERS
		{
		'name': 'BWA',
		'desc': 'fq -> sam -> bam -> sorted.bam',
		'fun': bwa_batch.align,
		'paramL': (baseDir, baseDir, '(.*)\.[12]\.fq', 10, 40000000000, False, 'hg19', False),
		'paramH': {},
		'logPostFix': '.bwa.qlog',
		},

		{
		'name': 'MarkDuplicate/ReadGroup',
		'desc': 'sorted.bam -> dedup.bam -> RG.bam',
		'fun': markDuplicates_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.dedup.qlog',
		},

		{
		'name': 'Realign',
		'desc': 'RG.bam -> realign.bam -> recal.bam',
		'fun': realign_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.realign.qlog',
		},

		{
		'name': 'Pileup',
		'desc': 'recal.bam -> pileup',
		'fun': pileup_batch.main,
		'paramL': (baseDir, baseDir, False),
		'paramH': {},
		'logPostFix': '.pileup.log',
		},

		]

## SYSTEM CONFIGURATION

storageBase = '/pipeline/'

apacheBase = '/var/www/html/pipeline/'

inputFileFmt = 'fq'

def printLog_execute(logF, fun,paramL,paramH={},stepNum=0):

	try :
		logF.write('<b> Step%s is starting ... </b><br>' % stepNum)
		apply(fun,paramL,paramH)
	except:
		logF.write('<b> Step%s is failed </b><br>' % stepNum)
		sys.exit()

def printLog_content(logF,baseDir,contentFileN):

	logF.write('<pre>' + ''.join(open('%s/%s' % (baseDir,contentFileN)).readlines()) + '</pre><br><br>')

def printLog_files(logF,baseDir,prevFileS):

	allFileS = set(glob(baseDir+'/*'))

	newFileL = list(allFileS.difference(prevFileS))
	newFileL.sort(lambda x,y: cmp(x,y))

	for i in range(len(newFileL)):
		logF.write('-- %s. %s<br>' % (i+1, newFileL[i]))
	logF.write('<hr>')

	return allFileS


def main(inputFilePre, projectN='test', sampN=''):

	if not sampN:
		sampN = inputFilePre.split('/')[-1]

	# HTML log file initiation

	logFileN = '%s/%s/%s.html' % (apacheBase,projectN,sampN)
	logF = open(logFileN, 'w', 0)
	os.system('chmod a+rw %s' % logFileN)

	logF.write('<DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"><html><head></head><body>')

	# creating sample data directory and linking input file

	baseDir = '%s/%s/%s' % (storageBase,projectN,sampN)

	if glob(baseDir):
		logF.write('<b> %s already exists </b></br>' % baseDir)
	else:
		ret1 = os.system('mkdir '+baseDir )

		if ret1 != 0:
			logF.write('<b> failed to created sample directory </b><br>')
			sys.exit()

		logF.write('<b> created sample directory </b></br>')

	ret2_1 = os.system('ln -f -s %s.1.%s %s/%s.1.%s' % (inputFilePre,inputFileFmt,baseDir,sampN,inputFileFmt))
	ret2_2 = os.system('ln -f -s %s.2.%s %s/%s.2.%s' % (inputFilePre,inputFileFmt,baseDir,sampN,inputFileFmt))

	if ret2_1!=0 or ret2_2!=0:
		logF.write('<b> failed to link input file</b><br>')
		sys.exit(1)

	logF.write('<b> linked input files </b></br>')
	prevFileS = printLog_files(logF,baseDir,set([]))

	# Step 1-N

	specL = genSpec(baseDir)

	for i in range(len(specL)):

		printLog_execute(logF, specL[i]['fun'], specL[i]['paramL'], specL[i]['paramH'], i+1)

		printLog_content(logF,baseDir,'%s%s' % (sampN,specL[i]['logPostFix']))

		logF.write('<b>files: </b><br>')
		prevFileS = printLog_files(logF,baseDir,prevFileS)

	logF.close()


if __name__ == '__main__':
	main('/home/yenakim/YN/linked_fq/S780_T_SS/S780_T_SS')
