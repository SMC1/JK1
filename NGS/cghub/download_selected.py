#!/usr/bin/python

import sys, os, getopt, time
import mybasic


def download_selected(outDirName,disease,dataType,verbose,credential='/data1/cghub.pem',inFileName=None):

	if verbose:
		gt_flag = '-v'
		wg_flag = ''
	else:
		gt_flag = ''
		wg_flag = '-q'

	if inFileName:

		sampleIdL= [l[:-1] for l in open(inFileName)]

		tmpFileN = time.time()

		for sampleId in sampleIdL:

			if verbose:
				print sampleId

			if 'TCGA' in sampleId:
				fieldN = 'filename'
			else:
				fieldN = 'aliquot_id'

			os.system('wget %s --no-check-certificate -O /tmp/cghub_%s.xml "https://cghub.ucsc.edu/cghub/metadata/analysisObject?library_strategy=%s&disease_abbr=%s&%s=*%s*"' \
				% (wg_flag,tmpFileN,dataType,disease,fieldN,sampleId))

			os.system('/usr/bin/GeneTorrent %s -c %s -d /tmp/cghub_%s.xml -p %s' % (gt_flag,credential,tmpFileN,outDirName))

	else:

		tmpFileN = time.time()

		os.system('wget %s --no-check-certificate -O /tmp/cghub_%s.xml "https://cghub.ucsc.edu/cghub/metadata/analysisObject?library_strategy=%s&disease_abbr=%s"' \
			% (wg_flag,tmpFileN,dataType,disease))

		os.system('/usr/bin/GeneTorrent %s -c %s -d /tmp/cghub_%s.xml -p %s' % (gt_flag,credential,tmpFileN,outDirName))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:d:t:v',[])

optH = mybasic.parseParam(optL)

outDirName = optH['-o']
disease = optH['-d']
dataType = optH['-t']

if '-i' in optH:
	download_selected(outDirName, disease, dataType, '-v' in optH, optH['-i'])
else:
	download_selected(outDirName, disease, dataType, '-v' in optH)
