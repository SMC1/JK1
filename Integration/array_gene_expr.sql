drop table IF EXISTS array_gene_expr;
CREATE TABLE array_gene_expr (
	samp_id varchar(63) NOT NULL,
	gene_sym varchar(31) NOT NULL,
	z_score double NOT NULL
);

