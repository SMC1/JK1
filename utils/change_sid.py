#!/usr/bin/python

import sys, os, re

fPatternH = {'rsq2expr': ['_RSq.rpkm'],
		'rsq2mut': ['_RSq_splice_cosmic.dat'],
		'rsq2eiJunc': ['_RSq_ei.dat'],
		'rsq2fusion': ['_RSq_splice_transloc_annot1.report.txt','_RSq_splice_transloc_annot1.report_annot.txt'],
		'rsq2skip': ['_RSq_splice_exonSkip_normal_report.txt','_RSq_splice_exonSkip_report.txt','_RSq_splice_exonSkip_report_annot.txt'],
		'xsq2mut':['_T_SS_cosmic.dat']}

def change_file(old_ID, new_ID, dirName):
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

def change_output(old_ID, new_ID, dirN, pType):
	inputL = filter(lambda x: new_ID in x and os.path.isdir('%s/%s' % (dirN,x)), os.listdir(dirN))
	for input in inputL:
		for pattern in fPatternH[pType]:
			file = '%s/%s/%s%s' % (dirN,input, new_ID, pattern)
			if os.path.isfile(file):
				print file
				if pType[:3] == 'rsq':
					cmd = "sed -i -e 's/%s_RSq/%s_RSq/g' %s" % (old_ID,new_ID, file)
				else:
					cmd = "sed -i -e 's/%s_T_SS/%s_T_SS/g' %s" % (old_ID,new_ID, file)
				print cmd
				os.system(cmd)
		

def change_sid(old, new, dirN, pType):
	change_file(old, new, dirN)
	change_output(old, new, dirN, pType)

#change_sid('S633B', 'S633', '/EQL3/pipeline/SGI20131226_rsq2expr', 'rsq2expr')
#change_sid('S633B', 'S633', '/EQL3/pipeline/SGI20131226_rsq2mut', 'rsq2mut')
#change_sid('S633B', 'S633', '/EQL3/pipeline/SGI20131226_rsq2eiJunc', 'rsq2eiJunc')
#change_sid('S633B', 'S633', '/EQL3/pipeline/SGI20131226_rsq2fusion', 'rsq2fusion')
#change_sid('S633B', 'S633', '/EQL3/pipeline/SGI20131226_rsq2skip', 'rsq2skip')
#change_sid('S633B', 'S633', '/EQL3/pipeline/SGI20140103_xsq2mut', 'xsq2mut')
#change_sid('S633A', 'S633_2', '/EQL2/pipeline/SGI20140128_xsq2mut', 'xsq2mut')
#change_sid('S317', 'S317_2', '/EQL3/pipeline/SGI20140331_xsq2mut', 'xsq2mut')
#change_sid('NCI_GBM_827', 'S827', '/EQL3/pipeline/SGI20140526_rsq2expr', 'rsq2expr')
change_sid('NCI_GBM_827', 'S827', '/EQL3/pipeline/SGI20140526_rsq2mut', 'rsq2mut')
change_sid('NCI_GBM_827', 'S827', '/EQL3/pipeline/SGI20140526_rsq2eiJunc', 'rsq2eiJunc')
change_sid('NCI_GBM_827', 'S827', '/EQL3/pipeline/SGI20140526_rsq2fusion', 'rsq2fusion')
change_sid('NCI_GBM_827', 'S827', '/EQL3/pipeline/SGI20140526_rsq2skip', 'rsq2skip')
