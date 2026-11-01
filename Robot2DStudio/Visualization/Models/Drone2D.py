import numpy as np
from numpy import ndarray
from Robot2DStudio.Visualization.Base.Visualization import Visualization
from Robot2DStudio.Services.Helpers.Helper import RotationMatrix2

class Drone2DVisual(Visualization):
    def __init__(self, visualationParams):
        super().__init__(visualationParams)

    def Init(self):
        # Creating the Drone graphics using plot, the markers are the two masses
        self.lineDrone, = self.axes.plot([],[],"o-",markersize = 6.5,lw = 2,color = "blue")
        self.lineDrone.set_data([],[])

    def Update(self, x :ndarray):
        self.DrawDrone(x)

    def DrawDrone(self,x :ndarray):
        center = x[0:2,:]
        # From the center to the right mass, rotated by phi
        s = RotationMatrix2.Rz(x[2,0]) @ np.array([[self.robotParams.l/2],[0.0]])
        right = center + s
        left = center - s
        self.lineDrone.set_data([left[0,0],right[0,0]],[left[1,0],right[1,0]])
