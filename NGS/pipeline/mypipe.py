#!/usr/bin/python

import sys, os
from glob import glob


## SYSTEM CONFIGURATION

storageBase = '/pipeline/'
apacheBase = '/var/www/html/pipeline/'

def fn_mkdir(logF,baseDir):

	logF.write('<p><b>Directory: </b>')

	logF.write('<br>' + baseDir.replace('//','/'))

	if glob(baseDir):
		logF.write(' already exists')
	else:
		ret = os.system('mkdir '+baseDir )

		if ret != 0:
			logF.write(' failed to be created')
			sys.exit(1)

		logF.write(' created')

	os.system('chmod a+rw '+baseDir)

def fn_ln(logF,baseDir,inputFilePathL,sampN):

	logF.write('<p><b>Input link files: </b>')

	for inputFileP in inputFilePathL:

		inputFileN = inputFileP.split('/')[-1]
		logF.write('<br>' + inputFileN)

		if glob('%s/%s' % (baseDir,inputFileN)):
			logF.write(' already exists')
		else:
			ret = os.system('ln -f -s %s %s/%s' % (inputFileP,baseDir,inputFileN))

			if ret!=0:
				logF.write(' failed to be created')
				sys.exit(1)

			logF.write(' created')

	logF.write('</p>')

def fn_exists(logF,baseDir,contentFileN,logExistsFn,outFilePostFix):

	resultFileOK = True

	for postFix in outFilePostFix:
		outFileNL = glob('%s/*.%s' % (baseDir,postFix))
		if len(outFileNL)!=1 or os.path.getsize(outFileNL[0])==0:
			resultFileOK = False
			break

	if glob('%s/%s' % (baseDir,contentFileN)):
		qlogFileOK = logExistsFn(open('%s/%s' % (baseDir,contentFileN)).readlines())
	else:
		qlogFileOK = False

	verdict = resultFileOK and qlogFileOK

	logF.write('<p><b>Execution: </b>')

	if verdict:
		logF.write('previously completed</p>')
	else:
		logF.write('running')
		if not resultFileOK:
			logF.write(' (result file not found or not integral)')
		if not qlogFileOK:
			logF.write(' (qlog file not found or not integral)')
		logF.write('</p>')

	return verdict

def fn_execute(logF, fn, paramL,paramH={},stepNum=0):

	apply(fn,paramL,paramH)

def fn_content(logF,baseDir,contentFileN):

	logF.write('<p><b>Log:</b>')
	logF.write('<pre>' + ''.join(open('%s/%s' % (baseDir,contentFileN)).readlines()) + '</pre></p>')

def fn_results(logF):

	logF.write('<p><b>Result files:</b><br>')

def fn_files(logF,baseDir,prevFileS):

	logF.write('<p><b>New files:</b><br>')

	allFileS = set(glob(baseDir+'/*'))

	newFileL = list(allFileS.difference(prevFileS))
	newFileL.sort(lambda x,y: cmp(x,y))

	for i in range(len(newFileL)):
		logF.write('-- %s. %s<br>' % (i+1, newFileL[i].split('/')[-1]))

	logF.write('</p>')

	return allFileS


def main(inputFilePathL, genSpecFn, sampN, projectN='test', clean=False):

	# HTML log file initiation

	logFileN = '%s/%s/%s.html' % (apacheBase,projectN,sampN)
	logF = open(logFileN, 'w', 0)
	os.system('chmod a+rw %s' % logFileN)

	logF.write('<DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"><html><head></head><body>')

	# creating sample data directory and linking input file

	baseDir = '%s/%s/%s' % (storageBase,projectN,sampN)

	logF.write('<h2>%s, %s</h2>' % (projectN,sampN))
	logF.write('<hr><b>Step 0: Set-up</b><hr>')

	fn_mkdir(logF,baseDir)

	fn_ln(logF,baseDir,inputFilePathL,sampN)

	prevFileS = fn_files(logF,baseDir,set([]))

	# Step 1-N

	execute = False
	specL = genSpecFn(baseDir)

	for i in range(len(specL)):

		contentFileN = '%s.%s' % (sampN,specL[i]['logPostFix'])

		logF.write('<hr><b>Step %s: %s: %s</b><hr>' % (i+1,specL[i]['name'],specL[i]['desc']))

		if execute or not fn_exists(logF, baseDir, contentFileN, specL[i]['logExistsFn'], specL[i]['outFilePostFix']):
			fn_execute(logF, specL[i]['fun'], specL[i]['paramL'], specL[i]['paramH'], i+1)
			execute = True

		fn_content(logF,baseDir,contentFileN)

		fn_results(logF)
		prevFileS = fn_files(logF,baseDir,prevFileS)

	logF.close()