# Stories
> This file includes stories to complete the project


## Starting the python project

- Time: 1h
- Acceptance criteria:
    - Should have virtual environment
    - Should have document README.md
    - Should have test folder
    - Should have common folder
    - Should have main.py
    - Should have document folder
    - Should have tests folder with data folder and test data in it
    - Should make common and root folder to be python package


## Researches

- Time: 3h
- Acceptance criteria:
    - Should learn the structure of DICOM files, and how to read using python
    - Should learn the structure of pos information file
    - Should learn transformation matrices
    - Should document research to README


## Read DICOM files

- Time: 2h
- Acceptance criteria:
    - Should have dicom_reader.py in common
    - Should be able to read .dicom file to list of picture matrices, (numpy)
    - Should have functionality to add one 'z' dimension to each matrix 

## Read .ts file
- Time: 1h
- Acceptance criteria:
    - Should have ts_reader.py
    - Should be able to read .ts file to list of transformation matrices, (numpy)


## Convert Pictures to 3d Graph
- Time: 2h
- Acceptance criteria:
    - Should have function which transform points to 3d
    - Should have function which transform a picture set to 3d


## Dump and Load Result
- Time: 1h
- Acceptance criteria:
    - Should be able to dump result
    - Should have load.py to load data


## Display 3d Image
- Time: 2h
- Acceptance criteria:
    - Should be able to display result data in load.py
    - Should convert result data to other structure if needed


## Optimize Build process
- Time: 2h
- Acceptance criteria:
    - Should make the building process faster by solving big O problem
    - Should fix build space function
