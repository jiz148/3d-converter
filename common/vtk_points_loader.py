"""
This Script includes VtkLoader class to load and visualize vtk points
"""
import vtk

from common.hole_filler import HoleFiller

DEFAULT_COLOR = {"r": 255, "g": 255, "b": 255}
DEFAULT_SAVE_PATH = '/home/bioprober/gh/3d-converter/tests/data/my_poly_result_try.vtk'


class VtkPointLoader:

    def __init__(self, z_min=-1000.0, z_max=1000.0):
        self.vtk_poly_data = vtk.vtkPolyData()
        self.clear_points()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(self.vtk_poly_data)
        mapper.SetColorModeToDefault()
        mapper.SetScalarRange(z_min, z_max)
        mapper.SetScalarVisibility(1)
        self.vtk_actor = vtk.vtkActor()
        self.vtk_actor.SetMapper(mapper)

    def add_points(self, point, c=DEFAULT_COLOR):
        """
        Adds points to the vtk point loader
        @param point: <list> point to be added, list of [x, y, z]
        @param c: <dictionary> dictionary of {"r": 1, "g": 2, "b": 3}
        """
        point_id = self.vtk_points.InsertNextPoint(point[:])
        self.vtk_depth.InsertNextValue(point[2])
        self.vtk_cells.InsertNextCell(1)
        self.vtk_cells.InsertCellPoint(point_id)

        # setup colors
        self.colors.InsertNextTuple3(c.get("r"), c.get("g"), c.get("b"))
        # self.colors.InsertNextTuple3(255, 255, 255)

    def add_points_from_list(self, points, colors=DEFAULT_COLOR):
        """
        Adds points to the vtk point loader from list
        @param points: <list> list of point coordinates
        @param colors: <list> list of color list [r, g, b],
                        needs to be the same length with colors
        """
        print('started scattering\n')
        for point, c in zip(points, colors):
            # change to [0, 0, 0] if want rgb
            if c != 0.0:
                point_id = self.vtk_points.InsertNextPoint(point[:])
                # self.vtk_depth.InsertNextValue(point[2])
                self.vtk_cells.InsertNextCell(1)
                self.vtk_cells.InsertCellPoint(point_id)

                # setup colors
                # self.colors.InsertNextTuple3(c[0], c[1], c[2])  # for rgb
                self.colors.InsertNextTuple([c])  # for grayscale

        print('-Done scattering\n')

    def add_points_from_3d_array(self, space):
        """
        Adds points to the vtk point loader from numpy array
        There are there parts of codes to be comment out to run without hole-filling
        @param space: <numpy.array> numpy 3d array with all color data
        """
        print('space shape: ', space.shape)
        print('started scattering points...')
        looped = 0

        # comment out following 1 line to run without hole filling
        # hole_filler = HoleFiller(space, 7)

        for y in range(space.shape[0]):
            for x in range(space.shape[1]):
                for z in range(space.shape[2]):
                    if space[y, x, z, :][0] != 0.0:
                        point_id = self.vtk_points.InsertNextPoint([x, y, z])
                        # self.vtk_depth.InsertNextValue(space[y, x, z][2])
                        self.vtk_cells.InsertNextCell(1)
                        self.vtk_cells.InsertCellPoint(point_id)
                        self.colors.InsertNextTuple([space[y, x, z, :][0].item()])  # for grayscale
                        looped += 1

                    # comment out following else part to run without hole filling
                    # else:
                    #     hole_filler.derive_points((x, y, z))
                    #     looped += 1

                    # comment out following else part to run without hole filling
                    # print('processed ', looped, ' points', end='\r')

        # comment out following 2 lines to run without hole filling
        # point_list, color_list = hole_filler.summarize()
        # self.add_points_from_list(point_list, color_list)

        print('-Done scattering points')

    def summarize(self):
        """
        finalize the cells and points in the polydata
        """
        self.vtk_poly_data.SetPoints(self.vtk_points)
        self.vtk_poly_data.SetVerts(self.vtk_cells)
        self.vtk_poly_data.GetPointData().SetScalars(self.colors)

        self.vtk_cells.Modified()
        self.vtk_points.Modified()
        # self.vtk_depth.Modified()
        self.vtk_poly_data.Modified()

    def clear_points(self):
        self.vtk_points = vtk.vtkPoints()
        self.vtk_cells = vtk.vtkCellArray()
        # self.vtk_depth = vtk.vtkDoubleArray()
        self.colors = vtk.vtkUnsignedCharArray()
        self.colors.SetName('Colors')
        self.colors.SetNumberOfComponents(1)
        # self.vtk_depth.SetName('DepthArray')
        self.vtk_poly_data.SetPoints(self.vtk_points)
        self.vtk_poly_data.SetVerts(self.vtk_cells)
        # self.vtk_poly_data.GetPointData().SetScalars(self.vtk_depth)
        # self.vtk_poly_data.GetPointData().SetActiveScalars('DepthArray')

    def dump(self, save_name=DEFAULT_SAVE_PATH):
        vtk_writer = vtk.vtkPolyDataWriter()
        vtk_writer.SetInputData(self.vtk_poly_data)
        vtk_writer.SetFileName(save_name)
        vtk_writer.Update()
