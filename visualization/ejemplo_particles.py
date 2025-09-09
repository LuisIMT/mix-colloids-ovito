import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Datos de ejemplo
np.random.seed(42)
n = 100
rng = np.random.default_rng()

# Primera mitad de las partículas (verde)
xs_green = rng.uniform(-2.5, 2.5, n//2)
ys_green = rng.uniform(-2.5, 2.5, n//2)
zs_green = rng.uniform(-10, 10, n//2)

# Segunda mitad de las partículas (rojo)
xs_red = rng.uniform(-2.5, 2.5, n//2)
ys_red = rng.uniform(-2.5, 2.5, n//2)
zs_red = rng.uniform(-10, 10, n//2)

# Crear figura 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Dibujar el cilindro morado claro
theta = np.linspace(0, 2*np.pi, 50)
z_cylinder = np.linspace(-10, 10, 50)
theta_grid, z_grid = np.meshgrid(theta, z_cylinder)
x_cylinder = 2.5 * np.cos(theta_grid)
y_cylinder = 2.5 * np.sin(theta_grid)

ax.plot_surface(x_cylinder, y_cylinder, z_grid, color='thistle', alpha=0.3, rstride=5, cstride=5)

# Dibujar las partículas verdes (nucleo y corona) dentro del cilindro
ax.scatter(xs_green, ys_green, zs_green, color='green', s=50, label="Núcleo verde")  # Núcleo
ax.scatter(xs_green, ys_green, zs_green, color='lightgreen', s=200, alpha=0.5, label="Corona verde")  # Corona

# Dibujar las partículas rojas (nucleo y corona) dentro del cilindro
ax.scatter(xs_red, ys_red, zs_red, color='red', s=50, label="Núcleo rojo")  # Núcleo
ax.scatter(xs_red, ys_red, zs_red, color='lightcoral', s=200, alpha=0.5, label="Corona roja")  # Corona

# Configuración de la gráfica
ax.set_xlim([-2.5, 2.5])
ax.set_ylim([-2.5, 2.5])
ax.set_zlim([-10, 10])
ax.set(xticklabels=[], yticklabels=[], zticklabels=[])
plt.legend(loc='upper right')

plt.show()
