import numpy as np

from src.test.test_binary import TestBinarizer


class VacuoleDiscard:

    def __init__(self):
        self.test_binary = TestBinarizer()

    def discard(self, cropped_list):
        """This function determines the quality of cropped images and only keeps vacuoles
        with high contrast and well defined edges."""
        vac_discard = []
        vac_keep = []

        im_original_keep = []  # Keep a copy of the original image
        var_list = []
        n = len(cropped_list)  # Calculate length of new array
        for i in range(n):
            value = np.var(cropped_list[i], dtype=int)
            var_list.append(value)
        # Apply threshold for variance
        # Keep images with high values
        for i in range(n):
            if var_list[i] >= 0.0:
                im_original_keep.append(cropped_list[i])
            else:
                vac_discard.append(cropped_list[i])

        # Display how many vacuole images we have
        print("number of images after filters is", len(im_original_keep))

        n = len(im_original_keep)
        for i in range(n):
            image = im_original_keep[i]
            mask_im = self.test_binary.binary_mask(image)
            binary_im = self.test_binary.binary_image(image)
            # Remove out of focus vacuoles
            af1 = ((np.count_nonzero(binary_im)) / 2500)
            x, y = mask_im.shape
            af2 = ((np.count_nonzero(mask_im)) / x * y)
            if af1 < 0.055 or af2 < 0.055:
                vac_discard.append(im_original_keep[i])
            else:
                vac_keep.append(im_original_keep[i])

        # Display how many vacuole images we have
        print("number of images after filters is", len(vac_keep))

        return vac_discard, vac_keep
