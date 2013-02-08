drop table IF EXISTS splice_skip;
CREATE TABLE splice_skip (
	samp_id varchar(63) NOT NULL,
	loc1 varchar(31) NOT NULL, -- hg19
	loc2 varchar(31) NOT NULL,
	gene_sym varchar(31) NOT NULL,
	exon1 text,
	exon2 text,
	frame text,
	nPos int unsigned NOT NULL,
	primary key (samp_id,loc1,loc2)
);

LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/alignment/splice_skip_NSL36_EGFR_n2.dat" INTO TABLE splice_skip;
