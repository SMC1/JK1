#!/usr/bin/python

import sys, getopt, re
import xml.etree.ElementTree as ET
import mybasic


def filterXml(inFileName,outFileName):

	#root = ET.fromstring(sys.stdin.read())

	tree = ET.parse(inFileName)
	root = tree.getroot()

	for result in root.findall('Result'):

		rm = re.match('.*TCGA-..-....-(..).*', result.find('files').find('file').find('filename').text)

		#if int(rm.group(1)) >= 10 or result.find('state').text != 'live':
		if int(rm.group(1)) < 10 or result.find('state').text != 'live':
			root.remove(result)

	root.find('Hits').text = str(len(root.findall('Result')))

	tree.write(outFileName)

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

inFileName = optH['-i']
outFileName = optH['-o']

filterXml(inFileName,outFileName)
