import numpy as np
from Robot.Base.Robot import Robot
from Robot.Models.DifferentialDriveRobotParams import DifferentialDriveRobotParams
from Services.PrintMessage.Result import ResultString

class DifferentialDriveRobot(Robot):

    def __init__(self,params :DifferentialDriveRobotParams):
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


    def __printAttributes(self) -> str:
        outputStr :str = ""
        for key,value in self.__dict__.items():
            outputStr += f"\n\t,{key} = {ResultString(value)}"
        return outputStr


    def __repr__(self):
        return super().__repr__().replace(")","") + self.__printAttributes() + "\n)"