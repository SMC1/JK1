#!/usr/bin/python

import sys, os, re, getopt, MySQLdb
import mybasic

def annotate_join_cosmic(inDirName, sampN, outDirName):

	mutscanFL = filter(lambda x: re.match('(.*)\.mutscan$', x), os.listdir(inDirName))

	vep_out=inDirName + '/' + sampN + '.vep'
	mutscanFN = filter(lambda x: re.match(sampN, x), mutscanFL)
	mutscanFN = inDirName + '/' + mutscanFN[0]
	## make tab-delimited txt for mysql
	vepF = open(vep_out);
	veplines = vepF.readlines();
	vepF.close()
	tmpN = inDirName + '/' + sampN + '.tmp'
	outF = open(tmpN, 'w')
	for line in veplines:
		if line[0] == '#':
			continue
		cols = line[:-1].split('\t')
		key_cols = cols[0].split('_')
		chr = key_cols[0]
		pos = key_cols[1]
		ref = key_cols[2].split('/')[0]
		alt = cols[2]

		if (chr[0].upper() != 'C'):
			chr = 'chr%s' % (chr)

		if (chr.upper() == 'CHRX'):
			chr = 'chr23'
		elif (chr.upper() == 'CHRY'):
			chr = 'chr24'
		elif (chr.upper() == 'CHRM' or chr.upper() == 'CHRMT'):
			chr = 'chr25'

		outF.write('%s\t%s\t%s\t%s\t%s\n' % (chr,pos,ref,alt,"\t".join(cols[3:])))

	outF.close()

	## connect to mysql db
	con = MySQLdb.connect(host="localhost", user="cancer", passwd="cancer", db="ircr1")
	con.autocommit = True
	cursor = con.cursor()

	cursor.execute('''
CREATE TEMPORARY TABLE t1 (
chrom varchar(31),
pos int unsigned,
ref char(31),
alt char(31),
gene varchar(31),
transcript varchar(31),
type varchar(31),
effect varchar(255),
cDNAPos varchar(15),
CDSPos varchar(15),
ProtPos varchar(15),
AA char(31),
codon varchar(31),
ids varchar(255),
extra varchar(7000),
index (chrom,pos,ref,alt)
);
''')

	cursor.execute('LOAD DATA LOCAL INFILE "%s" INTO TABLE t1' % (tmpN))
		
	cursor.execute('''
CREATE TEMPORARY TABLE t2 (
chrom varchar(31),
pos int unsigned,
ref char(31),
alt char(31),
reads1 int unsigned,
reads2 int unsigned,
freq varchar(31),
index (chrom,pos,ref,alt)
);
''')
	cursor.execute('LOAD DATA LOCAL INFILE "%s" INTO TABLE t2' % (mutscanFN))

	## join mutscan + cosmic first, only on snps
	cursor.execute('CREATE TEMPORARY TABLE t3 SELECT t2.chrom,t2.pos,t2.ref,t2.alt,t2.reads1,t2.reads2,t2.freq,cosmic.strand,cosmic.gene_symL,ch_dnaL,ch_aaL,ch_typeL FROM t2 JOIN cosmic ON t2.chrom=cosmic.chrom AND t2.pos=cosmic.chrSta AND t2.ref=cosmic.ref AND t2.alt=cosmic.alt WHERE cosmic.chrSta=cosmic.chrEnd;')

	cursor.execute('SELECT t1.chrom,t1.pos,t1.pos,t1.ref,t1.alt,reads1,reads2,t3.strand,t3.gene_symL,ch_dnaL,ch_aaL,ch_typeL,gene,transcript,effect,cDNAPos,CDSPos,ProtPos,AA,codon,ids,extra FROM t1 JOIN t3 ON t1.chrom=t3.chrom AND t1.pos=t3.pos and t1.ref=t3.ref AND t1.alt=t3.alt INTO OUTFILE "%S";' % (outDirName + '/' + sampN + '_cosmic.dat'))

	con.close()

optL, argL = getopt.getopt(sys.argv[1:], 'i:s:o:', [])
optH = mybasic.parseParam(optL)

annotate_join_cosmic(optH['-i'], optH['-s'], optH['-o'])
