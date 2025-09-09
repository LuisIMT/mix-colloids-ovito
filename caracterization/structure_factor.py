import freud
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from diffrations import create_particle_system, read_xyz
def graphs_k(box, points):
    bins = 500
    k_max = 30
    k_min = 1
    sfDirect = freud.diffraction.StaticStructureFactorDirect(
        bins=bins, k_max=k_max, k_min=k_min
    )
    sfDebye = freud.diffraction.StaticStructureFactorDebye(
        num_k_values=bins, k_max=k_max, k_min=k_min
    )
    sfDebye.compute((box,points), reset=False)
    sfDirect.compute((box,points), reset=False)

    plt.plot(sfDebye.k_values, sfDebye.S_k, label="Debye")
    plt.plot(sfDirect.bin_centers, sfDirect.S_k, label="Direct")
    plt.title("Static Structure Factor")
    plt.xlabel("$k$")
    plt.ylabel("$S(k)$")
    plt.legend()
    plt.show()

input_file = Path(r'C:\Users\Hp\simulations\core-shell\mix-colloids-ovito\proyeccion.xyz')
box_size =40
num_atoms, comment, atoms = read_xyz(input_file)
positions = np.array([[x,y,0] for _, x, y, _ in atoms])
# # # Crear el sistema de partículas
box, points = create_particle_system(positions, box_size)
graphs_k(box, points)
