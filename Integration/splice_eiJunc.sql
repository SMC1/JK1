drop table IF EXISTS splice_eiJunc;

CREATE TABLE splice_eiJunc (
	samp_id varchar(63) NOT NULL,
	loc varchar(31) NOT NULL, -- hg19
	gene_sym varchar(31) NOT NULL,
	juncInfo text,
	juncAlias varchar(7),
	nReads int unsigned,
	primary key (samp_id,loc)
);

LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/alignment/splice_Z/ei_junc/splice_eiJunc_NSL_RTK1.dat" INTO TABLE splice_eiJunc;
