library(shiny)
library(ggplot2)
inputPath = '/Users/hsinyu/Desktop/RLadiesshiny/AQI'
Air_data = read.csv(file.path(inputPath,'data_AQI_new.csv'), stringsAsFactors=FALSE)

shinyServer(function(input, output) {
  
  data_plot <- reactive({
    subset(Air_data,SiteName %in% c(input$site1,input$site2))
  })

  data_title <- renderText({ paste0(input$site1,' VS ',input$site2) })

  output$AQIPlot <- renderPlot({
    ggplot(data_plot(), aes(x = as.Date(MonitorDate), y = AQI , colour = SiteName)) +
      geom_line() + 
      labs(x = "Date", y = "AQI" , title=data_title() ) +
      theme(text=element_text(family="STHeitiTC-Light"))
  })
  
})



