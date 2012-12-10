#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def gsnap_splice_batch(inputDirN,procDirN,outputDirN):

	qualType = 'sanger'

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('.*\.fastq', x),inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.[12]\.fastq',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	print 'Samples: %s' % sampNL

	prosampNameL = list(set([re.match('.*/(.*).qlog:Processed.*',line).group(1) for line in os.popen('grep Processed %s/*.qlog' % procDirN)]))
	prosampNameL.sort()


	for sampN in sampNL:

		if not sampN in prosampNameL:
			
			print sampN

			os.system('echo "cat %s/%s.1.fastq %s/%s.2.fastq | \
				/usr/local/bin/gsnap --db=hg19 --batch=5 --nthreads=4 --npath=1 -N 1 --use-splicing=refGene_knownGene_splicesites --nofails -Q \
				--query-unk-mismatch=1 > %s/%s_splice.gsnap" | qsub -N %s -o %s/%s.qlog -j oe' % (inputDirN,sampN, inputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))

optL, argL = getopt.getopt(sys.argv[1:],'i:p:o:',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH and '-o' in optH):
	print 'input error'
	sys.exit(0)

inputDirN = optH['-i']
outputDirN = optH['-o']

if '-p' in optH:
	procDirN = optH['-p']
else:
	procDirN = outputDirN

gsnap_splice_batch(inputDirN,procDirN,outputDirN)
