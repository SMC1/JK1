drop table IF EXISTS xsq_loh;
CREATE TABLE xsq_loh (
	samp_id varchar(63) NOT NULL,
	gene_sym varchar(63) NOT NULL,
	loh varchar(6) NOT NULL
);

LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/LOH/XSQ_LOH_20140526.dat" INTO TABLE xsq_loh;
