import sys, os
sys.path.append(".\\src\\")
import CONST                     # import constants by user-defined



p0 = [97.8,  21.8, -70 / CONST.ANGLE2KILOMETERS]
p1 = [107.0, 21.8, -70 / CONST.ANGLE2KILOMETERS]
p2 = [107.0, 33.4, -70 / CONST.ANGLE2KILOMETERS]
p3 = [97.8,  33.4, -70 / CONST.ANGLE2KILOMETERS]

p4 = [97.8,  21.8, 5.25]#/ CONST.ANGLE2KILOMETERS]
p5 = [107.0, 21.8, 5.25]#/ CONST.ANGLE2KILOMETERS]
p6 = [107.0, 33.4, 5.25]#/ CONST.ANGLE2KILOMETERS]
p7 = [97.8,  33.4, 5.25]#/ CONST.ANGLE2KILOMETERS]

import vtk

colors = vtk.vtkNamedColors()

points = vtk.vtkPoints()
points.InsertNextPoint(p0)
points.InsertNextPoint(p1)
points.InsertNextPoint(p2)
points.InsertNextPoint(p3)

points.InsertNextPoint(p4)
points.InsertNextPoint(p5)
points.InsertNextPoint(p6)
points.InsertNextPoint(p7)

ugrid = vtk.vtkUnstructuredGrid()
ugrid.InsertNextCell(vtk.VTK_HEXAHEDRON, 8, [0, 1, 2, 3, 4, 5, 6, 7])

ugrid.SetPoints(points)
# ugrid.GetPointData().AddArray(vp)

writer = vtk.vtkUnstructuredGridWriter()
writer.SetInputData(ugrid)
writer.SetFileName(r'C:\Users\hepei\Desktop\vis_velocity_model\vtk_results\axes_box_52p5.vtk')
# writer.SetDataModeToAscii()
writer.Update()