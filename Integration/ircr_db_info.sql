drop table IF EXISTS ircr_db_info;
CREATE TABLE ircr_db_info (
	db_name varchar(31) NOT NULL, -- internal database name
	db_text varchar(127) NOT NULL -- text shown in dropdown menu
);

/* INITIAL DATA */
INSERT INTO ircr_db_info (db_name, db_text) VALUES ('ircr1','AVATAR GBM'),('tcga1','TCGA GBM'),('ccle1','CCLE');
INSERT INTO ircr_db_info (db_name, db_text) VALUES ('IRCR_GBM_352_SCS','SCS 352');
INSERT INTO ircr_db_info (db_name, db_text) VALUES ('IRCR_GBM_363_SCS','SCS 363');
INSERT INTO ircr_db_info (db_name, db_text) VALUES ('RC085_LC195_bulk','bulk RC');
INSERT INTO ircr_db_info (db_name, db_text) VALUES ('LC_195_SCS','SCS LC195');
INSERT INTO ircr_db_info (db_name, db_text) VALUES ('IRCR_GBM_412_SCS','SCS 412');
