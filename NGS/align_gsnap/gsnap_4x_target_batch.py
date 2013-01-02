#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def gsnap_4x_batch(inDirName,outDirName,pbs,template,qualType='sanger'):

	inputFileNL = os.listdir(inDirName)
	inputFileNL = filter(lambda x: re.match('.*\.fastq', x),inputFileNL)

	sampNL = list(set([re.match('(.*)\.[12]\.fastq',inputFileN).group(1) for inputFileN in inputFileNL]))
	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

		#if not sampN in ['C282.TCGA-32-2638-01A-01W-0922-08.1_WXS_4x_17nt','C484.TCGA-12-5299-01A-02D-1486-08.6_WXS_4x_17nt']:
		if not sampN in ['C484.TCGA-12-5299-01A-02D-1486-08.6_WXS_4x_27nt']:
			continue

		if pbs:

			os.system('echo "/usr/local/bin/gsnap --db=%s --batch=5 --nthreads=30 -m 0 --query-unk-mismatch=1 --terminal-threshold=9 -y 0 -z 0 -Y 0 -Z 0 \
				--nofails --quality-protocol=%s --npath=1 -Q --pairmax-dna=200000 %s/%s.1.fastq %s/%s.2.fastq > %s/%s_%s.gsnap" | qsub -N %s -o %s/%s_%s.gsnap.qlog -j oe' % \
				(template,qualType, inDirName,sampN, inDirName,sampN, outDirName,template,sampN, sampN, outDirName,template,sampN))

		else:

			print sampN

			os.system('(/usr/local/bin/gsnap --db=%s --batch=5 --nthreads=30 -m 0 --query-unk-mismatch=1 --terminal-threshold=9 -y 0 -z 0 -Y 0 -Z 0 \
				--nofails --quality-protocol=%s --npath=1 -Q --pairmax-dna=200000 %s/%s.1.fastq %s/%s.2.fastq > %s/%s_%s.gsnap) 2> %s/%s_%s.gsnap.qlog' % \
				(template,qualType, inDirName,sampN, inDirName,sampN, outDirName,template,sampN, outDirName,template,sampN))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

inDirName = optH['-i']
outDirName = optH['-o']

gsnap_4x_batch(inDirName,outDirName,'-p' in optH,'EGFR_25_27')
