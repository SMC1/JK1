#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mysetting


def align(inputDirN, outputDirN, pbs, qualType='sanger', db='hg19_nh'):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('.*t[12]\.fq\.gz', x),inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.t[12]\.fq\.gz',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

	#	if not sampN in ['G17189.TCGA-06-0132-01A-02R-1849-01.2_30nt','G17500.TCGA-27-1831-01A-01R-1850-01.2_30nt','G17501.TCGA-27-2528-01A-01R-1850-01.2_30nt','G17502.TCGA-14-0871-01A-01R-1849-01.2_30nt']:

		print sampN
		gsnap_opt = '--db=%s --batch=5 --nthreads=4 -m 0 --query-unk-mismatch=1 --terminal-threshold=9 -y 0 -z 0 -Y 0 -Z 0 --nofails --quality-protocol=%s --npath=1 -Q -A sam --gunzip --read-group-id %s --read-group-name %s --read-group-platform Illumina' % (db, qualType, sampN,sampN)
		iprefix = '%s/%s' % (inputDirN,sampN)
		oprefix = '%s/%s' % (outputDirN,sampN)
		cmd = '/usr/local/bin/gsnap %s %s.t1.fq.gz %s.t2.fq.gz | %s/NGS/align/sortSam.py | samtools view -Sb - > %s.bam' % (gsnap_opt, iprefix, iprefix, mysetting.SRC_HOME, oprefix)
		log = '%s.gsnap.qlog' % (oprefix)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))

		else:
			os.system('(%s) 2> %s' % (cmd, log))


if __name__ == '__main__':
#	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])
#
#	optH = mybasic.parseParam(optL)
#
#	inputDirN = optH['-i']
#	outputDirN = optH['-o']
#
	align(inputDirN, outputDirN, '-p' in optH)
