/*drop table IF EXISTS mutation_rsq;
CREATE TABLE mutation_rsq (
	samp_id varchar(63) NOT NULL,
	chrom varchar(31) NOT NULL, -- hg19
	chrSta int unsigned NOT NULL,
	chrEnd int unsigned NOT NULL,
	ref varchar(63) NOT NULL,
	alt varchar(63) NOT NULL,
	r_nReads_ref mediumint unsigned NOT NULL,
	r_nReads_alt mediumint unsigned NOT NULL,
	strand char(1) NOT NULL,
	gene_symL varchar(63),
	ch_dna varchar(63),
	ch_aa varchar(63),
	ch_type varchar(127),
	cosmic text,
	mutsig text,
	index (samp_id,gene_symL),
	index (samp_id,chrom,chrSta,chrEnd),
	index (samp_id,chrom,chrSta,ref,alt),
	index (samp_id,chrom,chrSta,chrEnd,ref,alt)
);*/

/* LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/results/mutation/NSL_GBM_mutation_Rsq_45.dat" INTO TABLE mutation_rsq; */
LOAD DATA LOCAL INFILE "/EQL2/SGI_20131031/RNASeq/results/mutation/mutation_Rsq_30.dat" INTO TABLE mutation_rsq;
