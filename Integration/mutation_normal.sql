drop table IF EXISTS mutation_normal;
CREATE TABLE mutation_normal (
	samp_id varchar(63) NOT NULL,
	chrom varchar(31) NOT NULL, -- hg19
	chrSta int unsigned NOT NULL,
	chrEnd int unsigned NOT NULL,
	ref varchar(63) NOT NULL,
	alt varchar(63) NOT NULL,
	n_nReads_ref mediumint unsigned NOT NULL,
	n_nReads_alt mediumint unsigned NOT NULL,
	nReads_ref mediumint unsigned NOT NULL,
	nReads_alt mediumint unsigned NOT NULL,
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
);

/* LOAD DATA LOCAL INFILE "/EQL1/NSL/Exome/mutation_cosmic_NSL27.dat" INTO TABLE mutation; */
/* LOAD DATA LOCAL INFILE "/EQL1/TCGA/GBM/mutation/TCGA_GBM_mutation.dat" INTO TABLE mutation; */
/* LOAD DATA LOCAL INFILE "/EQL1/NSL/exome_bam/mutation/NSL_GBM_mutation_13.dat" INTO TABLE mutation_normal; */
LOAD DATA LOCAL INFILE "/EQL1/NSL/exome_bam/mutation/NSL_GBM_NT_mutation_45.dat" INTO TABLE mutation_normal;
