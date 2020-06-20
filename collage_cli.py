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

from collage.collage import *
import glob
import os
import argparse

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

    cv2.imshow("image", target_image)
    cv2.imwrite("collage.jpg", target_image)
    cv2.waitKey(0)

    cv2.destroyAllWindows()

