import functools
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from PIL import Image


class ImageFilter:

    def __init__(self, image):
        self.image = image

    @staticmethod
    def lin_calc_px(xy, pixels, half_mask_size, mask):
        """
        Calculates the new color of a single pixel,
        given the mask to use, and the pixel position.
        """
        # Unpack x, y from tuple xy
        x, y = xy

        # If we are on the border, return 0
        if (x < half_mask_size or x >= pixels.shape[0] - half_mask_size or
                y < half_mask_size or y >= pixels.shape[1] - half_mask_size):
            return 0, 0, 0

        # Extract submatrix of the same size of the mask
        subm = pixels[x - half_mask_size: x + half_mask_size + 1,
                      y - half_mask_size:  y + half_mask_size + 1]

        # Compute R,G,B values flattening matrices
        # to use dot product in order to improve speed
        red = int(np.dot(subm[:, :, 0].flatten(), mask.flatten()))
        green = int(np.dot(subm[:, :, 1].flatten(), mask.flatten()))
        blue = int(np.dot(subm[:, :, 2].flatten(), mask.flatten()))

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
        partialized_new_px = functools.partial(self.lin_calc_px,
                                               pixels=pixels,
                                               half_mask_size=half_mask_size,
                                               mask=mask)

        # Create array on which we will iterate
        coords = np.empty((image_height, image_width, 2), dtype=np.intp)
        coords[..., 0] = np.arange(image_height)[:, None]
        coords[..., 1] = np.arange(image_width)
        flattened_coords = coords.reshape(image_width * image_height, 2)

        pool = ThreadPoolExecutor(image_width)

        map_result = pool.map(partialized_new_px, flattened_coords)

        new_pixels = np.array(list(map_result),
                              dtype='uint8').reshape(pixels.shape)

        # Crop the image
        self.image = Image.fromarray(new_pixels[
            half_mask_size: image_height - half_mask_size,
            half_mask_size: image_width - half_mask_size])
