import numpy as np
from PIL import Image


class ImageFilter:

    def __init__(self, image):
        self.image = image

    def lin_trans(self, mask):
        # Mask can be just an integer, handle it
        mask_width, mask_height = mask.shape if mask.shape else (1, 1)

        # Mask dimensions check
        if (mask_width % 2 == 0 or mask_width != mask_height):
            raise ValueError("The mask must be squared and of uneven size.")

        half_mask_size = mask_width // 2
        image_width, image_height = self.image.size

        pixels = np.array(self.image)

        # Copy original pixel array into a new one
        new_pixels = np.copy(pixels)

        for x in range(half_mask_size, image_width - half_mask_size):
            for y in range(half_mask_size, image_height - half_mask_size):
                # Extract submatrix of the same size of the mask
                subm = pixels[y - half_mask_size: y + half_mask_size + 1,
                              x - half_mask_size:  x + half_mask_size + 1]

                # Compute R,G,B values flattening matrices
                # to use dot product in order to improve speed
                red = np.dot(subm[:, :, 0].flatten(), mask.flatten())
                green = np.dot(subm[:, :, 1].flatten(), mask.flatten())
                blue = np.dot(subm[:, :, 2].flatten(), mask.flatten())

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

                new_pixels[y][x] = red, green, blue

        # Crop the image
        self.image = Image.fromarray(new_pixels[
            half_mask_size: image_height - half_mask_size,
            half_mask_size: image_width - half_mask_size])

    def median_trans(self, rank):
        # The rank must be uneven
        if (rank % 2 == 0):
            raise ValueError("The rank must be odd.")

        pixels = np.array(self.image)
        new_pixels = np.copy(pixels)

        half_mask_size, half_mask_size = rank // 2, rank // 2
        image_width, image_height = self.image.size

        for x in range(half_mask_size, image_width - half_mask_size):
            for y in range(half_mask_size, image_height - half_mask_size):
                subm = pixels[y - half_mask_size: y + half_mask_size + 1,
                              x - half_mask_size:  x + half_mask_size + 1]

                # Compute median for each component
                red = np.median(subm[:, :, 0])
                green = np.median(subm[:, :, 1])
                blue = np.median(subm[:, :, 2])

                new_pixels[y][x] = red, green, blue

        # Crop the image
        self.image = Image.fromarray(new_pixels[
            half_mask_size: image_height - half_mask_size,
            half_mask_size: image_width - half_mask_size])
