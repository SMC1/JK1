#!/usr/bin/python

import sys, cgi, re
import mymysql

dbN = 'ircr1' # 'tcga1'

(con,cursor) = mymysql.connectDB(db=dbN)

cursor.execute('drop table if exists mutation_rxsq')

cursor.execute('create temporary table t_m as \
	select n.samp_id,n.chrom,n.chrSta,n.chrEnd,n.ref,n.alt,n.n_nReads_ref,n.n_nReads_alt,n.nReads_ref,n.nReads_alt,r.r_nReads_ref,r.r_nReads_alt,n.strand,n.gene_symL,n.ch_dna,n.ch_aa,n.ch_type,n.cosmic,n.mutsig \
	from mutation_normal n left join mutation_rsq r \
	on n.samp_id = r.samp_id and n.chrom=r.chrom and n.chrSta=r.chrSta and n.ref=r.ref and n.alt=r.alt \
	union \
	select r.samp_id,r.chrom,r.chrSta,r.chrEnd,r.ref,r.alt,n.n_nReads_ref,n.n_nReads_alt,n.nReads_ref,n.nReads_alt,r.r_nReads_ref,r.r_nReads_alt,r.strand,r.gene_symL,r.ch_dna,r.ch_aa,r.ch_type,r.cosmic,r.mutsig \
	from mutation_normal n right join mutation_rsq r \
	on n.samp_id = r.samp_id and n.chrom=r.chrom and n.chrSta=r.chrSta and n.ref=r.ref and n.alt=r.alt')

cursor.execute('create table mutation_rxsq as \
	select * from (select * from t_m order by ch_dna desc) as i group by samp_id,chrom,chrSta,ref,alt,ch_aa')

cursor.execute('update mutation_rxsq set r_nReads_ref = 0, r_nReads_alt = 0 where r_nReads_ref is null')
cursor.execute('update mutation_rxsq set n_nReads_ref = 0, n_nReads_alt = 0 where n_nReads_ref is null')
cursor.execute('update mutation_rxsq set nReads_ref = 0, nReads_alt = 0 where nReads_ref is null')

cursor.execute('alter table mutation_rxsq add index (samp_id,gene_symL)')
cursor.execute('alter table mutation_rxsq add index (samp_id,chrom,chrSta,chrEnd)')
cursor.execute('alter table mutation_rxsq add index (samp_id,chrom,chrSta,ref,alt)')
cursor.execute('alter table mutation_rxsq add index (samp_id,chrom,chrSta,chrEnd,ref,alt)')
