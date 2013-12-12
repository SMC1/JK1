drop table if exists t_EGFR;
create temporary table t_EGFR as
select platform,pId,geneName,loc,sum(fraction)/count(fraction) fraction from tcga1.methyl where TN="T" and geneName = "EGFR"
group by platform, pId, loc;

drop table if exists methyl_EGFR;
create table methyl_EGFR as
SELECT pId as samp_id,geneName as gene_sym,fraction FROM t_EGFR where platform='Infinium27k' and loc='7:55086890';
