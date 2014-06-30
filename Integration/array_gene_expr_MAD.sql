drop table IF EXISTS array_gene_expr_MAD;
CREATE TABLE array_gene_expr_MAD (
	samp_id varchar(63) NOT NULL,
	gene_sym varchar(31) NOT NULL,
	expr_MAD double NOT NULL,
	primary key (samp_id,gene_sym),
	index (gene_sym),
	index (samp_id),
	index (samp_id,gene_sym,expr_MAD)
);

/* LOAD DATA LOCAL INFILE "/EQL1/NSL/array_gene/NSL_GBM_93_zNorm.dat" INTO TABLE array_gene_expr; */
LOAD DATA LOCAL INFILE "/EQL1/Phillips/array_gene/Phillips_U133A_prbClps_madNorm.dat" INTO TABLE array_gene_expr_MAD;
