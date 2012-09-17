#!/usr/bin/python

import sys, getopt, httplib
import mybasic


def barcode2uuid():

	for line in sys.stdin:

		barcode = line[:-1]

		conn = httplib.HTTPSConnection('tcga-data.nci.nih.gov')
		conn.request('GET','/uuid/uuidws/mapping/json/barcode/%s' % barcode)
		result = conn.getresponse().read()

		print eval(result)['uuidMapping']['uuid']

barcode2uuid()
