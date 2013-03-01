drop table IF EXISTS array_gene_expr;
CREATE TABLE array_gene_expr (
	samp_id varchar(63) NOT NULL,
	gene_sym varchar(31) NOT NULL,
	z_score double NOT NULL,
	primary key (samp_id,gene_sym),
	index (gene_sym)
);

/* LOAD DATA LOCAL INFILE "/EQL1/NSL/array_gene/NSL_GBM_93_zNorm.dat" INTO TABLE array_gene_expr; */
LOAD DATA LOCAL INFILE "/EQL1/TCGA/GBM/array_gene/TCGA_GBM_gene_BI_sIdClps_zNorm.dat" INTO TABLE array_gene_expr;
