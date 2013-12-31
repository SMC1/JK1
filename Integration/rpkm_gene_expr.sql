/*drop table IF EXISTS rpkm_gene_expr;
CREATE TABLE rpkm_gene_expr (
	samp_id varchar(63) NOT NULL,
	gene_sym varchar(31) NOT NULL,
	rpkm double NOT NULL,
	primary key (samp_id,gene_sym),
	index (gene_sym)
);

LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/results/expression/NSL_RPKM_45.dat" INTO TABLE rpkm_gene_expr;
LOAD DATA LOCAL INFILE "/EQL2/SGI_20131031/RNASeq/results/expression/RPKM_30.dat" INTO TABLE rpkm_gene_expr;*/
LOAD DATA LOCAL INFILE "/EQL1/NSL/RNASeq/results/expression/SGI20131119_6.dat" INTO TABLE rpkm_gene_expr;

drop view if exists rpkm_gene_expr_lg2;
create view rpkm_gene_expr_lg2 as select samp_id,gene_sym,log2(rpkm+1) as lg2_rpkm from rpkm_gene_expr;
