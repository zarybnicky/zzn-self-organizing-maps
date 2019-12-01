#!/usr/bin/env python3

import numpy as np
import time
from som.graphics import get_window, draw_2d_map
from som.map import SOM


def main():
    som = SOM(10, 10, 2)
    vec = np.random.random((900, 2)) * 0.2
    vec[1::3, 0] += 0.2
    vec[1::3, 1] += 0.6
    vec[2::3, 0] += 0.6
    vec[2::3, 1] += 0.2

    with get_window(950, 950) as win:
        for i, v in enumerate(vec):
            som.learn_one(v)
            if i % 50 == 0:
                draw_2d_map(win, som.weights, vec[:i])
                time.sleep(.5)


if __name__ == '__main__':
    main()
