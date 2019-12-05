import numpy
from mayavi.mlab import *

TEST_RESULT_PATH = '/home/bioprober/gh/3d-converter/tests/data/example_3d_output_5.dat'


def run():
    space = numpy.load(TEST_RESULT_PATH, allow_pickle=True)
    z, x, y, c = space.nonzero()
    colors = []
    for Z, X, Y in zip(z, x, y):
        colors.append(space[Z, X, Y, 0])
    points3d(x, y, -z)


if __name__ == "__main__":
    run()
