drop table IF EXISTS rpkm_pathway;
CREATE TABLE rpkm_pathway (
	samp_id varchar(63) NOT NULL,
	pathway varchar(31) NOT NULL,
	activity double NOT NULL,
	primary key (samp_id,pathway),
	index (pathway),
	index (samp_id),
	index (samp_id,pathway,activity)
);

LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/NSL_GBM_RPKM_45_pathway_NTP.dat" INTO TABLE rpkm_pathway;
