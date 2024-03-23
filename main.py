import SimpleITK as sitk
import numpy as np


def sitk_elastix_registration(fixed_volume, moving_volume, moving_mesh, volume_after_reg, mesh_after_reg, transformation_file):
    # Load the fixed and moving images
    fixed_image = sitk.ReadImage(fixed_volume)
    moving_image = sitk.ReadImage(moving_volume)

    # Set the initial affine transformation (align centers)
    initial_transform = sitk.CenteredTransformInitializer(fixed_image, moving_image, sitk.AffineTransform(3),
                                                          sitk.CenteredTransformInitializerFilter.GEOMETRY)

    affine_registration_method = sitk.ImageRegistrationMethod()

    # Configure the registration method
    affine_registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
    affine_registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100)
    affine_registration_method.SetOptimizerScalesFromPhysicalShift()
    affine_registration_method.SetInitialTransform(initial_transform, inPlace=False)

    # Perform registration
    final_transform = affine_registration_method.Execute(sitk.Cast(fixed_image, sitk.sitkFloat32),
                                                         sitk.Cast(moving_image, sitk.sitkFloat32))

    # Resample the moving image onto the fixed image's grid, using the final transformation
    resampled_image = sitk.Resample(moving_image, fixed_image, final_transform, sitk.sitkLinear, 0.0,
                                    moving_image.GetPixelID())

    # Save the resampled image
    sitk.WriteImage(resampled_image, volume_after_reg)

    # Save the transformation.
    sitk.WriteTransform(final_transform, transformation_file)

    transform = sitk.ReadTransform(transformation_file).GetInverse()

    # Read the mesh object from the OBJ file
    with open(moving_mesh, "r") as file:
        vertices = []
        faces = []
        for line in file:
            if line.startswith("v"):
                vertex = [float(x) for x in line.split()[1:4]]
                vertices.append(vertex)
            elif line.startswith("f"):
                face = [int(x.split("/")[0]) - 1 for x in line.split()[1:4]]  # Adjust for 0-based indexing
                faces.append(face)

    # Convert vertices to a numpy array
    vertices_array = np.array(vertices)

    # Apply the transformation to the vertices
    transformed_vertices = [transform.TransformPoint(vertex) for vertex in vertices_array]

    # Create a new OBJ file with the transformed vertices
    with open(mesh_after_reg, "w") as file:
        for vertex in transformed_vertices:
            file.write("v {} {} {}\n".format(vertex[0], vertex[1], vertex[2]))
        for face in faces:
            file.write("f {} {} {}\n".format(face[0] + 1, face[1] + 1,
                                             face[2] + 1))  # Adjust for 1-based indexing in OBJ format


if __name__ == '__main__':
    fixed_volume = 'data/fixed_mri.nii.gz'
    moving_volume = 'data/moving_mri.nii.gz'
    moving_mesh = 'data/moving_mesh.obj'

    volume_after_reg = 'data/volume_after_reg.nii.gz'
    mesh_after_reg = 'data/mesh_after_reg.obj'
    transformation_file = 'data/transformation.tfm'

    sitk_elastix_registration(fixed_volume, moving_volume, moving_mesh, volume_after_reg, mesh_after_reg, transformation_file)
