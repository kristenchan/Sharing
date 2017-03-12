#===================================================================================================================================
#
# Author : Kristen Chan
#
# Modify Date : 2017-03-07
#
# RLadies Taipei Global Map
#===================================================================================================================================
#******* Code Start *******
#===================================================================================================================================
# Step 1 : Setting Environment 
#===================================================================================================================================
time_1=Sys.time()

#--- Step1.2 Check Package (if didn't install yet then install those packages)
packages.need <- c("XML","RCurl","dplyr","leaflet","rgdal","rjson","httr")

packages.download <- !packages.need %in% installed.packages()[,"Package"]

if(any(packages.download))
  install.packages(packages.need[packages.download],dependencies=TRUE)

#--- Step1.3 Load packaes
lapply(packages.need, require, character.only = TRUE)

#===================================================================================================================================
# Step 2 : Data Prepare
#===================================================================================================================================
#--- Step2.1 Crawler Rladies Global Data
url='https://rladies.org/'
get_url = getURL(url,encoding = "UTF-8")

get_url_parse = htmlParse(get_url, encoding = "UTF-8")
#抓取需要的資訊：一個夾在div的class=entry-content裡<ul>中的<li>內的資訊
citycountry_original = xpathSApply(get_url_parse, "//div[@class='entry-content']/ul/li", xmlValue)

pattern = paste0("(?P<City>^[\\w|\\s]*)[\\,]?[\\s]?(?P<State>[\\w|\\s]*)\\s\\–\\s(?P<Country>[\\w]*$)")
reg_function = function(reg_pattern,input){
  reg = regexpr(reg_pattern, input, perl = TRUE)
  row = which(reg!=-1)
  col = attr(reg, "capture.names")
  data = input[row]  
  start = attr(reg,"capture.start")[row,]
  end = attr(reg,"capture.length")[row,]
  if(length(row)==0){
    result = matrix(NA,1,length(col))
  }else{
    result = matrix( gsub("UK","United Kingdom",gsub("US","United States",gsub('^ *| *$',"",substring(data,start,start+end-1)))) 
                     ,length(row),length(col)) 
  }
  colnames(result) = col
  return(result)
}
citycountry_data=as.data.frame(reg_function(pattern,citycountry_original))

#--- Step2.2 Country Data for Plot  (From http://data.okfn.org/data/datasets/geo-boundaries-world-110m)
countries = readOGR("/Users/hsinyu/Desktop/countries.geojson", "OGRGeoJSON")

#--- Step2.3 Factor Country
countries$category=factor((countries$name %in% citycountry_data$Country)+1) 
color_factor = colorFactor(c("#F0F0F0","#AC74AD"), countries$category)

#--- Step2.4 Mark Data
# Google API
api_key_geocoding = ''  #<---your api key
# Git lng and lat
City_location = function(go_city,type,language){
  lng_lat_url = paste0("https://maps.googleapis.com/maps/api/geocode/json?address=",go_city,
                       "&language=",language,
                       "&key=",api_key_geocoding)
  urldata_lng_lat = POST(lng_lat_url)
  lng_lat_result = content(urldata_lng_lat)
  longitude = format(lng_lat_result$results[[1]]$geometry$location$lng,nsmall=6)
  latitude =  format(round(lng_lat_result$results[[1]]$geometry$location$lat,6),nsmall=6)
  
  return(c(go_city,longitude,latitude))
}
# Seting Parameter
type = 'atm'
language = 'zh-TW'
go_city=as.vector(citycountry_data$City[c(9,17)])
# WeGo Data
WeGo=NULL
for(i in 1:length(go_city)){
  WeGo=rbind(WeGo,City_location(go_city[i],type,language))
}
WeGo=as.data.frame(WeGo)
colnames(WeGo)=c('City','Longitude','Latitude')
# Icon
Icon <- makeIcon(
  iconUrl = "https://raw.githubusercontent.com/rladiestaipei/R-Ladies-Taipei/master/R_Ladies_Taipei1.png",
  iconWidth = 30, iconHeight = 30,
  iconAnchorX = 0, iconAnchorY = 0
)
#===================================================================================================================================
# Step 3 : Plot
#===================================================================================================================================
map <- leaflet(countries) %>%
        addPolygons(stroke = FALSE, smoothFactor = 0.2, fillOpacity = 1,
              color = ~color_factor(category)) %>%
        addMarkers(lng=as.numeric(as.vector(WeGo$Longitude[1])), lat=as.numeric(as.vector(WeGo$Latitude[1])),
             popup = as.character(as.vector(WeGo$City[1])),
             icon = Icon) %>%
        addMarkers(lng=as.numeric(as.vector(WeGo$Longitude[2])), lat=as.numeric(as.vector(WeGo$Latitude[2])),
             popup = as.character(as.vector(WeGo$City[2])),
             icon = Icon) 
map

