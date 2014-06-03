#!/usr/bin/python

from glob import glob
import sys,os,re
import mysetting, mymysql
from mysetting import mysqlH

moduleL = ['Integration']
homeDir = os.popen('echo $HOME','r').read().rstrip()

for module in moduleL:
	sys.path.append('%s/JK1/%s' % (homeDir, module))
import prepDB_mutation_normal, makeDB_mutation_rxsq

def prep_single(outFileN, server='smc1', dbN='ircr1'):
	(con, cursor) = mymysql.connectDB(user=mysetting.mysqlH[server]['user'],passwd=mysetting.mysqlH[server]['passwd'],db=dbN,host=mysetting.mysqlH[server]['host'])
	cosmicL = []
	for dir in mysetting.wxsMutscanDirL:
		cosmicL += filter(lambda x: '_B_' not in x, glob('%s/*/*cosmic.dat' % dir) + glob('%s/*cosmic.dat' % dir))

	cursor.execute('SELECT DISTINCT samp_id FROM sample_tag WHERE tag LIKE "XSeq_%%"')
	results = cursor.fetchall()
	sidL = []
	for res in results:
		sidL.append(res[0])
	for cosmic in cosmicL:
		(sid, postfix, platform) = re.match('(.*)_([XT].{,2})_([STKN]{2})_cosmic.dat', os.path.basename(cosmic)).groups()
		if postfix not in ['T', 'RSq']:
			sid = '%s_%s' % (sid, postfix)
		if sid not in sidL:
			print sid, cosmic
			tag = 'XSeq_%s' % platform
			cursor.execute('INSERT INTO sample_tag SET samp_id="%s", tag="%s"' % (sid, tag))

	cmd = 'cat %s | python ~/JK1/Integration/prepDB_mutscan.py > %s' % (' '.join(cosmicL), outFileN)
	os.system(cmd)

def load_mutation(inFileN, server='smc1', dbN='ircr1'):
	(con, cursor) = mymysql.connectDB(user=mysetting.mysqlH[server]['user'],passwd=mysetting.mysqlH[server]['passwd'],db=dbN,host=mysetting.mysqlH[server]['host'])

	cursor.execute('DROP TABLE IF EXISTS mutation')
	stmt = '''
	CREATE TABLE mutation (
		samp_id varchar(63) NOT NULL,
		chrom varchar(10) NOT NULL,
		chrSta int unsigned NOT NULL,
		chrEnd int unsigned NOT NULL,
		ref varchar(63) NOT NULL,
		alt varchar(63) NOT NULL,
		nReads_ref mediumint unsigned NOT NULL,
		nReads_alt mediumint unsigned NOT NULL,
		strand char(1) NOT NULL,
		gene_symL varchar(63),
		ch_dna varchar(63),
		ch_aa varchar(63),
		ch_type varchar(63),
		cosmic text,
		mutsig text,
		index (samp_id,gene_symL),
		index (samp_id,chrom,chrSta,chrEnd),
		index (samp_id,chrom,chrSta,ref,alt),
		index (samp_id,chrom,chrSta,chrEnd,ref,alt)
	)'''
	cursor.execute(stmt)
	cursor.execute('LOAD DATA LOCAL INFILE "%s" INTO TABLE mutation' % inFileN)

def prep_somatic(outFileN, server='smc1', dbN='ircr1'):
	(con, cursor) = mymysql.connectDB(user=mysetting.mysqlH[server]['user'],passwd=mysetting.mysqlH[server]['passwd'],db=dbN,host=mysetting.mysqlH[server]['host'])
	cursor.execute('SELECT DISTINCT samp_id,tag FROM sample_tag WHERE tag LIKE "XSeq_%%"')
	results = cursor.fetchall()
	singleL = []
	somaticL = []
	for res in results:
		pl_typeL = re.match('XSeq_(.*)', res[1]).group(1).split(',')
		if 'N' in pl_typeL:
			somaticL.append(res[0])
		else:
			singleL.append(res[0])
	cmd = 'cat %s/*mutect_vep.dat | python ~/JK1/Integration/prepDB_mutation_mutect.py > %s' % (mysetting.wxsMutectDir, outFileN)
	os.system(cmd)
	mutectL = glob('%s/*mutect_vep.dat' % mysetting.wxsMutectDir)
	for mutect in mutectL:
		(sid, postfix, platform) = re.match('(.*)_([XT].{,2})_([STKN]{2}).mutect_vep.dat', os.path.basename(mutect)).groups()
		if postfix not in ['T']:
			sid = '%s_%s' % (sid, postfix)
		if sid in somaticL:
			continue
		else:
			if sid in singleL:
				##previously analyzed without matched normal
				cursor.execute('SELECT samp_id,tag FROM sample_tag WHERE samp_id="%s" AND tag LIKE "XSeq_%%"' % sid)
				results = cursor.fetchall()
				if len(results)>1:
					sys.stderr.write('Duplication in sample_tag: %s\n' % sid)
					sys.exit(1)
				tag = '%s,N' % results[0][1]
				cursor.execute('UPDATE sample_tag SET samp_id="%s", tag="%s" WHERE samp_id="%s" AND tag LIKE "XSeq_%%"' % (sid, tag, sid))
			else:
				##brand new sample
				tag = 'XSeq_%s,N' % platform
				cursor.execute('INSERT INTO sample_tag SET samp_id="%s", tag="%s"' % (sid, tag))
		#if

