drop table IF EXISTS rpkm_subtype;
/*CREATE TABLE rpkm_subtype (
	samp_id char(12),
	P float,
	U float,
	C float,
	M float,
	subtype char(1),
	primary key (samp_id)
);*/

CREATE TABLE rpkm_subtype (
	samp_id char(12),
	P float,
	N float,
	C float,
	M float,
	U float,
	subtype char(1),
	primary key (samp_id)
);

LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/NSL_GBM_RPKM_118_subtype.dat" INTO TABLE rpkm_subtype;
