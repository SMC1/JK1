#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def align(inputDirN, outputDirN, nThreads, pbs=False, gz=True):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('.*\.fq\.gz', x),inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.[12]\.fq\.gz',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	print 'Samples: %s' % sampNL

	if gz:
		cmd = 'z'
		ext = '.gz'
	else:
		cmd = ''
		ext = ''

	for sampN in sampNL:

	#	if not sampN in ['G17678.TCGA-06-5417-01A-01R-1849-01.2']:
	#		continue

		if pbs:

			print('%s' % sampN)

			os.system('echo %scat %s/%s.1.fq%s %s/%s.2.fq%s | \
				/usr/local/bin/gsnap --db=hg19 --batch=5 --nthreads=%s --npath=1 -N 1 --use-splicing=refGene_knownGene_splicesites --nofails -Q \
				 --query-unk-mismatch=1 > %s/%s_splice.gsnap" | qsub -N %s -o %s/%s.gsnap.qlog -j oe' % \
				 (cmd, inputDirN,sampN, ext, inputDirN, sampN, ext, nThreads, outputDirN,sampN, sampN, outputDir,sampN))

		else:

			print('%s' % sampN)
			
			os.system('(%scat %s/%s.1.fq%s %s/%s.2.fq%s | \
				/usr/local/bin/gsnap --db=hg19 --batch=5 --nthreads=%s --npath=1 -N 1 --use-splicing=refGene_knownGene_splicesites --nofails -Q \
				--query-unk-mismatch=1 > %s/%s_splice.gsnap) 2> %s/%s.gsnap.qlog' % (cmd, inputDirN, sampN, ext, inputDirN, sampN, ext, nThreads, outputDirN,sampN, outputDirN,sampN))


if __name__ == '__main__':
	#optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])
	#
	#optH = mybasic.parseParam(optL)
	#
	#inputDirN = optH['-i']
	#outputDirN = optH['-o']
	#align(inputDirN, outputDirN)

	align('/EQL2/TCGA/LUAD/RNASeq/fastq/', '/EQL2/TCGA/LUAD/RNASeq/align', 10, False)
