library(shiny)
library(plotly)

# Configura tu token de Mapbox
mapbox_token <- "pk.eyJ1IjoibG9yZW5uem8iLCJhIjoiY20xcHYyd3g2MDk0bTJxb2k4YWZvOHlmcSJ9.r4E2pcTSM89NNHBFSmvKHw"  # Reemplaza con tu token de Mapbox

# Cargamos los datos
data <- read_csv("../data/df_geo.csv", show_col_types = FALSE)

# Interfaz de usuario
ui <- fluidPage(
  titlePanel("Mapa de Puntos de Entrega"),
  
  sidebarLayout(
    sidebarPanel(
      sliderInput("num_points", "Cantidad de puntos a mostrar:", 
                  min = 1, max = nrow(data), value = 100)
    ),
    
    mainPanel(
      plotlyOutput("mapa")
    )
  )
)

# Lógica del servidor
server <- function(input, output) {
  
  output$mapa <- renderPlotly({
    # Filtra los datos según la cantidad seleccionada
    datos_filtrados <- head(data, input$num_points)
    
    # Crea el gráfico de mapa con plotly y mapbox
    fig <- plot_ly(data = datos_filtrados, 
                   type = 'scattermapbox',
                   lat = ~latitud,
                   lon = ~longitud,
                   mode = 'markers',
                   marker = list(size = 8, color = 'blue', opacity = 0.7),
                   text = ~paste("Cliente:", cliente))  # Personaliza el texto del tooltip
    
    fig <- fig %>%
      layout(
        mapbox = list(
          style = "streets",
          accesstoken = mapbox_token,
          center = list(lat = mean(data$latitud), lon = mean(data$longitud)),
          zoom = 12  # Ajusta el nivel de zoom
        ),
        title = "Mapa de Puntos de Entrega"
      )
    
    fig
  })
}

# Ejecuta la aplicación Shiny
shinyApp(ui = ui, server = server)