from itertools import cycle, islice
import numpy as np


class SOM(object):
    def __init__(self, m, n, width, init='regular'):
        self.m = m
        self.n = n
        self.width = width
        if init == 'regular':
            xs, ys = np.meshgrid(np.linspace(0, 1, m), np.linspace(0, 1, n))
            self.weights = np.dstack(list(islice(cycle([xs, ys]), width)))
        elif init == 'random':
            self.weights = np.random.random((m, n, width))
        else:
            raise ValueError('Unknown weight init type %s' % init)

    def learn(self, vs, epochs=3, starting_rate=.1, neighborhood=2):
        for epoch in range(epochs):
            rate = starting_rate * (.5 ** epoch)
            self.learn_once(vs, rate, neighborhood)

    def learn_once(self, vs, rate=.1, neighborhood=2):
        for v in vs:
            self.learn_one(v, rate, neighborhood)

    def learn_one(self, v, rate=.1, neighborhood=2):
        d = neighborhood
        diff = v - self.weights
        i, j = self.find_bmu(diff)

        range_x = np.arange(max(0, i - d), min(self.m, i + d + 1))
        range_y = np.arange(max(0, j - d), min(self.n, j + d + 1))
        theta = 2 + \
            np.abs(range_x[np.newaxis, :] - i) + \
            np.abs(range_y[:, np.newaxis] - j)
        xs, ys = np.meshgrid(range_x, range_y, copy=False)
        self.weights[xs, ys] += \
            rate * np.divide(diff[xs, ys], theta[:, :, np.newaxis])
        return i, j

    def find_bmu(self, diff):
        bmu = np.argmin(np.sum(diff ** 2, axis=2))
        return bmu // self.m, bmu % self.m

    def get_neighborhood(self, i, j, d):
        return ((x, y, 2 + abs(i - x) + abs(j - y))
                for x in range(i - d, i + d + 1)
                for y in range(j - d, j + d + 1)
                if 0 <= x < self.m and 0 <= y < self.n)
