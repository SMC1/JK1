#!/usr/bin/python

import sys, os, datetime, re
import mysetting
from glob import glob


## SYSTEM CONFIGURATION

storageBase = '/pipeline/'
storageBase = '/EQL7/pipeline/'
#storageBase = '/EQL2/pipeline/'
#apacheBase = '/var/www/html/pipeline/'
#apacheBase = '/var/www/html/pipeline2/'
apacheBase = '/EQL7/pipeline/'
#apacheBase = '/EQL2/pipeline/'

def prepare_baseDir(projectN, mkdir=True):
	global storageBase, apacheBase
	if projectN in ['CNA','CNA_corr','Purity','Clonality']:
		storageBase = '/EQL3/pipeline/'
		apacheBase = '/EQL3/pipeline/'
	elif projectN in ['test_cs2mut']:
		storageBase = '/EQL2/pipeline/'
		apacheBase = '/EQL2/pipeline/'
	elif projectN in ['CS_mut','CS_CNA']: ## cancerSCAN
		storageBase = '/EQL5/pipeline/'
		apacheBase = '/EQL5/pipeline/'
	elif 'rsq2' in projectN: ## RNASeq
		storageBase = '/EQL8/pipeline/'
		apacheBase = '/EQL8/pipeline/'
	elif 'xsq2' in projectN: ## WES
		storageBase = '/EQL7/pipeline/'
		apacheBase = '/EQL7/pipeline/'
	
	if mkdir:
		if glob(storageBase+projectN):
			print ('File directory: already exists')
		else:
			os.system('mkdir %s/%s; chmod a+w %s/%s' % (storageBase,projectN, storageBase,projectN))
			print ('File directory: created')
	
		if glob(apacheBase+projectN):
			print ('Log directory: already exists')
		else:
			os.system('mkdir %s/%s; chmod a+w %s/%s' % (apacheBase,projectN, apacheBase,projectN))
			print ('Log directory: created')

	return(storageBase+projectN)

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
			if ret == 0 and inputFileN.rstrip()[-3:] == 'bam':
				os.system('ln -f -s %s %s/%s' % (re.match('(.*)\.bam', inputFileP).group(1)+'.bai', baseDir,re.match('(.*)\.bam', inputFileN).group(1)+'.bai'))

			if ret!=0:
				logF.write(' failed to be created')
				sys.exit(1)

			logF.write(' created')

	logF.write('</p>')

def fn_exists(logF,baseDir,contentFileN,logExistsFn,outFilePostFix,reRun):

	resultFileOK = True

	for postFix in outFilePostFix:
		outFileNL = glob('%s/*%s' % (baseDir,postFix))
		if len(outFileNL)<1 or os.path.getsize(outFileNL[0])==0:
			resultFileOK = False
			break

	if glob('%s/%s' % (baseDir,contentFileN)):
		qlogFileOK = logExistsFn(open('%s/%s' % (baseDir,contentFileN)).readlines())
	else:
		qlogFileOK = False

	verdict = resultFileOK and qlogFileOK

	logF.write('<p><b>Execution: </b>')
	
	if verdict and not reRun:
		logF.write('previously completed</p>')
	elif verdict and reRun:
		logF.write('re-running</p>')
	else:
		logF.write('running')
		if not resultFileOK:
			logF.write(' (result file not found or not integral)')
		if not qlogFileOK:
			logF.write(' (qlog file not found or not integral)')
		logF.write('</p>')

	return verdict

def fn_execute(logF, fn, paramL,paramH={}, stepNum=0):

	apply(fn,paramL,paramH)

def fn_content(logF,baseDir,contentFileN):

	logF.write('<p><b>Log:</b>')
	logF.write('<div class="log_box" style="height:400px;width:65%;border:1px solid #ccc;overflow:auto;">')
	logF.write('<pre>' + ''.join(open('%s/%s' % (baseDir,contentFileN)).readlines()) + '</pre></p>')
	logF.write('</div>')

def fn_results(logF, baseDir, outFilePostFix):
	
	logF.write('<p><b>Result files:</b><br>')

	for postFix in outFilePostFix:
		outFileNL = glob('%s/*%s' % (baseDir, postFix))
#		if len(outFileNL) == -1 or os.path.getsize(outFileNL[0]) != 0:
		if len(outFileNL) > 0:
			for outFileN in outFileNL:
				sizeF = (float(os.path.getsize(outFileN)))/(1024*1024)
				creationD = datetime.datetime.fromtimestamp(os.path.getmtime(outFileN)).replace(microsecond=0)
				logF.write('-- %s , %s (%.3f MB) <br>' % (creationD, outFileN.split('/')[-1], sizeF))

def fn_links(logF, projectN, baseDir, outLinkPostFix):
	for postFix in outLinkPostFix:
		outLinkNL = glob('%s/*%s' % (baseDir, postFix))
		for outLinkN in outLinkNL:
			if os.path.getsize(outLinkN) != 0:
				creationD = datetime.datetime.fromtimestamp(os.path.getmtime(outLinkN)).replace(microsecond=0)
				logF.write('-- %s, <a href="./%s">%s</a> <br>' % (creationD, outLinkN[len(storageBase + projectN)+1:], outLinkN[len(baseDir)+1:]))
