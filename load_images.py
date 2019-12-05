import vtk

from common.matrix_transform import add_vtk_points_from_plane_list
from common.png_reader import PngReader
from common.ts_reader import TsReader

DEFAULT_PAHT = '/home/bioprober/gh/3d-converter/Fusion/us_frames_pos.txt '


def run():
    png_reader = PngReader()
    ts_reader = TsReader(DEFAULT_PAHT)
    pic_list = png_reader.load_images_from_folder()
    trans_matrix_list = ts_reader.get_trans_matrix_list()

    vtk_points_loader = add_vtk_points_from_plane_list(pic_list, trans_matrix_list)
    _render(vtk_points_loader.vtk_actor)


def _render(vtk_obj):
    """
    Render the environment to show vtk object
    @param vtk_obj: vtk obj to be shown
    """
    # Display VTK
    # Renderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(vtk_obj)
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


if __name__ == '__main__':
    run()
