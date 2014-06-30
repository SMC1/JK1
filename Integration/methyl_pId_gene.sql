drop table IF EXISTS methyl_pId_gene;
CREATE TABLE methyl_pId_gene (
	pId char(12),
	geneName varchar(31),
	fraction float unsigned,
	platform varchar(31),
	r float,
	index (pId),
	index (geneName),
	index (pId, geneName)
);

LOAD DATA LOCAL INFILE "/EQL1/TCGA/GBM/methyl/TCGA_GBM_methyl.dat" INTO TABLE methyl_pId_gene;

CREATE temporary table t as 
SELECT * FROM methyl_pId_gene order by pId, r;

DROP table methyl_pId_gene;

CREATE table methyl_pId_gene as
SELECT pId, geneName, fraction from t group by pId,geneName;

ALTER table methyl_pId_gene add index (pId);
ALTER table methyl_pId_gene add index (geneName);
ALTER table methyl_pId_gene add index (pId, geneName);
