#!/usr/bin/env python3

import random, csv, time, sys, numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from graphics import *


# generates array of given length with random value between 0-100
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

# create the map with random values
def matrix_init(x, y, vec_len):
    m = [0] * (x * y)
    random.seed(round(time.time()))
    for i in range(x * y):
        m[i] = generate_neuron(vec_len)
    return np.array(m, dtype=float)


# find best-matching unit in the map
def get_bmu(matrix, vec):
    return np.argmin(np.sum((matrix - vec) ** 2, axis=1))


# load a csv file into a numpy array
def load_csv(filepath, ignore_first_row=True, model_in_first_column=True):
    offset = 1 if model_in_first_column else 0
    model = []

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
                if model_in_first_column:
                    model.append(int(line[0]))
    except IOError:
        print('error: cannot open "' + filepath + '"', file=sys.stderr)
        sys.exit(2)
    return np.array(tmpdata, dtype=float), model


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

    xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25, indexing="ij")
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos = 0

    dx = dy = 0.5 * np.ones_like(zpos)

    dz = matrix.ravel()

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')

    plt.show()


# drawing functionality
win = None
draw_objs = []

def init_draw(x=600, y=600):
    global win
    win = GraphWin('', x, y)


def draw_2d_map(m, x, vec):
    global draw_objs
    global win

    for obj in draw_objs:
        obj.undraw()
    draw_objs = []

    for point in m:
        c = Circle(Point(point[0], point[1]), 5)
        c.setFill('black')
        draw_objs.append(c)
        c.draw(win)

    for i in range(len(m)):
        if (i + 1) % x != 0:
            l = Line(Point(m[i][0], m[i][1]), Point(m[i+1][0], m[i+1][1]))
            draw_objs.append(l)
            l.draw(win)
        if (i + x) < len(m):
            l = Line(Point(m[i][0], m[i][1]), Point(m[i+x][0], m[i+x][1]))
            draw_objs.append(l)
            l.draw(win)

    for v in vec:
        c = Circle(Point(v[0], v[1]), 2)
        c.setOutline('red')
        c.setFill('red')
        draw_objs.append(c)
        c.draw(win)


def finish_draw():
    win.getMouse()
    win.close()



