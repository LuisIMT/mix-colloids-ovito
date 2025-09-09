
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
# Función para leer archivo XYZ
def read_xyz(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        num_atoms = int(lines[0].strip())  # Leer número de átomos
        comment = lines[1].strip()  # Comentario (puede ser ignorado)
        
        # Leer las coordenadas de los átomos
        atoms = []
        for line in lines[2:]:
            parts = line.split()
            atom_type = parts[0]  # Tipo de átomo (C, O, H, etc.)
            x, y, z = map(float, parts[1:])  # Coordenadas x, y, z
            atoms.append((atom_type, x, y, z))
            # Extraer solo las coordenadas (x, z)
    return num_atoms, comment, atoms

def writeFile(input_file):
    num_atoms, comment, atoms = read_xyz(input_file)
    # Por ejemplo: positions = np.array([[x1, z1], [x2, z2], ...])
    positions = np.array([[x, z] for _, x, _, z in atoms])
    with open('coordenadas.dat', 'w') as file:
        # Escribir el número de partículas
        #file.write(f"\t{num_atoms}\n")
        #file.write(f"{comment}\n")    
        # Escribir las posiciones de X y Z
        for x, z in positions[:-1]:
            #file.write(f"H\t{x:.6f}\t{z:.6f}\t0\n")  # Formato con 6 decimales para consistencia
            file.write(f'{x:.6f}\t{z:.6f}\n')
    # Escribir la última línea sin salto de línea al final
        x, z = positions[-1]
        # file.write(f"H\t{x:.9f}\t{z:.9f}\t0") 
        file.write(f'{x:.6f}\t{z:.6f}')


def graphicposition( input_file):
    num_atoms, comment, atoms = read_xyz(input_file)
    # Por ejemplo: positions = np.array([[x1, z1], [x2, z2], ...])
    positions = np.array([[x, z] for _, x, _, z in atoms])

    # Separar los valores de X y Z
    x = positions[:, 0]
    z = positions[:, 1]

    # Crear el gráfico de dispersión
    plt.scatter(x, z)

    # Añadir etiquetas y título
    plt.xlabel('l')
    plt.ylabel('Z')
    plt.title('Gráfico de dispersión de posiciones atómicas')

    # Mostrar el gráfico
    plt.show()

input_file = Path(r'C:\Users\Hp\simulations\core-shell\mix-colloids-ovito\projection.xyz')
#graphicposition(input_file=input_file)
writeFile(  input_file=input_file )