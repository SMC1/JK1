drop table IF EXISTS methyl;
CREATE TABLE methyl (
	platform varchar(31),
	sId char(35),
	pId char(12),
	TN char(1),
	geneName varchar(31),
	loc varchar(31),
	fraction float unsigned,
	index (geneName)
);

LOAD DATA LOCAL INFILE "/EQL1/TCGA/GBM/methyl/methyl_loc_all.dat" INTO TABLE methyl;

/*drop table if exists methyl_pId;
CREATE table methyl_pId as
SELECT platform,pId,geneName,loc,sum(fraction)/count(fraction) fraction FROM tcga1.methyl where TN='T' group by platform,pId,geneName,loc;*/
