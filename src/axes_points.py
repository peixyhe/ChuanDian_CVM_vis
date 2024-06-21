
import sys
sys.path.append(".\\src\\")
import CONST                     # import constants by user-defined



X = [x0 for x0 in range(98, 106 + 2, 2)]
Y = [y0 for y0 in range(22, 32 + 2, 2)]
Z = [z0 for z0 in range(0, -70-10, -10)]
print(X, Y, Z)

x_min = 97.8
x_max = 107.0

y_min = 21.8
y_max = 33.4

z_max = 0
z_min = -70.0 / CONST.ANGLE2KILOMETERS

import vtk

vtk_points = vtk.vtkPoints()

for z1 in Z:
    vtk_points.InsertNextPoint(x_min, y_min, z1 / CONST.ANGLE2KILOMETERS)
    vtk_points.InsertNextPoint(x_max, y_min, z1 / CONST.ANGLE2KILOMETERS)
    vtk_points.InsertNextPoint(x_min, y_max, z1 / CONST.ANGLE2KILOMETERS)
    vtk_points.InsertNextPoint(x_max, y_max, z1 / CONST.ANGLE2KILOMETERS)

for y1 in Y:
    vtk_points.InsertNextPoint(x_min, y1, z_min)
    vtk_points.InsertNextPoint(x_max, y1, z_min)
    vtk_points.InsertNextPoint(x_min, y1, z_max)
    vtk_points.InsertNextPoint(x_max, y1, z_max)

for x1 in X:
    vtk_points.InsertNextPoint(x1, y_min, z_min)
    vtk_points.InsertNextPoint(x1, y_max, z_min)
    vtk_points.InsertNextPoint(x1, y_min, z_max)
    vtk_points.InsertNextPoint(x1, y_max, z_max)

polydata = vtk.vtkPolyData()
polydata.SetPoints(vtk_points)

# 创建 polyvertex 数据结构
verts = vtk.vtkCellArray()
for i in range(vtk_points.GetNumberOfPoints()):
    verts.InsertNextCell(1)
    verts.InsertCellPoint(i)
polydata.SetVerts(verts)

# 创建vtkPolyDataWriter将数据写入VTK文件
writer = vtk.vtkPolyDataWriter()
writer.SetFileName(r"C:\Users\hepei\Desktop\vis_velocity_model\vtk_results\axes_points.vtk")
writer.SetInputData(polydata)
writer.Write()
