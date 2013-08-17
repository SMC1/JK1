drop table IF EXISTS array_pathway;
CREATE TABLE array_pathway (
	samp_id varchar(63) NOT NULL,
	gene_sym varchar(31) NOT NULL,
	activity double NOT NULL,
	primary key (samp_id,gene_sym),
	index (gene_sym),
	index (samp_id),
	index (samp_id,gene_sym,activity)
);

/* LOAD DATA LOCAL INFILE "/EQL1/NSL/array_gene/NSL_GBM_93_zNorm.dat" INTO TABLE array_pathway; */
/* LOAD DATA LOCAL INFILE "/data1/CCLE_Sanger/array_pathway_CCLE.dat" INTO TABLE array_pathway; */
LOAD DATA LOCAL INFILE "/EQL1/NSL/array_gene/NSL_GBM_93_pathway_NTP.dat" INTO TABLE array_pathway;
