#!/usr/bin/python

import sys, getopt, re
import mybasic, mygsnap, mygenome


def loadAnnot(geneL=None):

	refFlatH = mygenome.loadRefFlatByChr()

	eiH = {}

	for chrom in refFlatH.keys():

		eiH[chrom] = {}

		refFlatL = refFlatH[chrom]

		for tH in refFlatL:

			if geneL!=None and tH['geneName'] not in geneL:
				continue

			for (s,e) in tH['exnList']:
				eiH[chrom][e] = [0,0]

	return eiH


def main(inGsnapFileName,outReportFileName,geneNL,overlap):

	eiH = loadAnnot(geneNL)

	result = mygsnap.gsnapFile(inGsnapFileName,False)

	for r in result:

		match = r.matchL()[0]

		if '(transloc)' in r.pairRel or len(match.segL) > 1:
			continue	

		

		splice_type = re.search('splice_type:([^,\t]*)', match.segL[0][3]).group(1)
		direction = re.search('dir:([^,\t]*)', match.segL[0][3]).group(1)
		offset = int(re.search('\.\.([0-9]*)', match.segL[0][1]).group(1))

		transcriptL = []

		for i in range(2):

			rm = re.search('label_[12]:([^,\t]*)', match.segL[i][3])

			if rm:
				transcriptL.append(rm.group(1).replace('|',','))
			else:
				transcriptL.append('')

		s1 = match.segL[0][2]
		s2 = match.segL[1][2]

		bp1 = re.match('([+-])([^:]+):[0-9]+..([0-9]+)',s1)
		bp2 = re.match('([+-])([^:]+):([0-9]+)..[0-9]+',s2)

		if (bp1.group(1),direction) in (('+','sense'),('-','antisense')):
			trans_strand1 = '+'
		elif (bp1.group(1),direction) in (('+','antisense'),('-','sense')):
			trans_strand1 = '-'
		else:
			raise Exception

		if (bp2.group(1),direction) in (('+','sense'),('-','antisense')):
			trans_strand2 = '+'
		elif (bp2.group(1),direction) in (('+','antisense'),('-','sense')):
			trans_strand2 = '-'
		else:
			raise Exception

		if direction=='sense':
			key = ((trans_strand1,)+bp1.groups()[1:],(trans_strand2,)+bp2.groups()[1:])
		elif direction=='antisense':
			key = ((trans_strand2,)+bp2.groups()[1:],(trans_strand1,)+bp1.groups()[1:])
			transcriptL = transcriptL[::-1]
		else:
			raise Exception

		if key in juncHH:

			juncHH[key]['match'].append(r)
			juncHH[key]['seq'].append(r.seq())
			juncHH[key]['pos'].append((direction,offset))

		else:

			juncHH[key] = {'match':[r], 'splice_type':splice_type, 'seq':[r.seq()], 'pos':[(direction,offset)], 'transcript':transcriptL}

	juncKH = juncHH.items()
	juncKH.sort(lambda x,y: cmp(len(set(y[1]['pos'])),len(set(x[1]['pos']))))

	outGsnapFile = open(outGsnapFileName,'w')
	outReportFile = open(outReportFileName,'w')

	for (key, juncH) in juncKH:

		outReportFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % \
			(juncH['splice_type'], sampN, key[0][0]+':'.join(key[0][1:]), key[1][0]+':'.join(key[1][1:]), \
			juncH['transcript'][0], juncH['transcript'][1],  \
			len(juncH['match']), len(set(juncH['seq'])), len(set(juncH['pos']))))

		for m in juncH['match']:
			outGsnapFile.write(m.rawText()+'\n')


optL, argL = getopt.getopt(sys.argv[1:],'i:o:r:s:',[])

optH = mybasic.parseParam(optL)

#if '-s' in optH:
#	main(optH['-i'],optH['-o'],optH['-r'],optH['-s'])
#else:
#	main(optH['-i'],optH['-o'],optH['-r'],optH['-i'])

main(optH['-i'],optH['-o'],['EGFR'],10)
