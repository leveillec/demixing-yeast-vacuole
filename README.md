# demixing-yeast-vacuole

## Goal

1. The primary goal of this program is to efficiently count the number of vacuoles with and without domains in a given image.
2. The secondary goal for the user to be blind to the sample conditions of the image to minimize bias in the analysis. 

## Context

In order to get good statistics on a popluation of cells with phase separated vacuoles, thousands of vacuolues were analyzed. It was important to have an efficient and accurate way to analyze this data. Key features of this program include: 
- Automatic sifting through files to extract file information and open the images.
- Vacuoles are automatically identified in an image and individually presented to the user. This prevents double counting.
- Manual keybaord input and automatic advancement to the next image for quick tabulation.
- Information is automatically saved for future plotting.

To minimize bias, the user is blind to the sample temperature, growth temperature and field of view. 
- If the user knew the images was taken at a lower temperature they could guess that there should be more vacuoles with domains, and at high temperature that there should be less. In addition, depending on the growth temperature the user might guess that the transition temperature be lower or higher. This bias was avoided by automatically extracting the sample and growth temperatures from the file name and path. In addition, the program pulls images from a file in a random order. 
- Lastly, viewing an image with a large field of view may allow the user to deduce if the sample is at higher or lower temperature based on the relative presence of vacuoles with domains. This bias was avoided by individually cropping vacuoles out of the field of view and presenting them to the user one at a time. 

## Contents

Python scripts are located in the source folder under analysis. 

Main Program
- vacuole_analysis.py

Scripts containing functions that the main program uses:
- vacuole_identifier.py
- vacuole_discard.py
- vacuole_assign.py

## What you need
- Image stack containing bright vacuoles on a dark background. 
- Images work best when vacuoles are evenly spaced in the plane of view (i.e. not on top of eachother or moving).
- File path contains the date of experiment and file name of the image contains the temperature of the sample. 
- image directory
- output directory

## How it works

![](src/images/workflow.png)

Running the main program vacuole_analysis.py will:
1. Extract the file information
2. The get_vacuoles function from the vacuole_identifier script\
        **(A)** Prepares the images for vacuole identification through contrast enhancement and de-noising each image.\
        **(B)** Using blob detection (difference of gaussians method), the coordinates and radius of each vacuole is determined.\
        **(C)** A mask is created to mark vacuoles of interest. Vacuoles that are too small or along the edges are discarded.\
        **(D)** Vacuoles are then individually labelled.\
        **(E)** An array containing the cropped images is returned.
3. The discard function from the discard_vacuoles script\
        - Filters out images of vacuoles that were out of focus or have pore contrast with the background.
4. The assign function from the vacuole_assign script\
        - Will present the user one image at a time for annotation (as shown in E).\
        - Keyboard inputs are saved\
                1: mixed (**E** top) 2: demixed domains (**E** bottom) 4: unknown (hard to tell or out of focus)\
        - Images autmoatically advance to the next one. If a non-digit is entered, the user is presented with a message to try again.
5. The main script will then\
        - Total the number of vacuoles counted as mixed and demixed\
        - Calculate the percent phase separated at that given temperature\
        - Return a .csv file containing the temperature and percent phase separated.
