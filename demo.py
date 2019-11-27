#!/usr/bin/env python3

import numpy as np
import sys, getopt, csv
import numpy.matlib, time, random
from somlib import *

################################################################################################################



def mainx():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 's:i:o:', [])
    except getopt.GetoptError as err:
        print(err, file=sys.stderr)
        sys.exit(2)

    mx, my, filepath_in = None, None, None
    for o, a in opts:
        if o == '-s':
            mx, my = get_sizes_from_cli(a)
        elif o == '-i':
            filepath_in = a
        elif o == '-o':
            filepath_out = a

    if mx == None or my == None or filepath_in == None:
        print ('ERROR', file=sys.stderr)
        sys.exit(2)

    data = load_csv(filepath_in)

    input_rows_cnt = len(data)
    input_rows_len = len(data[0])

    m = matrix_init(mx, my, input_rows_len)

    print("MATRIX INIT - DONE")


    cnt = 0
    percent = input_rows_cnt / 100
    percent_finished = 0
    for v in data:
        i = get_bmu(m, v)
        m[i] += 0.1 * (v - m[i])
        for neighbor_idx in get_idx_neighbors(mx, my, i):
            m[neighbor_idx] += 0.75 * 0.1 * (v - m[neighbor_idx])

        cnt += 1
        if cnt >= percent:
            percent_finished += 1
            print(percent_finished, '% DONE')
            cnt = 0
    #print ('Q', q)


    #sums = list(map(lambda x: sum(x), m))
    #show_3d_hist(np.array(sums).reshape(mx, my))


    #show_3d_hist(np.array(map(lambda x: sum(x), m)).reshape(mx, my))

def map_init_reg(x, y):
    arr = []
    for j in range(x):
        for i in range(y):
            arr.append([j*100, i*100])
    return np.array(arr, dtype=float)

def main():
    m = map_init_reg(5, 5)

    vec = np.array([[327,120],[293,318],[232,223],[90,381],[392,387],[105,282],[208,197],[129,298],[146,286],[320,210]], dtype=float)

    init_draw()
    draw_2d_map(m, 5, [])
    i = 0
    for v in vec:
        bmu = get_bmu(m, v)
        m[bmu] += 0.1 * (v - m[bmu])
        for neighbor in get_idx_neighbors(5, 5, bmu):
            m[bmu] += 0.1 * 0.75 * (v - m[bmu])

        i += 1
        draw_2d_map(m, 5, vec[:i])

    finish_draw()



if __name__ == '__main__':
    main()
