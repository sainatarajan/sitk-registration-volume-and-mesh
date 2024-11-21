# SimpleITK Elastix Registration with Mesh Transformation

This project implements a 3D image registration pipeline using **SimpleITK** and supports transformation of corresponding 3D mesh objects. The pipeline performs affine registration of medical imaging volumes and applies the resulting transformation to a mesh file in OBJ format.

---

## Features

- **Affine Image Registration**: Aligns a moving volume to a fixed volume using affine transformation.
- **Mesh Transformation**: Applies the registration transformation to a 3D mesh to ensure correspondence with the aligned volume.
- **Output Files**:
  - Registered volume in NIfTI format (`.nii.gz`).
  - Transformed mesh in OBJ format.
  - Transformation file in `.tfm` format.

---

## Prerequisites

### Software Requirements
- Python 3.7+
- SimpleITK
- NumPy

### Installation
Install the required Python packages:
```bash
pip install SimpleITK numpy
