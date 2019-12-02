#!/usr/bin/env python3

import numpy as np
import time

from som.graphics import get_window, draw_2d_map
from som.map import SOM


def main():
    som = SOM(6, 6, 2)
    vec = np.random.random((20, 2))

    with get_window() as win:
        draw_2d_map(win, som.weights, [])
        for i in range(15):
            som.learn(vec)
            draw_2d_map(win, som.weights, vec)
            time.sleep(0.5)


if __name__ == '__main__':
    main()
