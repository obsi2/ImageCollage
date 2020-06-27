#     collection of classes to generate image collages with square images
#     Copyright (C) 2020  Peter C. Seitz
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os
import cv2
import numpy as np
from ruamel.yaml import YAML


class CollageLayout:
    def __init__(self):
        self.layout = {0: [0, 0, 0]}
        self.description = ''
        self.shape = (0, 0)
        self.baselength = 100
        self.border = 1
        self.outer_border = 0

    def set_layout(self, index):
        ''' Return layout and layout_meta
        '''
        # layout of images in target image in units of baselength
        # layout_meta: Name, size x, size y
        # layout: index : size, position x, position y
        yaml = YAML()
        if index == 0:
            filename = r'collage/2x2_square.yaml'
        if index == 1:
            filename = r'collage/3x3_square.yaml'
        if index == 2:
            filename = r'collage/27x27_nowhere_neat_square.yaml'

        with open(filename) as file:
            code = yaml.load(file)

        self.description = code['description']
        self.shape = code['shape']
        self.layout = code['layout']

        return self.description, self.shape, self.layout


class ImageList:
    ''' Class representing a list of images loaded from file or from memory
    '''

    def __init__(self, path, filenames):
        self.path = path
        self.filenames = filenames

    def get_Image(self, index):
        #if index < len(self.filenames):
        image = cv2.imread(os.path.join(self.path, self.filenames[index]))
        return image

    def len(self):
        return len(self.filenames)


class Array_ImageList:
    ''' Class representing a list of images loaded from file
    '''

    def get_Image(self, index):
        print()

class Collage:
    ''' Class representing an image collage
    '''

    def __init__(self, layout:CollageLayout, background_color= (255, 255, 255)):
        """

        :type baselength: int
        """
        self.layout = layout
        self.background_color = background_color
        self.shape = self.get_target_image_shape_from_layout()
        self.collage = self.init_target_image()
        self.image_mapping = None
        self.filenames = None

    def init_target_image(self):
        target_image = np.full(self.shape, self.background_color, np.uint8)
        return target_image

    def get_target_image_shape_from_layout(self):
        # Calculate target image shape
        shape = (self.layout.shape[1] * self.layout.baselength + 2 * self.layout.outer_border,
                      self.layout.shape[0] * self.layout.baselength + 2 * self.layout.outer_border,
                      3)
        return shape


    def initialize_target_image_mapping(self, image_list:ImageList):
        self.image_list = image_list
        #self.filenames = filenames
        #self.path = path
        #min_length = np.min([len(self.layout.layout), len(filenames)])
        min_length = np.min([len(self.layout.layout), self.image_list.len()])
        self.image_mapping = {}
        for i in range(len(self.layout.layout)):
            self.image_mapping[i] = i % min_length

        return self.image_mapping

    def render_image(self):
        self.collage = self.init_target_image()
        for i, source in enumerate(self.image_mapping):
            #print('processing', os.path.join(self.path, self.filenames[self.image_mapping[source]]))
            #image = cv2.imread(os.path.join(self.path, self.filenames[self.image_mapping[source]]))
            image = self.image_list.get_Image(self.image_mapping[source])
            # resize input image to target size
            image_resized = cv2.resize(image, ((self.layout.layout[i][0] * self.layout.baselength) - 2 * self.layout.border,
                                               (self.layout.layout[i][0] * self.layout.baselength) - 2 * self.layout.border))
            # place in target image
            startx = (self.layout.layout[i][2] * self.layout.baselength) + self.layout.border + self.layout.outer_border
            starty = (self.layout.layout[i][1] * self.layout.baselength) + self.layout.border + self.layout.outer_border
            endx = startx + image_resized.shape[0]
            endy = starty + image_resized.shape[1]
            # print(startx, endx, starty, endy)
            self.collage[startx:endx, starty:endy, :] = image_resized
        return self.collage


    def render_image_layout(self):
        return target_image
