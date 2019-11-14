#!/usr/bin/env python3

import numpy as np

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
