#!/usr/bin/python

import sys, os, re, getopt
import mybasic

# EGFR - single end mode

def align(inputDirN, outputDirN, pbs, qualType='sanger'):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('.*\.fq', x),inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.[12]\.fq',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	sampNL = list(set([re.match('.*/(.*).gsnap.qlog:IndexError.*',line).group(1) for line in os.popen('grep IndexError %s/*.qlog' % outputDirN)]))
	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

		if pbs:

			os.system('echo "cat %s/%s.1.fq %s/%s.2.fq | \
				/usr/local/bin/gsnap --db=EGFR --batch=5 --nthreads=2 -m 0 --query-unk-mismatch=1 --terminal-threshold=9 -y 0 -z 0 -Y 0 -Z 0 \
				--nofails --quality-protocol=%s --npath=1 -Q -A sam | \
				samtools view -Sb - > %s/%s.bam" | qsub -N %s -o %s/%s.gsnap.qlog -j oe' % \
				(inputDirN,sampN, inputDirN,sampN, qualType, outputDirN,sampN, sampN, outputDirN,sampN))

		else:

			print sampN

			os.system('(cat %s/%s.1.fq %s/%s.2.fq | \
				/usr/local/bin/gsnap --db=EGFR --batch=5 --nthreads=2 -m 0 --query-unk-mismatch=1 --terminal-threshold=9 -y 0 -z 0 -Y 0 -Z 0 \
				--nofails --quality-protocol=%s --npath=1 -Q -A sam | \
				samtools view -Sb - > %s/%s.bam) 2> %s/%s.gsnap.qlog' % \
				(inputDirN,sampN, inputDirN,sampN, qualType, outputDirN,sampN, outputDirN,sampN))


if __name__ == '__main__':
#	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])
#
#	optH = mybasic.parseParam(optL)
#
#	inputDirN = optH['-i']
#	outputDirN = optH['-o']
#
	align('/EQL2/TCGA/LUAD/RNASeq/fastq/30nt', '/EQL2/TCGA/LUAD/RNASeq/alignment/30nt',pbs=True)
