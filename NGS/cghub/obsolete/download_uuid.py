#!/usr/bin/python

import sys, os, getopt, time
import mybasic


def download_selected(inFileName,outDirName,credential='/home/jinkuk/cghub.pem'):

	inFile = open(inFileName)
	aliquotIdL= [l[:-1] for l in inFile]

	tmpFileN = time.time()

	for aliquotId in aliquotIdL:

		print aliquotId
		os.system('wget --no-check-certificate -O /tmp/cghub_%s.xml "https://cghub.ucsc.edu/cghub/metadata/analysisObject?library_strategy=RNA-Seq&disease_abbr=BRCA&aliquot_id=%s"' \
			% (tmpFileN,aliquotId))
		os.system('/usr/bin/GeneTorrent -v -c %s -d /tmp/cghub_%s.xml -p %s' % (credential,tmpFileN,outDirName))

optL, argL = getopt.getopt(sys.argv[1:],'i:o:',[])

optH = mybasic.parseParam(optL)

if '-i' in optH and '-o' in optH:
	download_selected(optH['-i'], optH['-o'])

# download_selected('','')
