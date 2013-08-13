drop table IF EXISTS array_gene_expr_ori;
CREATE TABLE array_gene_expr_ori (
	samp_id varchar(63) NOT NULL,
	gene_sym varchar(31) NOT NULL,
	value double NOT NULL,
	primary key (samp_id,gene_sym),
	index (gene_sym),
	index (samp_id),
	index (samp_id,gene_sym,value)
);

/* LOAD DATA LOCAL INFILE "/EQL1/TCGA/GBM/array_gene/TCGA_GBM_gene_BI_sIdClps.dat" INTO TABLE array_gene_expr_ori; */
LOAD DATA LOCAL INFILE "/EQL1/NSL/array_gene/NSL_GBM_93.dat" INTO TABLE array_gene_expr_ori;
