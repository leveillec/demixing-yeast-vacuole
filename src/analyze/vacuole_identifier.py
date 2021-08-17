import numpy as np
from skimage import io, exposure, filters, draw
from skimage.feature import blob_dog
from skimage.util import invert
from skimage.morphology import remove_small_objects
from skimage.segmentation import clear_border
from scipy.ndimage import label
from skimage.measure import regionprops


class VacuoleIdentifier:

    def get_vacuoles(self, name):
        """This function opens up tif files. It prepares the images for vacuole identification
        through contrast enhancement and de-noising each image. Using blob detection, the
        coordinates and approximate radius of each vacuole determined. A mask is created to
        mark vacuoles of interest. Vacuoles are then cropped into individual images."""

        # Create array to store individually cropped vacuole images
        cropped_list = []

        # Open up the tiff stack and save as an array
        # The array has dimensions (z, y, x)
        # z represents the number of slices in the stack
        # x and y are the width and height
        image_stack = io.imread(name)

        # Sometimes the dimension order gets reversed. If encountering this problem,
        im_shape = image_stack.shape

        if im_shape[2] < 10:
            position1 = -1  # Transpose the stack so that z is first
        else:
            position1 = 0

        image_stack = np.moveaxis(image_stack, position1, 0)

        # Loop through the images in the image stack:
        for im in image_stack:

            # Prepare image for vacuole detection
            # Enhance contrast
            p_low, p_high = np.percentile(im, (30, 99.999))
            im_rescale = exposure.rescale_intensity(im, in_range=(p_low, p_high))
            # De-noise image
            im_gaussian_filter = filters.gaussian(im_rescale, sigma=2)

            # Detect Vacuoles
            # Blob detection - difference of gaussian method
            # Detects bright spots in image. Finds their center coordinates and radii.
            blobs_dog = blob_dog(im_gaussian_filter, min_sigma=.9, max_sigma=30, threshold=.2)

            # Identify each vacuole and create the mask image
            # Use the dimensions from the original image, so the size matches
            mask = np.ones(shape=im.shape[0:2], dtype="bool")
            for blob in blobs_dog:
                y, x, r = blob
                # Take the coordinates from the blob detection, draw circles on mask
                rr, cc = draw.disk((y, x), r, shape=im.shape[0:2])
                mask[rr, cc] = False

            mask1 = invert(mask)  # Invert to make white on black circles so that remove small objects works
            # Set the lower size limit to remove bright spots and too small vacuoles
            mask2 = remove_small_objects(mask1, min_size=500)
            # Remove vacuoles touching the edge of the frame
            mask3 = clear_border(mask2)

            # Mark vacuoles of interest as the white areas of the mask
            # Label each vacuole its own area
            labeled_vacuoles, _ = label(mask3)

            # Crop each labelled vacuole into its own image
            # Define amount of padding to add to the perimeter of the vacuole radius for the cropped image
            pad = 18

            for region_index, region in enumerate(regionprops(labeled_vacuoles, intensity_image=im_gaussian_filter)):
                # Draw a rectangle around the segmented vacuoles, bbox describes: min_row, min_col, max_row, max_col
                minr, minc, maxr, maxc = region.bbox
                # Use those bounding box coordinates to crop the image
                cropped_list.append(im[minr - pad:maxr + pad, minc - pad:maxc + pad])

        # Display how many vacuole images we have
        print("number of cropped vacuoles is", len(cropped_list))

        return cropped_list
