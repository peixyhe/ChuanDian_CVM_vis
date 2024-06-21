import numpy as np
from scipy.interpolate import RegularGridInterpolator

# xyz_step = np.array(  [0.05, 0.05, 0.5]  )
xyz_step = np.array(  [0.1, 0.1, 1.0]  )
half_xyz_step = xyz_step * 0.5
double_xyz_step = xyz_step * 2.0



data = []
with open(".\\rawData\\velocity_model\\1667962663929053661.txt", 'r') as r:
    linesData = r.readlines()
    for i in range(  1, len(linesData)  ):
        lineData = linesData[i].split()
        data0 = [  float(d) for d in lineData  ]
        
        data.append(    [  data0[0], data0[1], data0[2], data0[3], data0[4]  ]    )
r.close()
data = np.array(data)


X = list(    sorted(  set(data[:, 0])  )    )
Y = list(    sorted(  set(data[:, 1])  )    )
Z = list(    sorted(  set(data[:, 2])  )    )
# print(X)
# print(Y)
print(Z)


j = 0
Vp = []
Vs = []
for z0 in Z:
    vp_x = []
    vs_x = []
    for x0 in X:
        vp_y = []
        vs_y = []
        for y0 in Y:
            xyz0 = np.array(  [x0, y0, z0]  )
            if j < len(data):
                if np.all(  xyz0-data[j, 0:3] == 0.0  ):
                    vp0, vs0 = data[j, 3], data[j, 4]
                    j += 1
                else:
                    vp0, vs0 = np.nan, np.nan
            else:
                vp0, vs0 = np.nan, np.nan
            
            vp_y.append(vp0)
            vs_y.append(vs0)
        
        vp_x.append(vp_y)
        vs_x.append(vs_y)
    
    Vp.append(vp_x)
    Vs.append(vs_x)
    
Vp = np.array(Vp)
Vs = np.array(Vs)

dim = np.shape(Vp)
dim_dict = {    str(dim[0]):0,
                str(dim[1]):1,
                str(dim[2]):2     }
VP = np.transpose(    Vp, axes=(  dim_dict[ str(len(X)) ], dim_dict[ str(len(Y)) ], dim_dict[ str(len(Z)) ]  )    )
VS = np.transpose(    Vs, axes=(  dim_dict[ str(len(X)) ], dim_dict[ str(len(Y)) ], dim_dict[ str(len(Z)) ]  )    )


vp_interpolator = RegularGridInterpolator(    (X, Y, Z), VP    )
vs_interpolator = RegularGridInterpolator(    (X, Y, Z), VS    )



result_X = np.round(    np.arange(  X[0] + xyz_step[0], X[-1] - half_xyz_step[0], xyz_step[0]  ), 5    )
result_Y = np.round(    np.arange(  Y[0] + xyz_step[1], Y[-1] - half_xyz_step[1], xyz_step[1]  ), 5    )
result_Z = np.round(    np.arange(  Z[0] + xyz_step[2], Z[-1] - half_xyz_step[2], xyz_step[2]  ), 5    )
print(result_X)
print(result_Y)
print(result_Z)

