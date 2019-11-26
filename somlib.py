#!/usr/bin/env python3

import random, csv, time, sys, numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_neuron(length):
    arr = [0] * length
    for i in range(length):
         arr[i] = round(random.random() * 100)
    return arr


# get the map sizes from cli input in format: NxM
def get_sizes_from_cli(s):
    try:
        x, y = map(lambda c: int(c), s.split('x'))
        if x <= 0 or y <= 0:
            raise ValueError
    except ValueError:
        print('error: wrong format of matrix size, should be: "NxM"', file=sys.stderr)
        sys.exit(2)

    return x, y

# create the map
def matrix_init(x, y, vec_len):
    m = [0] * (x * y)
    random.seed(round(time.time()))
    for i in range(x * y):
        m[i] = generate_neuron(vec_len)
    return np.array(m, dtype=float)


def get_bmu(matrix, vec):
    return np.argmin(np.sum((matrix - vec) ** 2, axis=1))

# load a csv file into a numpy array
def load_csv(filepath, ignore_first_row=True, ignore_first_column=True):
    offset = 1 if ignore_first_column else 0

    try:
        with open(filepath, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            y = 0
            tmpdata = []
            for line in csv_reader:
                y += 1
                if ignore_first_row and y == 1:
                    continue
                tmpdata.append(tuple(map(lambda x: int(x), line[offset:])))
    except IOError:
        print('error: cannot open "' + filepath + '"', file=sys.stderr)
        sys.exit(2)
    return np.array(tmpdata, dtype=float)

# get neighboring indexes for index 'i' in matrix of sizes x,y
def get_idx_neighbors(x, y, i):
    ns = []
    if i % x != 0:
        ns.append(i - 1)
    if (i + 1) % x != 0:
        ns.append(i + 1)
    if i >= x:
        ns.append(i - x)
    if i < (x - 1) * y - 1:
        ns.append(i + x)

    return ns

# plot a matrix into a 3D graph
def show_3d_hist(matrix):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    xedges = np.array(range(len(matrix) + 1))
    yedges = np.array(range(len(matrix[0]) + 1))

    # Construct arrays for the anchor positions of the 16 bars.
    xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25, indexing="ij")
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos = 0

    # Construct arrays with the dimensions for the 16 bars.
    dx = dy = 0.5 * np.ones_like(zpos)

    dz = matrix.ravel()

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')

    plt.show()
