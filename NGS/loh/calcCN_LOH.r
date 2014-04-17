args <- commandArgs(TRUE)

inLOHfileName = args[1]
inCNfileName = args[2]
outFileName = args[3]

df_loh = read.delim(inLOHfileName)
df_loh = df_loh[df_loh[,"num.mark"] >50,]

df_cn = read.delim(inCNfileName)

df_loh_ft = df_loh[df_loh[,"seg.mean"] >= .2,]

loh_cn = c()
loh_type = c()

if (nrow(df_loh_ft) < 1) {
  df_out = df_loh_ft
  names(df_out) = c("ID","chrom","loc.start","loc.end","loh_type","loh_cn")
} else {
for (i in 1:nrow(df_loh_ft)){
  type = NA
  cn = 0
  
  chrom = df_loh_ft[i,"chrom"]
  start = df_loh_ft[i,"loc.start"]
  end = df_loh_ft[i,"loc.end"]
  loh_len = end-start+1
  
  df_cn_ft = df_cn[df_cn[,"chrom"]==sprintf('chr%s',as.character(chrom)),]
  
  df_cn_ft = df_cn_ft[df_cn_ft[,"loc.end"]>=start & df_cn_ft[,"loc.start"]<=end,]
  
  if (nrow(df_cn_ft) > 0) {
  
  for (j in 1:nrow(df_cn_ft)){
    cn_s = NA
    cn_e = NA
    
    if (df_cn_ft[j,"loc.start"] < start) {
      cn_s = start
    } else {cn_s = df_cn_ft[j,"loc.start"]
    }
    
    if (df_cn_ft[j,"loc.end"] > end) {
      cn_e = end
    } else {cn_e = df_cn_ft[j,"loc.end"]
    }
    
    cn_len = cn_e - cn_s + 1
    
    r = cn_len/loh_len
    
    cn = cn + (r * df_cn_ft[j,"seg.mean"])
  }
  
  if (abs(cn) < 0.15) type = 'CNLOH'
  else if (cn <= -0.15) type = 'LOH'
  else type = 'gain'
  
  loh_cn[i] = sprintf('%.4f',cn)
  } else {
    cn = NA
    loh_cn[i] = NA
  }
  loh_type[i] = type
}


df_out = data.frame(df_loh_ft["ID"],"chrom"=df_loh_ft[,"chrom"],"loc.start"=df_loh_ft[,"loc.start"],"loc.end"=df_loh_ft[,"loc.end"],loh_type,loh_cn)
}
write.table(df_out, file = outFileName, row.names=F, col.names=T, quote=F, sep="\t")
