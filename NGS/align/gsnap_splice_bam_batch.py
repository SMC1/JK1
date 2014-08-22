#!/usr/bin/python

import sys, os, re, getopt
import mybasic


def align(inputDirN, outputDirN, pbs=False, genome='hg19'):

	inputFileNL = os.listdir(inputDirN)
	inputFileNL = filter(lambda x: re.match('.*\.fq\.gz', x),inputFileNL)

	print 'Files: %s' % inputFileNL

	sampNL = list(set([re.match('(.*)\.[12]\.fq\.gz',inputFileN).group(1) for inputFileN in inputFileNL]))

	sampNL.sort()

	print 'Samples: %s' % sampNL

	for sampN in sampNL:

#		if sampN[1:4] not in ['671','740','592','660','586','428','642','460','568','372','608','572','618','458','594','453','775']:
#			continue

#		if sampN in ['S647_RSq']:
#			continue

		print('%s' % sampN)
		iprefix = '%s/%s' % (inputDirN,sampN)
		oprefix = '%s/%s' % (outputDirN,sampN)
		cmd = '(zcat %s.1.fq.gz %s.2.fq.gz' % (iprefix, iprefix)
		cmd = '%s | /home/tools/gmap-2012-12-20-patched/src/gsnap --db=%s --batch=5 --nthreads=10 --npath=1 -N 1 --nofails -Q -A sam --query-unk-mismatch=1 --use-splicing=refGene_knownGene_splicesites --read-group-id %s --read-group-name %s --read-group-platform Illumina' % (cmd, genome, sampN,sampN)
		cmd = '%s | python ~/JK1/NGS/align/split_gsnap_sam.py -s -g %s_splice.gsnap | samtools view -Sb - > %s_splice.bam' % (cmd, oprefix, oprefix)
		cmd = '%s); gzip %s_splice.gsnap' % (cmd, oprefix)
		log = '%s.gsnap.qlog' % (oprefix)
		if pbs:
			os.system('echo "%s" | qsub -N %s -o %s -j oe' % (cmd, sampN, log))


		else:
			os.system('(%s) 2> %s' % (cmd, log))


if __name__ == '__main__':

	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

	optH = mybasic.parseParam(optL)

	#inputDirN = optH['-i']
	#outputDirN = optH['-o']
	#align(inputDirN, outputDirN)

	align('/EQL1/NSL/RNASeq/fastq/link41', '/EQL1/NSL/RNASeq/align/splice_bam', True)
