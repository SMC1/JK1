drop table IF EXISTS array_gene_expr;
CREATE TABLE array_gene_expr (
	samp_id varchar(63) NOT NULL,
	gene_sym varchar(31) NOT NULL,
	z_score double NOT NULL,
	primary key (samp_id,gene_sym),
	index (gene_sym),
	index (samp_id),
	index (samp_id,gene_sym,z_score)
);

/* LOAD DATA LOCAL INFILE "/EQL1/NSL/array_gene/NSL_GBM_93_zNorm.dat" INTO TABLE array_gene_expr; */
LOAD DATA LOCAL INFILE "/data1/CCLE_Sanger/array_gene_expr_CCLE.dat" INTO TABLE array_gene_expr;
