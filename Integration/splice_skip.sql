/*drop table IF EXISTS splice_skip;
CREATE TABLE splice_skip (
	samp_id varchar(63) NOT NULL,
	loc1 varchar(31) NOT NULL, -- hg19
	loc2 varchar(31) NOT NULL,
	gene_sym varchar(31) NOT NULL,
	frame text,
	delExons varchar(63),
	exon1 text,
	exon2 text,
	nReads mediumint unsigned NOT NULL,
	nPos tinyint unsigned NOT NULL,
	primary key (samp_id,loc1,loc2),
	index (samp_id,delExons)
);*/

/* LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/alignment/splice_skip_NSL36_p5.dat" IGNORE INTO TABLE splice_skip; */
/* LOAD DATA LOCAL INFILE "/EQL3/TCGA/GBM/RNASeq/alignment/splice_skipping_170_p5.dat" IGNORE INTO TABLE splice_skip; */
/* LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/alignment/splice_skip_NSL41_p5.dat" IGNORE INTO TABLE splice_skip; */
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/results/exonSkip/splice_skip_NSL45.dat" IGNORE INTO TABLE splice_skip; */
/*LOAD DATA LOCAL INFILE "/EQL2/SGI_20131031/RNASeq/results/exonSkip/splice_skip_30.dat" IGNORE INTO TABLE splice_skip;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/results/exonSkip/splice_skip_SGI20131119_6.dat" INTO TABLE splice_skip;*/
LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/results/exonSkip/splice_skip_SGI20131212_6.dat" INTO TABLE splice_skip;
