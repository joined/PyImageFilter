import numpy as np
from PIL import Image


class ImageFilter:

    def __init__(self, image):
        self.image = image

    def lin_trans(self, mask):
        # Mask can be just an integer, handle it
        if 'numpy' in str(type(mask)):
            mask_width, mask_height = mask.shape
        else:
            mask_width, mask_height = 1, 1

        # The mask size must be uneven
        if (mask_width % 2 == 0):
            raise ValueError("Le dimensioni della maschera devono "
                             "essere dispari.")

        pixels = np.array(self.image)
        # Copy original pixel array into a new one
        # to not modify the original
        new_pixels = np.copy(pixels)
        half_mask_width, half_mask_height = mask_width // 2, mask_height // 2
        image_width, image_height = self.image.size

        for x in range(half_mask_width, image_width - half_mask_width):
            for y in range(half_mask_height, image_height - half_mask_height):
                # Extract submatrix of the same size of the mask
                subm = pixels[y - half_mask_height: y + half_mask_height + 1,
                              x - half_mask_width:  x + half_mask_width + 1]

                # Compute sum of R,G,B values
                if mask_width > 1:
                    red = np.sum(subm[:, :, 0] * mask)
                    green = np.sum(subm[:, :, 1] * mask)
                    blue = np.sum(subm[:, :, 2] * mask)
                else:
                    red = int(subm[:, :, 0] * mask)
                    green = int(subm[:, :, 1] * mask)
                    blue = int(subm[:, :, 2] * mask)

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

        return Image.fromarray(new_pixels)

    def median_trans(self, rank):
        # The rank must be uneven
        if (rank % 2 == 0):
            raise ValueError("The rank must be odd.")

        pixels = np.array(self.image)
        half_mask_width, half_mask_height = rank // 2, rank // 2
        image_width, image_height = self.image.size

        for x in range(half_mask_width, image_width - half_mask_width):
            for y in range(half_mask_height, image_height - half_mask_height):
                subm = pixels[y - half_mask_height: y + half_mask_height + 1,
                              x - half_mask_width:  x + half_mask_width + 1]

                # Compute median for each component
                red = np.median(subm[:, :, 0])
                green = np.median(subm[:, :, 1])
                blue = np.median(subm[:, :, 2])

                pixels[y][x] = red, green, blue

        return Image.fromarray(pixels)
