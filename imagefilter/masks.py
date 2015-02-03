import numpy as np
import math


class Masks:

    def avg(rank):
        if (rank % 2 == 0):
            raise ValueError("The rank must be odd.")

        return np.ones((rank, rank)) / (rank ** 2)

    def tone(tone):
        return tone

    sharpen = [
        np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]),
        np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]),
        np.array([[1, -2, 1], [-2, 5, -2], [1, -2, 1]])
    ]

    prewitt = [
        np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]]),
        np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    ]

    sobel = [
        np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]]),
        np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    ]
