import functools
import multiprocessing
import numpy as np
from itertools import starmap
from PIL import Image


# For some reason this function must be outside the class
# in order to be pickled
def lin_calc_px(x, y, pixels, half_mask_size, mask):
    """
    Calculates the new color of a single pixel,
    given the mask to use, and the pixel position.
    """
    # If we are on the border, return 0
    if (x < half_mask_size or x >= pixels.shape[0] - half_mask_size or
            y < half_mask_size or y >= pixels.shape[1] - half_mask_size):
        return 0, 0, 0

    # Extract submatrix of the same size of the mask
    subm = pixels[x - half_mask_size: x + half_mask_size + 1,
                  y - half_mask_size:  y + half_mask_size + 1]

    # Compute R,G,B values flattening matrices
    # to use dot product in order to improve speed
    red = int(np.dot(subm[:, :, 0].ravel(), mask.ravel()))
    green = int(np.dot(subm[:, :, 1].ravel(), mask.ravel()))
    blue = int(np.dot(subm[:, :, 2].ravel(), mask.ravel()))

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

    def __init__(self, image, parallel=True):
        self.image = image
        self.parallel = parallel

    def lin_trans(self, mask):
        """
        Applies a linear filter to the current image object,
        given the mask to apply
        """
        # Mask can be just an integer, handle it
        mask_width, mask_height = mask.shape

        half_mask_size = mask_width // 2
        image_width, image_height = self.image.size

        # Extract image into array
        pixels = np.array(self.image)

        # Partialize constant arguments of new pixel function
        partialized_new_px = functools.partial(lin_calc_px,
                                               pixels=pixels,
                                               half_mask_size=half_mask_size,
                                               mask=mask)

        # Create iterator to use in parallel map
        coords = ((x, y)
                  for x in range(image_height)
                  for y in range(image_width))

        if self.parallel:
            # Create process pool
            pool = multiprocessing.Pool(4)

            # Run parallel map unpacking coord tuple
            map_result = pool.starmap(partialized_new_px, coords)
        else:
            # Run map unpacking coord tuple
            map_result = starmap(partialized_new_px, coords)

        # Transform map result to array, reshaping it
        # to the same size of the original pixels array
        new_pixels = np.array(list(map_result),
                              dtype='uint8').reshape(pixels.shape)

        # Crop the image
        self.image = Image.fromarray(new_pixels[
            half_mask_size: image_height - half_mask_size,
            half_mask_size: image_width - half_mask_size])
