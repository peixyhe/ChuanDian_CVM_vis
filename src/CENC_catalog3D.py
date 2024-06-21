import sys
sys.path.append(".\\src\\")
import CONST                     # import constants by user-defined



import vtk, math
import pandas as pd

df = pd.read_csv("src\\catalog_3d\\CENC_minMag1.0.csv")
data = df[  ["lon", "lat", "dep", "mag"]  ].values
xyz = data[  data[:, 2] > 0.0  ]

lon = xyz[:, 0]
lat = xyz[:, 1]
dep = xyz[:, 2]
mag = xyz[:, 3]

def mag2radius(mag0):
    # return math.exp(  (mag - 4.56) / 1.96  )
    return math.pow(  2.0, (mag0 - 4.56) / 1.96  )
    # return 2.0 ** mag0
max_radius = mag2radius(  max(mag)  )

polydata = vtk.vtkPolyData()

vtk_points = vtk.vtkPoints()

diameter_array = vtk.vtkFloatArray()
diameter_array.SetName("diameter")

dep_array = vtk.vtkFloatArray()
dep_array.SetName("depth(km)")

mag_array = vtk.vtkFloatArray()
mag_array.SetName("magnitude")

sphereNum = 0
for i in range(len(mag)):
    sphereNum += 1
    diameter = (  mag2radius(mag[i]) / max_radius  ) * 0.25
    
    vtk_points.InsertNextPoint(  lon[i], lat[i], -1.0 * dep[i] / CONST.ANGLE2KILOMETERS  )
    diameter_array.InsertNextValue(diameter)
    dep_array.InsertNextValue(dep[i])
    mag_array.InsertNextValue(mag[i])
print("sphere numbers: " + str(sphereNum))

polydata.SetPoints(vtk_points)
polydata.GetPointData().SetScalars(diameter_array)    # SetScalars; not AddArray
polydata.GetPointData().AddArray(dep_array)
polydata.GetPointData().AddArray(mag_array)

# 创建vtkSphereSource
sphere_source = vtk.vtkSphereSource()
sphere_source.SetPhiResolution(6)
sphere_source.SetThetaResolution(6)

# 使用vtkGlyph3D将球体放置在点上
glyph = vtk.vtkGlyph3D()
glyph.SetInputData(polydata)
glyph.SetSourceConnection(sphere_source.GetOutputPort())
glyph.SetScaleModeToScaleByScalar()

# 创建vtkPolyDataWriter将数据写入VTK文件
writer = vtk.vtkPolyDataWriter()
writer.SetFileName("src\\catalog_3d\\CENC_catalog_3d.vtk")
writer.SetInputConnection(glyph.GetOutputPort())
writer.Write()

# # Create a mapper and actor
# mapper = vtk.vtkDataSetMapper()
# mapper.SetInputData(glyph.GetOutputPort())

# actor = vtk.vtkActor()
# actor.SetMapper(mapper)
# actor.GetProperty().SetColor(colors.GetColor3d('Silver'))
# actor.GetProperty().SetPointSize(2)

# # Visualize
# renderer = vtk.vtkRenderer()
# renderWindow = vtk.vtkRenderWindow()
# renderWindow.SetWindowName('Polyhedron')
# renderWindow.AddRenderer(renderer)
# renderWindowInteractor = vtk.vtkRenderWindowInteractor()
# renderWindowInteractor.SetRenderWindow(renderWindow)

# renderer.AddActor(actor)
# renderer.SetBackground(colors.GetColor3d('Salmon'))
# renderer.ResetCamera()
# renderer.GetActiveCamera().Azimuth(30)
# renderer.GetActiveCamera().Elevation(30)
# renderWindow.Render()
# renderWindowInteractor.Start()
