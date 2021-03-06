#!.env/bin/python

import argparse
import sys
from PIL import Image
from random import randrange
from pyimagefilter import masks
from pyimagefilter.core import ImageFilter
from pyimagefilter.clitools import OrderNamespace, CustomArgTypes

if __name__ == "__main__":
    #########################################################
    # CLI arguments definition
    #########################################################
    parser = argparse.ArgumentParser(
        description="Toolkit for linear and nonlinear image filtering")

    parser.add_argument('input_image',
                        type=str,
                        help='Input image file name.')

    parser.add_argument('--average',
                        type=CustomArgTypes.rank,
                        metavar='RANK',
                        help='average mask transform. rank must be unven')

    parser.add_argument('--gauss',
                        type=CustomArgTypes.gauss_filter,
                        metavar='STDEV,RANK',
                        help='gauss average transform. rank must be uneven')

    parser.add_argument('--sharpen',
                        type=int,
                        metavar='TYPE',
                        choices=[1, 2, 3],
                        help='sharpen mask transform. available types '
                             '1,2,3')

    parser.add_argument('--prewitt',
                        type=int,
                        metavar='TYPE',
                        choices=[1, 2],
                        help='prewitt mask transform. available types '
                             '1,2')

    parser.add_argument('--sobel',
                        type=int,
                        metavar='TYPE',
                        choices=[1, 2],
                        help='sobel mask transform. available types '
                             '1,2')

    parser.add_argument('--volterra',
                        type=CustomArgTypes.volterra,
                        metavar='COEFFICIENT_FILE',
                        help='quadratic volterra filtering. file must be json')

    parser.add_argument('--custom',
                        type=CustomArgTypes.custom_mask,
                        metavar='MASK',
                        help='custom mask linear filter, json-style format')

    parser.add_argument('--no-parallel',
                        action='store_true',
                        help='disable parallel execution')

    # If no output was specified, generate a pseudo-random filename
    parser.add_argument('--output',
                        metavar='OUTPUT_IMAGE',
                        default='output_%d.jpg' % randrange(100),
                        help='output image filename')

    args = parser.parse_args(None, OrderNamespace())

    ######################################################################
    # File opening
    ######################################################################
    try:
        print('> Opening file "{}"...'.format(args.input_image))
        im = Image.open(args.input_image)
    except FileNotFoundError:
        print('> File not found.')
        sys.exit(1)
    else:
        print('> Image file opened.')

    # Filter out elements which were added in the arguments definition
    ordered_args = args.order[10:]

    im_f = ImageFilter(im, parallel=(not args.no_parallel))

    #####################################################################
    # Filter application
    #####################################################################
    for arg in ordered_args:
        if arg == 'average':
            print('> Applying average mask with size '
                  '{0}x{0}...'.format(args.average))
            im_f.lin_trans(masks.avg(args.average))

        elif arg == 'sharpen':
            print('> Applying sharpen mask type {}...'.format(args.sharpen))
            im_f.lin_trans(masks.sharpen[args.sharpen - 1])

        elif arg == 'prewitt':
            print('> Applying prewitt mask type {}...'.format(args.prewitt))
            im_f.lin_trans(masks.prewitt[args.prewitt - 1])

        elif arg == 'sobel':
            print('> Applying sobel mask type {}...'.format(args.sobel))
            im_f.lin_trans(masks.sobel[args.sobel - 1])

        elif arg == 'gauss':
            print('> Applying Gauss filter with '
                  'stdev {0} and size {1}x{1}...'.format(*args.gauss))
            im_f.lin_trans(masks.gauss(*args.gauss))

        elif arg == 'volterra':
            print('> Applying Volterra filter with coefficients\n'
                  'A:\n{}\nB:\n{}'.format(*args.volterra))
            im_f.volterra_trans(*args.volterra)

        elif arg == 'custom':
            print('> Applying custom mask\n{}'.format(args.custom))
            im_f.lin_trans(args.custom)

    #######################################################################
    # File saving
    #######################################################################
    try:
        print('> Filtering completed.\n> Saving file to "%s"...' % args.output)
        im_f.image.save(args.output)
    except IOError:
        print('> Error saving file.')
        sys.exit(1)
    else:
        print('> File saved.')
