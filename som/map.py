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
        i, j = self.find_bmu(v)
        for ii, jj, theta in self.get_neighborhood(i, j, neighborhood):
            self.weights[ii, jj] += rate / theta * (v - self.weights[ii, jj])
        return i, j

    def find_bmu(self, v):
        bmu = np.argmin(np.sum((self.weights - v) ** 2, axis=2))
        return bmu // self.m, bmu % self.m

    def get_neighborhood(self, i, j, d):
        return ((x, y, theta_fn(i, j, x, y))
                for x in range(i - d, i + d + 1)
                for y in range(j - d, j + d + 1)
                if 0 <= x < self.m and 0 <= y < self.n)


def theta_fn(ai, aj, bi, bj):
    return 2 + abs(ai - bi) + abs(aj - bj)
