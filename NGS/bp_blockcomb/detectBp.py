#!/usr/bin/python

import sys, os, getopt
import mybasic, mygenome


def detectBp(range1, range2, blockSize, assembly='hg19'):

	# process coordinate

	range1 = mygenome.locus(range1)
	range2 = mygenome.locus(range2)

	# fetch sequence

	seq1 = range1.nibFrag('/data1/Sequence/ucsc_%s' % assembly, blockSize,0)
	seq2 = range2.nibFrag('/data1/Sequence/ucsc_%s' % assembly, 0,blockSize)

	# generate block combination

	outFile = open('/EQL2/RNASeq_LymphNK/bpTemplate.fa','w')

	for i in range(len(seq1)-blockSize+1):
		for j in range(len(seq2)-blockSize+1):
			outFile.write('>seq1:%s-%s|seq2:%s-%s\n%s%s\n' % (i,i+blockSize,j,j+blockSize, seq1[i:i+blockSize], seq2[j:j+blockSize]))

	outFile.close()

	# run bowtie

	print 'building bowtie index'
	os.system('bowtie-build -q -f /EQL2/RNASeq_LymphNK/bpTemplate.fa /data1/Sequence/bowtie/bpTemplate')

optL, argL = getopt.getopt(sys.argv[1:],'o:t',[])

optH = mybasic.parseParam(optL)

#if '-o' in optH:
#
#	detectBp(optH['-o'])

#detectBp('chr6:36100440-36100478+','chr16:921284-921412-',86)

detectBp('chr6:36100500-36103840+','chr16:925410-930530-',86)

print 'running bowtie'
os.system('bowtie -p 30 -r /data1/Sequence/bowtie/bpTemplate bpInput.txt bp.bowtie')
