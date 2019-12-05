"""
Load space and display with VTK
"""

import vtk

TEST_SAVE_PATH = '/home/bioprober/gh/3d-converter/tests/data/my_poly_result_try.vtk'


def run():
    # Read files
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(TEST_SAVE_PATH)
    reader.Update()
    poly_data = reader.GetOutput()

    # Create mapper and actor
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(poly_data)
    mapper.SetColorModeToDefault()
    mapper.SetScalarRange(-1000, 1000)
    mapper.SetScalarVisibility(1)
    vtk_actor = vtk.vtkActor()
    vtk_actor.SetMapper(mapper)

    # Display VTK
    # Renderer
    renderer = vtk.vtkRenderer()
    renderer.AddActor(vtk_actor)
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


if __name__ == "__main__":
    run()
