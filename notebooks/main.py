import pygame
import pandas as pd
import pygame.gfxdraw

df_geo = pd.read_csv('notebooks/df_geo.csv')

pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Puntos de entrega")

# Load data
x = df_geo['longitud'].values
y = df_geo['latitud'].values

# Scale data to fit screen
x_scale = screen_width / (max(x) - min(x))
y_scale = screen_height / (max(y) - min(y))
scaled_x = [(x_i - min(x)) * x_scale for x_i in x]
scaled_y = [(y_i - min(y)) * y_scale for y_i in y]

# Colors
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
dark_gray = (50, 50, 50)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Slider
slider_width = 200
slider_height = 20
slider_x = (screen_width - slider_width) // 2
slider_y = screen_height - 50
slider_pos = 0
slider_max = len(df_geo) - 1
slider_color = (255, 255, 255)
slider_handle_color = (0, 0, 0)
slider_handle_radius = 10

# Play button
button_width = 50
button_height = 30
button_x = slider_x + slider_width + 20
button_y = slider_y
button_color = (255, 255, 255)
button_text_color = (0, 0, 0)
button_text = "Play"
button_font = pygame.font.Font(None, 20)
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

# Message
message_font = pygame.font.Font(None, 20)
message_color = (255, 255, 255)

# Main loop
running = True
i = 0
playing = False
# Canvas drag variables
canvas_x = 0
canvas_y = 0
dragging = False
drag_start_x = 0
drag_start_y = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                playing = not playing
            if event.button == 1:  # Left mouse button
                dragging = True
                drag_start_x = event.pos[0] - canvas_x
                drag_start_y = event.pos[1] - canvas_y
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                dragging = False
        if event.type == pygame.MOUSEMOTION:
            if dragging:
                canvas_x = event.pos[0] - drag_start_x
                canvas_y = event.pos[1] - drag_start_y
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                i += 1
                if i >= len(df_geo):
                    i = 0
            if event.key == pygame.K_LEFT:
                i -= 1
                if i < 0:
                    i = len(df_geo) - 1

    # Clear the screen
    screen.fill(dark_gray)

    # Draw points
    for j in range(i + 1):
        pygame.draw.circle(screen, red, (int(scaled_x[j] + canvas_x), int(screen_height - scaled_y[j] + canvas_y)), 10)
        font = pygame.font.Font(None, 20)
        text = font.render(str(j + 1), True, black)
        text_rect = text.get_rect(center=(int(scaled_x[j] + canvas_x), int(screen_height - scaled_y[j] + canvas_y)))
        screen.blit(text, text_rect)

    # Draw lines
    if i > 0:
        pygame.draw.lines(screen, blue, False, [(int(scaled_x[j] + canvas_x), int(screen_height - scaled_y[j] + canvas_y)) for j in range(i + 1)], 2)

    # Draw slider
    pygame.draw.rect(screen, slider_color, (slider_x, slider_y, slider_width, slider_height))
    slider_handle_x = slider_x + (slider_pos / slider_max) * slider_width
    pygame.draw.circle(screen, slider_handle_color, (int(slider_handle_x), slider_y + slider_height // 2), slider_handle_radius)

    # Draw play button
    pygame.draw.rect(screen, button_color, button_rect)
    button_text_surface = button_font.render(button_text, True, button_text_color)
    button_text_rect = button_text_surface.get_rect(center=button_rect.center)
    screen.blit(button_text_surface, button_text_rect)

    # Draw message
    message = f"Circles displayed: {i + 1}"
    message_surface = message_font.render(message, True, message_color)
    message_rect = message_surface.get_rect(center=(screen_width // 2, slider_y - 20))
    screen.blit(message_surface, message_rect)

    # Update display
    pygame.display.flip()

    # Increment index
    if playing:
        i += 1
        if i >= len(df_geo):
            i = 0
            playing = False

    # Control frame rate
    clock.tick(10)

pygame.quit()