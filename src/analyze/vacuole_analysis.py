import os
import re
import pandas as pd
import ntpath

from src.analyze.vacuole_identifier import VacuoleIdentifier
from src.analyze.vacuole_discard import VacuoleDiscard
from src.analyze.vacuole_assign import VacuoleAssign


class VacuoleAnalysis:

    def __init__(self, image_directory, output_directory):
        self.image_directory = image_directory
        self.output_directory = output_directory

        self.identifier = VacuoleIdentifier()
        self.vacuole_discard = VacuoleDiscard()
        self.vacuole_assign = VacuoleAssign()

    def analyze(self):
        for name in self.get_image_files(self):
            # Get file info
            temperature, experiment = self.extract_file_info(name, image_directory)
            # Load images and get vacuoles
            cropped_list = self.identifier.get_vacuoles(name)
            # Keep arrays with imaged vacuoles
            vac_discard, vac_keep = self.vacuole_discard.discard(cropped_list)
            # Annotate images and save data
            annotation, designation_num = \
                self.vacuole_assign.assign(vac_keep, output_directory, experiment, temperature)
            # Count the number of PS vacuoles
            not_ps = designation_num.count(0)
            ps = designation_num.count(1)
            discard_pile = designation_num.count(4)
            morph_domains = annotation.count(2)
            morph_hex = annotation.count(3)
            unknown = annotation.count(4)
            # Output percent PS
            total = not_ps + ps
            discard = len(vac_discard) + discard_pile
            percent_ps = (ps / total) * 100
            dictionary_1 = {'Temperatures': [temperature], 'PercentPS': [percent_ps]}
            dictionary_2 = {'Temperatures': [temperature], 'Total_Counted': [total], 'Mixed': [not_ps],
                            'Morph_domains': [morph_domains], 'Morph_hex': [morph_hex], 'Unknown': [unknown],
                            'Total_Discard': [discard]}
            df1 = pd.DataFrame(dictionary_1)
            df2 = pd.DataFrame(dictionary_2)
            file_name1 = \
                output_directory + '/' + str(experiment) + '/' + str(temperature) + '_' + str(experiment) + '.csv'
            file_name2 = \
                output_directory + '/' + str(experiment) + '/info_' + str(temperature) + '_' + str(experiment) + '.csv'
            df1.to_csv(file_name1)
            df2.to_csv(file_name2)

    @staticmethod
    def get_image_files(self):
        """This function returns the file path of all the tiff files within root directory."""

        fnames = []
        for root, dirs, files in os.walk(self.image_directory):

            # Loop through the files
            # Check for .tif extension
            # save if it has one

            for file in files:
                if file.endswith(".tif"):
                    fnames.append(os.path.join(root, file))

            return fnames

    @staticmethod
    def extract_file_info(name, image_directory):
        """This function will extract the temperature the image was taken from the file name.
        Such that the user does not have to do it manually and the user is blind to the temperature
        of the sample in the analysis to prevent bias."""

        file = ntpath.basename(name)
        temp = re.search(r'\d+', file).group(0)
        temperature = int(temp)

        head, tail = os.path.split(image_directory)
        experiment = tail

        return temperature, experiment


if __name__ == "__main__":
    image_directory = "/Users/chantelleleveille/Desktop/Images_counting/08_06_21_Exp3"
    output_directory = "/Users/chantelleleveille/Desktop/Workspaces/Vacuole_image_classification/output"

    vacuole_analysis = VacuoleAnalysis(image_directory, output_directory)
    vacuole_analysis.analyze()
