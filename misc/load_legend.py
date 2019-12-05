"""
Load space
"""
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
from mayavi import mlab
import numpy
from matplotlib import pyplot

TEST_RESULT_PATH = '/home/bioprober/gh/3d-converter/tests/data/example_3d_output_5.dat'
TEST_RESULT_IMAGE_PATH = '/home/bioprober/gh/3d-converter/tests/data/example_result_6.png'


def run():
    space = numpy.load(TEST_RESULT_PATH, allow_pickle=True)
    # print(space, '\n')
    # print(space.shape)
    # print(space[:, :, 2].shape)
    # print(type(space[:, :, 2]))

    # plot the space

    z, x, y, c = space.nonzero()
    # print(x.shape)
    # print(y.shape)
    # print(z.shape)
    # print('z: ', z)
    # print(c)
    # print(type(c))
    colors = []
    for Z, X, Y in zip(z, x, y):
        colors.append(space[Z, X, Y, 0])

    # print(len(c))
    # print(colors[7777:8888])
    print('started saving picture...\n')
    # fig = pyplot.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(x, y, -z, zdir='z', c=c)
    # pyplot.savefig(TEST_RESULT_IMAGE_PATH)
    fig = pyplot.figure()
    ax = fig.gca(projection='3d')
    ax.scatter(x, y, -z, c=numpy.array(colors))
    pyplot.savefig(TEST_RESULT_IMAGE_PATH)
    print('done\n')


if __name__ == "__main__":
    run()
