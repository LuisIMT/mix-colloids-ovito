import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import freud, json
from cylinder_bending import CylinderBending

class PatternDiffraction:
    def __init__(self) -> None:
        self.my_data = CylinderBending()
        
        pass
    def create_particle_system(self,positions, box_size, is2D=True):
        box = freud.box.Box(Lx=40,Ly=40,Lz=box_size) 
        points = np.array(positions)          
        return box, points
    
    def diffraction_pattern(self,input_file, output_file, box_size = 40):
        _, _, atoms = self.my_data.read_xyz(file_path=input_file)

        positions = np.array([[x,y,0] for _, x, y, _, in atoms])
        box, points = self.create_particle_system(positions, box_size)
        dp = freud.diffraction.DiffractionPattern(grid_size=520)
        fig, ax = plt.subplots(figsize=(4, 4), dpi=520)
        dp.compute((box, points),view_orientation=[1, 0, 0, 0],peak_width=14)
        dp.plot(ax, cmap='hot')
        ax.set_title(f'Patrón de Difracción', fontsize=16)

        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close(fig)
        #plt.show()

    def plot_rdf(self,input_file,output_file,prop, box_size=40, r_max=5, bins=120):
        _, _, atoms = self.my_data.read_xyz(file_path=input_file)
        positions = np.array([[x,y,0] for _, x, y, _ in atoms])
        box, points = self.create_particle_system(positions, box_size)
        fig, ax = plt.subplots(figsize=(6, 6),dpi=300)
        rdf = freud.density.RDF(bins, r_max)
        rdf.compute(system=(box, points))
        ax.plot(rdf.bin_centers, getattr(rdf, prop), color='black', linewidth=2)
        ax.set_title("Función de Distribución Radial", fontsize=16)
        ax.set_xlabel(r"$r$", fontsize=14)
        ax.set_ylabel(r"$g(r)$", fontsize=14)
    
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close(fig)
        #plt.show()
    def plot_rdf(self, input_file, output_file, prop, box_size=40, r_max=5, bins=120):
        _, _, atoms = self.my_data.read_xyz(file_path=input_file)
        positions = np.array([[x, y, 0] for _, x, y, _ in atoms])
        box, points = self.create_particle_system(positions, box_size)
        
        # Cambiar figsize para hacerlo cuadrado (mismo valor en ambos ejes)
        fig, ax = plt.subplots(figsize=(6, 6), dpi=520)  # Ajusta 6, 6 para el tamaño deseado
        rdf = freud.density.RDF(bins, r_max)
        rdf.compute(system=(box, points))
        
        ax.plot(rdf.bin_centers, getattr(rdf, prop), color='black', linewidth=2)
        
        # Modificar fontsize del título y los labels
        ax.set_title("Función de Distribución Radial", fontsize=16)  # Título con fontsize 16
        ax.set_xlabel(r"$r$", fontsize=14)  # Etiqueta x con fontsize 14
        ax.set_ylabel(r"$g(r)$", fontsize=14)  # Etiqueta y con fontsize 14

        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close(fig)
        # plt.show()

# def main():
#     patterndiffraction = PatternDiffraction()
#     try:
#         with open('particles.json', 'r') as file:
#             data = json.load(file)

#         for r in data['radio']:
#             for rho in data['rho']:
#                 for lA in data['lA']:
#                     for lB in data['lB']:
#                         # input_file = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//proj_r{float(r)}rho{rho}lA{lA}lB{lB}.xyz")
#                         # output_file = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//dp_r{float(r)}rho{rho}lA{lA}lB{lB}.png")
#                         input_file = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//r_{int(r)}rho{rho}lA{lA}//proj_r{r}rho{rho}lA{lA}.xyz")
#                         output_file = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//r_{int(r)}rho{rho}lA{lA}//dp_r{r}rho{rho}lA{lA}.png")
#                         # output_file_rdf = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//rdf_r{float(r)}rho{rho}lA{lA}lB{lB}.png")
#                         output_file_rdf = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//r_{int(r)}rho{rho}lA{lA}//rdf_r{float(r)}rho{rho}lA{lA}.png")
#                         # output_file_sk = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//sk_r{float(r)}rho{rho}lA{lA}lB{lB}.png")
#                         output_file_sk = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//r_{int(r)}rho{rho}lA{lA}//sk_r{float(r)}rho{rho}lA{lA}.png")
#                         if input_file.is_file():
#                             patterndiffraction.diffraction_pattern(input_file=input_file, output_file=output_file)
#                             patterndiffraction.plot_rdf(input_file=input_file,output_file=output_file_rdf, prop= "rdf")
#                             patterndiffraction.structure_factor(input_file=input_file, output_file=output_file_sk)
#                         else:
#                             print(f'not found {input_file}')
#                             continue
#     except Exception as e:
#         print(str(e))