def load_mutation_all(inFileN, server='smc1', dbN='ircr1'):
	(con, cursor) = mymysql.connectDB(user=mysetting.mysqlH[server]['user'],passwd=mysetting.mysqlH[server]['passwd'],db=dbN,host=mysetting.mysqlH[server]['host'])

	cursor.execute('DROP TABLE IF EXISTS mutation_normal')
	stmt = '''
	CREATE TABLE mutation_normal (
		samp_id varchar(63) NOT NULL,
		chrom varchar(10) NOT NULL,
		chrSta int unsigned NOT NULL,
		chrEnd int unsigned NOT NULL,
		ref varchar(15) NOT NULL,
		alt varchar(15) NOT NULL,
		n_nReads_ref mediumint unsigned NOT NULL,
		n_nReads_alt mediumint unsigned NOT NULL,
		nReads_ref mediumint unsigned NOT NULL,
		nReads_alt mediumint unsigned NOT NULL,
		strand char(1) NOT NULL,
		gene_symL varchar(63),
		ch_dna varchar(127),
		ch_aa varchar(63),
		ch_type varchar(127),
		cosmic text,
		mutsig text,
		index (samp_id,gene_symL),
		index (samp_id,chrom,chrSta,chrEnd),
		index (samp_id,chrom,chrSta,ref,alt),
		index (samp_id,chrom,chrSta,chrEnd,ref,alt)
	)
	'''
	cursor.execute(stmt)
	cursor.execute('CREATE TEMPORARY TABLE tmp LIKE mutation_normal')
	cursor.execute('LOAD DATA LOCAL INFILE "%s" INTO TABLE tmp' % inFileN)
	cursor.execute('CREATE TEMPORARY TABLE t2 SELECT tmp.samp_id,tmp.chrom,tmp.chrSta,tmp.chrEnd,tmp.ref,tmp.alt,tmp.n_nReads_ref,tmp.n_nReads_alt,tmp.nReads_ref,tmp.nReads_alt,tmp.strand,tmp.gene_symL,tmp.ch_dna,tmp.ch_aa,tmp.ch_type,cosmic.ch_aaL AS cosmic,cosmic.ch_typeL AS cosmic_type,tmp.mutsig FROM tmp LEFT JOIN cosmic ON tmp.chrom=cosmic.chrom AND tmp.chrSta=cosmic.chrSta AND tmp.chrEnd=cosmic.chrEnd AND tmp.ref=cosmic.ref AND tmp.alt=cosmic.alt AND tmp.gene_symL=cosmic.gene_symL')
	cursor.execute('INSERT INTO mutation_normal SELECT samp_id,chrom,chrSta,chrEnd,ref,alt,n_nReads_ref,n_nReads_alt,nReads_ref,nReads_alt,strand,gene_symL,ch_dna,ch_aa,ch_type,"" AS cosmic,mutsig FROM t2 WHERE cosmic IS NULL')
	cursor.execute('INSERT INTO mutation_normal SELECT samp_id,chrom,chrSta,chrEnd,ref,alt,n_nReads_ref,n_nReads_alt,nReads_ref,nReads_alt,strand,gene_symL,ch_dna,cosmic AS ch_aa,cosmic_type AS ch_type,cosmic,mutsig FROM t2 WHERE cosmic IS NOT NULL')

def main(singleFileN, somaticFileN, allFileN, server='smc1', dbN='ircr1'):
	if not os.path.isfile(singleFileN):
		prep_single(singleFileN, server, dbN)
		load_mutation(singleFileN, server, dbN)

	if not os.path.isfile(somaticFileN):
		prep_somatic(somaticFileN, server, dbN)
	
	if not os.path.isfile(allFileN):
		prepDB_mutation_normal.main(inTFileName=singleFileN, inNFileName=somaticFileN, geneList=[], outFileN=allFileN)
		load_mutation_all(allFileN, server, dbN)
		makeDB_mutation_rxsq.main(dbN)

if __name__ == '__main__':
#	main(singleFileN='single', somaticFileN='somatic', allFileN='all', server='smc1', dbN='ihlee_test')
