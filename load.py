"""
Load space and display with VTK
"""

from common.dicom_reader import DicomReader
from common.matrix_transform import add_vtk_points_from_plane_list
from common.ts_reader import TsReader
import numpy
import vtk

TEST_DICOM_PATH = 'tests/data/USm.1.2.840.113663.1500.1.405766469.3.2.20160304.153558.949'
TEST_TS_PATH = '/home/bioprober/gh/3d-converter/tests/data/z50r90'
TEST_RESULT_PATH = '/home/bioprober/gh/3d-converter/tests/data/example_3d_output_5.dat'


def run():
    # Read files
    # dicom_reader = DicomReader(TEST_DICOM_PATH)
    ts_reader = TsReader(TEST_TS_PATH)
    # image_list = dicom_reader.read_to_image_list()
    trans_matrix_list = ts_reader.get_trans_matrix_list()

    image = numpy.zeros((100, 100, 3))
    image[:, :, :] = 255
    image[0:9, :, :] = image[90:100, :, :] = image[:, 0:9, :] = image[:, 90:100, :] = 5

    image_list = []
    for i in range(50):
        image_list.append(image)

    # transform pictures and place to a space
    vtk_points_loader = add_vtk_points_from_plane_list(image_list, trans_matrix_list)

    # Display VTK
    # Renderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(vtk_points_loader.vtk_actor)
    renderer.SetBackground(.2, .3, .4)
    renderer.ResetCamera()

    # Render Window
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    # Interactor
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(render_window)

    # Begin Interaction
    render_window.Render()
    renderWindowInteractor.Start()

    # # Dump
    # print('Dumping vtk file...\n')
    # vtk_points_loader.dump()
    # print('-Done\n')


if __name__ == "__main__":
    run()
