#!/usr/bin/python

import sys, os, re, getopt, MySQLdb
import mybasic


def main(dirN,inFileN,outFileN,sampN):

	cursor.execute('''
create temporary table t1 (
	chrom varchar(31),
	pos int unsigned,
	ref char(31),
	cons char(31),
	reads1 int unsigned,
	reads2 int unsigned,
	freq varchar(31),
	strands1 tinyint unsigned,
	strands2 tinyint unsigned,
	qual1 mediumint unsigned,
	qual2 mediumint unsigned,
	pval double,
	mapqual1 mediumint unsigned,
	mapqual2 mediumint unsigned,
	reads1plus int unsigned,
	reads1minus int unsigned,
	reads2plus int unsigned,
	reads2minus int unsigned,
	alt char(31),
	index (chrom,pos,ref,alt)
);
''')

	cursor.execute('load data local infile "%s/%s" into table t1' % (dirN,inFileN))

	cursor.execute('''select \
		"%s",t1.chrom,t1.pos,t1.pos, t1.ref,t1.alt, reads1,reads2, \
		cosmic.strand,cosmic.gene_symL,ch_dnaL,ch_aaL,ch_typeL \
		from t1 join cosmic on t1.chrom=cosmic.chrom and t1.pos=cosmic.chrSta and t1.ref=cosmic.ref and t1.alt=cosmic.alt \
		where cosmic.chrSta=cosmic.chrEnd into outfile "%s/%s"
''' % (sampN,dirN,outFileN))


con = MySQLdb.connect(host="localhost", user="cancer", passwd="cancer", db="ircr1")

con.autocommit = True
cursor = con.cursor()

optL, argL = getopt.getopt(sys.argv[1:],'d:i:o:s:',[])

optH = mybasic.parseParam(optL)

main(optH['-d'],optH['-i'],optH['-o'],optH['-s'])
