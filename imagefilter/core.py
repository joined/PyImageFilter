import functools
import multiprocessing
import numpy as np
import itertools as itt
from PIL import Image


# For some reason these 2 functions must be outside the class
# in order to be pickled (multiprocessing)
def lin_calc_px(x, y, pixels, half_mask_size, mask):
    """
    Calculates the new color of a single pixel,
    given the mask to use, and the pixel position.
    """
    # If we are on the border, return (0,0,0) = black pixel
    if (x < half_mask_size or x >= pixels.shape[0] - half_mask_size or
            y < half_mask_size or y >= pixels.shape[1] - half_mask_size):
        return 0, 0, 0

    # Extract submatrix of the same size of the mask
    subm = pixels[x - half_mask_size:  x + half_mask_size + 1,
                  y - half_mask_size:  y + half_mask_size + 1]

    # Compute R,G,B values flattening arrays
    # to use dot product in order to improve speed
    red = int(np.dot(subm[...,   0].ravel(),  mask.ravel()))
    green = int(np.dot(subm[..., 1].ravel(),  mask.ravel()))
    blue = int(np.dot(subm[...,  2].ravel(),  mask.ravel()))

    # Normalize out-of-scale values
    if red > 255:
        red = 255
    elif red < 0:
        red = 0

    if green > 255:
        green = 255
    elif green < 0:
        green = 0

    if blue > 255:
        blue = 255
    elif blue < 0:
        blue = 0

    return red, green, blue


def volterra_new_px(x, y, pixels, N, A, B):
    """
    Calculates the new color of a single pixel
    using quadratic Volterra filter, given the pixel
    position and the A, B coefficient arrays
    """
    half_N = N // 2

    # If we are on the border, return (0,0,0) = black pixel
    if (x < half_N or x >= pixels.shape[0] - half_N or
            y < half_N or y >= pixels.shape[1] - half_N):
        return 0, 0, 0

    # Extract submatrix on which we'll work on
    subm = pixels[x - half_N:  x + half_N + 1,
                  y - half_N:  y + half_N + 1]

    # Compute R,G,B values of the first part of the formula
    # (the one relative to the A array) in the same way of
    # the linear filtering
    A_red = int(np.dot(subm[...,   0].ravel(), A.ravel()))
    A_green = int(np.dot(subm[..., 1].ravel(), A.ravel()))
    A_blue = int(np.dot(subm[...,  2].ravel(), A.ravel()))

    # Compute R,G,B values of the second part of the formula
    # (the one relative to the B array)
    B_red, B_green, B_blue = 0, 0, 0
    # This is equal to 4 nested for loops with range 0 -> N-1
    for i, j, k, l in itt.product(range(N), repeat=4):
        B_red += B[i, j, k, l] * subm[..., 0][i, j] \
                               * subm[..., 0][k, l]
        B_green += B[i, j, k, l] * subm[..., 1][i, j] \
                                 * subm[..., 1][k, l]
        B_blue += B[i, j, k, l] * subm[..., 2][i, j] \
                                * subm[..., 2][k, l]

    red = int(A_red + B_red)
    green = int(A_green + B_green)
    blue = int(A_blue + B_blue)

    # Normalize out-of-scale values
    if red > 255:
        red = 255
    elif red < 0:
        red = 0

    if green > 255:
        green = 255
    elif green < 0:
        green = 0

    if blue > 255:
        blue = 255
    elif blue < 0:
        blue = 0

    return red, green, blue


class ImageFilter:

    def __init__(self, image, parallel):
        self.image = image
        self.parallel = parallel

    def volterra_trans(self, A, B):
        """
        Applies the Volterra quadratic filter to the current image object,
        given the coefficients arrays
        """
        # Arrays' dimension
        N = A.shape[0]

        half_N = N // 2

        # Unpack image dimensions
        image_width, image_height = self.image.size

        # Extract image into array
        pixels = np.array(self.image)

        # Partialize shared arguments of new pixel function
        partialized_new_px = functools.partial(volterra_new_px,
                                               pixels=pixels,
                                               N=N, A=A, B=B)

        # Create iterator to use in parallel map
        coords = itt.product(range(image_height), range(image_width))

        if self.parallel:
            # Create process pool, number of processes defaults to
            # the number of CPU's cores
            pool = multiprocessing.Pool()

            # Run parallel map unpacking coord tuple
            map_result = pool.starmap(partialized_new_px, coords)
        else:
            # Run map unpacking coord tuple
            map_result = itt.starmap(partialized_new_px, coords)

        # Transform map result to array, reshaping it
        # to the same size of the original pixels array
        new_pixels = np.array(list(map_result),
                              dtype='uint8').reshape(pixels.shape)

        # Crop the image to leave out black borders
        self.image = Image.fromarray(new_pixels[
            half_N: image_height - half_N,
            half_N: image_width - half_N])

    def lin_trans(self, mask):
        """
        Applies a linear filter to the current image object,
        given the mask to apply
        """
        # Unpack image dimensions
        mask_width, mask_height = mask.shape

        half_mask_size = mask_width // 2
        image_width, image_height = self.image.size

        # Extract image into array
        pixels = np.array(self.image)

        # Partialize shared arguments of new pixel function
        partialized_new_px = functools.partial(lin_calc_px,
                                               pixels=pixels,
                                               half_mask_size=half_mask_size,
                                               mask=mask)

        # Create iterator to use in parallel map
        coords = itt.product(range(image_height), range(image_width))

        if self.parallel:
            # Create process pool, number of processes defaults to
            # the number of CPU's cores
            pool = multiprocessing.Pool()

            # Run parallel map unpacking coord tuple
            map_result = pool.starmap(partialized_new_px, coords)
        else:
            # Run map unpacking coord tuple
            map_result = itt.starmap(partialized_new_px, coords)

        # Transform map result to array, reshaping it
        # to the same size of the original pixels array
        new_pixels = np.array(list(map_result),
                              dtype='uint8').reshape(pixels.shape)

        # Crop the image to leave out black borders
        self.image = Image.fromarray(new_pixels[
            half_mask_size: image_height - half_mask_size,
            half_mask_size: image_width - half_mask_size])
