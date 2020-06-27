#     cli example to use collage for creating a collage from a collection of images
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

import glob
import os
import cv2
from prompt_toolkit.validation import Validator
from prompt_toolkit import prompt
import argparse

from collage.collage import ImageList, Collage, CollageLayout

def is_number(text):
    return text.isdigit()

validator = Validator.from_callable(
    is_number,
    error_message='This input contains non-numeric characters',
    move_cursor_to_end=True)


if __name__ == "__main__":
    ''' Example usage of collage
        Given a directory with images of specified filetype
        those are loaded and compiled to a collage with nowhere neat tiling
        this collage is shown in a window until user presses a key and stored to disk as collage.jpg
    '''

    parser = argparse.ArgumentParser(description='Create a collage from some images.')
    parser.add_argument('-p', '--path' )
    parser.add_argument('-t', '--filetype', default='jpg')

    args = parser.parse_args()
    if args.path is None:
        parser.print_usage()
        exit(1)
    path = args.path

    filenames = glob.glob(os.path.join(path, '*.' + args.filetype))
    my_image_list = ImageList(path, filenames)

    my_layout = CollageLayout()
    my_layout.set_layout(2)

    # Create target image
    my_layout.baselength = 30
    my_layout.border = 1
    my_layout.outer_border = 0

    background_color = (255, 255, 255)

    my_collage = Collage(my_layout, background_color)

    # relate input images to index in target image
    my_collage.initialize_target_image_mapping(my_image_list)

    target_image = my_collage.render_image()

    cv2.namedWindow('image')
    cv2.imshow("image", target_image)
    cv2.imwrite("collage.jpg", target_image)
    cv2.waitKey(10)

    exit_program = False
    while not exit_program:
        text = prompt('> ')

        print('You said: %s' % text)
        if text == 'exit':
            exit_program = True
            cv2.destroyAllWindows()

        if text in ['h', 'help']:
            print('available commands:')
            print('exit: exit the program')
            print('h, help: print this help')
            print('i, indices: toggle display of image indices in collage')
            print('save: save the collage as collage.jpg')
            print('s, switch: switch the images at the given indices')

        if text == 'save':
            save_filename = 'collage.jpg'
            cv2.imwrite(save_filename, target_image)
            print(f'Wrote collage to {save_filename}')

        if text in ['s', 'switch']:
            image_1 = int(prompt('First image index: ', validator=validator)) - 1
            image_2 = int(prompt('Second image index: ', validator=validator)) - 1
            print(f'switching images {image_1+1} and {image_2+1}')
            target_image = my_collage.switch(image_1, image_2)
            cv2.imshow("image", target_image)
            cv2.waitKey(10)

        if text in ['i', 'indices']:
            if my_collage.show_indices:
                my_collage.show_indices = False
            else:
                my_collage.show_indices = True
            target_image = my_collage.render_image()
            cv2.imshow("image", target_image)
            cv2.waitKey(10)

