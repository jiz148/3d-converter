"""
This script writes continuous transformation information to file
"""
import numpy
import re


SAVE_PATH = '/home/bioprober/gh/3d-converter/tests/data/'


class TransWriter:

    def __init__(self, filename):
        self.filename = filename
        self.info = ''

    def config(self, axis, degree, steps=65, move=(0, 0, 0)):
        """
        Configs self.info string by given parameters
        @param axis: <Tuple> formed by a tuple of two coordinates ((x, y, z), (x, y, z)), axis to be rotate about
        @param degree: <float> final rotation along the axis
        @param steps <int> total steps it takes, same with the number of rows in position file
        @param move: <Tuple> final movement along x, y, z axis, (x, y, z)
        """
        print('Configuring position information...')
        # get id array for first element
        id_arr = numpy.array(list(range(int(steps))))
        move_x_arr = move_y_arr = move_z_arr = radian_arr = numpy.zeros(len(id_arr)).tolist()
        # get move arrays
        if int(move[0]/steps) != 0:
            move_x_arr = list(numpy.arange(0, move[0], move[0]/steps))
        if int(move[1]/steps) != 0:
            move_y_arr = list(numpy.arange(0, move[1], move[1]/steps))
        if int(move[2]/steps) != 0:
            move_z_arr = list(numpy.arange(0, move[2], move[2]/steps))

        # get radian arrays
        if int(degree/steps) != 0:
            degrees = list(numpy.arange(0, degree, degree/steps))
            radian_arr = numpy.radians(degrees)

        # Calculate the rotated arrays and save their strings to self.info
        for i, x, y, z, theta in zip(id_arr, move_x_arr, move_y_arr, move_z_arr, radian_arr):
            move_matrix = self._get_move_matrix(x, y, z)
            x_1, y_1, z_1, x_2, y_2, z_2 = axis[0][0], axis[0][1], axis[0][2], axis[1][0], axis[1][1], axis[1][2]
            t, t_inverse = self._get_t_and_inverse(x_1, y_1, z_1)
            rx, rx_inverse, ry, ry_inverse = self._get_r_x_y_and_inverse(x_1, y_1, z_1, x_2, y_2, z_2)
            rz = self._get_r_z(theta)
            trans = move_matrix.dot(t_inverse).dot(rx_inverse).dot(ry_inverse).dot(rz).dot(ry).dot(rx).dot(t)
            s = ' '.join(str(item) for item in trans)
            s = re.sub(r'[\[\]]', '', s)
            self.info += str(i) + ' ' + s + '\n'
        print('-Done configuring position information')

    def save_to_file(self):
        """
        Save the string in self.info to file
        """
        print('writing to file {}...'.format(self.filename))
        file = open(self.filename, 'w')
        file.write(self.info)
        print('-Done writing to file')

    @staticmethod
    def _calculate_unit_vector_elements(x_1, y_1, z_1, x_2, y_2, z_2):
        """
        Calculates the elements in unit vector
        @return: <Tuple> unit x, y, z
        """
        if (x_2 - x_1) == (y_2 - y_1) == (z_2 - z_1) == 0:
            return 0, 1, 0
        mag = numpy.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2 + (z_2 - z_1) ** 2)
        return (x_2 - x_1) / mag, (y_2 - y_1 ** 2) / mag if (y_2 - y_1 ** 2) / mag != 0 else 1, (z_2 - z_1) / mag

    @staticmethod
    def _get_move_matrix(x, y, z):
        """
        Gets move matrix
        @return: move matrix
        """
        return numpy.array([[1, 0, 0, x],
                            [0, 1, 0, y],
                            [0, 0, 1, z],
                            [0, 0, 0, 1]])

    def _get_r_x_y_and_inverse(self, x_1, y_1, z_1, x_2, y_2, z_2):
        """
        Gets the Rx, Rx inverse, Ry, Ry inverse matrices
        @return: <numpy.array> Rx, Rx inverse, Ry, Ry inverse matrices
        """
        a, b, c = self._calculate_unit_vector_elements(x_1, y_1, z_1, x_2, y_2, z_2)
        d = numpy.sqrt(b**2 + c**2)
        rx = numpy.array([[1, 0, 0, 0],
                          [0, c/d, -b/d, 0],
                          [0, b/d, c/d, 0],
                          [0, 0, 0, 1]])
        rx_inverse = numpy.array([[1, 0, 0, 0],
                                  [0, c/d, b/d, 0],
                                  [0, -b/d, c/d, 0],
                                  [0, 0, 0, 1]])
        ry = numpy.array([[d, 0, -a, 0],
                          [0, 1, 0, 0],
                          [a, 0, d, 0],
                          [0, 0, 0, 1]])
        ry_inverse = numpy.array([[d, 0, a, 0],
                                  [0, 1, 0, 0],
                                  [-a, 0, d, 0],
                                  [0, 0, 0, 1]])
        return rx, rx_inverse, ry, ry_inverse

    @staticmethod
    def _get_r_z(theta):
        """
        Gets Rz matrix
        @param theta: theta radian of rotation
        @return: Rz matrix
        """
        return numpy.array([[numpy.cos(theta), -numpy.sin(theta), 0, 0],
                            [numpy.sin(theta), numpy.cos(theta), 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])

    @staticmethod
    def _get_t_and_inverse(x, y, z):
        """
        Gets T and T inverse matrices
        @param: x
        @param: y
        @param: z
        @return: <Tuple> T and T inverse
        """
        t = numpy.array([[1, 0, 0, -x],
                         [0, 1, 0, -y],
                         [0, 0, 1, -z],
                         [0, 0, 0, 1]])
        t_inverse = numpy.array([[1, 0, 0, x],
                                  [0, 1, 0, y],
                                  [0, 0, 1, z],
                                  [0, 0, 0, 1]])
        return t, t_inverse


def run():
    print('---Transformation Information CLI---\n')
    print('Please enter following information...\n')
    x_1 = float(input('axis parameter x1: '))
    y_1 = float(input('axis parameter y1: '))
    z_1 = float(input('axis parameter z1: '))
    x_2 = float(input('axis parameter x2: '))
    y_2 = float(input('axis parameter y2: '))
    z_2 = float(input('axis parameter z2: '))

    degree = float(input('rotation degree: '))
    steps = int(input('steps: '))
    move_x = int(input('move along x: '))
    move_y = int(input('move along y: '))
    move_z = int(input('move along z: '))

    filename = input('Please enter the file name to save file: ')
    filename = SAVE_PATH + filename

    axis = ((x_1, y_1, z_1), (x_2, y_2, z_2))
    move = (move_x, move_y, move_z)

    writer = TransWriter(filename)
    writer.config(axis, degree, steps, move)
    writer.save_to_file()


if __name__ == '__main__':
    run()
