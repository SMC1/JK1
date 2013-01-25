#!/usr/bin/python

import sys, os, re, getopt
import mybasic

def allsallgene_batch(inputDirN,outputDirN,refFlatfile,pbs):

	inputFileNL = os.listdir(inputDirN)
	
	inputFileNL = filter(lambda x: re.match('.*\.bedgraph', x),inputFileNL)
	
	for inputFileN in inputFileNL:

		sampN = re.match('(.*)\.bedgraph', inputFileN).group(1)

		if pbs:
	
			os.system('echo "python ~/JK1/NGS/coverage/lastExon/1s1gene.py -i %s/%s -j %s" | qsub -N %s -o %s/%s_lastExon.qlog -j oe' % (inputDirN,inputFileN,refFlatfile,sampN,outputDirN,sampN))
	
		else:
	
			print sampN
	
			os.system('python 1s1gene.py -i %s/%s -j %s 2> %s/%s_lastExon.qlog' % (inputDirN,inputFileN,refFlatfile,outputDirN,sampN))

optL, argL = getopt.getopt(sys.argv[1:],'i:o:j:p',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH and '-j' in optH):
	print 'Usage: ./allsallgene_batch.py -i [input file dir] -j [refFlatfile] -o [output file dir]'
	sys.exit(0)

inputDirN = optH['-i']

refFlatfile = optH['-j']

if '-o' in optH:
	outputDirN = optH['-o']
else:
	outputDirN = inputDirN

allsallgene_batch(inputDirN, outputDirN, refFlatfile, '-p' in optH)
