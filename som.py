#!/usr/bin/env python3

import click
import numpy as np
import sys
import time

from som.map import SOM


@click.group()
def cli():
    pass


@cli.command()
@click.option('--animate', is_flag=True, help='whether to show a training visualization')
@click.option('--animate-interval', default=50, help='redraw every N epochs')
@click.option('--animate-pause', default=0.5, help='pause between frames')
@click.option('--model', '-m', default='', help='Where to save the trained model')
@click.option('--skip-rows', default=0)
@click.option('--rate', default=0.1)
@click.option('--rate-decay', default=0)
@click.option('--neighborhood', default=2)
@click.option('--size', '-S', default='10x10')
@click.option('--epochs', default=3)
@click.argument('INFILE')
def train(animate, animate_interval, animate_pause, model, skip_rows,
          rate, rate_decay, neighborhood, size, epochs, infile):
    mx, my = [int(x) for x in size.split('x')]
    data = np.loadtxt(infile)
    som = SOM(mx, my, len(data[0]))

    def train_inner(rate, win=None):
        for i in range(epochs):
            if rate_decay:
                rate *= rate_decay ** i
            som.learn_once(data, rate=rate, neighborhood=neighborhood)
            if animate and i % animate_interval == 0:
                draw_2d_map(win, som.weights)
                time.sleep(animate_pause)

    if animate:
        from som.graphics import get_window, draw_2d_map, draw_vecs
        with get_window() as win:
            draw_vecs(win, data)
            draw_2d_map(win, som.weights)
            train_inner(rate, win)
    else:
        train_inner(rate)

    if model:
        np.savez(model, weights=som.weights)


@cli.command()
@click.argument('model')
def visualize(model):
    from som.graphics import get_window, get_windows, draw_2d_map
    data = np.load(model)
    if len(data.files) == 1:
        with get_window() as win:
            draw_2d_map(win, data[data.files[0]])
    else:
        for i, win in enumerate(get_windows(len(data.files))):
            draw_2d_map(win, data[data.files[i]])
        click.pause()


@cli.command()
@click.option('--dims', default=2, help='sample length')
@click.option('--clusters', default=0, help='number clusters to generate')
@click.argument('count', type=int)
def generate(dims, clusters, count):
    data = np.random.random((count, dims))
    if clusters > 0:
        data /= clusters
        for i in range(1, clusters):
            for dim in range(dims):
                if dim % 2 == 0:
                    data[i::clusters, dim] += i / clusters
                else:
                    data[i::clusters, dim] += (clusters - i) / clusters
    np.savetxt(sys.stdout, data)


@cli.command()
@click.option('--shuffle/--no-shuffle', default=True)
@click.option('--ratio', default=.8)
@click.option('--skip-rows', default=0)
@click.argument('infile')
@click.argument('train')
@click.argument('test')
def split_train_test(shuffle, ratio, skip_rows, infile, train, test):
    csv = np.loadtxt(infile, delimiter=',', skiprows=skip_rows)
    training_size = round(len(csv) * ratio)
    if shuffle:
        shuffled = np.random.permutation(csv.shape[0])
        np.savetxt(train, csv[shuffled[:training_size], :])
        np.savetxt(test, csv[shuffled[training_size:], :])
    else:
        np.savetxt(train, csv[:training_size, :])
        np.savetxt(test, csv[training_size:, :])


if __name__ == '__main__':
    cli()
