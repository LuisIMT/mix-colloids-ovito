import freud
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from scipy.spatial import Voronoi, voronoi_plot_2d
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.collections import LineCollection
import matplotlib.cm as cm
from diffrations import create_particle_system, read_xyz


def representation(box, points):
    # # Compute the Voronoi diagram
    # voro = freud.locality.Voronoi()
    # voro.compute((box, points))

    # # Plot Voronoi with points and a custom cmap
    # plt.figure()
    # ax = plt.gca()
    # voro.plot(ax=ax, cmap="hot")
    # ax.scatter(points[:, 0], points[:, 1], s=4, c="k")
    # plt.show()
    voro = freud.locality.Voronoi()
    voro.compute((box, points))
    ax = plt.gca()
    voro.plot(ax=ax, cmap="hot")
    nlist = voro.nlist
    line_data = np.asarray(
        [[points[i], points[i] + box.wrap(points[j] - points[i])] for i, j in nlist]
    )[:, :, :2]
    line_collection = LineCollection(line_data, alpha=0.2)
    plt.figure()
    ax = plt.gca()
    voro.plot(ax=ax, cmap="RdBu")
    ax.add_collection(line_collection)
    plt.show()

def is_square(polygon):
    # Calcular las longitudes de los lados y los ángulos internos
    n = len(polygon)
    sides = [np.linalg.norm(polygon[i] - polygon[(i + 1) % n]) for i in range(n)]
    angles = []

    # Calcular los ángulos internos
    for i in range(n):
        v1 = polygon[i] - polygon[(i - 1) % n]
        v2 = polygon[(i + 1) % n] - polygon[i]
        angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        angles.append(np.degrees(angle))

    # Condición para ser cercano a un cuadrado: lados similares y ángulos cercanos a 90 grados
    side_ratio = max(sides) / min(sides) if min(sides) > 0 else np.inf
    angle_diff = max(angles) - min(angles)
    
    # Ajusta estos valores según cuán estrictos quieras ser
    return side_ratio < 1.1 and angle_diff < 10

def example(particles):
    vor = Voronoi(particles)

    # Crear la figura y el eje
    fig, ax = plt.subplots()

    # Dibujar el diagrama de Voronoi sin vértices y con líneas de color
    voronoi_plot_2d(vor, ax=ax, show_vertices=True, line_colors='orange', line_width=1.0, point_size=0.1)

    # Colorear las regiones de Voronoi basadas en si son "cuadradas" o no
    patches = []
    colors = []
    colormap = cm.get_cmap('coolwarm')  # Puedes elegir otros mapas de colores

    for region_index in vor.regions:
        if not -1 in region_index and len(region_index) > 0:
            polygon = [vor.vertices[i] for i in region_index]

            if len(polygon) >= 4:  # Necesitamos al menos 4 lados para comprobar si es un cuadrado
                patches.append(Polygon(polygon))
                is_square_shape = is_square(np.array(polygon))
                colors.append(1 if is_square_shape else 0)  # 1 si es cuadrado, 0 si no lo es

    # Crear una colección de parches coloreando los polígonos cuadrado en un color y los demás en otro
    p = PatchCollection(patches, cmap=colormap, alpha=0.6, edgecolor='orange')
    p.set_array(np.array(colors))  # Asignar el array de colores
    ax.add_collection(p)

    # Graficar las partículas simuladas (puntos rojos)
    ax.plot(particles[:, 0], particles[:, 1], 'ro', label='Partículas')

    # Ajustar los límites de visualización
    min_x, max_x = np.min(particles[:, 0]), np.max(particles[:, 0])
    min_y, max_y = np.min(particles[:, 1]), np.max(particles[:, 1])
    
    # Añadir un margen para mejor visualización
    margin = 0.1 * (max_x - min_x)
    ax.set_xlim(min_x - margin, max_x + margin)
    ax.set_ylim(min_y - margin, max_y + margin)

    ax.legend()
    plt.colorbar(p, ax=ax)  # Agregar una barra de colores para visualizar la escala de colores
    plt.show()

def read_ovito_file(filename):
    # Leer el archivo usando OVITO
    pipeline = import_file(filename)
    
    # Evaluar los datos
    data = pipeline.compute()
    
    # Extraer las posiciones de las partículas
    positions = data.particles.positions
    
    # Extraer la caja de simulación
    box_matrix = data.cell.matrix
    box = freud.box.Box.from_matrix(box_matrix[:3, :3]) 
    return box, positions

input_file = Path(r'C:\Users\Hp\simulations\core-shell\mix-colloids-ovito\proyeccion.xyz')
box_size =40
num_atoms, comment, atoms = read_xyz(input_file)
positions = np.array([[x,y,0] for _, x, y, _ in atoms])
# # # Crear el sistema de partículas
box, points = create_particle_system(positions, box_size)
# box, points = read_ovito_file(input_file)
#print(positions)
representation(box, points)
#example(positions)