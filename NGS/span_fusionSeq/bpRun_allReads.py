#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:t',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH):

	print 'Usage: bpRun_allReads.py -i [input file dir]'
	sys.exit(0)

inputDirN = optH['-i']

inputFileNL = os.listdir(inputDirN)
inputFileNL = filter(lambda x: re.match('S08.*\.fastq', x),inputFileNL)

print 'Files: %s' % inputFileNL

sampNL = list(set([re.match('(.*)\.[12]\.fastq',inputFileN).group(1) for inputFileN in inputFileNL]))

sampNL.sort()

print 'Samples: %s' % sampNL

for sampN in sampNL:

	if '-t' in optH:

		print 'rm -f %s/%s_allReads.txt' % (inputDirN,sampN)

		print 'echo "cat %s/%s.1.fastq %s/%s.2.fastq | ./allReads.py > %s/%s_allReads.txt" | qsub -l walltime=99:99:99:99 -N %s -o %s/%s.qlog -j oe' % \
			(inputDirN,sampN, inputDirN,sampN, inputDirN,sampN, sampN, inputDirN,sampN)
	else:

		os.system('rm -f %s/%s_allReads.txt' % (inputDirN,sampN))

		os.system('echo "cat %s/%s.1.fastq %s/%s.2.fastq | /home/jinkuk/Codes/NGS/fusionSeq/allReads.py > %s/%s_allReads.txt" | qsub -l walltime=99:99:99:99 -N %s -o %s/%s.qlog -j oe' % \
			(inputDirN,sampN, inputDirN,sampN, inputDirN,sampN, sampN, inputDirN,sampN))
