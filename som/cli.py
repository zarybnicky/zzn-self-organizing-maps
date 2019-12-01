import getopt
import sys


class Config:
    mx = None
    my = None
    infile = None
    skip_first = None
    outfile = None


def parse_cli(args):
    try:
        opts, args = getopt.getopt(args, 's:i:o:S', [])
    except getopt.GetoptError as err:
        print(err, file=sys.stderr)
        sys.exit(2)

    cfg = Config()
    for o, a in opts:
        if o == '-s':
            try:
                mx, my = map(int, a.split('x'))
                if mx < 1 or my < 1:
                    raise ValueError
                cfg.mx = mx
                cfg.my = my
            except ValueError:
                print('error: wrong format of matrix size, should be: "MxN"', file=sys.stderr)
                sys.exit(2)
        elif o == '-i':
            cfg.infile = a
        elif o == '-o':
            cfg.outfile = a
        elif o == '-S':
            cfg.skip_first = True

    if cfg.mx is None or cfg.my is None or cfg.infile is None:
        print('usage: som.py -s SIZE -i INPUT_FILE [-o OUTPUT_FILE] [-S]', file=sys.stderr)
        sys.exit(2)

    return cfg
