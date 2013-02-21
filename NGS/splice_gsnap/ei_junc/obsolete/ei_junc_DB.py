#!/usr/bin/python

import sys, getopt, re, MySQLdb
import mybasic, mygsnap, mygenome


def loadAnnot(geneL=[]):

	refFlatH = mygenome.loadRefFlatByChr()

	eiH = {}
	ei_keyH = {}
	juncInfoH = {}

	for chrom in refFlatH.keys():

		eiH[chrom] = {}
		juncInfoH[chrom] = {}

		refFlatL = refFlatH[chrom]

		for tH in refFlatL:

			if geneL!=[] and tH['geneName'] not in geneL:
				continue

			for i in range(len(tH['exnList'])):

				if tH['strand'] == '+':
					pos = tH['exnList'][i][1]
					e_num = i+1
				else:
					pos = tH['exnList'][i][0]
					e_num = len(tH['exnList'])-i

				mybasic.addHash(juncInfoH[chrom], pos, '%s%s:%s:%s/%s' % (tH['strand'], tH['geneName'], tH['refSeqId'], e_num, len(tH['exnList'])))
				eiH[chrom][pos] = 0

				cursor.execute('replace into temp_table (chrom,pos) values ("%s",%s)' % (chrom,pos))

		ei_keyH[chrom] = eiH[chrom].keys()
		ei_keyH[chrom].sort()

	return eiH,ei_keyH,juncInfoH


def main(inGsnapFileName,outReportFileName,sampN,geneNL=[],overlap=10):

	eiH, ei_keyH, juncInfoH = loadAnnot(geneNL)

	print 'Finished loading refFlat'

	result = mygsnap.gsnapFile(inGsnapFileName,False)

	count = 0

	for r in result:

		if r.nLoci != 1:
			continue

		match = r.matchL()[0]

		for seg in match.segL:

			loc = mygenome.locus(seg[2])

			cursor.execute('select 1 from temp_table where chrom="%s" and pos>=%s and pos<=%s' % (loc.chrom,loc.chrSta+overlap,loc.chrEnd-overlap))

			if cursor.fetchone():
				eiH[loc.chrom][pos] += 1

		count += 1

		if count % 10000 == 0:
			print count

	outReportFile = open(outReportFileName,'w')

	for chrom in ei_keyH.keys():

		for e in ei_keyH[chrom]:

			if eiH[chrom][e]==[]:
				continue

			outReportFile.write('%s\t%s\t%s\t%s\n' % (sampN, '%s:%s' % (chrom,e), ','.join(juncInfoH[chrom][e]), eiH[chrom][e]))


con = MySQLdb.connect(host="localhost", user="cancer", passwd="cancer", db="ircr1")

con.autocommit = True
cursor = con.cursor()

cursor.execute('drop table if exists temp_table')

cursor.execute('''
create table temp_table (
	chrom varchar(15),
	pos int,
	primary key (chrom,pos),
	index (chrom)
);
''')


optL, argL = getopt.getopt(sys.argv[1:],'i:o:s:',[])

optH = mybasic.parseParam(optL)

if '-s' in optH:
	sampN = optH['-s']
else:
	sampN = optH['-i']

#main(optH['-i'], optH['-o'], sampN, ['EGFR'], 10)
main(optH['-i'], optH['-o'], sampN, ['MET', 'PDGFRA', 'RET', 'EGFR', 'EPHA1', 'EPHA2', 'EPHA3', 'EPHA4', 'EPHA5', 'EPHA6', 'EPHA7', 'EPHA8', 'EPHA10', 'FGFR1', 'FGFR2', 'FGFR3', 'FGFR4', 'FLT1', 'FLT3', 'FLT4'], 10)
#main(optH['-i'], optH['-o'], sampN, [], 10)
