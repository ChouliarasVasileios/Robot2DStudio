import numpy as np
from numpy import ndarray
from Robot2DStudio.Visualization.Base.Visualization import Visualization
from Robot2DStudio.Services.Helpers.Helper import RotationMatrix2

class DoublePendulumVisual(Visualization):
    def __init__(self, visualationParams):
        super().__init__(visualationParams)

    def Init(self):
        # Creating the Double Pendulum graphics using plot
        self.lineDoublePendulum, = self.axes.plot([],[],"o-",markersize = 6.5,lw = 2)
        self.lineDoublePendulum.set_data([],[]) # Initialize the first ploting line with no data

    def Update(self, x :ndarray):
        self.DrawDoublePendulum(x)

    def DrawDoublePendulum(self,x :ndarray):
        q1 = x[0,0]
        q2 = x[1,0]
        # -pi/2 cause we assume that for q1 == q2 == 0 is on oy'
        s1 = self.robotParams.l1*RotationMatrix2.Rz(-np.pi/2) @ np.array([[np.cos(q1)],[np.sin(q1)]])
        s2 = s1 + self.robotParams.l2*RotationMatrix2.Rz(-np.pi/2) @ np.array([[np.cos(q1 + q2)],[np.sin(q1 + q2)]])
        self.lineDoublePendulum.set_data([0.0,s1[0,0],s2[0,0]],[0.0,s1[1,0],s2[1,0]])