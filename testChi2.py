import cv2

# Cargar la imagen
imagen = cv2.imread('mapa.jpg')

# Redimensionar la imagen a un cuarto de su tamaño original
imagen = cv2.resize(imagen, (imagen.shape[1] // 2, imagen.shape[0] // 2))

# Función que se llama cada vez que el mouse se mueve o se hace clic
def mostrar_coordenadas(event, x, y, flags, param):
    # Mostrar las coordenadas del cursor en tiempo real en la imagen
    img_temp = imagen.copy()
    cv2.putText(img_temp, f'X: {x} Y: {y}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    cv2.imshow('Mapa', img_temp)

    # Imprimir las coordenadas cuando se hace clic con el botón izquierdo del mouse
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'Click en: X={x}, Y={y}')

# Crear la ventana y asociar la función al evento del mouse
cv2.namedWindow('Mapa')
cv2.setMouseCallback('Mapa', mostrar_coordenadas)

# Mantener la ventana abierta hasta que se presione la tecla ESC
while True:
    cv2.imshow('Mapa', imagen)
    if cv2.waitKey(1) & 0xFF == 27:  # Presiona ESC para salir
        break

# Cerrar la ventana al finalizar
cv2.destroyAllWindows()
