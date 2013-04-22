drop table IF EXISTS rpkm_gene_expr;
CREATE TABLE rpkm_gene_expr (
	samp_id varchar(63) NOT NULL,
	gene_sym varchar(31) NOT NULL,
	rpkm double NOT NULL,
	primary key (samp_id,gene_sym),
	index (gene_sym)
);

/* LOAD DATA LOCAL INFILE "/EQL1/NSL/array_gene/NSL_GBM_93_zNorm.dat" INTO TABLE array_gene_expr; */
LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/NSL_GBM_RPKM_36.dat" INTO TABLE rpkm_gene_expr;