# if __name__ == '__main__':
#     main()

def main():
    patterndiffraction = PatternDiffraction()
    try:
        with open('particles.json', 'r') as file:
            data = json.load(file)

        r = 3.0
        rho = 0.3
        lA = 2.5
        lB = 1.11

        input_file_sys = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//proj_r{float(r)}rho{rho}lA{lA}lB{lB}.xyz")
        output_file_sys = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//dp_r{float(r)}rho{rho}lA{lA}lB{lB}.png")
        output_file_rdf_sys = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//rdf_r{float(r)}rho{rho}lA{lA}lB{lB}.png")
        output_file_sk_sys = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//sk_r{float(r)}rho{rho}lA{lA}lB{lB}.png")
        
        if input_file_sys.is_file():
            # patterndiffraction.diffraction_pattern(input_file=input_file_sys, output_file=output_file_sys)
            patterndiffraction.plot_rdf(input_file=input_file_sys,output_file=output_file_rdf_sys, prop= "rdf")
            # patterndiffraction.structure_factor(input_file=input_file_sys, output_file=output_file_sk_sys)
        else:
            print(f'not found {input_file_sys}') 

        # input_file_A = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//r_{int(r)}rho{rho}lA{lA}//proj_r{r}rho{rho}lA{lA}.xyz")
        # output_file_A = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//r_{int(r)}rho{rho}lA{lA}//dp_r{r}rho{rho}lA{lA}.png")
        # output_file_rdf_A = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//r_{int(r)}rho{rho}lA{lA}//rdf_r{float(r)}rho{rho}lA{lA}.png")
        # output_file_sk_A = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//r_{int(r)}rho{rho}lA{lA}//sk_r{float(r)}rho{rho}lA{lA}.png")
        # if input_file_A.is_file():
        #     # patterndiffraction.diffraction_pattern(input_file=input_file_A, output_file=output_file_A)
        #     patterndiffraction.plot_rdf(input_file=input_file_A,output_file=output_file_rdf_A, prop= "rdf")
        #     # patterndiffraction.structure_factor(input_file=input_file_A, output_file=output_file_sk_A)
        # else:
        #     print(f'not found {input_file_A}') 

        # input_file_B = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//r_{int(r)}rho{rho}lB{lB}//proj_r{r}rho{rho}lB{lB}.xyz")
        # output_file_B = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//r_{int(r)}rho{rho}lB{lB}//dp_r{r}rho{rho}lB{lB}.png")
        # output_file_rdf_B = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//r_{int(r)}rho{rho}lB{lB}//rdf_r{float(r)}rho{rho}lB{lB}.png")
        # output_file_sk_B = Path(f"C://Users//Hp//simulations//core-shell//50_50//Radio_{int(r)}//rho_{rho}//lambdA_{lA}//lambdB_{lB}//r_{int(r)}rho{rho}lB{lB}//sk_r{float(r)}rho{rho}lB{lB}.png")
        # if input_file_B.is_file():
        #     patterndiffraction.diffraction_pattern(input_file=input_file_B, output_file=output_file_B)
        #     patterndiffraction.plot_rdf(input_file=input_file_B,output_file=output_file_rdf_B, prop= "rdf")
        #     patterndiffraction.structure_factor(input_file=input_file_B, output_file=output_file_sk_B)
        # else:
        #     print(f'not found {input_file_B}')
        
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main()