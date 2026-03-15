import numpy as np
from numpy import ndarray
from Robot.Base.Robot import Robot
from Robot.Models.PendulumParams import PendulumParams 
from Services.PrintMessage.Result import ResultString

class Pendulum(Robot):

    def __init__(self,params :PendulumParams):
        super().__init__(params)

        # The Length of pendulum
        self.l = params.l
        
        # Mass of pendulum
        self.m = params.m
        
        # Gravity acceleration
        self.g = params.g

        # Air resistant coefficient 
        self.b = params.b 

    def Dynamics(self, x :ndarray, u :ndarray):
        """
        Input:
            State = [x1,x2].T -> [theta,theta_dot].T
            Control = [t] -> Torque

        Ouput: 
            d(State)/dt = [x1_dot,x2_dot].T -> [theta_dot,theta_double_dot].T
        """
        A = np.array([[0, 1],
                      [0, -self.b / (self.m* (self.l**2) )]
                      ])
        
        E = np.array([[0, 0],
                      [(-self.g / self.l) * np.sin(x[0,0]), 0]
                      ])
        
        B = np.array([[0, 1/self.m*self.l]]).T
        
        return A@x + E + B@u


    def __printAttributes(self) -> str:
        outputStr :str = ""
        for key,value in self.__dict__.items():
            outputStr += f"\n\t,{key} = {ResultString(value)}"
        return outputStr


    def __repr__(self):
        return super().__repr__().replace(")","") + self.__printAttributes()