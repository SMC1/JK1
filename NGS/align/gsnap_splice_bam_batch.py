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

		if pbs:

			print('%s' % sampN)

			os.system('echo "zcat %s/%s.1.fq.gz %s/%s.2.fq.gz | \
				/home/tools/gmap-2012-12-20-patched/src/gsnap --db=%s --batch=5 --nthreads=10 --npath=1 -N 1 --nofails -Q -A sam --query-unk-mismatch=1 --use-splicing=refGene_knownGene_splicesites | python ~/JK1/NGS/align/split_gsnap_sam.py -s -g %s/%s_splice.gsnap |\
				samtools view -Sb - > %s/%s_splice.bam; gzip %s/%s_splice.gsnap" | qsub -N %s -o %s/%s.gsnap.qlog -j oe' % (inputDirN,sampN, inputDirN,sampN, genome, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, sampN, outputDirN,sampN))

		else:

			print('%s' % sampN)

			os.system('(zcat %s/%s.1.fq.gz %s/%s.2.fq.gz | \
				/home/tools/gmap-2012-12-20-patched/src/gsnap --db=%s --batch=5 --nthreads=10 --npath=1 -N 1 --nofails -Q -A sam --query-unk-mismatch=1 --use-splicing=refGene_knownGene_splicesites | python ~/JK1/NGS/align/split_gsnap_sam.py -s -g %s/%s_splice.gsnap |\
				samtools view -Sb - > %s/%s_splice.bam; gzip %s/%s_splice.gsnap) 2> %s/%s.gsnap.qlog' % (inputDirN,sampN, inputDirN,sampN, genome, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN, outputDirN,sampN))


if __name__ == '__main__':

	optL, argL = getopt.getopt(sys.argv[1:],'i:o:p',[])

	optH = mybasic.parseParam(optL)

	#inputDirN = optH['-i']
	#outputDirN = optH['-o']
	#align(inputDirN, outputDirN)

	align('/EQL1/NSL/RNASeq/fastq/link41', '/EQL1/NSL/RNASeq/align/splice_bam', True)
