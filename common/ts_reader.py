"""
This script includes reader class for .ts files
"""
import numpy


class TsReader:

    def __init__(self, file_name):
        self.text = self._get_text(file_name)
        self.item_list = self._parse_text(self.text)
        pass

    def get_trans_matrix_list(self):
        """
        For position information .ts files
        Gets a list the transformation matrix from self.item_list
        """
        if not self.item_list or not isinstance(self.item_list, list):
            print('Need to have correct item list from file first!')
            return
        result_list = []
        for item in self.item_list:
            pos = item[1:17]
            pos = [float(string) for string in pos]  # convert all items to floats
            np_obj = numpy.array(pos)
            result_list.append(np_obj.reshape((4, 4)))  # reshape to the form of transformation matrix
        return result_list

    @staticmethod
    def _get_text(file_name: str):
        """
        Reads the file adn return the its text
        @param file_name: <str> file path
        @return: <str> text
        """
        with open(file_name, 'r') as file:
            text = file.read()
        return text

    @staticmethod
    def _parse_text(text: str):
        """
        Parses the text to a list of item list
        @param text: <str> text to be parsed
        @return: <list> 2d list array
        """
        result_list = []
        list_of_rows = text.strip().split('\n')
        for row in list_of_rows:
            result_list.append(row.strip().split())
        return result_list
