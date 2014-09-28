#!/usr/bin/python

import sys
import mybasic

motifL = ['TAAT','TAATT','TAATTG']
motifL_rc = [mybasic.rc(m,'DNA') for m in motifL]

bed = open('/data1/IRCR/PKS/promoter_hg19.bed')
fa = open('/data1/IRCR/PKS/promoter_hg19.fa')

geneNameL = [x.split('\t')[3] for x in bed]

sys.stdout.write('geneName')

for i in range(len(motifL)):
	sys.stdout.write('\tm%sf\tm%sr\tm%st' % (i+1,i+1,i+1))

sys.stdout.write('\n')

idx = 0

while True:

	h = fa.readline()[:-1]
	s = fa.readline()[:-1].upper()

	sys.stdout.write('%s' % (geneNameL[idx]))

	countL = (s.count(motifL[i]),s.count(motifL_rc[i]))

	for i in range(len(motifL)):
		sys.stdout.write('\t%s\t%s\t%s' % (countL[0],countL[1],sum(countL)))

	sys.stdout.write('\n')

	idx += 1

	if idx >= len(geneNameL):
		break
