# 3D Converter
> This project is to convert pictures and their position information sequence to a 3D array


## Content

- [Test Information](ti)



<br/><a name="ti"></a>
## Test Information

### Pictures Data
- Data are storded in dicom files
- To read dicom file, use pydicom for Python, pixel_array is the property we are looking for
- DICOM file name: USm.1.2.840.113663.1500.1.405766469.3.2.20160304.153558.949
- The dicom file will be read and parsed to a list of pictures in common.dicom

### Position Information Data
- Stored in .ts files
- Each position information is stored in the each line with 18 parameters, we need the 2-17th parameters to define the position of each picture
- 16 parameters is used as 16 values of the **transformation matrix**
- .ts file name: '/home/bioprober/gh/3d-converter/tests/data/tracking_65_corrected.ts'
 