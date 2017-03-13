library(rCharts)
library(reshape2)

inputpath='C:/Users/Lee/Desktop/RLadies_1205'

data_103 = read.csv(file.path(inputpath,'103.csv'),header=TRUE,stringsAsFactors=FALSE)
data_city = read.csv(file.path(inputpath,'city.csv'),header=TRUE,stringsAsFactors=FALSE)
colnames(data_city)=c('OWNERCITYCODE','CITY')
data_nattacke =read.csv(file.path(inputpath,'nattacke.csv'),header=TRUE,stringsAsFactors=FALSE)

data_103$NATTACKEDTYPE=gsub(data_nattacke[1,1],replacement=data_nattacke[1,2],data_103$NATTACKEDTYPE) 
data_103$NATTACKEDTYPE=gsub(data_nattacke[2,1],replacement=data_nattacke[2,2],data_103$NATTACKEDTYPE)
data_103$NATTACKEDTYPE=gsub(data_nattacke[3,1],replacement=data_nattacke[3,2],data_103$NATTACKEDTYPE)
data_103$NATTACKEDTYPE=gsub(data_nattacke[4,1],replacement=data_nattacke[4,2],data_103$NATTACKEDTYPE)

data_all = merge(data_103,data_city,by='OWNERCITYCODE',all.x=TRUE)

data_table = table(data_all$SEXID,data_all$NATTACKEDTYPE)


