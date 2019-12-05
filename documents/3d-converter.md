# 3D Converter

> This is an introduction documentation for 3D Converter application. Concepts and basic algorithm is introduced in this paper:  https://www.sciencedirect.com/science/article/pii/S1746809413000839, by *Tiexiang wen, Qingsong Zhu, Wenjian Qin, Ling Li, Fan Yang, Yaoqin Xie, Jia Gu* in Nov. 2013

## Introduction

> 3D  Converter is an project to convert set of medical scans to a 3D model for further medical analysis. 



## Open the 3D Converter GUI

1. To open the 3D Converter Gui. Users  needs to enter the python virtual environment by

   ```$ source .venv/bin/activate```

2. CD to root the of the project and

   ```$ python 3d-convereter.py```

   

   ### Issues

   1. This program is a python program, therefore system needs to have python 3.x installed. 
   2. Anaconda has some of the packages, therefore without entering virtual environment. Users needs to install pyqt5 and vtk packages.



## Project Structure

> It is important to know the project structure before maintaining, The main controller 3d-convert.py uses interfaces in the "common" directory.

> Here is a diagram for the basic project structure

* root directory:
  * 3d-converter.py
  * README.md
  * .venv
    * (virtual environment)
  * common
    * dicom_reader.py
    * hole_filler.py
    * matrix_transform.py
    * png_reader.py
    * ts_reader.py
    * vtk_points_loader.py
  * documents
    * (All documentations)
  * Fusion
    * (a test example with 105 png images)
    * us_frames_pos.txt
  * misc
    * trans_writer.py
  * tests
    * data
      * (directory to store test files and test results)



> In the common directory, dicom_reader.py is currently not used since the program now reads a folder of pictures. hole_filler.py is a latest interface which helps filling colors for uncolored voxels. matrix_transformation.py is a model which contains  functions for 2d-to-3d matrix transformation. png_reader.py reads png images in a directory, crop the pictures and output them in lists of numpy arrays. ts reader reads ts, txt, or other files that contains strings and output them in transformation matrices. vtk_pointt_loader interfaces takes numpy 3d array as 3d spaces with color, and scatter points in vtk space. 



> In the misc folder, there is a CLI program name trans_writer.py. This program can be executed in virtual environment by ```$ python trans_writer.py``` This program is created for auto generating position information to the required form of 3d-converter. CLI will ask for the moving parameters, including the coordinates of two points representing a designed axis that the 3d object rotates, how many step it takes and how will the object travel along x, y, z z axis. This program is fully for testing. Therefore, in order to test the position information. User needs to go to 3d-converter.py -> convert_to_vtk and comment and uncomment codes as instructed. 



## Performance

> Performance for the hole-filling method now is extremely slow. This is caused by too many "empty points" need to be filled. Possible solution is to continue optimize the algorithm using vectorization and broadcast. Another is solution, and, must-done is to use the propagation methodology in the paper to reduce the amount of points to fill. 



> When comment out 3 parts of codes in vtk_points _loader.add_points_from_3d_array, which means running without the hole-filling part, it will take about 5 minus to process and render a 3d model.



## Future Suggestion

> Therefore a few suggestions for maintaining this project. 

* As said before performance for this project is very important. Increasing the speed for ultrasound 3d model building is necessary. As the Hole filling part is very slow. I suggest to use the propagation methodology in the paper for hole filling. This will require a change to the current algorithm used in hole_filler.py.

* Use vtk volume instead of vtk point cloud to render the result. This will need a numpy-3d-array-to-vtk-volume interface. 