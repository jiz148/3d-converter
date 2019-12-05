"""
Main.py
"""
import vtk

from common.dicom_reader import DicomReader
from common.matrix_transform import plane_set_to_3d
from common.ts_reader import TsReader

TEST_DICOM_PATH = 'tests/data/USm.1.2.840.113663.1500.1.405766469.3.2.20160304.153558.949'
TEST_TS_PATH = '/home/bioprober/gh/3d-converter/tests/data/tracking_65_corrected.ts'
TEST_RESULT_PATH = '/home/bioprober/gh/3d-converter/tests/data/example_3d_output_5.dat'


def run():
    # Read files
    dicom_reader = DicomReader(TEST_DICOM_PATH)
    ts_reader = TsReader(TEST_TS_PATH)
    image_list = dicom_reader.read_to_image_list()
    trans_matrix_list = ts_reader.get_trans_matrix_list()

    # transform pictures and place to a space
    space, colors_list = plane_set_to_3d(image_list, trans_matrix_list)
    y_len, x_len, z_len = space.shape[0], space.shape[1], space.shape[2]
    print(space.shape, '\n')

    # # Store numpy array sa vtk image
    # data_importer = vtk.vtkImageImporter()
    # data_string = space.tostring()
    # data_importer.CopyImportVoidPointer(data_string, len(data_string))
    # data_importer.SetDataScalarTypeToUnsignedChar()
    #
    # # describe how the data is stored
    # data_importer.SetDataExtent(0, y_len, 0, x_len, 0, z_len)
    # data_importer.SetWholeExtent(0, y_len, 0, x_len, 0, z_len)

    colors = vtk.vtkNamedColors()

    # numpy to vtk image
    data_importer = vtk.vtkImageImport()
    data_string = space.tostring()
    data_importer.CopyImportVoidPointer(data_string, len(data_string))

    # The type of the newly imported data is set to unsigned char (uint8)
    data_importer.SetDataScalarTypeToUnsignedChar()
    data_importer.SetNumberOfScalarComponents(1)

    #  describe the dimensions
    data_importer.SetDataExtent(0, y_len, 0, x_len, 0, z_len)
    data_importer.SetWholeExtent(0, y_len, 0, x_len, 0, z_len)

    # The following class is used to store transparency-values for later retrival.
    #  In our case, we want the value 0 to be
    # completely opaque whereas the three different cubes are given different transparency-values to show how it works.
    alpha_channel_func = vtk.vtkPiecewiseFunction()
    alpha_channel_func.AddPoint(0, 0.02)
    alpha_channel_func.AddPoint(50, 0.05)
    alpha_channel_func.AddPoint(100, 0.1)
    alpha_channel_func.AddPoint(150, 0.2)

    # This class stores color data and can create color tables from a few color points.
    #  For this demo, we want the three cubes to be of the colors red green and blue.
    color_func = vtk.vtkColorTransferFunction()
    # color_func.AddRGBPoint(0, 1.0, 1.0, 1.0)
    # color_func.AddRGBPoint(100, 0.0, 1.0, 0.0)
    # color_func.AddRGBPoint(150, 0.0, 0.0, 1.0)
    print('Adding colors...\n')
    loop = 0
    for i, colors in zip(range(len(colors_list)), colors_list):
        color_func.AddRGBPoint(i, colors[0]/255, colors[1]/255, colors[2]/255)
        loop += 1
        print('looped: ', loop)
    print('-Done adding colors\n')

    # The previous two classes stored properties.
    #  Because we want to apply these properties to the volume we want to render,
    # we have to store them in a class that stores volume properties.
    volume_property = vtk.vtkVolumeProperty()
    volume_property.SetColor(color_func)
    volume_property.SetScalarOpacity(alpha_channel_func)

    volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
    volumeMapper.SetInputConnection(data_importer.GetOutputPort())

    # The class vtkVolume is used to pair the previously declared volume as well as the properties
    #  to be used when rendering that volume.
    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volume_property)

    # With almost everything else ready, its time to initialize the renderer and window, as well as
    #  creating a method for exiting the application
    renderer = vtk.vtkRenderer()
    renderWin = vtk.vtkRenderWindow()
    renderWin.AddRenderer(renderer)
    renderInteractor = vtk.vtkRenderWindowInteractor()
    renderInteractor.SetRenderWindow(renderWin)

    # We add the volume to the renderer ...
    renderer.AddVolume(volume)
    renderer.SetBackground(colors.GetColor3d("MistyRose"))

    # ... and set window size.
    renderWin.SetSize(400, 400)

    # A simple function to be called when the user decides to quit the application.
    def exitCheck(obj, event):
        if obj.GetEventPending() != 0:
            obj.SetAbortRender(1)

    # Tell the application to use the function as an exit check.
    renderWin.AddObserver("AbortCheckEvent", exitCheck)

    renderInteractor.Initialize()
    # Because nothing will be rendered without any input, we order the first render manually
    #  before control is handed over to the main-loop.
    renderWin.Render()
    renderInteractor.Start()


if __name__ == "__main__":
    run()
