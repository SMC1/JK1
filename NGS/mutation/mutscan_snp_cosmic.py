#!/usr/bin/python

import sys, os, re, getopt
import mybasic, mymysql
from mysetting import mysqlH


def main(dirN,inFileN,outFileN,sampN,server='smc1'):
	(con, cursor) = mymysql.connectDB(user=mysqlH[server]['user'], passwd=mysqlH[server]['passwd'], host=mysqlH[server]['host'], db='ircr1')

	cursor.execute('''
create temporary table t1 (
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

	cursor.execute('load data local infile "%s/%s" into table t1' % (dirN,inFileN))

	cursor.execute('''select \
		"%s",t1.chrom,t1.pos,t1.pos, t1.ref,t1.alt, reads1,reads2, \
		cosmic.strand,cosmic.gene_symL,ch_dnaL,ch_aaL,ch_typeL \
		from t1 join cosmic on t1.chrom=cosmic.chrom and t1.pos=cosmic.chrSta and t1.ref=cosmic.ref and t1.alt=cosmic.alt \
		where cosmic.chrSta=cosmic.chrEnd into outfile "%s/%s"
''' % (sampN,dirN,outFileN))

if __name__ == '__main__':
	optL, argL = getopt.getopt(sys.argv[1:],'d:i:o:s:v:b:',[])

	optH = mybasic.parseParam(optL)
	server='smc1'
	if '-v' in optH:
		server = optH['-v']

	main(optH['-d'],optH['-i'],optH['-o'],optH['-s'], server=server)
