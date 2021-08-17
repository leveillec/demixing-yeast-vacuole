import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import numpy as np
from itertools import chain, repeat
import os


class VacuoleAssign:

    @staticmethod
    def assign(vac_keep, output_directory, experiment, temperature):
        """This function displays an individually cropped vacuole to the user for annotation.
        The user is unaware of the temperature of the sample being analyzed and the user is presented
        a cropped image so that the temperature can't be deduced by the field of view, limiting bias.
        After annotation key is input by the user, the next image is displayed and the information is saved."""

        # Input category- 1: mixed, 2: demixed domains, 3: demixed hexagonal, 4: unknown, 5: out_of_focus
        annotation = []
        n = len(vac_keep)
        for i in range(n):
            plt.ion()
            plt.imshow(vac_keep[i], cmap='gray')
            plt.pause(0.00000001)
            prompt_msg = "Enter category: "
            bad_input_msg = "Sorry, not a valid input."
            prompts = chain([prompt_msg], repeat('\n'.join([bad_input_msg, prompt_msg])))
            replies = map(input, prompts)
            valid_category = next(filter(str.isdigit, replies))
            annotation.append(int(valid_category[:1]))
            plt.cla()

        index = []
        image_path = []
        flat_images = []
        im_shape = []
        os.makedirs(output_directory + '/cropped_images/' + str(experiment) + '_' + str(temperature))
        for i in range(n):
            path = output_directory + '/cropped_images/' + str(experiment) + '_' + str(temperature) + '/'
            filename = str(experiment) + '_' + str(temperature) + '_image_' + str(i) + '.png'
            image_path.append(filename)
            Image.fromarray(vac_keep[i]).save(path + filename)
            size = vac_keep[i].shape
            im_shape.append(size)
            flat_image = np.ndarray.flatten(vac_keep[i])
            flat_images.append(flat_image)
            index.append(i)

        # Input category label
        # Designation label
        # 1: not_ps:0, 2: ps:1, 3: ps:1, 4: discard:2, 5: discard:2
        category = []
        designation = []
        designation_num = []
        for i in range(n):
            if annotation[i] == 1:
                category.append('mixed')
                designation.append('not_ps')
                designation_num.append(0)
            if annotation[i] == 2:
                category.append('demixed_domains')
                designation.append('ps')
                designation_num.append(1)
            if annotation[i] == 3:
                category.append('demixed_hexagonal')
                designation.append('ps')
                designation_num.append(1)
            if annotation[i] == 4:
                category.append('unknown')
                designation.append('discard')
                designation_num.append(2)
            if annotation[i] == 5:
                category.append('out_of_focus')
                designation.append('discard')
                designation_num.append(2)

        dictionary = {'index': index, 'annotation': annotation, 'morphology': category,
                      'designation': designation, 'designation_key': designation_num,
                      'im_path': image_path, 'im_shape': im_shape, 'image': flat_images}
        df = pd.DataFrame(dictionary)
        file_name = \
            output_directory + '/annotated_data/' + 'annotated_data_' + str(experiment) + '_' + str(temperature) \
            + '.csv'
        df.to_csv(file_name)

        return annotation, designation_num
