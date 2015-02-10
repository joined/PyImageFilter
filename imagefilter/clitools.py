import argparse
import json
import numpy as np


class OrderNamespace(argparse.Namespace):

    """
    Override default arguments Namespace to keep
    optional arguments order, to be able to apply
    multiple filters in the right order
    """

    def __init__(self, **kwargs):
        self.__dict__['order'] = []
        super(OrderNamespace, self).__init__(**kwargs)

    def __setattr__(self, attr, value):
        self.__dict__['order'].append(attr)
        super(OrderNamespace, self).__setattr__(attr, value)


class CustomArgTypes:

    """
    Define custom argument types
    to check input sanity
    """

    @staticmethod
    def custom_mask(string):
        try:
            mask = np.array(json.loads(string))
            # The mask must have 2 dimensions
            assert len(mask.shape) == 2
            # It must be squared
            assert mask.shape[0] == mask.shape[1]
            # It must be of uneven size
            assert mask.shape[0] % 2 != 0
        except:
            raise argparse.ArgumentTypeError('Invalid custom mask.')
        else:
            return mask

    @staticmethod
    def volterra(string):
        try:
            with open(string) as json_file:
                json_data = json.load(json_file)
            A = np.array(json_data['A'])
            B = np.array(json_data['B'])
            # The A array must have 2 dimensions
            assert len(A.shape) == 2
            # The B array must have 4 dimensions
            assert len(B.shape) == 4
            # The arrays A and B must be "squared", and have the same
            # "dimension size"
            assert A.shape[0] == A.shape[1] == B.shape[0] == B.shape[1] \
                              == B.shape[2] == B.shape[3]
            # The arrays size must be uneven
            assert A.shape[0] % 2 != 0
        except:
            raise argparse.ArgumentTypeError('Invalid coefficients file.')
        else:
            return A, B

    @staticmethod
    def gauss_filter(string):
        try:
            # Extract stdev and rank from arguments
            stdev = float(string.split(',')[0])
            rank = int(string.split(',')[1])
            # Rank must be uneven
            assert rank % 2 != 0
        except:
            raise argparse.ArgumentTypeError('Invalid gauss filter arguments.')
        else:
            return stdev, rank

    @staticmethod
    def rank(string):
        rank = int(string)
        if (rank % 2 == 0):
            raise argparse.ArgumentTypeError('Rank must be uneven.')
        return rank
