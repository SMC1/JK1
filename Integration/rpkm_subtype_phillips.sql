drop table IF EXISTS rpkm_subtype_phillips;
CREATE TABLE rpkm_subtype_phillips (
	samp_id char(12),
	PN float,
	MES float,
	subtype char(3),
	primary key (samp_id)
);

/*drop table IF EXISTS rpkm_subtype_phillips;
CREATE TABLE rpkm_subtype_phillips (
	samp_id char(12),
	PN float,
	MES float,
	PRO float,
	subtype char(3),
	primary key (samp_id)
);*/

/*LOAD DATA LOCAL INFILE "/EQL1/Phillips/Phillips_U133A_subtype_metagene.dat" INTO TABLE rpkm_subtype_phillips;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/NSL_GBM_RPKM_45_phillips_subtype.dat" INTO TABLE rpkm_subtype_phillips;*/
LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/NSL_GBM_RPKM_45_subtype_metagene.dat" INTO TABLE rpkm_subtype_phillips;
