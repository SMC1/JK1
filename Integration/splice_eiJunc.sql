/*drop table IF EXISTS splice_eiJunc;

CREATE TABLE splice_eiJunc (
	samp_id varchar(63) NOT NULL,
	loc varchar(31) NOT NULL, -- hg19
	gene_sym varchar(31) NOT NULL,
	juncInfo text,
	juncAlias varchar(7),
	isLastExon char(1),
	nReads int unsigned,
	primary key (samp_id,loc)
);*/

/* LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/alignment/splice_eiJunc_NSL36_ft2.dat" INTO TABLE splice_eiJunc; */
/* LOAD DATA LOCAL INFILE "/EQL3/TCGA/GBM/RNASeq/alignment/splice_eiJunc_170_ft2.dat" INTO TABLE splice_eiJunc; */
/* LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/alignment/splice_eiJunc_NSL41_ft_n1.dat" INTO TABLE splice_eiJunc; */
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/results/eiJunc/splice_eiJunc_NSL45.dat" INTO TABLE splice_eiJunc;*/
/*LOAD DATA LOCAL INFILE "/EQL2/SGI_20131031/RNASeq/results/eiJunc/splice_eiJunc_30.dat" INTO TABLE splice_eiJunc;*/
LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/results/eiJunc/splice_eiJunc_SGI20131119_6.dat" INTO TABLE splice_eiJunc;
