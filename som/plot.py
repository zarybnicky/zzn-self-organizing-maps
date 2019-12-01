import matplotlib.pyplot as plt
import numpy as np


# plot a matrix into a 3D graph
def show_3d_hist(matrix):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    xedges = np.array(range(len(matrix) + 1))
    yedges = np.array(range(len(matrix[0]) + 1))

    xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25, indexing="ij")
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos = 0

    dx = dy = 0.5 * np.ones_like(zpos)
    dz = matrix.ravel()
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')

    plt.show()
