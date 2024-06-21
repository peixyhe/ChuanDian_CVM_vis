import sys, os
sys.path.append(r"src")
import CONST                     # import constants by user-defined



import vtk, numpy as np, pandas as pd
sys.path.append(r"src\velocity_model")
import layer_triMesh

colors = vtk.vtkNamedColors()

points = vtk.vtkPoints()

vp = vtk.vtkFloatArray()
vp.SetNumberOfComponents(1)
vp.SetName('Vp')

vp_gradx = vtk.vtkFloatArray()
vp_gradx.SetNumberOfComponents(1)
vp_gradx.SetName('vp_gradx')

vp_grady = vtk.vtkFloatArray()
vp_grady.SetNumberOfComponents(1)
vp_grady.SetName('vp_grady')

vp_gradz = vtk.vtkFloatArray()
vp_gradz.SetNumberOfComponents(1)
vp_gradz.SetName('vp_gradz')

vp_grad_norm = vtk.vtkFloatArray()
vp_grad_norm.SetNumberOfComponents(1)
vp_grad_norm.SetName('vp_grad_norm')

vs = vtk.vtkFloatArray()
vs.SetNumberOfComponents(1)
vs.SetName('Vs')

vs_gradx = vtk.vtkFloatArray()
vs_gradx.SetNumberOfComponents(1)
vs_gradx.SetName('vs_gradx')

vs_grady = vtk.vtkFloatArray()
vs_grady.SetNumberOfComponents(1)
vs_grady.SetName('vs_grady')

vs_gradz = vtk.vtkFloatArray()
vs_gradz.SetNumberOfComponents(1)
vs_gradz.SetName('vs_gradz')

vs_grad_norm = vtk.vtkFloatArray()
vs_grad_norm.SetNumberOfComponents(1)
vs_grad_norm.SetName('vs_grad_norm')

vp_divide_vs = vtk.vtkFloatArray()
vp_divide_vs.SetNumberOfComponents(1)
vp_divide_vs.SetName('Vp/Vs')

vp_divide_vs_norm = vtk.vtkFloatArray()
vp_divide_vs_norm.SetNumberOfComponents(1)
vp_divide_vs_norm.SetName('grad of Vp/Vs')



# df = pd.read_csv(r"src\velocity_model\gradient\gradientData0.05-0.05-0.5_Z0.5.csv")
df = pd.read_csv(r"src\velocity_model\gradient\gradientData0.1-0.1-1.0_Z1.0.csv")
data = df[  ["lon", "lat" ,"dep", "Vp", "Vs", \
             "vp_grad_x" ,"vp_grad_y", "vp_grad_z", \
             "vs_grad_x", "vs_grad_y", "vs_grad_z", \
             "vp_grad_norm", "vs_grad_norm", \
             "vp_divide_vs_norm"]  ].values

for d in data:
    points.InsertNextPoint(    d[0], d[1], -1.0 * d[2] / CONST.ANGLE2KILOMETERS    )
    vp.InsertNextValue(d[3])
    vs.InsertNextValue(d[4])
    vp_divide_vs.InsertNextValue(  d[3] / d[4]  )
    
    vp_gradx.InsertNextValue(d[5])
    vp_grady.InsertNextValue(d[6])
    vp_gradz.InsertNextValue(d[7])
    
    vs_gradx.InsertNextValue(d[8])
    vs_grady.InsertNextValue(d[9])
    vs_gradz.InsertNextValue(d[10])
    
    vp_grad_norm.InsertNextValue(d[11])
    vs_grad_norm.InsertNextValue(d[12])
    
    vp_divide_vs_norm.InsertNextValue(d[-1])
    
xyz = data[:, 0:3]



ugrid = vtk.vtkUnstructuredGrid()

z = list(    sorted(  set( (xyz[:, -1]).tolist() )  )    )
print(z)

xy = (    xyz[  xyz[:, -1] == min(z)  ]    )[:, 0:-1]
triangle = layer_triMesh.triMesh_oneLayer(xy)
xy_len = len(xy)

for k in range(  len(z) - 1  ):
    for tri in triangle:
        id_up   = (    tri + (  k*xy_len  ) * np.ones(3)    ).astype(int)
        id_down = (    id_up +    xy_len    * np.ones(3)    ).astype(int)
        
        faceId0 = [  id_up[0], id_up[1],   id_up[2],   id_down[0]  ]
        faceId1 = [  id_up[1], id_up[2],   id_down[0], id_down[1]  ]
        faceId2 = [  id_up[2], id_down[0], id_down[1], id_down[2]  ]
        
        ugrid.InsertNextCell(vtk.VTK_TETRA, 4, faceId0)
        ugrid.InsertNextCell(vtk.VTK_TETRA, 4, faceId1)
        ugrid.InsertNextCell(vtk.VTK_TETRA, 4, faceId2)

ugrid.SetPoints(points)
ugrid.GetPointData().AddArray(vp)
ugrid.GetPointData().AddArray(vs)
ugrid.GetPointData().AddArray(vp_divide_vs)

ugrid.GetPointData().AddArray(vp_divide_vs_norm)
ugrid.GetPointData().AddArray(vp_grad_norm)
ugrid.GetPointData().AddArray(vs_grad_norm)

# ugrid.GetPointData().AddArray(vp_gradx)
# ugrid.GetPointData().AddArray(vp_grady)
# ugrid.GetPointData().AddArray(vp_gradz)

# ugrid.GetPointData().AddArray(vs_gradx)
# ugrid.GetPointData().AddArray(vs_grady)
# ugrid.GetPointData().AddArray(vs_gradz)



writer = vtk.vtkUnstructuredGridWriter()
writer.SetInputData(ugrid)
writer.SetFileName(r'C:\Users\hepei\Desktop\vis_velocity_model\vtk_results\V-gradientData0.1-0.1-1.0_-1.vtk')
# writer.SetDataModeToAscii()
writer.Update()

# Create a mapper and actor
mapper = vtk.vtkDataSetMapper()
mapper.SetInputData(ugrid)

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(colors.GetColor3d('Silver'))

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
