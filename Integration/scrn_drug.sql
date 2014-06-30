drop table IF EXISTS scrn_drug;
CREATE TABLE scrn_drug (
	drug text NOT NULL,
	gene_sym varchar(31) NOT NULL
);

LOAD DATA LOCAL INFILE "/EQL1/NSL/clinical/screen_targets.dat" INTO TABLE scrn_drug;
