#!/usr/bin/env python3

import functools
import numpy as np
import sys

from som.cli import parse_cli
from som.map import SOM

print = functools.partial(print, flush=True)


def main():
    cfg = parse_cli(sys.argv[1:])

    print('Loading CSV...', end='')
    csv = np.loadtxt(cfg.infile, delimiter=',', skiprows=1 if cfg.skip_first else 0)
    shuffled = np.random.permutation(csv.shape[0])
    training_size = round(len(shuffled) * .8)
    training_set = csv[shuffled[:training_size], :]
    validate_set = csv[shuffled[training_size:], :]
    print(' done.')

    print('Initializing map...', end='')
    som = SOM(cfg.mx, cfg.my, len(csv[0]) - 1)
    digits = np.zeros((cfg.mx, cfg.my, 10))
    print(' done.')

    print('Training', end='')
    rate = .1
    rate_step = rate / 800
    for subset in np.array_split(training_set, len(training_set) // 100):
        for row in subset:
            digit = int(row[0])
            i, j = som.learn_one(row[1:], rate=rate, neighborhood=3)
            for ii, jj, theta in som.get_neighborhood(i, j, 1):
                digits[ii, jj, digit] += 12 / theta
        rate -= rate_step
        print('.', end='')
    print(' done.')

    print('Classifying...', end='')
    succ = 0
    for row in validate_set:
        if np.argmax(digits[som.find_bmu(row[1:])]) == row[0]:
            succ += 1
    print(' done.')

    print('Success rate: %s%% (%s out of %s)' % (
        round(succ / len(validate_set) * 100, 2),
        succ, len(validate_set)
    ))

    print('Map:')
    for i in range(cfg.mx):
        for j in range(cfg.my):
            print(np.argmax(digits[i, j]), end='  ')
        print('')


if __name__ == '__main__':
    main()
