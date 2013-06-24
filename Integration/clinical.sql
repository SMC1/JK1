drop table IF EXISTS clinical;
CREATE TABLE clinical (
	pId char(12),
	pId_uuid char(36),
	year char(4),
	age varchar(3),
	gender varchar(1),
	days_death smallint unsigned,
	days_followup smallint unsigned,
	pathology varchar(63),
	prior_glioma char(1),
	neoadjuvant char(1),
	KPS tinyint unsigned,
	KPS_time varchar(63),
	primary key (pId)
);

LOAD DATA LOCAL INFILE "/EQL1/TCGA/GBM/clinical/clinical_TCGA_GBM.dat" INTO TABLE clinical;
