#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:p',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH):

	print 'Usage: fusionSeq.2.py -i (input file dir)'
	sys.exit(0)

inputDirN = optH['-i']

repeatMaskerBase = '/data1/Sequence/FusionSeq_Data_hg19'
blackListBase = '/data1/Sequence/FusionSeq_Data'

inputFileNL = os.listdir(inputDirN)
inputFileNL = filter(lambda x: re.match('.*\.1\.gfr', x),inputFileNL)

print 'Files: %s' % inputFileNL

sampNL = [re.match('(.*)\.1\.gfr',inputFileN).group(1) for inputFileN in inputFileNL]

sampNL.sort()

print 'Samples: %s' % sampNL

for sampN in sampNL:

	if '-p' in optH:

		os.system('echo "(gfrMitochondrialFilter < %s/%s.1.gfr | gfrRepeatMaskerFilter %s/repeatMasker.interval 5 | gfrCountPairTypes | gfrExpressionConsistencyFilter | gfrPCRFilter 4 4 | gfrProximityFilter 1000 | gfrAddInfo |  gfrAnnotationConsistencyFilter ribosomal | gfrAnnotationConsistencyFilter pseudogenes | gfrBlackListFilter %s/blackList.txt |  gfrLargeScaleHomologyFilter | gfrRibosomalFilter | gfrSmallScaleHomologyFilter) > %s/%s.gfr" | qsub -N %s -o %s/qlog/%s.2.qlog -j oe' % \
			(inputDirN,sampN, repeatMaskerBase, blackListBase, inputDirN,sampN, sampN, inputDirN,sampN))

	else:

		print sampN

		os.system('(gfrMitochondrialFilter < %s/%s.1.gfr | gfrRepeatMaskerFilter %s/repeatMasker.interval 5 | gfrCountPairTypes | gfrExpressionConsistencyFilter | gfrPCRFilter 4 4 | gfrProximityFilter 1000 | gfrAddInfo |  gfrAnnotationConsistencyFilter ribosomal | gfrAnnotationConsistencyFilter pseudogenes | gfrBlackListFilter %s/blackList.txt |  gfrLargeScaleHomologyFilter | gfrRibosomalFilter | gfrSmallScaleHomologyFilter) > %s/%s.gfr 2> %s/qlog/%s.2.qlog' % \
			(inputDirN,sampN, repeatMaskerBase, blackListBase, inputDirN,sampN, inputDirN,sampN))
