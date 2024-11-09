library(shiny)
library(jpeg)

# Cargar la imagen fuera del render para usar sus dimensiones
img <- readJPEG("../mapa.jpg")  # Asegúrate de que 'mapa.jpg' esté en el mismo directorio
img_width <- dim(img)[2]
img_height <- dim(img)[1]

# Definir la interfaz de usuario
ui <- fluidPage(
    titlePanel("Visualización de Coordenadas sobre el Mapa"),
    
    sidebarLayout(
        sidebarPanel(
            h4("Pase el cursor sobre el mapa para ver las coordenadas"),
            helpText("Las coordenadas se muestran en píxeles."),
            h4("Coordenadas de clics"),
            verbatimTextOutput("click_coords")
        ),
        
        mainPanel(
            plotOutput("mapPlot", 
                       hover = hoverOpts(id = "plot_hover", delay = 100, delayType = "throttle"),
                       click = "plot_click",  # Registrar clics en el mapa
                       width = paste0(img_width, "px"), height = paste0(img_height, "px")),
            verbatimTextOutput("coords"),
            plotOutput("clickScatter", width = paste0(img_width, "px"), height = paste0(img_height, "px"))  # Gráfico de puntos de clics
        )
    )
)

# Definir la lógica del servidor
server <- function(input, output, session) {
    
    # Almacenar coordenadas de clics
    coords <- reactiveVal(data.frame(X = integer(), Y = integer()))
    
    # Mostrar la imagen en el tamaño original con la coordenada Y invertida
    output$mapPlot <- renderPlot({
        plot(1, type = 'n', xlab = '', ylab = '', xaxt = 'n', yaxt = 'n', 
             xlim = c(0, img_width), ylim = c(img_height, 0))
        rasterImage(img, 0, img_height, img_width, 0)  # Dibujar la imagen con Y invertida
    })
    
    # Calcular y mostrar las coordenadas del cursor en píxeles
    output$coords <- renderPrint({
        hover <- input$plot_hover
        if (!is.null(hover)) {
            x_pixel <- round(hover$x)
            y_pixel <- round(hover$y)
            cat("Coordenadas del cursor en píxeles:\nX:", x_pixel, "\nY:", y_pixel)
        } else {
            "Pase el cursor sobre el mapa para ver las coordenadas."
        }
    })
    
    # Guardar las coordenadas de los clics en la imagen
    observeEvent(input$plot_click, {
        new_coords <- data.frame(X = round(input$plot_click$x), 
                                 Y = round(input$plot_click$y))  # No invertir la coordenada Y aquí
        coords(rbind(coords(), new_coords))
    })
    
    # Mostrar las coordenadas de los clics en pantalla
    output$click_coords <- renderPrint({
        cat("Coordenadas guardadas de los clics:\n")
        print(coords())
    })
    
    # Dibujar un scatterplot con los puntos de clics sobre una copia de la imagen
    output$clickScatter <- renderPlot({
        plot(1, type = 'n', xlab = '', ylab = '', xaxt = 'n', yaxt = 'n', 
             xlim = c(0, img_width), ylim = c(img_height, 0))
        rasterImage(img, 0, img_height, img_width, 0)  # Mostrar la imagen en el fondo con Y invertida
        points(coords()$X, coords()$Y, col = "red", pch = 19, cex = 1.5)  # Dibujar puntos en las coordenadas
    })
}

# Ejecutar la aplicación
shinyApp(ui = ui, server = server)
