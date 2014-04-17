drop table IF EXISTS mutation;
CREATE TABLE mutation (
	samp_id varchar(63) NOT NULL,
	chrom varchar(31) NOT NULL, -- hg19
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
	ch_type varchar(127),
	cosmic text,
	mutsig text,
	index (samp_id,gene_symL),
	index (samp_id,chrom,chrSta,chrEnd),
	index (samp_id,chrom,chrSta,ref,alt),
	index (samp_id,chrom,chrSta,chrEnd,ref,alt)
);

/* LOAD DATA LOCAL INFILE "/data1/CCLE_Sanger/mutation_CCLE.dat" INTO TABLE mutation; */
/* LOAD DATA LOCAL INFILE "/EQL1/NSL/Exome/mutation_cosmic_NSL27.dat" INTO TABLE mutation; */
/* LOAD DATA LOCAL INFILE "/EQL1/TCGA/GBM/mutation/TCGA_GBM_mutation.dat" INTO TABLE mutation; */
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/mutation/NSL_GBM_mutation_45.dat" INTO TABLE mutation;*/
/**LOAD DATA LOCAL INFILE "/EQL2/SGI_20131119/WXS/results/mutation/mutation_single_30.dat" INTO TABLE mutation; **/ /* has mutations for 30 samples only */
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/mutation/mutation_single_20140106.dat" INTO TABLE mutation;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/mutation/mutation_single_20140121.dat" INTO TABLE mutation;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/mutation/mutation_single_20140204.dat" INTO TABLE mutation;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/mutation/mutation_single_20140217.dat" INTO TABLE mutation;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/mutation/mutation_single_20140228.dat" INTO TABLE mutation;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/mutation/mutation_single_20140304.dat" INTO TABLE mutation;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/mutation/mutation_single_20140403.dat" INTO TABLE mutation;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/mutation/mutation_single_20140409.dat" INTO TABLE mutation;*/
LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/mutation/mutation_single_20140414.dat" INTO TABLE mutation;