e = 0
with open(    ".\\src\\velocity_model\\gradient\\gradientData" + '-'.join(  map(str, xyz_step)  ) + "_Z" + str(result_Z[0]) + ".csv", 'w'    ) as w:
    w.write(  "lon,lat,dep,Vp,Vs,vp_grad_x,vp_grad_y,vp_grad_z,vs_grad_x,vs_grad_y,vs_grad_z,vp_grad_norm,vs_grad_norm,vp_divide_vs_norm\n"  )
    for z in result_Z:
        print(z)
        for x in result_X:
            for y in result_Y:
                point = np.array(  [x, y, z]  )
                
                x1 = np.array(  [x + xyz_step[0], y,               z              ]  )
                x0 = np.array(  [x - xyz_step[0], y,               z              ]  )
                
                y1 = np.array(  [x,               y + xyz_step[1], z              ]  )
                y0 = np.array(  [x,               y - xyz_step[1], z              ]  )
                
                z1 = np.array(  [x,               y,               z + xyz_step[2]]  )
                z0 = np.array(  [x,               y,               z - xyz_step[2]]  )
                
                try:
                    vp_fx1 = vp_interpolator(x1)[0]
                    vp_fx0 = vp_interpolator(x0)[0]
                    
                    vp_fy1 = vp_interpolator(y1)[0]
                    vp_fy0 = vp_interpolator(y0)[0]
                    
                    vp_fz1 = vp_interpolator(z1)[0]
                    vp_fz0 = vp_interpolator(z0)[0]
                    
                    vp_interpolated_value = round(  vp_interpolator(point)[0], 8  )
                    
                    if (  not np.isnan(vp_fx1)  ) and (  not np.isnan(vp_fx0)  ) and \
                    (  not np.isnan(vp_fy1)  ) and (  not np.isnan(vp_fy0)  ) and \
                    (  not np.isnan(vp_fz1)  ) and (  not np.isnan(vp_fz0)  ) and (  not np.isnan(vp_interpolated_value)  ):
                        
                        vs_fx1 = vs_interpolator(x1)[0]
                        vs_fx0 = vs_interpolator(x0)[0]
                        
                        vs_fy1 = vs_interpolator(y1)[0]
                        vs_fy0 = vs_interpolator(y0)[0]
                        
                        vs_fz1 = vs_interpolator(z1)[0]
                        vs_fz0 = vs_interpolator(z0)[0]
                    
                    
                        vp_grad_x = round(    (vp_fx1 - vp_fx0) / double_xyz_step[0], 8    )
                        vp_grad_y = round(    (vp_fy1 - vp_fy0) / double_xyz_step[1], 8    )
                        vp_grad_z = round(    (vp_fz1 - vp_fz0) / double_xyz_step[2], 8    )
                        vp_grad = np.array(  [vp_grad_x, vp_grad_y, vp_grad_z]  )
                        vp_norm = round(  np.linalg.norm(vp_grad), 8  )
                        
                        vs_grad_x = round(    (vs_fx1 - vs_fx0) / double_xyz_step[0], 8    )
                        vs_grad_y = round(    (vs_fy1 - vs_fy0) / double_xyz_step[1], 8    )
                        vs_grad_z = round(    (vs_fz1 - vs_fz0) / double_xyz_step[2], 8    )
                        vs_grad = np.array(  [vs_grad_x, vs_grad_y, vs_grad_z]  )
                        vs_norm = round(  np.linalg.norm(vs_grad), 8  )
                        
                        
                        vp_divide_vs_x = (  (vp_fx1 / vs_fx1) - (vp_fx0 / vs_fx0)  ) / double_xyz_step[0]
                        vp_divide_vs_y = (  (vp_fy1 / vs_fy1) - (vp_fy0 / vs_fy0)  ) / double_xyz_step[0]
                        vp_divide_vs_z = (  (vp_fz1 / vs_fz1) - (vp_fz0 / vs_fz0)  ) / double_xyz_step[0]
                        
                        vp_divide_vs = np.array(  [vp_divide_vs_x, vp_divide_vs_y, vp_divide_vs_z]  )
                        vp_divide_vs_norm = round(  np.linalg.norm(vp_divide_vs), 8  )
                        
                        
                        vs_interpolated_value = round(  vs_interpolator(point)[0], 8  )
                        
                        w.write(   str(x) + ',' + str(y) + ',' + str(z) + ',' + 
                                    str(vp_interpolated_value) + ',' + str(vs_interpolated_value) + ',' +
                                    ','.join(  map(str, vp_grad)  ) + ',' +
                                    ','.join(  map(str, vs_grad)  ) + ',' + 
                                    str(vp_norm) + ',' + str(vs_norm) + ',' + 
                                    str(vp_divide_vs_norm) + '\n'    )
                except:
                    e += 1
w.close()

print("before interpolated data dim : ", end=" ")
print(    len(X), len(Y), len(Z),  len(X) * len(Y) * len(Z)    )
print("after interpolated data dim : ", end=" ")
print(    len(result_X), len(result_Y), len(result_Z),  len(result_X) * len(result_Y) * len(result_Z)    )

print("ValueError num: " + str(e))
