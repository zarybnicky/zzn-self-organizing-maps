#!/usr/bin/env python3

import numpy as np
import sys
import numpy.matlib, time, random, sys
from somlib import *

def generate_input():
    ret = []
    for i in range(300):
        ret.append([round(random.random() * 200+600), round(random.random() * 200 + 200)])
        ret.append([round(random.random() * 200+200), round(random.random() * 200+600)])
        ret.append([round(random.random() * 200), round(random.random() * 200)])

    return np.array(ret, dtype=float)

def map_init_reg(x, y):
    arr = []
    for j in range(x):
        for i in range(y):
            arr.append([j*100, i*100])
    return np.array(arr, dtype=float)

def main():
    mx, my = 10, 10
    m = map_init_reg(mx, my)

    vec = generate_input()

    init_draw(950, 950)
    draw_2d_map(m, mx, [])
    i = 0
    for v in vec:
        bmu = get_bmu(m, v)
        m[bmu] += 0.1 * (v - m[bmu])
        for neighbor in get_idx_neighbors(mx, my, bmu):
            m[neighbor] += 0.1 * 0.75 * (v - m[neighbor])

        i += 1
        if i % 100 == 0:
            draw_2d_map(m, mx, vec[:i])
            time.sleep(1)

    finish_draw()

if __name__ == '__main__':
    main()
