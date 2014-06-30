DROP table IF EXISTS xsq_clonality;
CREATE TABLE xsq_clonality (
	samp_id varchar(63) NOT NULL,
	chrom varchar(15) NOT NULL,
	chrSta int unsigned NOT NULL,
	chrEnd int unsigned NOT NULL,
	ref varchar(15) NOT NULL,
	alt varchar(15) NOT NULL,
	clonality  varchar(10) NOT NULL,
	index (samp_id,chrom,chrSta,chrEnd),
	index (samp_id,chrom,chrSta,chrEnd,ref,alt)
);

/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/Clonality/XSQ_clonality_20140409.dat" INTO TABLE xsq_phylotree;*/
LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/Clonality/XSQ_clonality_20140414.dat" INTO TABLE xsq_phylotree;
