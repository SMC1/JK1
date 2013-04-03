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

/* LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/alignment/splice_eiJunc_NSL.dat" INTO TABLE splice_eiJunc; */
/* LOAD DATA LOCAL INFILE "/EQL3/TCGA/GBM/RNASeq/alignment/splice_eiJunc_170_RTK1.dat" INTO TABLE splice_eiJunc; */

LOAD DATA LOCAL INFILE "/EQL3/TCGA/GBM/RNASeq/alignment/splice_eiJunc_170.dat" INTO TABLE splice_eiJunc;
