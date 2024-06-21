# Project: Volume rendering of VCM of southwest China 
# He Pei 
# 04/05/2024

""" Description:
Use volume rendering to render the VCM

Command line interface: python volume_rendering_vtk.py  data.vtk

"""


import vtk
import sys
import argparse

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout
from PyQt5.QtCore import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

# color transfer function
# format: [isovalue, R, G, B]
CTF = [[2.65   , 0,   0, 0.5625],
       [2.88638, 0,   0, 1],
       [3.42256, 0,   1, 1],
       [3.69064, 0.5, 1, 0.5],
       [3.95873, 1,   1, 0],
       [4.49491, 1,   0, 0],
       [4.76   , 0.5, 0, 0]]

# opacity transfer function
# format: [isovalue, opacity]
# OTF = [[0.00066 , 0.0022],
#        [0.4     , 0.1272],
#        [0.474367, 0.3039],
#        [0.590473, 0.4978],
#        [0.63    , 0.6659],
#        [0.66    , 0.8082],
#        [0.7     , 0.9418],
#        [0.8     , 1],
#        [1.64    , 1]]
OTF = [[2.65, 0.0],
       [4.76, 1.0]]

SAMP_DIST = 0.5

# camera settings
CAM = [[126.692 , 35.3048 , 11.387],             # position
       [102.4   , 27.65   , -1.66563],             # focal point
       [-0.47151, -0.00733, 0.88183],      # up vector
       [0, 1000]]                 # clipping range

def make(filename):
    # read the head image
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()

    # define the color map
    colorTrans = vtk.vtkColorTransferFunction()
    colorTrans.SetColorSpaceToRGB()
    for [isoVal, R, G, B] in CTF:
        colorTrans.AddRGBPoint(isoVal, R, G, B)

    # define the opacity transfer function
    opacityTrans = vtk.vtkPiecewiseFunction()
    for [isoVal, o] in OTF:
        opacityTrans.AddPoint(isoVal, o)

    # define volume property
    vProp = vtk.vtkVolumeProperty()
    vProp.SetColor(colorTrans)
    vProp.SetScalarOpacity(opacityTrans)
    vProp.SetInterpolationTypeToLinear()
    vProp.ShadeOn()

    mapper = vtk.vtkSmartVolumeMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    mapper.SetSampleDistance(SAMP_DIST)

    volume = vtk.vtkVolume()
    volume.SetMapper(mapper)
    volume.SetProperty(vProp)

    # enable depth peeling in renderer
    ren = vtk.vtkRenderer()
    ren.SetBackground(0.75, 0.75, 0.75)
    # ren.AddVolume(volume)
    ren.AddViewProp(volume)
    ren.ResetCamera()

    return ren, mapper


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName('The Main Window')
        MainWindow.setWindowTitle('VCM of Southwest China')

        self.centralWidget = QWidget(MainWindow)
        self.gridlayout = QGridLayout(self.centralWidget)
        self.vtkWidget = QVTKRenderWindowInteractor(self.centralWidget)

        self.gridlayout.addWidget(self.vtkWidget, 0, 0, 4, 4)

        MainWindow.setCentralWidget(self.centralWidget)


class IsosurfaceDemo(QMainWindow):

    def __init__(self, margs, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        filename = margs.file                # head dataset file name
        self.frame_counter = 0

        self.ren, self.mapper = make(filename)
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()

        # set camera position
        self.camera = self.ren.GetActiveCamera()
        self.camera.SetPosition(CAM[0][0], CAM[0][1], CAM[0][2])
        self.camera.SetFocalPoint(CAM[1][0], CAM[1][1], CAM[1][2])
        self.camera.SetViewUp(CAM[2])
        self.camera.SetClippingRange(CAM[3])

        self.iren.AddObserver("KeyPressEvent", self.key_pressed_callback)


    def key_pressed_callback(self, obj, event):
        key = obj.GetKeySym()
        if key == "s":
            # save frame
            file_name = "dvr_head_" + str(self.frame_counter).zfill(5) + ".png"
            window = self.ui.vtkWidget.GetRenderWindow()
            image = vtk.vtkWindowToImageFilter()
            image.SetInput(window)
            png_writer = vtk.vtkPNGWriter()
            png_writer.SetInputConnection(image.GetOutputPort())
            png_writer.SetFileName(file_name)
            window.Render()
            png_writer.Write()
            self.frame_counter += 1
        elif key == "c":
            # print camera setting
            camera = self.ren.GetActiveCamera()
            print("Camera settings:")
            print("  * position:        %s" % (camera.GetPosition(),))
            print("  * focal point:     %s" % (camera.GetFocalPoint(),))
            print("  * up vector:       %s" % (camera.GetViewUp(),))
            print("  * clipping range:  %s" % (camera.GetClippingRange(),))


if __name__ == "__main__":

    # --define argument parser and parse arguments--
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()

    # --main app--
    app = QApplication(sys.argv)
    window = IsosurfaceDemo(margs=args)
    window.ui.vtkWidget.GetRenderWindow().SetSize(800, 800)
    window.show()
    window.setWindowState(Qt.WindowMaximized)
    window.iren.Initialize()

    sys.exit(app.exec_())
