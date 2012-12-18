#!/usr/bin/python

import sys, os, getopt, time
import mybasic


def download_selected(inFileName,outDirName,disease,dataType,verbose,credential='/home/jinkuk/cghub.pem'):

	inFile = open(inFileName)
	sampleIdL= [l[:-1] for l in inFile]

	tmpFileN = time.time()

	for sampleId in sampleIdL:

		if verbose:
			print sampleId

		if 'TCGA' in sampleId:
			fieldN = 'filename'
		else:
			fieldN = 'aliquot_id'

		if verbose:
			gt_flag = '-v'
			wg_flag = ''
		else:
			gt_flag = ''
			wg_flag = '-q'

		os.system('wget %s --no-check-certificate -O /tmp/cghub_%s.xml "https://cghub.ucsc.edu/cghub/metadata/analysisObject?library_strategy=%s&disease_abbr=%s&%s=*%s*"' \
			% (wg_flag,tmpFileN,dataType,disease,fieldN,sampleId))

		os.system('/usr/bin/GeneTorrent %s -c %s -d /tmp/cghub_%s.xml -p %s' % (gt_flag,credential,tmpFileN,outDirName))

optL, argL = getopt.getopt(sys.argv[1:],'i:o:d:t:v',[])

optH = mybasic.parseParam(optL)

outDirName = optH['-o']
disease = optH['-d']

download_selected(optH['-i'], outDirName, disease, '-v' in optH)
