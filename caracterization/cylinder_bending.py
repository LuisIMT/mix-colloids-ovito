import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import json

class CylinderBending:

    def __init__(self) -> None:
        pass

    def read_xyz( self, file_path:str ) -> tuple:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            num_atoms = int(lines[0].strip())  # Leer número de átomos
            comment = lines[1].strip()  # Comentario (puede ser ignorado)
        
        # Leer las coordenadas de los átomos
        atoms = []
        for line in lines[2:]:
            parts = line.split()
            atom_type = parts[0]  # Tipo de átomo (C, O, H, etc.)
            x, y, z, = map(float, parts[1:])  # Coordenadas x, y, z
            atoms.append((atom_type, x, y, z))
        return num_atoms, comment, atoms
    
    # Función para convertir coordenadas cartesianas a cilíndricas
    def cartesian_to_cylindrical(self, x, y, z):
        r = np.sqrt(x**2 + y**2)  # Calcular el radio
        theta = np.arctan2(y, x)  # Calcular el ángulo theta
        return r, theta, z

    # Función para escribir el archivo XYZ modificado
    def write_xyz(self, file_path, num_atoms, comment, modified_atoms):
        with open(file_path, 'w') as file:
            file.write(f"{num_atoms}\n")  # Escribir número de átomos
            file.write(f"{comment}\n")    # Escribir comentario
            
            # Escribir las coordenadas modificadas
            for especie, x, z in modified_atoms[:-1]:
                file.write(f"{especie}\t{x:.6f}\t{z:.6f}\t0\n")  # Formato con 6 decimales para consistencia
            
            # Escribir la última línea sin salto de línea al final
            especie, x, z = modified_atoms[-1]  # Cambiado para desempaquetar correctamente
            file.write(f"{especie}\t{x:.9f}\t{z:.9f}\t0")  # Formato con 9 decimales


    # Función principal para procesar las coordenadas
    def process_xyz(self,input_file, output_file):
        num_atoms, comment, atoms = self.read_xyz(input_file)
        
        # Modificar las coordenadas
        modified_atoms = []
        for atom_type, x, y, z in atoms:
            r, theta, z = self.cartesian_to_cylindrical(x, y, z)
            new_x = r * theta  # Usar r * theta en lugar de x
            new_y = z       # Valor constante 12 en lugar de y
            modified_atoms.append((atom_type, new_x, new_y))
        
        # Escribir el nuevo archivo XYZ
        self.write_xyz(output_file, num_atoms, comment, modified_atoms)

    def scatter_plot_proj(self, atoms, color_file, new_file):

        # Obtener todas las especies únicas presentes en el conjunto de datos
        especies_presentes = set([especie for especie, _, _, _ in atoms])
        # Filtrar las posiciones de las especies presentes
        filtered_atoms = [(especie, x, y) for especie, x, y, _ in atoms if especie in especies_presentes]

        positions = np.array([[str(especie), x, y] for especie, x, y, _ in atoms])
        colors = np.array([color_file[str(especie)][:3] for especie in positions[:, 0].astype(str)])
        alphas = np.array([color_file[str(especie)][3] for especie in positions[:, 0].astype(str)])        
        # Crear la gráfica
        fig, ax = plt.subplots(figsize=(4, 4), dpi=300)
        scatter = ax.scatter(positions[:, 1].astype(float), positions[:, 2].astype(float), c=colors,alpha=alphas, s=10)
        
        # Añadir leyenda solo para las especies presentes en los datos
        for especie in especies_presentes:
            if especie in color_file:  # Verifica si la especie está definida en el color_file
                ax.scatter([], [], c=[color_file[especie]], label=especie, s=20)

        plt.tight_layout()
        ax.set_title('Posiciones', fontsize=16)
        ax.set_xlabel(r"$\iota$", fontsize=14)
        ax.set_ylabel(r"$\zeta$", fontsize=14)
        plt.savefig(new_file, dpi=300, bbox_inches='tight')
        plt.close(fig=fig)


# def main():
#     cylinder_to_plane = CylinderBending()
#     try:
#         with open('particles.json', 'r') as file:
#             data = json.load(file)
#         with open('specie_particles_color.json','r') as f:
#             species_color = json.load(f)

#         for r in data['radio']:
#             for rho in data['rho']:
#                 for lA in data['lA']:
#                     for lB in data['lB']:
#                         # input_file = Path(f"C://Users//Hp//Documents//data_simulations//XYZ_ADA//r{float(r)}rho{rho}lA{lA}lB{lB}.xyz")
#                         # input_file =  Path(f"C://Users//Hp//Documents//data_simulations//XYZ_miztli//r{float(r)}rho{rho}lA{lA}lB{lB}.xyz") 
#                         # output_file = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//proj_r{float(r)}rho{rho}lA{lA}lB{lB}.xyz")
#                         input_file = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//r_{int(r)}rho{rho}lB{lB}//r{r}rho{rho}lB{lB}.xyz")
#                         output_file = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//r_{int(r)}rho{rho}lB{lB}//proj_r{r}rho{rho}lB{lB}.xyz")
#                         if input_file.is_file():
#                             cylinder_to_plane.process_xyz(input_file=input_file, output_file=output_file)
#                             num_atoms, comment, atoms = cylinder_to_plane.read_xyz(output_file)
#                             cylinder_to_plane.scatter_plot_proj(atoms, species_color, f'{output_file}.png')

#                         else:
#                             print(f'Not cylinder_bending in {input_file} ')
#                             input_file = Path(f"C://Users//Hp//Documents//data_simulations//XYZ_miztli//r{float(r)}rho{rho}lA{lA}lB{lB}.xyz") 
                            
#                             if input_file.is_file():
#                                 cylinder_to_plane.process_xyz(input_file=input_file, output_file=output_file)
#                                 num_atoms, comment, atoms = cylinder_to_plane.read_xyz(output_file)
#                                 cylinder_to_plane.scatter_plot_proj(atoms, species_color, f'{output_file}.png')

#                             #     print(input_file)
#                             #     print(output_file)
#                             else:
#                                 print(f'Not cylinder_bending:{input_file}')
#                                 continue
#                             #continue
#     except Exception as e:
#         print(str(e))

# if __name__ == '__main__':
#     main()

def main():
    cylinder_to_plane = CylinderBending()
    try:
        with open('particles.json', 'r') as file:
            data = json.load(file)
        with open('specie_particles_color.json','r') as f:
            species_color = json.load(f)

        r = 3.0
        rho = 0.3
        lA = 2.5
        lB = 1.11
        
        # input_file =  Path(f"C://Users//Hp//Documents//data_simulations/XYZ_ADA//r{float(r)}rho{rho}lA{lA}lB{lB}.xyz") 
        # output_file = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//proj_r{r}rho{rho}lA{lA}lB{lB}.xyz")

        input_file = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//r_{int(r)}rho{rho}lA{lA}//r{r}rho{rho}lA{lA}.xyz")
        output_file = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//r_{int(r)}rho{rho}la{lA}//proj_r{r}rho{rho}lA{lA}.xyz")
        if input_file.is_file():
            cylinder_to_plane.process_xyz(input_file=input_file, output_file=output_file)
            num_atoms, comment, atoms = cylinder_to_plane.read_xyz(output_file)
            cylinder_to_plane.scatter_plot_proj(atoms, species_color, f'{output_file}.png')

        else:
            print(f'Not cylinder_bending in {input_file} ')            

    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main()