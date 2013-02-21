drop table IF EXISTS splice_skip;
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
);

LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/alignment/splice_skip_NSL36_p5.dat" INTO TABLE splice_skip;
