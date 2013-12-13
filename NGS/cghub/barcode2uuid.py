#!/usr/bin/python

import sys, getopt, httplib
import mybasic

def uuid2barcode():

	for line in sys.stdin:

		uuid = line[:-1]
		
		conn = httplib.HTTPSConnection('tcga-data.nci.nih.gov')
		conn.request('GET','/uuid/uuidws/mapping/json/uuid/%s' % uuid)
		result = conn.getresponse().read()

		print eval(result)['barcode']


def barcode2uuid():

	for line in sys.stdin:

		barcode = line[:-1]

		conn = httplib.HTTPSConnection('tcga-data.nci.nih.gov')
		conn.request('GET','/uuid/uuidws/mapping/json/barcode/%s' % barcode)
		result = conn.getresponse().read()

		print eval(result)['uuidMapping']['uuid']

uuid2barcode()