#				logF.write('-- %s, <a href="./%s">%s</a> <br>' % (creationD, outLinkN[len(apacheBase+projectN)+1:], outLinkN[len(apacheBase+projectN)+1:] ))

def fn_files(logF,baseDir,prevFileS):

	logF.write('<p><b>New files:</b><br>')

	allFileS = set(glob(baseDir+'/*'))

	newFileL = list(allFileS.difference(prevFileS))
	newFileL.sort(lambda x,y: cmp(x,y))

	for i in range(len(newFileL)):
		sizeF = (float(os.path.getsize(newFileL[i])))/(1024*1024)
		logF.write('-- %s. %s (%.3f MB) <br>' % (i+1, newFileL[i].split('/')[-1], sizeF))

	logF.write('</p>')

	return allFileS

def fn_clean(baseDir, prevFileS, logPostFix, outFilePostFix):
	
	allFileS = set(glob(baseDir+'/*'))
	newFileL = list(allFileS.difference(prevFileS))
	newFileL.sort(lambda x,y: cmp(x,y))

	for i in range(len(newFileL)):
		for postFix in outFilePostFix:
			if not (logPostFix in newFileL[i].split('/')[-1] or postFix in newFileL[i].split('/')[-1]):
				os.system('rm %s' % newFileL[i])

def main(inputFilePathL, genSpecFn, sampN, projectN='test_yn', clean=False, server='smc1', genome='hg19'):

	## adjust storageBase/apacheBase depending on project(CNA, CNA_corr, Purity, Clonality)
	prepare_baseDir(projectN, mkdir=False)

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
	specL = genSpecFn(baseDir, server, genome)

	for i in range(len(specL)):
		startTime = datetime.datetime.now().replace(microsecond=0)

		contentFileN = '%s%s' % (sampN,specL[i]['logPostFix'])

		logF.write('<hr><b>Step %s: %s: %s</b><hr>' % (i+1,specL[i]['name'],specL[i]['desc']))
		
		if execute or not fn_exists(logF, baseDir, contentFileN, specL[i]['logExistsFn'], specL[i]['outFilePostFix'], specL[i]['rerun']) or specL[i]['rerun']:
			fn_execute(logF, specL[i]['fun'], specL[i]['paramL'], specL[i]['paramH'], i+1)
			if specL[i]['clean']:
				 fn_clean(baseDir, prevFileS, specL[i]['logPostFix'], specL[i]['outFilePostFix'])

			execute = True

		fn_content(logF,baseDir,contentFileN)

		fn_results(logF, baseDir, specL[i]['outFilePostFix'])
		if 'outLinkPostFix' in specL[i]:
			fn_links(logF, projectN, baseDir, specL[i]['outLinkPostFix'])
		prevFileS = fn_files(logF,baseDir,prevFileS)
		
		endTime = datetime.datetime.now().replace(microsecond=0)
		elapsedT = (endTime - startTime)
		logF.write('<b> Step %s elapsed time : %s </b><br><br>' % (i+1, elapsedT))

	logF.close()

def read_trio(trioFileN='/EQL1/NSL/clinical/trio_info.txt', bamDirL=mysetting.wxsBamDirL):
	## trio_info.txt (tab-delimited txt)
	## column 1: trio #
	## column 2: role in trio ('Normal', 'Primary', 'Recurrent')
	## column 3: sample #
	## column 4: bam file name or standardized sample prefix
	trioF = open(trioFileN, 'r')

	trioH = {}
	for line in trioF:
		if line[0] == '#':
			continue
		cols = line.rstrip().split('\t')
		tid = cols[0]
		role = cols[1]
		sid = cols[2]
		if len(cols) > 3:
			prefix = cols[3]
		else:
			if role == 'Normal':
				prefix = 'S'+sid+'_B_SS'
			else:
				prefix = 'S'+sid+'_T_SS'
		sampFileNL = []
		for bamDir in bamDirL:
			sampFileNL += filter(lambda x: 'backup' not in x, os.popen('find %s -name %s*recal.bam' % (bamDir, prefix)).readlines())
		if tid not in trioH:
			trioH[tid] = {'prim_id':[], 'recur_id':[], 'norm_id':[], 'Normal':[], 'Primary':[], 'Recurrent':[]}
			if role == 'Primary':
				trioH[tid]['prim_id'].append(prefix)
			elif role == 'Recurrent':
				trioH[tid]['recur_id'].append(prefix)
			elif role == 'Normal':
				trioH[tid]['norm_id'].append(prefix)
			if len(sampFileNL) > 0:
				trioH[tid][role].append(sampFileNL[0].rstrip())
		else:
			if role == 'Primary':
				trioH[tid]['prim_id'].append(prefix)
			elif role == 'Recurrent':
				trioH[tid]['recur_id'].append(prefix)
			elif role == 'Normal':
				trioH[tid]['norm_id'].append(prefix)
			if len(sampFileNL) > 0:
				trioH[tid][role].append(sampFileNL[0].rstrip())
	return trioH
