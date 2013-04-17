drop table IF EXISTS splice_fusion;
CREATE TABLE splice_fusion (
	samp_id varchar(63) NOT NULL,
	loc1 varchar(31) NOT NULL, -- hg19
	loc2 varchar(31) NOT NULL,
	gene_sym1 varchar(31),
	gene_sym2 varchar(31),
	ftype varchar(15) NOT NULL,
	exon1 text,
	exon2 text,
	frame text,
	nReads int unsigned NOT NULL,
	nPos int unsigned NOT NULL,
	primary key (samp_id,loc1,loc2)
);

/* LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/alignment/splice_fusion_NSL36_p1.dat" IGNORE INTO TABLE splice_fusion; */
LOAD DATA LOCAL INFILE "/EQL3/TCGA/GBM/RNASeq/alignment/splice_fusion_170_p1.dat" IGNORE INTO TABLE splice_fusion;
