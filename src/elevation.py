import sys
sys.path.append(".\\src\\")
import CONST                     # import constants by user-defined


z_translate = 50.0 / CONST.ANGLE2KILOMETERS

import vtk, os
import xarray as xr, pandas as pd

colors = vtk.vtkNamedColors()
points = vtk.vtkPoints()
ugrid = vtk.vtkUnstructuredGrid()

elevation = vtk.vtkFloatArray()
elevation.SetNumberOfComponents(1)
elevation.SetName(  'elevation(m)'  )

x_set = set()
y_set = set()

if os.path.exists(    ".\\src\\elevation\\temp_Data\\" + str(CONST.up) + '_' + str(CONST.down) + '_' + str(CONST.left) + "_" + str(CONST.right) + "-30s_elevation.csv"    ):
    df = pd.read_csv(    ".\\src\\elevation\\temp_Data\\" + str(CONST.up) + '_' + str(CONST.down) + '_' + str(CONST.left) + "_" + str(CONST.right) + "-30s_elevation.csv"    )
    x = df["lon"]
    y = df["lat"]
    z = df["elevation"]
    for i in range(len(x)):
        points.InsertNextPoint(    x[i], y[i], z[i] / (1000.0 * CONST.ANGLE2KILOMETERS) + z_translate    )
        elevation.InsertNextValue(z[i])
        
    x_set = set(x)
    y_set = set(y)
    
else:
    elevation_data = xr.open_dataset(    ".\\rawData\\elevation\\ETOPO_2022_v1_30s_N90W180_surface.nc"    )
    lon = elevation_data.lon.values[:]      # x
    lat = elevation_data.lat.values[:]      # y
    ele = elevation_data.z.values[:, :]     # z

    with open(    ".\\src\\elevation\\temp_Data\\" + str(CONST.up) + '_' + str(CONST.down) + '_' + str(CONST.left) + "_" + str(CONST.right) + "-30s_elevation.csv", 'w'    ) as w:
        w.write(    "lon,lat,elevation" + '\n'    )
        for j in range(  len(lat)  ):
            y = round(lat[j], 10)
            if y >= CONST.down and y <= CONST.up:
                print(y)
                y_set.add(y)
                for i in range(  len(lon)  ):
                    x = round(lon[i], 10)
                    if x >= CONST.left and x <= CONST.right:
                        x_set.add(x)
                        z0 = ele[j][i]
                        
                        w.write(    str(x) + ',' + str(y) + ',' + str(z0) + '\n'    )
                        points.InsertNextPoint(    x, y, z0 / (1000.0 * CONST.ANGLE2KILOMETERS)    )
                        elevation.InsertNextValue(z0)
    w.close()

x_num = len(x_set)
y_num = len(y_set)

for j in range(y_num - 1):
    for i in range(x_num - 1):
        id0 = i + j * x_num
        id1 = id0 + 1
        id2 = id1 + x_num
        id3 = id0 + x_num
        """
           id3------id2
            |        |
            |        |
           id0------id1
        """
        ugrid.InsertNextCell(    vtk.VTK_TRIANGLE, 3, [id3, id0, id1]    )
        ugrid.InsertNextCell(    vtk.VTK_TRIANGLE, 3, [id3, id1, id2]    )    # ugrid.InsertNextCell(    vtk.VTK_QUAD, 4, [id0, id1, id2, id3]    )



ugrid.SetPoints(points)
ugrid.GetPointData().AddArray(elevation)

writer = vtk.vtkUnstructuredGridWriter()
writer.SetInputData(ugrid)
writer.SetFileName(  r"C:\Users\hepei\Desktop\vis_velocity_model\vtk_results\elevation-30s_Z50km.vtk"  )
# writer.SetDataModeToAscii()
writer.Update()

# Create a mapper and actor
mapper = vtk.vtkDataSetMapper()
mapper.SetInputData(ugrid)

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(colors.GetColor3d('Silver'))
actor.GetProperty().SetPointSize(2)

# Visualize
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.SetWindowName('Polyhedron')
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

renderer.AddActor(actor)
renderer.SetBackground(colors.GetColor3d('Salmon'))
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderWindow.Render()
renderWindowInteractor.Start()
