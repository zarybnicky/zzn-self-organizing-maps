#!/usr/bin/env python3

import click
import functools
import numpy as np
from som.graphics import get_windows, draw_2d_map, draw_vecs
from som.map import SOM

print = functools.partial(print, flush=True)


@click.command()
@click.option('--epochs', default=10)
@click.option('--size', '-S', default='10x10')
@click.argument('infile')
def main(epochs, size, infile):
    mx, my = [int(x) for x in size.split('x')]

    print('Loading CSV...', end='')
    csv = np.loadtxt(infile, delimiter=',')
    maximum = np.max(csv)
    if maximum != 0:
        csv[:, :-1] /= maximum
    shuffled = np.random.permutation(csv.shape[0])
    training_size = round(len(shuffled) * .8)
    training_set = csv[shuffled[:training_size], :]
    print(training_set)
    validate_set = csv[shuffled[training_size:], :]
    print(' done.')

    print('Initializing map...', end='')
    som = SOM(mx, my, len(csv[0]) - 1)
    labels = np.zeros((mx, my, 3))
    label_map = {0: '  setosa  ',
                 1: 'versicolor',
                 2: 'virginica '}
    print(' done.')

    wins = list(get_windows(2))
    draw_vecs(wins[0], training_set[:, 0:2])
    draw_vecs(wins[1], training_set[:, 2:4])

    print('Training', end='')
    for epoch in range(epochs):
        for row in training_set:
            label = int(row[-1])
            i, j = som.learn_one(row[:-1], rate=.1, neighborhood=3)
            for ii, jj, theta in som.get_neighborhood(i, j, 2):
                labels[ii, jj, label] += 12 / theta
        print('.', end='')
        draw_2d_map(wins[0], som.weights[:, :, 0:2])
        draw_2d_map(wins[1], som.weights[:, :, 2:4])
    print(' done.')

    print('Classifying...', end='')
    succ = 0
    for row in validate_set:
        if np.argmax(labels[som.find_bmu(row[1:] - som.weights)]) == row[0]:
            succ += 1
    print(' done.')

    print('Success rate: %s%% (%s out of %s)' % (
        round(succ / len(validate_set) * 100, 2),
        succ, len(validate_set)
    ))

    print('Map:')
    for i in range(mx):
        for j in range(my):
            print(label_map[np.argmax(labels[i, j])], end='  ')
        print('')
    click.pause()


if __name__ == '__main__':
    main()
