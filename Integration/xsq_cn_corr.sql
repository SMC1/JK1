DROP table IF EXISTS xsq_cn_corr;
CREATE TABLE xsq_cn_corr (
	samp_id varchar(63) NOT NULL,
	gene_sym varchar(31) NOT NULL,
	value_log2 double NOT NULL,
	primary key (samp_id,gene_sym),
	index (gene_sym)
);

/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/CNA/XSQ_CNCORR_20140326_51.dat" INTO TABLE xsq_cn_corr;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/CNA/XSQ_CNCORR_20140403_54.dat" INTO TABLE xsq_cn_corr;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/CNA/XSQ_CNCORR_20140408_55.dat" INTO TABLE xsq_cn_corr;*/
LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/CNA/XSQ_CNCORR_20140414_57.dat" INTO TABLE xsq_cn_corr;
