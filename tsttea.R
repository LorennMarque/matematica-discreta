# Instala los paquetes si aún no los tienes
# install.packages("ggplot2")
# install.packages("magick")
library(ggplot2)
library(magick)

# Cargar la imagen
img <- image_read("mapa.jpg")
img_info <- image_info(img)
img_width <- img_info$width
img_height <- img_info$height

# Crear data frame con las coordenadas y etiquetas
coords <- data.frame(
  X = c(904, 1233, 747, 422, 1364, 854, 982, 1064, 1067, 721, 826, 944),
  Y = c(336, 742, 936, 1179, 1288, 1375, 1390, 1523, 1719, 1444, 1545, 1561),
  Label = LETTERS[1:12]  # Genera letras de A a L
)

# Convertir la imagen a fondo de ggplot y agregar puntos y etiquetas
ggplot(coords, aes(x = X, y = img_height - Y)) +  # Restar Y para alinear con la esquina superior
  annotation_raster(as.raster(img), xmin = 0, xmax = img_width, ymin = 0, ymax = img_height) +
  geom_point(color = "red", size = 3) +
  geom_text(aes(label = Label), vjust = -1, color = "blue", size = 3) +  # Mostrar las etiquetas
  xlim(0, img_width) +
  ylim(0, img_height) +
  theme_void()

