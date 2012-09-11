#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH):

	print 'Usage: fusionSeq.1.py -i (input file dir) [-o (output file dir)]'
	sys.exit(0)

inputDirN = optH['-i']

if '-o' in optH:
	outputDirN = optH['-o']
else:
	outputDirN = inputDirN

inputFileNL = os.listdir(inputDirN)
#inputFileNL = filter(lambda x: re.match('.*\.mrf', x),inputFileNL)
inputFileNL = filter(lambda x: re.match('.*\.sorted\.sam', x),inputFileNL)

print 'Files: %s' % inputFileNL

#sampNL = list(set([re.match('(.*)\.mrf',inputFileN).group(1) for inputFileN in inputFileNL]))
sampNL = list(set([re.match('(.*)\.sorted\.sam',inputFileN).group(1) for inputFileN in inputFileNL]))

sampNL.sort()

print 'Samples: %s' % sampNL

#excL = ['G17188.TCGA-02-0047-01A-01R-1849-01.2_30nt', 'G17189.TCGA-06-0132-01A-02R-1849-01.2_30nt', 'G17190.TCGA-06-0174-01A-01R-1849-01.2_30nt', 'G17191.TCGA-06-0211-01A-01R-1849-01.2_30nt', 'G17192.TCGA-06-0645-01A-01R-1849-01.2_30nt', 'G17193.TCGA-06-0743-01A-01R-1849-01.2_30nt', 'G17194.TCGA-02-0055-01A-01R-1849-01.2_30nt', 'G17195.TCGA-06-0138-01A-02R-1849-01.2_30nt', 'G17196.TCGA-06-0178-01A-01R-1849-01.2_30nt', 'G17197.TCGA-06-0211-01B-01R-1849-01.2_30nt', 'G17198.TCGA-06-0646-01A-01R-1849-01.2_30nt', 'G17199.TCGA-06-0744-01A-01R-1849-01.2_30nt', 'G17200.TCGA-06-0125-01A-01R-1849-01.2_30nt', 'G17201.TCGA-06-0156-01A-02R-1849-01.2_30nt', 'G17203.TCGA-06-0211-02A-02R-2005-01.2_30nt', 'G17204.TCGA-08-0386-01A-01R-1849-01.2_30nt', 'G17205.TCGA-06-0745-01A-01R-1849-01.2_30nt', 'G17206.TCGA-06-0125-02A-11R-2005-01.2_30nt', 'G17207.TCGA-06-0156-01A-03R-1849-01.2_30nt', 'G17208.TCGA-06-0187-01A-01R-1849-01.2_30nt', 'G17209.TCGA-06-0219-01A-01R-1849-01.2_30nt', 'G17210.TCGA-12-0616-01A-01R-1849-01.2_30nt', 'G17211.TCGA-06-0747-01A-01R-1849-01.2_30nt', 'G17212.TCGA-06-0129-01A-01R-1849-01.2_30nt', 'G17213.TCGA-06-0157-01A-01R-1849-01.2_30nt', 'G17214.TCGA-06-0190-01A-01R-1849-01.2_30nt', 'G17215.TCGA-06-0221-02A-11R-2005-01.2_30nt', 'G17216.TCGA-12-0618-01A-01R-1849-01.2_30nt', 'G17217.TCGA-06-0749-01A-01R-1849-01.2_30nt', 'G17218.TCGA-06-0130-01A-01R-1849-01.2_30nt', 'G17219.TCGA-06-0158-01A-01R-1849-01.2_30nt', 'G17220.TCGA-06-0190-02A-01R-2005-01.2_30nt', 'G17221.TCGA-06-0152-02A-01R-2005-01.2_30nt', 'G17222.TCGA-12-0619-01A-01R-1849-01.2_30nt', 'G17223.TCGA-06-0750-01A-01R-1849-01.2_30nt', 'G17225.TCGA-06-0168-01A-01R-1849-01.2_30nt', 'G17226.TCGA-06-0210-01A-01R-1849-01.2_30nt', 'G17227.TCGA-06-0238-01A-02R-1849-01.2_30nt', 'G17228.TCGA-06-0649-01B-01R-1849-01.2_30nt', 'G17229.TCGA-15-0742-01A-01R-1850-01.2_30nt', 'G17230.TCGA-06-0141-01A-01R-1849-01.2_30nt', 'G17231.TCGA-06-0171-02A-11R-2005-01.2_30nt', 'G17232.TCGA-06-0210-02A-01R-2005-01.2_30nt', 'G17233.TCGA-06-0644-01A-02R-1849-01.2_30nt', 'G17234.TCGA-06-0686-01A-01R-1849-01.2_30nt', 'G17466.TCGA-06-0878-01A-01R-1849-01.2_30nt', 'G17467.TCGA-14-0736-02A-01R-2005-01.2_30nt', 'G17468.TCGA-19-0957-02A-11R-2005-01.2_30nt', 'G17469.TCGA-06-2557-01A-01R-1849-01.2_30nt', 'G17470.TCGA-06-2567-01A-01R-1849-01.2_30nt', 'G17471.TCGA-27-2519-01A-01R-1850-01.2_30nt', 'G17472.TCGA-06-0882-01A-01R-1849-01.2_30nt', 'G17473.TCGA-14-1034-01A-01R-1849-01.2_30nt', 'G17474.TCGA-19-1389-02A-21R-2005-01.2_30nt']

for sampN in sampNL:

	if sampN in ['G17189.TCGA-06-0132-01A-02R-1849-01.2_30nt','G17500.TCGA-27-1831-01A-01R-1850-01.2_30nt','G17501.TCGA-27-2528-01A-01R-1850-01.2_30nt','G17502.TCGA-14-0871-01A-01R-1849-01.2_30nt']:

		if '-p' in optH:

			os.system('echo "geneFusions %s 4 < %s/%s.mrf | gfrClassify > %s/%s.1.gfr" | qsub -N %s -o %s/qlog/%s.1.qlog -j oe' % \
				(sampN, inputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))

		else:

			print '(geneFusions %s 4 < %s/%s.mrf | gfrClassify > %s/%s.1.gfr) 2> %s/qlog/%s.1.qlog' % \
				(sampN, inputDirN,sampN, outputDirN,sampN, outputDirN,sampN)

			os.system('(geneFusions %s 4 < %s/%s.mrf | gfrClassify > %s/%s.1.gfr) 2> %s/qlog/%s.1.qlog' % \
				(sampN, inputDirN,sampN, outputDirN,sampN, outputDirN,sampN))
