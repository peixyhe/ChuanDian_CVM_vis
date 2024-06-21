import sys, os
sys.path.append(".\\src\\")
import CONST                     # import constants by user-defined


z_translate = -70.0 / CONST.ANGLE2KILOMETERS


import vtk
import numpy as np, pandas as pd

input_files_path = ".\\src\\faults_2d\\temp_Data\\csv\\"
files_list = os.listdir(input_files_path)

points = vtk.vtkPoints()

for file in files_list:
    df0 = pd.read_csv(    input_files_path + file    )
    data0 = np.array(    df0[  ['lon', 'lat', 'faults_elevation']  ].values.tolist()    )
    
    for d in data0:
        points.InsertNextPoint(    d[0], d[1], (  d[2]  ) / (  1000.0 * CONST.ANGLE2KILOMETERS  ) + z_translate    )

points_id = 0
lines = vtk.vtkCellArray()
for file in files_list:
    vtk_line = vtk.vtkLine()
    
    df1 = pd.read_csv(    input_files_path + file    )
    data1 = np.array(    df1[  ['lon', 'lat', 'faults_elevation']  ].values.tolist()    )
    
    vtk_line.GetPointIds().SetNumberOfIds(  len(data1)  )
    for i in range(  len(data1)  ):
        vtk_line.GetPointIds().SetId(i, points_id)
        points_id += 1
    
    lines.InsertNextCell(vtk_line)

# 创建 polydata
polydata = vtk.vtkPolyData()
polydata.SetPoints(points)
# polydata.GetPointData().AddArray(faults_ID)
polydata.SetLines(lines)

# 创建 mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(polydata)

# 创建 actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# 创建 renderer
renderer = vtk.vtkRenderer()

# 创建 render window
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

# 创建 render window interactor
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# 将 actor 添加到 renderer 中
renderer.AddActor(actor)

# 设置背景色
renderer.SetBackground(0, 0, 0)

# 渲染并启动交互
renderWindow.Render()

# 将 polydata 保存为 VTK 格式文件
writer = vtk.vtkPolyDataWriter()
writer.SetFileName(".\\result_Data\\faluts_2d-70.vtk")
writer.SetInputData(polydata)
writer.Write()

# 启动交互
renderWindowInteractor.Start()
