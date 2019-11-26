#!/usr/bin/env python3

import numpy as np
import getopt, sys
from somlib import *

def main():
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
        print ('usage: som.py -s SIZE -i INPUT_FILE [-o OUTPUT_FILE]', file=sys.stderr)
        sys.exit(2)

    data = load_csv(filepath_in)

    input_rows_cnt = len(data)
    input_rows_len = len(data[0])

    m = matrix_init(mx, my, input_rows_len)

    # the init is basically complete at this point


    # TODO: 3D matrix representation
    neighborhood = {
        0: [1, 2],
        1: [0, 3],
        2: [0, 3],
        3: [1, 2],
    }
    # weights = np.random((x, y), ?)
    weights = np.array([
        (1, 2, 3),
        (3, 2, 1),
        (2, 3, 1),
        (0, 0, 0),
    ], dtype=float)
    vector = np.array((0, 1, 0))

    def theta(degrees_of_separation):
        if degrees_of_separation == 0:
            return 1.
        else:
            return 0.75

    def rate(epoch_number):
        return 0.1

    # Best matching unit = idx of smallest ||weight - input||
    bmu = np.argmin(np.sum((weights - vector) ** 2, axis=1))
    neighbors = neighborhood[bmu]
    print(weights)
    weights[bmu] += theta(0) * rate(0) * (vector - weights[bmu])
    for n in neighbors:
        weights[n] += theta(1) * rate(0) * (vector - weights[n])
    print(weights)

if __name__ == '__main__':
    main()
