import numpy as np
from numpy import ndarray
from Robot2DStudio.Visualization.Base.Visualization import Visualization

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

        x1 = self.robotParams.l1 * np.cos(q1 - np.pi/2) # -pi/2 cause we assume that for q1 == q2 == 0 is on oy'
        y1 = self.robotParams.l1 * np.sin(q1- np.pi/2)
        x2 = self.robotParams.l1 * np.cos(q1- np.pi/2) + self.robotParams.l2 * np.cos(q1 + q2 - np.pi/2)
        y2 = self.robotParams.l1 * np.sin(q1- np.pi/2) + self.robotParams.l2 * np.sin(q1 + q2 - np.pi/2)
        
        self.lineDoublePendulum.set_data([0.0,x1,x2],[0.0,y1,y2])