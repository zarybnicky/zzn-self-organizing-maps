import argparse


parser = argparse.ArgumentParser(prog='som.py')
subparsers = parser.add_subparsers(help='Actions')
parser_learn = subparsers.add_parser('train', help='Train a SOM on specified CSV data')
parser_learn.add_argument('size', nargs=2, metavar='N', type=int)
parser_learn.add_argument('infile', metavar='FILE')
parser_learn.add_argument('-m', '--model', metavar='MODEL')
parser_learn.add_argument('-L', '--label-pos', metavar='POSITION', type=int)
parser_learn.add_argument('-l', '--label-model', metavar='MODEL')
parser_learn.add_argument('--skip-first-row', action='store_true')
