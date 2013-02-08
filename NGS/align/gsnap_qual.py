#!/usr/bin/python

import sys, re, numpy
import mygsnap


if len(sys.argv) >= 4:
	inFileName = sys.argv[1]
	outFileName_matches = sys.argv[2]
	outFileName_mmPos = sys.argv[3]
else:
	inFileName = 'GH.txt'
	outFileName_matches = 'GH_matches.dst'
	outFileName_mmPos = 'GH_mmPos.txt'

result = mygsnap.gsnapFile(inFileName)
out_matches = open(outFileName_matches, 'w')
out_mmPos = open(outFileName_mmPos, 'w')

matches_count = {'unpaired':[], 'concordant':[]}
matches_score = {'unpaired':[], 'concordant':[]}

totalPairs = {'unpaired':0, 'concordant':0}
mmPos = {'unpaired':{0:None, 1:None}, 'concordant':{0:None, 1:None}}

for rL in result:

	if rL[0].nLoci==1 and rL[1].nLoci==1 and not '(transloc)' in rL[0].pairRel: # unique, no-within-read-splicing
	
		mL = [rL[0].matchL()[0], rL[1].matchL()[0]]

		if len(mL[0].mergedLocusL())==1 and len(mL[1].mergedLocusL())==1: # mapped to a single mergable locus

			pairRel = rL[0].pairRel

			if pairRel=='unpaired' or pairRel=='concordant':

				for i in (0,1):

					seq_read = rL[i].seq()

					matches_count[pairRel].append(mL[i].numMatch(seq_read))
					matches_score[pairRel].append(mL[i].score())

					try:
						mmPos[pairRel][i] += numpy.array(mL[i].posProfile(seq_read))
					except:
						mmPos[pairRel][i] = numpy.array(mL[i].posProfile(seq_read))

				totalPairs[pairRel] += 1

for pairRel in matches_count.keys():

	out_matches.write('%s\nmatches_count\t%s\t%s\n%s\n' % \
		(pairRel,min(min(matches_count['unpaired']),min(matches_count['concordant'])),max(max(matches_count['unpaired']),max(matches_count['concordant'])), '\t'.join(map(str,matches_count[pairRel]))))
	out_matches.write('%s\nmatches_score\t%s\t%s\n%s\n' % \
		(pairRel,0,max(max(matches_score['unpaired']),max(matches_score['concordant'])), '\t'.join(map(str,matches_score[pairRel]))))

	for i in (0,1):
		out_mmPos.write('%s\t%s\t%s\n' % (pairRel,i, ','.join(['%.1f' % v for v in mmPos[pairRel][i]/float(totalPairs[pairRel])*100])))

out_matches.close()
out_mmPos.close()
