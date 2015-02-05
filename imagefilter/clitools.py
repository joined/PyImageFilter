import argparse
import json
import numpy as np


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


class CustomArgTypes:
    def custom_mask(string):
        try:
            mask = np.array(json.loads(string))
        except:
            raise argparse.ArgumentTypeError('Invalid custom mask.')
        else:
            if (len(mask.shape) != 2 or
                    mask.shape[0] != mask.shape[1] or
                    mask.shape[0] % 2 == 0):
                raise argparse.ArgumentTypeError(
                    'Custom mask must be squared and of uneven size')
            return mask

    def gauss_filter(string):
        try:
            stdev = float(string.split(',')[0])
            rank = int(string.split(',')[1])
        except:
            raise argparse.ArgumentTypeError('Invalid gauss filter arguments.')
        else:
            if (rank % 2 == 0):
                raise argparse.ArgumentTypeError('Gauss filter rank must'
                                                 'be uneven.')
            return stdev, rank

    def rank(string):
        rank = int(string)
        if (rank % 2 == 0):
            raise argparse.ArgumentTypeError('Rank must be uneven.')
        return rank
