import pandas as pd
import networkx as nx
from geopy.distance import geodesic
import matplotlib.pyplot as plt

# Cargar el archivo CSV y seleccionar las primeras 20 filas
df = pd.read_csv('notebooks/df_geo.csv').head(20)  # Asegúrate de que esta ruta sea correcta

# Convertir la columna 'fin_visita' a formato datetime
df['fin_visita'] = pd.to_datetime(df['fin_visita'])

# Definir rangos de umbrales para distancia (en km) y tiempo (en minutos)
distance_thresholds = [0.5, 1.0, 1.5, 2.0]  # Ajusta según tus datos
time_thresholds = [10, 20, 30, 40]  # Ajusta según tus datos

# Almacenar resultados para visualización
results = []

# Iterar sobre cada combinación de umbrales
for distance_threshold in distance_thresholds:
    for time_min in time_thresholds:
        time_threshold = pd.Timedelta(minutes=time_min)

        # Crear el grafo
        G = nx.Graph()

        # Añadir nodos al grafo
        for idx, row in df.iterrows():
            G.add_node(idx, lat=row['latitud'], lon=row['longitud'], time=row['fin_visita'])

        # Añadir aristas si cumplen con el umbral de distancia y tiempo
        for i, row1 in df.iterrows():
            for j, row2 in df.iterrows():
                if i >= j:
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
        results.append((distance_threshold, time_min, num_repartidores))
        print(f"Distancia: {distance_threshold} km, Tiempo: {time_min} min -> Repartidores: {num_repartidores}")

# Visualizar resultados
plt.figure(figsize=(10, 6))
for distance_threshold in distance_thresholds:
    subset = [r[2] for r in results if r[0] == distance_threshold]
    plt.plot(time_thresholds, subset, marker='o', label=f'Distancia {distance_threshold} km')

plt.xlabel('Umbral de Tiempo (minutos)')
plt.ylabel('Cantidad de Repartidores Estimados')
plt.title('Ajuste de Umbrales para Detectar Repartidores Distintos')
plt.legend()
plt.show()
