#!/usr/bin/env python3

import click
import functools
import numpy as np
from som.map import SOM

print = functools.partial(print, flush=True)


@click.command()
@click.option('--skip-rows', default=0)
@click.option('--size', '-S', default='10x10')
@click.argument('infile')
def main(skip_rows, size, infile):
    mx, my = [int(x) for x in size.split('x')]

    print('Loading CSV...', end='')
    csv = np.loadtxt(infile, delimiter=',', skiprows=skip_rows)
    shuffled = np.random.permutation(csv.shape[0])
    training_size = round(len(shuffled) * .8)
    training_set = csv[shuffled[:training_size], :]
    validate_set = csv[shuffled[training_size:], :]
    print(' done.')

    print('Initializing map...', end='')
    som = SOM(mx, my, len(csv[0]) - 1)
    digits = np.zeros((mx, my, 10))
    print(' done.')

    print('Training', end='')
    rate = .1
    rate_step = rate / 400
    for subset in np.array_split(training_set, len(training_set) // 200 + 1):
        for row in subset:
            digit = int(row[0])
            i, j = som.learn_one(row[1:], rate=rate, neighborhood=3)
            for ii, jj, theta in som.get_neighborhood(i, j, 2):
                digits[ii, jj, digit] += 12 / theta
        rate -= rate_step
        print('.', end='')
    print(' done.')

    print('Classifying...', end='')
    succ = 0
    for row in validate_set:
        if np.argmax(digits[som.find_bmu(row[1:] - som.weights)]) == row[0]:
            succ += 1
    print(' done.')

    print('Success rate: %s%% (%s out of %s)' % (
        round(succ / len(validate_set) * 100, 2),
        succ, len(validate_set)
    ))

    print('Map:')
    for i in range(mx):
        for j in range(my):
            print(np.argmax(digits[i, j]), end='  ')
        print('')


if __name__ == '__main__':
    main()
