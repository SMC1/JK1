DROP table IF EXISTS xsq_cn;
CREATE TABLE xsq_cn (
	samp_id varchar(63) NOT NULL,
	gene_sym varchar(31) NOT NULL,
	value_log2 double NOT NULL,
	primary key (samp_id,gene_sym),
	index (gene_sym)
);

/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/CNA/XSQ_CN_20140114_54.dat" INTO TABLE xsq_cn;
LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/CNA/XSQ_CN_20140121_2.dat" INTO TABLE xsq_cn;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/CNA/XSQ_CN_20140204_66.dat" INTO TABLE xsq_cn;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/CNA/XSQ_CN_20140206_72.dat" INTO TABLE xsq_cn;*/
/* restart using ngCGH */
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/CNA/XSQ_CN_20140212_61.dat" INTO TABLE xsq_cn;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/CNA/XSQ_CN_20140213_72.dat" INTO TABLE xsq_cn;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/CNA/XSQ_CN_20140217_82.dat" INTO TABLE xsq_cn;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/CNA/XSQ_CN_20140218_83.dat" INTO TABLE xsq_cn;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/CNA/XSQ_CN_20140228_89.dat" INTO TABLE xsq_cn;*/
LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/CNA/XSQ_CN_20140304_92.dat" INTO TABLE xsq_cn;
