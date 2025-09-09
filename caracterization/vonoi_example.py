import freud
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def hexagonal_lattice(rows=3, cols=3, noise=0, seed=None):
    if seed is not None:
        np.random.seed(seed)
    # Assemble a hexagonal lattice
    points = []
    for row in range(rows * 2):
        for col in range(cols):
            x = (col + (0.5 * (row % 2))) * np.sqrt(3)
            y = row * 0.5
            points.append((x, y, 0))
    points = np.asarray(points)
    points += np.random.multivariate_normal(
        mean=np.zeros(3), cov=np.eye(3) * noise, size=points.shape[0]
    )
    # Set z=0 again for all points after adding Gaussian noise
    points[:, 2] = 0

    # Wrap the points into the box
    box = freud.box.Box(Lx=cols * np.sqrt(3), Ly=rows, is2D=True)
    points = box.wrap(points)
    return box, points

# Compute the Voronoi diagram
box, points = hexagonal_lattice(rows=12, cols=8, noise=0.03, seed=2)
voro = freud.locality.Voronoi()
voro.compute((box, points))

# Plot Voronoi with points and a custom cmap
plt.figure()
ax = plt.gca()
voro.plot(ax=ax, cmap="RdBu")
ax.scatter(points[:, 0], points[:, 1], s=2, c="k")
plt.show()