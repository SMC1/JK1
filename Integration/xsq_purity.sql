drop table IF EXISTS xsq_purity;

CREATE TABLE xsq_purity (
	samp_id varchar(63) NOT NULL,
	normal_frac double NOT NULL,
	tumor_frac double NOT NULL,
	primary key (samp_id)
);

LOAD DATA LOCAL INFILE "/EQL1/NSL/exome_bam/purity/NSL_GBM_xsq_tumor_frac.txt" INTO TABLE xsq_purity;
