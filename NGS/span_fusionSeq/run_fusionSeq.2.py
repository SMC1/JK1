#!/usr/bin/python

import sys, os, re, getopt
import mybasic


optL, argL = getopt.getopt(sys.argv[1:],'i:t',[])

optH = mybasic.parseParam(optL)

if not ('-i' in optH):

	print 'Usage: run_fusionSeq.2.py -i [input file dir]'
	sys.exit(0)

inputDirN = optH['-i']

repeatMaskerBase = '/data1/Sequence/FusionSeq_Data_hg19'
blackListBase = '/data1/Sequence/FusionSeq_Data'

inputFileNL = os.listdir(inputDirN)
inputFileNL = filter(lambda x: re.match('.*\.1\.gfr', x),inputFileNL)

print 'Files: %s' % inputFileNL

sampNL = list(set([re.match('(.*)\.1\.gfr',inputFileN).group(1) for inputFileN in inputFileNL]))

sampNL.sort()

print 'Samples: %s' % sampNL

for sampN in sampNL:

	if '-t' in optH:

		print 'rm -f %s/%s.gfr %s/%s.fusionSeq.2.log' % (inputDirN,sampN, inputDirN,sampN)

		print 'echo "(gfrMitochondrialFilter < %s/%s.1.gfr | gfrRepeatMaskerFilter %s/repeatMasker.interval 5 | gfrCountPairTypes | gfrExpressionConsistencyFilter  | gfrAbnormalInsertSizeFilter 0.01 |  gfrPCRFilter 4 4 | gfrProximityFilter 1000 | gfrAddInfo |  gfrAnnotationConsistencyFilter ribosomal | gfrAnnotationConsistencyFilter pseudogenes | gfrBlackListFilter %s/blackList.txt |  gfrLargeScaleHomologyFilter | gfrRibosomalFilter | gfrSmallScaleHomologyFilter) > %s/%s.gfr" | qsub -l walltime=99:99:99:99 -N %s -o %s/%s.fusionSeq.2.log -j oe' % \
			(inputDirN,sampN, repeatMaskerBase, blackListBase, inputDirN,sampN, sampN, inputDirN,sampN)
	else:

		os.system('rm -f %s/%s.gfr %s/%s.fusionSeq.2.log' % (inputDirN,sampN, inputDirN,sampN))

		os.system('echo "(gfrMitochondrialFilter < %s/%s.1.gfr | gfrRepeatMaskerFilter %s/repeatMasker.interval 5 | gfrCountPairTypes | gfrExpressionConsistencyFilter  | gfrAbnormalInsertSizeFilter 0.01 |  gfrPCRFilter 4 4 | gfrProximityFilter 1000 | gfrAddInfo |  gfrAnnotationConsistencyFilter ribosomal | gfrAnnotationConsistencyFilter pseudogenes | gfrBlackListFilter %s/blackList.txt |  gfrLargeScaleHomologyFilter | gfrRibosomalFilter | gfrSmallScaleHomologyFilter) > %s/%s.gfr" | qsub -l walltime=99:99:99:99 -N %s -o %s/%s.fusionSeq.2.log -j oe' % \
			(inputDirN,sampN, repeatMaskerBase, blackListBase, inputDirN,sampN, sampN, inputDirN,sampN))
