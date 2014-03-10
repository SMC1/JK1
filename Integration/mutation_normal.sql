drop table IF EXISTS mutation_normal;
CREATE TABLE mutation_normal (
	samp_id varchar(63) NOT NULL,
--	chrom varchar(31) NOT NULL, -- hg19*/
	chrom varchar(15) NOT NULL, -- hg19
	chrSta int unsigned NOT NULL,
	chrEnd int unsigned NOT NULL,
--	ref varchar(63) NOT NULL,
--	alt varchar(63) NOT NULL,
	ref varchar(15) NOT NULL,
	alt varchar(15) NOT NULL,
	n_nReads_ref mediumint unsigned NOT NULL,
	n_nReads_alt mediumint unsigned NOT NULL,
	nReads_ref mediumint unsigned NOT NULL,
	nReads_alt mediumint unsigned NOT NULL,
	strand char(1) NOT NULL,
	gene_symL varchar(63),
--	ch_dna varchar(63),
	ch_dna varchar(127),
	ch_aa varchar(63),
	ch_type varchar(127),
	cosmic text,
	mutsig text,
	index (samp_id,gene_symL),
	index (samp_id,chrom,chrSta,chrEnd),
	index (samp_id,chrom,chrSta,ref,alt),
	index (samp_id,chrom,chrSta,chrEnd,ref,alt)
);

/* LOAD DATA LOCAL INFILE "/EQL1/NSL/Exome/mutation_cosmic_NSL27.dat" INTO TABLE mutation; */
/* LOAD DATA LOCAL INFILE "/EQL1/TCGA/GBM/mutation/TCGA_GBM_mutation.dat" INTO TABLE mutation; */
/* LOAD DATA LOCAL INFILE "/EQL1/NSL/exome_bam/mutation/NSL_GBM_mutation_13.dat" INTO TABLE mutation_normal; */
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/exome_bam/mutation/NSL_GBM_NT_mutation_45.dat" INTO TABLE mutation_normal;*/

/* left join cosmic for cosmic annotation */
CREATE TEMPORARY TABLE tmp like mutation_normal;
/*LOAD DATA LOCAL INFILE "/EQL2/SGI_20131119/WXS/results/mutation/mutation_all_75.dat" INTO TABLE tmp;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/mutation/mutation_all_20140106.dat" INTO TABLE tmp;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/mutation/mutation_all_20140121.dat" INTO TABLE tmp;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/mutation/mutation_all_20140204.dat" INTO TABLE tmp;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/mutation/mutation_all_20140214.dat" INTO TABLE tmp;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/mutation/mutation_all_20140217.dat" INTO TABLE tmp;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/mutation/mutation_all_20140218.dat" INTO TABLE tmp;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/mutation/mutation_all_20140224.dat" INTO TABLE tmp;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/mutation/mutation_all_20140228.dat" INTO TABLE tmp;*/
LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/mutation/mutation_all_20140304.dat" INTO TABLE tmp;
CREATE TEMPORARY TABLE t2 SELECT tmp.samp_id,tmp.chrom,tmp.chrSta,tmp.chrEnd,tmp.ref,tmp.alt,tmp.n_nReads_ref,tmp.n_nReads_alt,tmp.nReads_ref,tmp.nReads_alt,tmp.strand,tmp.gene_symL,tmp.ch_dna,tmp.ch_aa,tmp.ch_type,cosmic.ch_aaL AS cosmic,cosmic.ch_typeL AS cosmic_type,tmp.mutsig FROM tmp LEFT JOIN cosmic ON tmp.chrom=cosmic.chrom AND tmp.chrSta=cosmic.chrSta AND tmp.chrEnd=cosmic.chrEnd AND tmp.ref=cosmic.ref AND tmp.alt=cosmic.alt AND tmp.gene_symL=cosmic.gene_symL;
INSERT INTO mutation_normal SELECT samp_id,chrom,chrSta,chrEnd,ref,alt,n_nReads_ref,n_nReads_alt,nReads_ref,nReads_alt,strand,gene_symL,ch_dna,ch_aa,ch_type,'' AS cosmic,mutsig FROM t2 WHERE cosmic IS NULL;
INSERT INTO mutation_normal SELECT samp_id,chrom,chrSta,chrEnd,ref,alt,n_nReads_ref,n_nReads_alt,nReads_ref,nReads_alt,strand,gene_symL,ch_dna,cosmic AS ch_aa,cosmic_type AS ch_type,cosmic,mutsig FROM t2 WHERE cosmic IS NOT NULL;
