import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
from geopy.distance import geodesic

# Cargar el archivo CSV
df = pd.read_csv('notebooks/df_geo.csv')

# Convertir la columna 'fin_visita' a formato datetime
df['fin_visita'] = pd.to_datetime(df['fin_visita'])

# Ordenar el DataFrame por 'fin_visita' en orden ascendente
df_sorted = df.sort_values('fin_visita')

# Seleccionar las primeras 20 entregas
df_first_20 = df_sorted.head(20).reset_index(drop=True)

# Mostrar las primeras 20 entregas
print(df_first_20)

# Función para mostrar el scatterplot
def plot_deliveries(df, color_by_client=False):
    """
    Muestra un scatterplot de las entregas.

    Args:
        df (DataFrame): DataFrame con las entregas.
        color_by_client (bool): Si es True, colorea los puntos según el cliente.
    """
    plt.figure(figsize=(10, 10))
    if color_by_client:
        # Mapear los clientes a colores
        color_map = {20: 'red', 70: 'blue'}
        colors = df['cliente'].map(color_map)
        plt.scatter(df['longitud'], df['latitud'], c=colors, edgecolor='k')
        # Crear una leyenda personalizada
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Cliente 20',
                   markerfacecolor='red', markersize=10, markeredgecolor='k'),
            Line2D([0], [0], marker='o', color='w', label='Cliente 70',
                   markerfacecolor='blue', markersize=10, markeredgecolor='k')
        ]
        plt.legend(handles=legend_elements)
    else:
        plt.scatter(df['longitud'], df['latitud'], color='green', edgecolor='k')
    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    plt.title('Entregas - Primeras 20')
    plt.grid(True)

    for idx, row in df.iterrows():
        plt.text(row['longitud'], row['latitud'], str(row['order']), fontsize=10)

    plt.show()

# Usar la función para mostrar el scatterplot con puntos coloreados por cliente
plot_deliveries(df_first_20, color_by_client=True)


# Parámetros del modelo
VELOCIDAD_PROMEDIO = 30  # km/h (ajustar según condiciones reales)
TIEMPO_SERVICIO = 15  # minutos (tiempo promedio de servicio en cada entrega)

def build_conflict_graph(df):
    """
    Construye el grafo de conflicto donde las aristas conectan entregas
    que no pueden ser realizadas por el mismo camión.
    """
    G = nx.Graph()

    # Agregar nodos al grafo
    for idx, row in df.iterrows():
        G.add_node(idx,
                   index=row['index'],
                   cliente=row['cliente'],
                   latitud=row['latitud'],
                   longitud=row['longitud'],
                   fin_visita=row['fin_visita'],
                   order=row['order'])

    # Calcular el tiempo de servicio en horas
    t_servicio = TIEMPO_SERVICIO / 60  # Convertir a horas

    # Lista de nodos
    nodes = list(G.nodes(data=True))

    # Construir el grafo de conflicto
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            nodo_i = nodes[i]
            nodo_j = nodes[j]

            # Calcular diferencia de tiempo en horas    
            delta_t = abs((nodo_i[1]['fin_visita'] - nodo_j[1]['fin_visita']).total_seconds() / 3600)

            # Coordenadas geográficas
            coord_i = (nodo_i[1]['latitud'], nodo_i[1]['longitud'])
            coord_j = (nodo_j[1]['latitud'], nodo_j[1]['longitud'])

            # Calcular distancia en kilómetros
            distancia = geodesic(coord_i, coord_j).kilometers

            # Calcular tiempo de viaje en horas
            t_viaje = distancia / VELOCIDAD_PROMEDIO

            # Criterio de incompatibilidad
            tiempo_minimo = t_viaje + t_servicio
            if delta_t < tiempo_minimo:
                # Las entregas no pueden ser realizadas por el mismo camión
                G.add_edge(nodo_i[0], nodo_j[0])

    return G

def color_graph(G):
    """
    Aplica un algoritmo de coloración al grafo de conflicto.
    Cada color representa un camión diferente.
    """
    coloring = nx.coloring.greedy_color(G, strategy='largest_first')
    nx.set_node_attributes(G, coloring, 'color')
    return coloring

def visualize_colored_graph(G):
    """
    Visualiza el grafo de conflicto coloreado.
    """
    pos = nx.spring_layout(G)  # Posición de los nodos para la visualización
    colors = [G.nodes[node]['color'] for node in G.nodes()]
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, node_color=colors, with_labels=True, cmap=plt.cm.Set3)
    plt.title("Grafo de Conflicto Coloreado - Asignación de Camiones")
    plt.show()

def plot_deliveries_by_truck(df, coloring):
    """
    Muestra un mapa de las entregas, coloreadas según el camión asignado.
    """
    # Añadir el color (camión) al DataFrame
    df = df.copy()
    df['camion'] = df.index.map(coloring)

    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(df['longitud'], df['latitud'], c=df['camion'], cmap=plt.cm.Set3, edgecolor='k')
    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    plt.title('Entregas - Asignación de Camiones')
    plt.grid(True)
    plt.colorbar(scatter, label='Camión')
    plt.show()


def main():
    # Cargar y preparar los datos
    df = df_first_20

    # Construir el grafo de conflicto
    G = build_conflict_graph(df)

    # Aplicar coloración
    coloring = color_graph(G)

    # Mostrar resultados
    print(f"Se requieren {max(coloring.values()) + 1} camiones para realizar las entregas.")

    # Visualizar el grafo coloreado
    visualize_colored_graph(G)

    # Visualizar las entregas en el mapa
    plot_deliveries_by_truck(df, coloring)

if __name__ == "__main__":
    main()
