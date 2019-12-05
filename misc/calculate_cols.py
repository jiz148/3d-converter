"""
Calculate the columns for ts file
"""
import math
import numpy


def run():
    range_list = list(range(0, 75, 5))
    radian_list = []
    for item in range_list:
        radian_list.append(math.radians(item))
    numpy_radians = numpy.array(radian_list)
    sin = numpy.sin(numpy_radians)
    neg_sin = numpy.sin(numpy_radians) * -1
    cos = numpy.cos([numpy_radians])
    print('sin is\n')
    print(sin, '\n')
    print('-sin is\n')
    print(neg_sin, '\n')
    print('cos is\n')
    print(cos, '\n')


if __name__ == "__main__":
    run()
