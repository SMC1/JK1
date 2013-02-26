drop table IF EXISTS cosmic;
CREATE TABLE cosmic (
	chrom varchar(31) NOT NULL, -- hg19
	chrSta int unsigned NOT NULL,
	chrEnd int unsigned NOT NULL,
	strand char(1) NOT NULL,
	ref varchar(63),
	alt varchar(63),
	gene_symL varchar(31),
	ch_dnaL varchar(63),
	ch_aaL varchar(63),
	ch_typeL varchar(127),
	index (chrom,chrSta,chrEnd),
	index (chrom,chrSta,ref,alt),
	index (chrom,chrSta,chrEnd,ref,alt)
);

LOAD DATA LOCAL INFILE "/data1/Sequence/cosmic/cosmic.dat" INTO TABLE cosmic;
