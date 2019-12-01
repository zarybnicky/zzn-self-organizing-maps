#!/usr/bin/env python3

import numpy as np
import sys

from som.cli import parse_cli
from som.map import SOM


def main():
    cfg = parse_cli(sys.argv[1:])
    data = np.loadtxt(cfg.infile)
    som = SOM(cfg.mx, cfg.my, len(data[0]))
    som.learn(data, epochs=3)
    if cfg.outfile:
        np.savetxt(cfg.outfile, som.weights)
    else:
        print(som.weights)


if __name__ == '__main__':
    main()
