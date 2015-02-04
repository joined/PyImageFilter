import numpy as np
import math


class Masks:

    @staticmethod
    def gauss(stdev, rank):
        def gaussian_f(r):
            num = math.e ** (- (r ** 2) / (2 * (stdev ** 2)))
            den = stdev * math.sqrt(2 * math.pi)

            return num / den

        mask = np.fromfunction(
            lambda x, y: gaussian_f(abs(x - rank // 2) + abs(y - rank // 2)),
            (rank, rank),
            dtype=float)

        # Normalize mask to have unitary sum of elements
        return mask / np.sum(mask)

    @staticmethod
    def avg(rank):
        return np.ones((rank, rank)) / (rank ** 2)

    @staticmethod
    def tone(tone):
        return np.array([[tone]])

    sharpen = [
        np.array([[0,  -1,  0],
                  [-1,  5, -1],
                  [0,  -1,  0]]),

        np.array([[-1, -1, -1],
                  [-1,  9, -1],
                  [-1, -1, -1]]),

        np.array([[1, -2,  1],
                  [-2, 5, -2],
                  [1, -2,  1]])
    ]

    prewitt = [
        np.array([[-1, -1, -1],
                  [0,   0,  0],
                  [1,   1,  1]]),

        np.array([[-1, 0, 1],
                  [-1, 0, 1],
                  [-1, 0, 1]])
    ]

    sobel = [
        np.array([[-1, -2, -1],
                  [0,   0,  0],
                  [1,   2,  1]]),

        np.array([[-1, 0, 1],
                  [-2, 0, 2],
                  [-1, 0, 1]])
    ]
