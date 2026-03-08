import numpy as np
from Robot.Robot import Robot
from Robot.RobotParams import DiffDriveParams
from Services.PrintMessage.Result import ResultString

class Differential_Drive(Robot):

    def __init__(self,params :DiffDriveParams):
        super().__init__(params)

        # Distance between the center of L wheel to the center of R wheel
        self.s = params.s
        # The Radius of the wheels
        self.r = params.r 

    def Jacobian(self,x):
        return self.r * np.array([[ np.cos(x[2, 0])/2, np.cos(x[2, 0])/2],
                                [np.sin(x[2, 0])/2, np.sin(x[2, 0])/2],
                                [-1/self.s, 1/self.s]
                                ])

    def DifferentialKinematics(self,x,u):        
        return self.Jacobian(x) @ u

    def __repr__(self):
        return super().__repr__().replace(")","") + f"\n\t,s={ResultString(self.s)}\n\t,r={ResultString(self.r)})"