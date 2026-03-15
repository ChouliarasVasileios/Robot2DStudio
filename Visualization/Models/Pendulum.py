import numpy as np
from numpy import ndarray
from Visualization.Base.Visulization import Visualization

# TODO : Neet to have acces to Pendulum params for the legnht or other stuff

class PendulumVisual(Visualization):

    def __init__(self, visulationParams):
        super().__init__(visulationParams)

        # Init BodyFrame
        self.PendulumLine, = self.axes.plot([],[],"o-",markersize = 1.5,lw = 1.5,color = "blue")
        self.PendulumLine.set_data([],[])
        
        # self.LineYBody, = self.axes.plot([],[],"o-",markersize = 0.5,lw = 1.5,color = "green")
        # self.LineYBody.set_data([],[])


    def Init(self):
        pass

    def Update(self, x :ndarray):
        self.DrawPendulum(x)

    def DrawPendulum(self,x :ndarray):
        
        self.PendulumLine.set_data([0.0,-np.sin(x[0,0])*1.5],[0.0, -np.cos(x[0,0]) * 1.5])