#!/usr/bin/python

import sys
import mygsnap


if len(sys.argv) >= 2:
	inFileName = sys.argv[1]
else:
	inFileName = '/Data2/GH.txt'

result = mygsnap.gsnapFile(inFileName)


pairs_unique_inter = 0
pairs_unique_else = 0
pairs_else = 0

set_pairs = set([])
set_reads = set([])

for rL in result:

	if len(set_pairs)==0:
		seqLen = len(rL[0].seq())

	set_pairs.add(rL[0].seq()+rL[1].seq())
	set_reads.add(rL[0].seq())
	set_reads.add(rL[1].seq())

	if rL[0].nLoci==1 and rL[1].nLoci==1: # unique

		if rL[0].pairRel=='unpaired' and not '(transloc)' in rL[0].pairRel and len(rL[0].matchL()[0].mergedLocusL())==1 and len(rL[1].matchL()[0].mergedLocusL())==1: # interchromosomal split pairs
			pairs_unique_inter += 1 
		else:
			pairs_unique_else += 1

	else:
		
		pairs_else += 1

pairs_unique = pairs_unique_inter + pairs_unique_else
pairs_all = pairs_unique + pairs_else
reads_all = pairs_all*2

# column header: 'dataName\tseqLen\tpairs_unique_inter\tpairs_unique_else\tpairs_else\tpairs_all\tunique_pairs\t%unique_pairs\treads_all\tunique_reads\t%unique_reads'
print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%d\t%s\t%s\t%d' % \
	(inFileName, seqLen, pairs_unique_inter, pairs_unique_else, pairs_else, pairs_all, len(set_pairs), len(set_pairs)/float(pairs_all)*100, reads_all, len(set_reads), len(set_reads)/float(reads_all)*100)
