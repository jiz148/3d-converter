"""
This script is for reading the dicom files
"""
from matplotlib import pyplot
import numpy
import pydicom


class DicomReader:

    def __init__(self, file_name):
        self.file_name = file_name
        self.data_set = pydicom.dcmread(file_name)

    def read_to_image_list(self):
        """
        Read DICOM file and select images and output to list
        @return: <list> a list of numpy matrices which represents the images
        """
        pixel_array = self.data_set.pixel_array
        result_list = []
        for pic in pixel_array:
            np_obj = numpy.array(pic)
            # # converting to grayscale
            # for y in range(np_obj.shape[0]):
            #     for x in range(np_obj.shape[1]):
            #         r, g, b = np_obj[y, x, :][0], np_obj[y, x, :][1], np_obj[y, x, :][2]
            #         gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
            #         np_obj[y, x, :][0] = int(gray)
            # np_obj = numpy.delete(np_obj, (1, 2), axis=2)
            result_list.append(np_obj)
        return result_list

    def show_image(self, image_id):
        """
        Show the specific image using pyplot
        @param image_id: id of image
        """
        pyplot.imshow(self.data_set.pixel_array[image_id])
        pyplot.show()
