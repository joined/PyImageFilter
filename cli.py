#!.env/bin/python

import argparse
import numpy as np
import sys
import json
from random import randrange
from PIL import Image
from imagefilter.imagefilter import ImageFilter
from imagefilter.masks import Masks
from imagefilter.extras import OrderNamespace

if __name__ == "__main__":
    description = """Toolkit for linear and nonlinear image filtering.
                     LG 2015"""

    #########################################################
    # CLI arguments definition
    #########################################################
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('input_image',
                        type=str,
                        help='input image filename')

    parser.add_argument('--average',
                        type=int,
                        metavar='RANK',
                        choices=[3, 5, 7, 9],
                        help='average mask')

    parser.add_argument('--median',
                        type=int,
                        metavar='RANK',
                        choices=[3, 5, 7, 9],
                        help='median transform')

    parser.add_argument('--tone',
                        type=float,
                        help='tone mask, must be between 0 and 1')

    parser.add_argument('--sharpen',
                        type=int,
                        metavar='TYPE',
                        choices=[1, 2, 3],
                        help='sharpen transform mask')

    parser.add_argument('--prewitt',
                        type=int,
                        metavar='TYPE',
                        choices=[1, 2],
                        help='prewitt transform mask')

    parser.add_argument('--sobel',
                        type=int,
                        metavar='TYPE',
                        choices=[1, 2],
                        help='sobel transform mask')

    parser.add_argument('--output',
                        metavar='OUTPUT_IMAGE',
                        default='output_%d.jpg' % randrange(100),
                        help='output image filename')

    parser.add_argument('--custom',
                        metavar='MASK',
                        help='custom mask linear filter, json-style format')

    args = parser.parse_args(None, OrderNamespace())

    ######################################################################
    # File opening
    ######################################################################
    try:
        print('Opening file "{}"...'.format(args.input_image))
        im = Image.open(args.input_image)
    except FileNotFoundError:
        print('File not found.')
        sys.exit(1)
    else:
        print('Image file opened.')

    ordered_args = args.order[9:-1]

    im_f = ImageFilter(im)

    #####################################################################
    # Filter application
    #####################################################################
    for arg in ordered_args:
        if arg == 'average':
            print('Applying average mask with size '
                  '{0}x{0}...'.format(args.average))
            im_f.lin_trans(Masks.avg(args.average))

        elif arg == 'tone':
            print('Applying tone mask with tone {}...'.format(args.tone))
            im_f.lin_trans(Masks.tone(args.tone))

        elif arg == 'sharpen':
            print('Applying sharpen mask type {}...'.format(args.sharpen))
            im_f.lin_trans(Masks.sharpen[args.sharpen - 1])

        elif arg == 'prewitt':
            print('Applying prewitt mask type {}...'.format(args.prewitt))
            im_f.lin_trans(Masks.prewitt[args.prewitt - 1])

        elif arg == 'sobel':
            print('Applying sobel mask type {}...'.format(args.sobel))
            im_f.lin_trans(Masks.sobel[args.sobel - 1])

        elif arg == 'custom':
            print('Applying custom mask {}'.format(args.custom))
            try:
                mask = np.array(json.loads(args.custom))
            except ValueError:
                print('Error loading custom mask, skipped step.')
            else:
                im_f.lin_trans(mask)

        elif arg == 'median':
            print('Applying median filter with size '
                  '{0}x{0}...'.format(args.median))
            im_f.median_trans(args.median)

    #######################################################################
    # File saving
    #######################################################################
    try:
        print('Filtering completed.\nSaving file to "%s"...' % args.output)
        im_f.image.save(args.output)
    except IOError:
        print('Error saving file.')
        sys.exit(1)
    else:
        print('File saved.')
