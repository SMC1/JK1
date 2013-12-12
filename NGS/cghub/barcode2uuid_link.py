#!/usr/bin/python

import sys, os, re, getopt, httplib
import mybasic

def uuid2barcode(id):

	conn = httplib.HTTPSConnection('tcga-data.nci.nih.gov')
	conn.request('GET','/uuid/uuidws/mapping/json/uuid/%s' % id)
	result = conn.getresponse().read()

	return eval(result)['barcode']
	#print eval(result)['barcode']

def barcode2uuid():

	for line in sys.stdin:

		barcode = line[:-1]

		conn = httplib.HTTPSConnection('tcga-data.nci.nih.gov')
		conn.request('GET','/uuid/uuidws/mapping/json/barcode/%s' % barcode)
		result = conn.getresponse().read()

		print eval(result)['uuidMapping']['uuid']


def link(dirName,outDirName,filePattern,type):

	inputFilePL = os.popen('find %s -maxdepth 1 -name "*.2.fastq.gz"' % dirName, 'r')

	for fileP in inputFilePL:

		fileP = fileP[:-1]

		fileN = fileP.split('/')[-1]

		ro = re.match(filePattern, fileN)

		if type == 'u2b':
			name = uuid2barcode(ro.group(1))

			print ro.group(1), name

			os.system('ln -s %s %s/%s.2.fq.gz' % (fileP, outDirName, name))
		
		else:
			barcode2uuid()


link('/EQL2/TCGA/LUAD/RNASeq/fastq/fqgz','/EQL2/TCGA/LUAD/RNASeq/fastq','([a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}).[12].fastq.gz','u2b')
