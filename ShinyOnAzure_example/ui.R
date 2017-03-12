library(shiny)
inputPath = '/Users/hsinyu/Desktop/RLadiesshiny/AQI'
Air_data = read.csv(file.path(inputPath,'data_AQI_new.csv'), stringsAsFactors=FALSE)
site = unique(Air_data$SiteName)

shinyUI(fluidPage( 
  
  titlePanel("比較兩測站AQI趨勢") ,
  
  sidebarLayout(
    sidebarPanel(
      selectInput("site1", "選擇測站1 :", as.vector(site)),
      selectInput("site2", "選擇測站2 :", as.vector(site)),
      width=3) ,
    mainPanel = ( plotOutput("AQIPlot") ) 
  )
  
))


