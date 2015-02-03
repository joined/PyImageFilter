#!.env/bin/python

import argparse
import numpy as np
import sys
from random import randrange
from PIL import Image
from imagefilter.imagefilter import ImageFilter
from imagefilter.masks import Masks


class OrderNamespace(argparse.Namespace):

    """
    Override default Namespace to keep
    optional arguments order, in order to
    apply the transformations correctly
    """

    def __init__(self, **kwargs):
        self.__dict__['order'] = []
        super(OrderNamespace, self).__init__(**kwargs)

    def __setattr__(self, attr, value):
        self.__dict__['order'].append(attr)
        super(OrderNamespace, self).__setattr__(attr, value)

if __name__ == "__main__":
    description = """
    Script for linear and nonlinear image filtering.
    LG 2015
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('input_image',
                        type=str,
                        help='input image filename')
    parser.add_argument('-a', '--average',
                        type=int,
                        metavar='RANK',
                        choices=[3, 5, 7, 9],
                        help='average mask')
    parser.add_argument('-m', '--median',
                        type=int,
                        metavar='RANK',
                        choices=[3, 5, 7, 9],
                        help='median transform')
    parser.add_argument('-t', '--tone',
                        type=float,
                        help='tone mask, must be between 0 and 1')
    parser.add_argument('-s', '--sharpen',
                        type=int,
                        metavar='TYPE',
                        choices=[1, 2, 3],
                        help='sharpen transform mask')
    parser.add_argument('-p', '--prewitt',
                        type=int,
                        metavar='TYPE',
                        choices=[1, 2],
                        help='prewitt transform mask')
    parser.add_argument('-sb', '--sobel',
                        type=int,
                        metavar='TYPE',
                        choices=[1, 2],
                        help='sobel transform mask')
    parser.add_argument('-o', '--output',
                        metavar='OUTPUT_IMAGE',
                        default='output_%d.jpg' % randrange(100),
                        help='output image filename')
    parser.add_argument('-c', '--custom',
                        metavar='MASK',
                        help='custom mask transform')
    args = parser.parse_args(None, OrderNamespace())

    try:
        im = Image.open(args.input_image)
    except FileNotFoundError:
        print('File not found.')
        sys.exit(1)

    ordered_args = args.order[9:-1]

    for arg in ordered_args:
        if arg == 'average':
            im = ImageFilter(im).lin_trans(Masks.avg(args.average))
        elif arg == 'tone':
            im = ImageFilter(im).lin_trans(Masks.tone(args.tone))
        elif arg == 'sharpen':
            im = ImageFilter(im).lin_trans(Masks.sharpen[args.sharpen - 1])
        elif arg == 'prewitt':
            im = ImageFilter(im).lin_trans(Masks.prewitt[args.prewitt - 1])
        elif arg == 'sobel':
            im = ImageFilter(im).lin_trans(Masks.sobel[args.sobel - 1])
        elif arg == 'median':
            im = ImageFilter(im).median_trans(args.median)

    try:
        im.save(args.output)
    except IOError:
        print('Error saving file.')
