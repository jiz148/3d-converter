"""
HoleFiller class to implement hole-filling method for manipulate  3d model
"""
import numpy


class HoleFiller:

    def __init__(self, model, radius):
        """
        @param model: 3d array of a volume model
        @param radius: radius of the spherical space for each propagation
        """
        self.model = model
        self.radius = radius
        self.point_list = None
        # find array of all points inside sphere around origin
        self.origin_sphere_arr = self._find_points_in_sphere(self.radius)

        self.q_vectors = None
        self.q_gray_values = None

    def derive_points(self, coordinate):
        """
        Derives q vectors and q gray values and add them to self.q-vectors and self.q_gray_values
        Appends coordinate to self.point_list
        @param coordinate: <Tuple> tuple of (x, y, z)
        """
        # find the points in spherical space
        sphere_pt_arr = self.origin_sphere_arr + numpy.array(coordinate)

        # broadcast to get gray scale and weight for each sphere point
        try:
            if self.q_vectors is not None:
                self.q_vectors = numpy.concatenate((self.q_vectors, (coordinate - sphere_pt_arr)), axis=0)
            else:
                self.q_vectors = coordinate - sphere_pt_arr
            # swap first and second column in the point array
            sphere_pt_arr.T[[0, 1]] = sphere_pt_arr.T[[1, 0]]
            if self.q_gray_values is not None:
                self.q_gray_values = numpy.concatenate((self.q_gray_values, self.model[sphere_pt_arr.transpose().tolist()]), axis=0)
            else:
                self.q_gray_values = self.model[sphere_pt_arr.transpose().tolist()]
            if self.point_list is not None:
                self.point_list = numpy.concatenate((self.point_list, numpy.array([coordinate])), axis=0)
            else:
                self.point_list = numpy.array([coordinate])
        except IndexError:
            pass
        pass

    def summarize(self):
        """
        Summarize stored q-vectors and q-gray-values and returns a list of coordinates and a list of colors
        @return: <Tuple> a <list> fo coordinates and a <list> of colors
        """
        print('self.point_list size: ', self.point_list.shape)
        print('self.q_vector size: ', self.q_vectors.shape)
        print('self.q_gray_values size: ', self.q_gray_values.shape)
        # broadcast to get d, w and gray weights for every q vectors
        d = numpy.sqrt(numpy.sum(self.q_vectors ** 2, axis=1))
        w = 1 / (1 + d ** 2)
        gray_weight = self.q_gray_values * w

        # add every r**3 gray weights and weights together
        gray_weight = numpy.add.reduceat(gray_weight, numpy.arange(0, len(gray_weight)), len(self.origin_sphere_arr))
        w = numpy.add.reduceat(w, numpy.arange(0, len(w)), len(self.origin_sphere_arr))

        # finally broadcast to get new gray values
        new_colors = gray_weight/w

        return self.point_list.tolist(), new_colors

    @staticmethod
    def _find_points_in_sphere(radius):
        """
        Find a all points inside the spherical space around the origin
        @param radius: radius of the sphere
        @return: <numpy.array> array of coordinates of the points in the spherical space around
        """
        result_list = []
        for x in range(radius):
            for y in range(radius):
                for z in range(radius):
                    if x**2 + y**2 + z**2 <= radius**2:
                        result_list.append([x, y, z])
        return numpy.array(result_list)
