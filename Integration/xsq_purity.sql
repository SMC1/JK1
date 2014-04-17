drop table IF EXISTS xsq_purity;

CREATE TABLE xsq_purity (
	samp_id varchar(63) NOT NULL,
	normal_frac varchar(10) NOT NULL,
	tumor_frac varchar(10) NOT NULL,
	primary key (samp_id)
);

/*LOAD DATA LOCAL INFILE "/EQL1/NSL/exome_bam/purity/NSL_GBM_xsq_tumor_frac.txt" INTO TABLE xsq_purity;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/Purity/XSQ_Purity_20140219_72.dat" INTO TABLE xsq_purity;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/Purity/XSQ_Purity_20140228_78.dat" INTO TABLE xsq_purity;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/Purity/XSQ_Purity_20140304_81.dat" INTO TABLE xsq_purity;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/Purity/XSQ_Purity_20140403_84.dat" INTO TABLE xsq_purity;*/
/*LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/Purity/XSQ_Purity_20140408_86.dat" INTO TABLE xsq_purity;*/
LOAD DATA LOCAL INFILE "/EQL1/NSL/WXS/results/Purity/XSQ_Purity_20140414_88.dat" INTO TABLE xsq_purity;
