import sys, json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Obtén la ruta absoluta del directorio 'caracterization'
script_dir = Path(__file__).resolve().parent  # Directorio donde se encuentra el script actual
caracterization_dir = script_dir.parent / 'caracterization'  # Un nivel arriba y luego en 'caracterization'

# Verifica si ya está en el sys.path, si no, añádelo
if str(caracterization_dir) not in sys.path:
    sys.path.append(str(caracterization_dir))

# Imprimir sys.path para depuración
print("sys.path:", sys.path)

# Ahora intenta importar el módulo
try:
    from cylinder_bending import CylinderBending
except ModuleNotFoundError as e:
    print(f"Error al importar: {e}")


class ASpeciesParticles:
    def __init__(self, file_path) -> None:
        self.my_data = CylinderBending()
        self.file_path = file_path
        self.base_name = self.file_path.stem  # Nombre del archivo sin extensión
        self.particle_type_A = []  # Lista para partículas del tipo A
        self.particle_type_B = []  # Lista para partículas del tipo B

    def process(self, xyz_file):
        """Lee el archivo xyz y separa las partículas en dos listas (A y B)."""
        _, space, particles = self.my_data.read_xyz(file_path=xyz_file)
        particles_A = []
        particles_B = []

        for species in particles:
            if species[0] == 'H':
                particles_A.append(species)  # Corregido: añadir solo la partícula A
            elif species[0] == 'F':
                particles_B.append(species)  # Corregido: añadir solo la partícula B
        num_A = len(particles_A)
        num_B = len(particles_B)
        return num_A, particles_A, num_B, particles_B, space

    def find_folder_structure(self, r, rho, lA, lB):
        """Buscar carpetas con los nombres correspondientes basados en el archivo original."""
        # Ruta base donde se buscarán las carpetas
        base_dir = Path(f"C://Users//Hp//simulations//core-shell//50_50//")

        # Rutas completas para las carpetas
        folder_A = base_dir/f"Radio_{int(r)}"/f"rho_{rho}"/f"lambdA_{lA}"/f"lambdB_{lB}"/f"r_{int(r)}rho{rho}lA{lA}"
        folder_B =  base_dir/f"Radio_{int(r)}"/f"rho_{rho}"/f"lambdA_{lA}"/f"lambdB_{lB}"/f"r_{int(r)}rho{rho}lB{lB}"

        # Verificar si las carpetas existen
        folder_A_exists = folder_A.exists()
        folder_B_exists = folder_B.exists()

        # Crear nombres de archivo
        if folder_A_exists:
            file_name_A = f"r{float(r)}rho{rho}lA{lA}.xyz"
        else:
            print(f"folder not found : {folder_A}")
    
        if folder_B_exists:
            file_name_B = f"r{float(r)}rho{rho}lB{lB}.xyz"
        else:
            print(f"folder not found: {folder_B}")

        # Retornar la información, junto con el estado de existencia de las carpetas
        return folder_A, folder_B, file_name_A, file_name_B


    def write_xyz_3D(self,folder, file_name , num_atoms, comment, modified_atoms):
        file_path = folder / file_name
        with open(file_path, 'w') as file:
            file.write(f"{num_atoms}\n")  # Escribir número de átomos
            file.write(f"{comment}\n")    # Escribir comentario
            
            # Escribir las coordenadas modificadas
            for especie, x,y,z in modified_atoms[:-1]:
                file.write(f"{especie}\t{x:.6f}\t{y:.6f}\t{z:.6f}\n")  # Formato con 6 decimales para consistencia
            
            # Escribir la última línea sin salto de línea al final
            especie, x,y, z = modified_atoms[-1]  # Cambiado para desempaquetar correctamente
            file.write(f"{especie}\t{x:.9f}\t{y:.6f}\t{z:.9f}")  # Formato con 9 decimales    

    
def main():
    try:
        with open('particles.json', 'r') as file:
            data = json.load(file)
        with open('specie_particles_color.json','r') as f:
            color_file = json.load(f)
        for r in data['radio']:
            for rho in data['rho']:
                for lA in data['lA']:
                    for lB in data['lB']:
                        input_file = Path(f"C://Users//Hp//Documents//data_simulations//XYZ_ADA//r{float(r)}rho{rho}lA{lA}lB{lB}.xyz")
                        species_particles = ASpeciesParticles(  file_path=input_file )
                        if input_file.is_file():
                            folder_A, folder_B, file_name_A, file_name_B = species_particles.find_folder_structure(r=r,rho=rho,lA=lA,lB=lB)
                            n_A, particles_A, n_B, particles_B, comment = species_particles.process(xyz_file=input_file)
                            species_particles.write_xyz_3D(folder=folder_A, file_name= file_name_A,  modified_atoms=  particles_A, num_atoms= n_A,comment=comment)
                            species_particles.write_xyz_3D(folder=folder_B, file_name= file_name_B, modified_atoms= particles_B, num_atoms= n_B,comment=comment)
                        else:
                            print(f'file not found :{input_file}')
                            input_file = Path(f"C://Users//Hp//Documents//data_simulations//XYZ_miztli//r{float(r)}rho{rho}lA{lA}lB{lB}.xyz") 
                            if input_file.is_file():
                                folder_A, folder_B, file_name_A, file_name_B = species_particles.find_folder_structure(r=r,rho=rho,lA=lA,lB=lB)
                                n_A, particles_A, n_B, particles_B, comment = species_particles.process(xyz_file=input_file)
                                species_particles.write_xyz_3D(folder=folder_A, file_name= file_name_A, modified_atoms= particles_A, num_atoms= n_A,comment=comment)
                                species_particles.write_xyz_3D(folder=folder_B, file_name= file_name_B, modified_atoms= particles_B, num_atoms= n_B,comment=comment) 
                            else:
                                print(f'file not found :{input_file}')
                                continue
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main()
