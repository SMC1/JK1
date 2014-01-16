DROP table IF EXISTS xsq_cn;
CREATE TABLE xsq_cn (
	samp_id varchar(63) NOT NULL,
	gene_sym varchar(31) NOT NULL,
	value_log2 double NOT NULL,
	primary key (samp_id,gene_sym),
	index (gene_sym)
);

LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/CNA/XSQ_CN_20140114_54.dat" INTO TABLE xsq_cn;
