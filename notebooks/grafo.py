import pandas as pd
import networkx as nx
from geopy.distance import geodesic
import folium
import random

# Cargar el archivo CSV y seleccionar las primeras 20 filas
df = pd.read_csv('notebooks/df_geo_2.csv')

# Convertir la columna 'fin_visita' a formato datetime
df['fin_visita'] = pd.to_datetime(df['fin_visita'])

# Ordenar el DataFrame por el tiempo de fin de visita
df = df.sort_values(by='fin_visita').reset_index(drop=True)

# Definir los umbrales de distancia (en km) y tiempo (en minutos)
distance_threshold = 2.0  # Umbral de distancia en kilómetros
time_threshold = pd.Timedelta(minutes=40)  # Umbral de tiempo en minutos

# Crear el grafo
G = nx.Graph()

# Añadir nodos al grafo
for idx, row in df.iterrows():
    G.add_node(idx, lat=row['latitud'], lon=row['longitud'], time=row['fin_visita'], cliente=row['cliente'])

# Añadir aristas si cumplen con los umbrales de distancia, tiempo y tienen el mismo valor en "cliente"
for i in range(len(df)):
    for j in range(i + 1, len(df)):
        row1 = df.iloc[i]
        row2 = df.iloc[j]

        # Verificar que los clientes sean iguales
        if row1['cliente'] != row2['cliente']:
            continue

        # Calcular la distancia geográfica
        coords_1 = (row1['latitud'], row1['longitud'])
        coords_2 = (row2['latitud'], row2['longitud'])
        distance = geodesic(coords_1, coords_2).kilometers

        # Calcular la diferencia de tiempo
        time_diff = abs(row1['fin_visita'] - row2['fin_visita'])

        # Si la distancia y el tiempo cumplen con los umbrales, añadir una arista
        if distance <= distance_threshold and time_diff <= time_threshold:
            G.add_edge(i, j)

# Calcular la cantidad de componentes conectados (repartidores distintos)
num_repartidores = nx.number_connected_components(G)
print(f"Número de repartidores distintos: {num_repartidores}")

# Obtener los componentes conectados y asignar un color único a cada uno
components = list(nx.connected_components(G))
colors = [f"#{''.join([random.choice('0123456789ABCDEF') for _ in range(6)])}" for _ in range(len(components))]

# Crear un diccionario de colores para los nodos
color_map = {}
for color, component in zip(colors, components):
    for node in component:
        color_map[node] = color

# Crear el mapa centrado en el promedio de las coordenadas
avg_lat = df['latitud'].mean()
avg_lon = df['longitud'].mean()
mapa = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

# Añadir los nodos al mapa
for node in G.nodes:
    lat = G.nodes[node]['lat']
    lon = G.nodes[node]['lon']
    folium.CircleMarker(
        location=(lat, lon),
        radius=6,
        color=color_map[node],
        fill=True,
        fill_color=color_map[node],
        fill_opacity=0.7,
        popup=f"Entrega {node} - Cliente {G.nodes[node]['cliente']}"
    ).add_to(mapa)

# Guardar el mapa como un archivo HTML
mapa.save("mapa_entregas.html")
print("Mapa guardado como mapa_entregas.html")
