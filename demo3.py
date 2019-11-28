#!/usr/bin/env python3

import numpy as np
import sys, getopt, csv
import numpy.matlib, time, random
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

    if mx == None or my == None or filepath_in == None:
        print ('ERROR', file=sys.stderr)
        sys.exit(2)

    print('loading CSV...  ', end='', flush=True)
    data, model = load_csv(filepath_in)
    print('DONE', flush=True)

    input_rows_cnt = len(data)
    input_rows_len = len(data[0])

    print("INITIALIZING MAP...  ", end='', flush=True)

    m = matrix_init(mx, my, input_rows_len)
    neuron_digit_count = np.array([[0,0,0,0,0,0,0,0,0,0]] * (mx*my))

    print('DONE', flush=True)

    percent_done = 0
    classify_cnt = 1000
    percent_cnt = 0
    one_percent = (input_rows_cnt - classify_cnt)/ 100

    for i in range(input_rows_cnt - classify_cnt):
        vec = data[i]
        bmu_idx = get_bmu(m, vec)
        cur_dig = model[i]

        neuron_digit_count[bmu_idx][cur_dig] += 4

        m[bmu_idx] += 0.1 * (vec - m[bmu_idx])
        for neighbor_idx in get_idx_neighbors(mx, my, bmu_idx):
            m[neighbor_idx] += 0.75 * 0.1 * (vec - m[neighbor_idx])
            neuron_digit_count[neighbor_idx][cur_dig] += 3

        percent_cnt += 1
        if percent_cnt >= one_percent and input_rows_cnt >= 100:
            percent_done += 1
            print('TRAINING ', percent_done, '%')
            percent_cnt = 0

    print('CLASSIFY...')
    succ = 0
    for i in range(input_rows_cnt - classify_cnt, input_rows_cnt):
        bmu = get_bmu(m, data[i])
        pdig = np.argmax(neuron_digit_count[bmu])
        if pdig == model[i]:
            succ += 1

    print ('SUCCESS:', succ, 'out of', classify_cnt, '   ', round(succ/classify_cnt * 100, 2), '%')

    print ('\nMAP:')
    for i in range(mx):
        for j in range(my):
            print (np.argmax(neuron_digit_count[i*mx+j]), end='  ')
        print('')

if __name__ == '__main__':
    main()
