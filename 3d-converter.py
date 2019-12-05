"""
3D converter
Loads pictures and position files and convert into 3d Volumes.
author: Jinchi Zhang
Date: 11/5/2019
email: gene.zhang@bioprober.com
"""
import numpy
import sys
from PyQt5.QtWidgets import \
    QApplication, \
    QTextEdit, \
    QWidget, \
    QPushButton, \
    QVBoxLayout, \
    QHBoxLayout, \
    QFileDialog

from common.png_reader import PngReader
from common.matrix_transform import add_vtk_points_from_plane_list, plane_set_to_3d
from common.ts_reader import TsReader
from common.vtk_points_loader import VtkPointLoader
import vtk

DATA_PATH = '/home/bioprober/gh/3d-converter/'
SCALE_FACTOR = 0.026134659708742038


class Converter(QWidget):

    def __init__(self):
        super(Converter, self).__init__()
        self.pic_text = QTextEdit(self)
        self.pos_text = QTextEdit(self)
        self.file_text = QTextEdit(self)
        self.load_dir_button = QPushButton('Load Pictures Path')
        self.load_pos_button = QPushButton('Load Positions')
        self.convert_button = QPushButton('Convert')
        self.show_button = QPushButton('Show')
        self.save_file_button = QPushButton('Save VTK')
        self.load_file_button = QPushButton('Load VTK')
        self.show_file_button = QPushButton('Show File')

        self.vtk_points_loader = None

        self.init_ui()

    def init_ui(self):
        v_layout = QVBoxLayout()
        v_layout_sl = QVBoxLayout()
        h_layout_1 = QHBoxLayout()
        h_layout_2 = QHBoxLayout()
        h_layout_3 = QHBoxLayout()

        h_layout_1.addWidget(self.pic_text)
        h_layout_1.addWidget(self.pos_text)

        h_layout_2.addWidget(self.load_dir_button)
        h_layout_2.addWidget(self.load_pos_button)

        h_layout_3.addWidget(self.file_text)
        v_layout_sl.addWidget(self.save_file_button)
        v_layout_sl.addWidget(self.load_file_button)
        v_layout_sl.addWidget(self.show_file_button)
        h_layout_3.addLayout(v_layout_sl)

        v_layout.addLayout(h_layout_1)
        v_layout.addLayout(h_layout_2)
        v_layout.addWidget(self.convert_button)
        v_layout.addWidget(self.show_button)
        v_layout.addLayout(h_layout_3)

        self.load_dir_button.clicked.connect(lambda: self.load_dir_name(self.pic_text))
        self.load_pos_button.clicked.connect(lambda: self.load_file_name(self.pos_text))
        self.convert_button.clicked.connect(self.convert_to_vtk)
        self.show_button.clicked.connect(self.show_vtk)

        self.save_file_button.clicked.connect(self.save_to_file)
        self.load_file_button.clicked.connect(lambda: self.load_file_name(self.file_text))
        self.show_file_button.clicked.connect(self.show_file)

        self.setLayout(v_layout)
        self.file_text.setText(DATA_PATH)
        self.setWindowTitle('3d Converter')

        self.show()

    def convert_to_vtk(self):
        """
        Converts files from self.pic_text and self.pos_text to vtk objects
        """
        # Read files
        png_reader = PngReader(self.pic_text.toPlainText())
        ts_reader = TsReader(self.pos_text.toPlainText())
        # comment out when testing
        image_list = png_reader.load_images_from_folder()

        # for demo, please comment out when using
        # image = numpy.zeros((100, 100, 3))
        # image[:, :, :] = 255
        # image[0:9, :, :] = image[90:100, :, :] = image[:, 0:9, :] = image[:, 90:100, :] = 5

        # image_list = []
        # for i in range(500):
        #     image_list.append(image)

        trans_matrix_list = ts_reader.get_trans_matrix_list()

        # transform pictures and place to a space
        space = plane_set_to_3d(image_list, trans_matrix_list, (SCALE_FACTOR, SCALE_FACTOR))
        self.vtk_points_loader = VtkPointLoader()
        self.vtk_points_loader.add_points_from_3d_array(space)
        self.vtk_points_loader.summarize()
        # self.vtk_points_loader = add_vtk_points_from_plane_list(
        #     image_list,
        #     trans_matrix_list,
        #     (SCALE_FACTOR, SCALE_FACTOR)
        # )

    def load_dir_name(self, text):
        """
        Loads directory name by file dialog
        """
        dirname = QFileDialog.getExistingDirectory(self, 'Choose Directory', DATA_PATH)
        print(dirname)
        if not dirname:
            return
        text.setText(dirname)

    def load_file_name(self, text):
        """
        Loads file names by file dialog
        @param text: <QTextEdit> Text field to put file names in
        """
        filename = QFileDialog.getOpenFileName(self, 'Load File Name', DATA_PATH)
        print(filename)
        if not filename[0]:
            return
        text.setText(filename[0])

    def save_to_file(self):
        """
        Saves the vtk objects in self.vtk_points_loader to file
        """
        print('Dumping vtk file...\n')
        self.vtk_points_loader.dump(self.file_text.toPlainText())
        print('-Done\n')

    def show_file(self):
        """
        Renders and shows the file name in self.save_text
        """
        # Read files
        reader = vtk.vtkPolyDataReader()
        reader.SetFileName(self.file_text.toPlainText())
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

        # rendering
        self._render(vtk_actor)

    def show_vtk(self):
        """
        Renders and shows self.vtk_points_loader
        """
        self._render(self.vtk_points_loader.vtk_actor)

    def _render(self, vtk_obj):
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


app = QApplication(sys.argv)
converter = Converter()
sys.exit(app.exec_())
