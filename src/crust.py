import sys
sys.path.append(".\\src\\")
import CONST                     # import constants by user-defined



import vtk, os
import pandas as pd

colors = vtk.vtkNamedColors()
points = vtk.vtkPoints()
ugrid = vtk.vtkUnstructuredGrid()

depth = vtk.vtkFloatArray()
depth.SetNumberOfComponents(1)
depth.SetName(  'crustalthickness(km)'  )

x_set = set()
y_set = set()

if os.path.exists(    ".\\src\\crust\\temp_Data\\crust_dep.csv"    ):
    df = pd.read_csv(    ".\\src\\crust\\temp_Data\\crust_dep.csv"    )
    x = df["lon"]
    y = df["lat"]
    z = df["crustalthickness"]
    for i in range(len(x)):
        points.InsertNextPoint(    x[i], y[i], -1.0 * z[i] / CONST.ANGLE2KILOMETERS    )
        depth.InsertNextValue(z[i])
        
    x_set = set(x)
    y_set = set(y)
    
else:
    with open(    ".\\rawData\\crust\\1-s2.0-S0040195113006847-mmc2.txt", "r"    ) as r:
        linesData = r.readlines()
        with open(    ".\\src\\crust\\temp_Data\\crust_dep.csv", 'w'    ) as w:
            w.write(    "lon,lat,crustalthickness" + '\n'    )
            for i in range(2, len(linesData)):
                lineData0 = linesData[i].split()
                if (float(lineData0[0]) >= CONST.left) and (float(lineData0[0]) <= CONST.right) and (float(lineData0[1]) >= CONST.down) and (float(lineData0[1]) <= CONST.up):
                    w.write(    ','.join(lineData0) + '\n'    )
                    
                    points.InsertNextPoint(    float(lineData0[0]), float(lineData0[1]), -1.0 * (  float(lineData0[2])  ) / CONST.ANGLE2KILOMETERS    )
                    depth.InsertNextValue(  float(lineData0[2])  )
                    
                    x_set.add(  float(lineData0[0])  )
                    y_set.add(  float(lineData0[1])  )
        w.close()
    r.close()

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
ugrid.GetPointData().AddArray(depth)

writer = vtk.vtkUnstructuredGridWriter()
writer.SetInputData(ugrid)
writer.SetFileName(  r"C:\Users\hepei\Desktop\vis_velocity_model\vtk_results\crust_dep.vtk"  )
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
