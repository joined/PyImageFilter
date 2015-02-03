import argparse


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
