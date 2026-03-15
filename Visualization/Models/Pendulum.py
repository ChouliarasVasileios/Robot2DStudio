import numpy as np
from numpy import ndarray
from Visualization.Base.Visulization import Visualization

class PendulumVisual(Visualization):
    def __init__(self, visulationParams):
        super().__init__(visulationParams)
        
        #README : In RunTime the Robot2DStudio will add the robotParams that you specified in .json file
        # So feel free to access your robotParams and use them to visualize your robot


    def Init(self):
        # Init BodyFrame
        self.PendulumLine, = self.axes.plot([],[],"o-",markersize = 6.5,lw = self.robotParams.l,color = "blue")
        self.PendulumLine.set_data([],[])

    def Update(self, x :ndarray):
        self.DrawPendulum(x)

    def DrawPendulum(self,x :ndarray):
        
        self.PendulumLine.set_data([0.0,-np.sin(x[0,0])*self.robotParams.l],[0.0, -np.cos(x[0,0]) * self.robotParams.l])