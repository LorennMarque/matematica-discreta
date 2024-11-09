import pygame
from PIL import Image
import sys

# Inicializar pygame
pygame.init()

# Cargar la imagen con PIL y convertirla a un formato que Pygame pueda usar
imagen_pil = Image.open("mapa.jpg")
imagen_pil = imagen_pil.convert("RGB")
ancho, alto = imagen_pil.size

# Aplicar un primer factor de escala
factor_escala_imagen = 0.5
ancho_redimensionado = int(ancho * factor_escala_imagen)
alto_redimensionado = int(alto * factor_escala_imagen)
imagen_pil = imagen_pil.resize((ancho_redimensionado, alto_redimensionado))

# Aplicar un segundo factor de escala adicional para reducir aún más
factor_escala_ventana = 0.7
ancho_final = int(ancho_redimensionado * factor_escala_ventana)
alto_final = int(alto_redimensionado * factor_escala_ventana)
imagen_pil = imagen_pil.resize((ancho_final, alto_final))
imagen = pygame.image.fromstring(imagen_pil.tobytes(), imagen_pil.size, imagen_pil.mode)

# Configurar la ventana con las dimensiones finales
screen = pygame.display.set_mode((ancho_final, alto_final + 100))
pygame.display.set_caption("Mover Círculo con Sliders")

# Posición inicial del círculo
circle_x, circle_y = ancho_final // 2, alto_final // 2
circle_radius = 15

# Definir colores
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configuración de los sliders
slider_width = ancho_final  # El slider abarcará todo el ancho de la imagen
slider_height = 10
slider_x_pos = 0  # Posición horizontal del slider
slider_y_pos_x = alto_final + 30  # Posición vertical del slider X
slider_y_pos_y = alto_final + 60  # Posición vertical del slider Y

# Valores iniciales de los sliders
slider_x = ancho_final // 2
slider_y = alto_final // 2

# Función para actualizar el círculo según los sliders
def update_circle_position():
    global circle_x, circle_y
    circle_x = slider_x
    circle_y = slider_y

# Bucle principal
running = True
while running:
    screen.fill(WHITE)
    screen.blit(imagen, (0, 0))

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Verificar si se hizo clic en el slider X o Y
            if slider_x_pos <= mouse_x <= slider_x_pos + slider_width:
                if slider_y_pos_x <= mouse_y <= slider_y_pos_x + slider_height:
                    slider_x = mouse_x  # Actualizar posición X del slider
                elif slider_y_pos_y <= mouse_y <= slider_y_pos_y + slider_height:
                    slider_y = mouse_x  # Actualizar posición Y del slider
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            if event.buttons[0]:  # Si el botón izquierdo está presionado
                if slider_x_pos <= mouse_x <= slider_x_pos + slider_width:
                    if slider_y_pos_x <= mouse_y <= slider_y_pos_x + slider_height:
                        slider_x = mouse_x
                    elif slider_y_pos_y <= mouse_y <= slider_y_pos_y + slider_height:
                        slider_y = mouse_x

    # Actualizar la posición del círculo
    update_circle_position()

    # Dibujar sliders
    pygame.draw.rect(screen, BLACK, (slider_x_pos, slider_y_pos_x, slider_width, slider_height))
    pygame.draw.rect(screen, BLACK, (slider_x_pos, slider_y_pos_y, slider_width, slider_height))
    pygame.draw.circle(screen, RED, (slider_x, slider_y_pos_x + slider_height // 2), 10)
    pygame.draw.circle(screen, RED, (slider_y, slider_y_pos_y + slider_height // 2), 10)

    # Dibujar círculo en la posición deseada
    pygame.draw.circle(screen, RED, (circle_x, circle_y), circle_radius)

    # Mostrar las coordenadas del círculo
    font = pygame.font.Font(None, 24)
    coords_text = font.render(f"Coordenadas: ({circle_x}, {circle_y})", True, BLACK)
    screen.blit(coords_text, (10, alto_final + 10))

    # Actualizar la pantalla
    pygame.display.flip()

# Salir de pygame
pygame.quit()
sys.exit()
