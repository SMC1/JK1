#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def bowtie_4x_batch(inDirName,outDirName,pbs,template,nthreads,qualType='sanger'):

	inputFileNL = os.listdir(inDirName)
	inputFileNL = filter(lambda x: re.match('.*\.fastq', x),inputFileNL)

	sampNL = list(set([re.match('(.*)\.[12]\.fastq',inputFileN).group(1) for inputFileN in inputFileNL]))
	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

#		if not sampN in ['C282.TCGA-32-2638-01A-01W-0922-08.1_WXS_4x_17nt','C484.TCGA-12-5299-01A-02D-1486-08.6_WXS_4x_17nt']:
		if not sampN in ['C484.TCGA-12-5299-01A-02D-1486-08.6_WXS_4x_17nt']:
			continue

		if pbs:

			os.system('echo "/home/tools/bowtie/bowtie \
				-p %s -n 0 -l 17 -m 1 -y -I 0 -X 200000 %s -1 %s/%s.1.fastq -2 %s/%s.2.fastq %s/%s.bowtie" | qsub -N %s -o %s/%s.bowtie.qlog -j oe' % \
				(nthreads,template, inDirName,sampN, inDirName,sampN, outDirName,sampN, sampN, outDirName,sampN))

		else:

			print sampN

			os.system('(/home/tools/bowtie/bowtie \
				-p %s -n 0 -l 17 -m 1 -y -I 0 -X 200000 %s -1 %s/%s.1.fastq -2 %s/%s.2.fastq %s/%s.bowtie) 2> %s/%s.bowtie.qlog' % \
				(nthreads,template, inDirName,sampN, inDirName,sampN, outDirName,sampN, outDirName,sampN))


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

inDirName = optH['-i']
outDirName = optH['-o']

bowtie_4x_batch(inDirName,outDirName,'-p' in optH,'hg19/hg19', 15)
