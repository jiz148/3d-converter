"""
This script includes all the functions to transform picture or 3d matrices
"""
from .vtk_points_loader import VtkPointLoader
import numpy

TOTAL_NUM_OF_PICS = 65
TOTAL_NUM_OF_PIXELS = 31200000


def add_vtk_points_from_plane_list(pic_set: list, trans_set: list, same_shape=True, scale_factor=(1.0, 1.0)):
    """
    Adds atk points from set of planes and its transformation matrix set
    @param pic_set: <list> plane set
    @param trans_set: <list> transformation matrix set
    @param same_shape: <bool> whether pictures are in same shape
    @param scale_factor: <Tuple> scale factor for scaling the matrix
    @return: <VtkPointLoad> Point load, a vtk object
    """
    vtk_point_loader = VtkPointLoader()
    # get first flatten matrix
    flattened_matrix = get_plane_matrix_flatten(pic_set[0])
    # create scaling matrix
    scale_matrix = _create_scale_matrix(scale_factor)
    # put planes into the vtk object
    print('Creating data...')
    loop, volume_list, colors_list = 0, [], []
    for pic, trans in zip(pic_set, trans_set):
        plane_matrix = flattened_matrix if same_shape is True else get_plane_matrix_flatten(pic)
        colors = pic.reshape([int(pic.size/3), 3]).tolist()
        volume = numpy.dot(plane_matrix, trans.transpose()).dot(scale_matrix) * -1
        volume = numpy.delete(volume, 3, 1).tolist()
        volume_list = volume_list + volume
        colors_list = colors_list + colors
        loop += 1
        _print_progress_bar(loop, len(trans_set))

    # set colors to grayscale
    print('-Done Creating data')
    print('changing colors to grayscale...')
    for i in range(len(colors_list)):
        colors_list[i] = 0.2989 * colors_list[i][0] + 0.5870 * colors_list[i][1] + 0.1140 * colors_list[i][2]
    print('-Done changing colors to grayscale')
    vtk_point_loader.add_points_from_list(volume_list, colors_list)

    vtk_point_loader.summarize()

    return vtk_point_loader


def get_plane_matrix_flatten(plane):
    """
    Gets a matrix in the form of
    | X0 Y0 0 1 X0 Y1 0 1 ... ... ... ... Xi Yi 0 1 |
    @param plane: plane
    @return: <numpy.array> Matrix
    """
    trans_list = []
    for y in range(plane.shape[0]):
        for x in range(plane.shape[1]):
            trans_list.append(numpy.array([x, y, 0, 1]))
    return numpy.array(trans_list)


def plane_pt_to_3d_point(pos, trans_matrix):
    """
    Transform plane point position eg. P(x, y, 0, 1) to 3d point eg. P'(X, Y, Z, 1)
    @param pos: <array_like> position
    @param trans_matrix: <numpy.array> transformation matrix
    @return: <Tuple> 3d position
    """
    orig_matrix = numpy.array(pos, ndmin=2)
    return numpy.dot(orig_matrix, trans_matrix.transpose())


def plane_set_to_3d(pic_set: list, trans_set: list, same_shape=True, scale_factor=(1.0, 1.0)):
    """
    Transform plane set to 3d graph and put it to the space matrix by transformation matrices
    Number of transformation matrices is same with number of planes
    @param pic_set: set of picture planes
    @param trans_set: set of transformation matrices
    @param same_shape: if the planes has same shape
    @param scale_factor: <Tuple> scale factor for scaling the matrix
    @return:
    """
    # get first flatten matrix
    flattened_matrix = get_plane_matrix_flatten(pic_set[0])
    volume_list, colors_list = [], []
    # create scaling matrix
    scale_matrix = _create_scale_matrix(scale_factor)
    # put coordinates and colors into lists
    print('building list...\n')
    for pic, trans in zip(pic_set, trans_set):
        plane_matrix = flattened_matrix if same_shape is True else get_plane_matrix_flatten(pic)
        colors = pic.reshape([int(pic.size/3), 3]).tolist()
        volume = numpy.dot(plane_matrix, trans.transpose()).dot(scale_matrix) * -1
        volume = numpy.delete(volume, 3, 1).tolist()
        volume_list = volume_list + volume
        colors_list = colors_list + colors
    print('-Done building list\n')

    print('building space...\n')
    space, min_x, min_y, min_z = _build_space(volume_list)
    print('-Done building space\n')
    print('inserting colors\n')
    for volume, colors in zip(volume_list, colors_list):
        # normalize coordinates
        x = volume[0] + min_x * -1
        y = volume[1] + min_y * -1
        z = volume[2] + min_z * -1
        # change colors to grayscale
        gray_scale_color = 0.2989 * colors[0] + 0.5870 * colors[1] + 0.1140 * colors[2]
        space[int(y), int(x), int(z)] = gray_scale_color
    print('-Done inserting colors\n')
    return space


def _build_space(coordinate_set):
    """
    Builds an empty space to place planes
    @param coordinate_set: set of planes
    @return: <numpy.array> empty space
    """
    coordinate_set_lists = numpy.array(coordinate_set).transpose().tolist()
    max_x, max_y, max_z = max(coordinate_set_lists[0]), max(coordinate_set_lists[1]), max(coordinate_set_lists[2])
    min_x, min_y, min_z = min(coordinate_set_lists[0]), min(coordinate_set_lists[1]), min(coordinate_set_lists[2])

    y = int(max_y) + 2 if min_y >= 0 else int(max_y) + int(min_y) * -1 + 2
    x = int(max_x) + 2 if min_x >= 0 else int(max_x) + int(min_x) * -1 + 2
    z = int(max_z) + 2 if min_z >= 0 else int(max_z) + int(min_z) * -1 + 2
    space = numpy.zeros((y, x, z, 1), float)
    return space, min_x if min_x < 0 else 0, min_y if min_y < 0 else 0, min_z if min_z < 0 else 0


def _create_scale_matrix(scale_factors):
    """
    Creates scale matrix for scaling
    """
    return numpy.array([[scale_factors[0], 0, 0, 0],
                        [0, scale_factors[1], 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])


def _print_progress_bar(iteration, total, decimals=1, length=100, fill='█'):
    """
    Print progress bar for CLI
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    length = int(length * iteration // total)
    bar = fill * length
    print('\r|%s| %s%%' % (bar, percent), end='\r')
    if iteration == total:
        print()
