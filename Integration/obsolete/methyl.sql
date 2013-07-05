drop table IF EXISTS methyl;
CREATE TABLE methyl (
	platform varchar(31),
	sId char(35),
	pId char(12),
	TN char(1),
	geneName varchar(31),
	fraction float unsigned,
	primary key (sId,geneName),
	index (pId,geneName)
);

LOAD DATA LOCAL INFILE "/EQL1/TCGA/GBM/methyl/methyl.dat" INTO TABLE methyl;

drop table if exists methyl_pId;

CREATE table methyl_pId as
SELECT platform,pId,geneName,sum(value)/count(value) fraction FROM tcga1.methyl where TN='T' group by pId,geneName;

ALTER table methyl_pId add primary key (pId,geneName);

