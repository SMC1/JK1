drop table IF EXISTS methyl;
CREATE TABLE methyl (
	platform varchar(31),
	sId char(35),
	pId char(12),
	TN char(1),
	geneName varchar(31),
	loc varchar(31),
	fraction float unsigned,
	primary key (sId,loc)
);

LOAD DATA LOCAL INFILE "/EQL1/TCGA/GBM/methyl/methyl_MGMT.dat" INTO TABLE methyl;

drop table if exists methyl_pId;
CREATE table methyl_pId as
SELECT platform,pId,geneName,loc,sum(fraction)/count(fraction) fraction FROM tcga1.methyl where TN='T' group by platform,pId,loc;


drop table if exists methyl_pId_gene;
CREATE table methyl_pId_gene as
SELECT pId,geneName,fraction FROM tcga1.methyl_pId where loc='P281_F' or loc='10:131265575';


create view methyl_view as
select pId samp_id, geneName gene_sym, fraction from tcga1.methyl_pId_gene;
