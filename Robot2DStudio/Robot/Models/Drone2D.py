import numpy as np
from numpy import ndarray
from Robot2DStudio.Robot.Base.Robot import Robot
from Robot2DStudio.Robot.Models.Drone2DParams import Drone2DParams 
from Robot2DStudio.Services.PrintMessage.Result import ResultString

class Drone2D(Robot):

    #TODO: Waring the physics now is not support the different for the m1 and m2 of the masses
    # to support m1 != m2 should calulate the dF along the side of the l and integrate

    def __init__(self,params :Drone2DParams):
        super().__init__(params)

        # The Length of Drone2D
        self.l = params.l
        
        # Right mass
        self.m1 = params.m1

        # Left mass
        self.m2 = params.m2
        
        # Gravity acceleration
        self.g = params.g

        # Air density
        self.rho = params.rho

        # Drag coefficient
        self.cd = params.cd

        # Top area space
        self.Ay = params.Ay

        # Side area space
        self.Ax = params.Ax

        #Total mass of the drone
        self.mTotal = params.m1 + params.m2

    def __Fd(self,A :float,vel :float) -> str:
        return (1/2)*self.rho*self.cd*A*vel

    def Dynamics(self, x :ndarray, u :ndarray) -> ndarray:
        """
        Input:
            State = [x1,x2,x3,x4,x5,x6].T -> [x,y,phi,x_dot,y_dot,phi_dot].T
            Control = [F1,F2].T -> Forces of the rotors (right and left)

        Output:
            d(State)/dt = [x1_dot,x2_dot,x3_dot,x4_dot,x5_dot,x6_dot].T -> [x_dot,y_dot,phi_dot,x_ddot,y_ddot,phi_ddot].T 
        """
        s_phi = np.sin(x[2,0])
        c_phi = np.cos(x[2,0])

        # Velocity along the body meets the side area, across the body meets the top area
        v_par = x[3,0]*c_phi + x[4,0]*s_phi
        v_perp = -x[3,0]*s_phi + x[4,0]*c_phi

        k = self.__Fd(self.Ay,abs(v_perp)) + self.__Fd(self.Ax,abs(v_par))
        v_R = v_perp + (self.l/2)*x[5,0]
        v_L = v_perp - (self.l/2)*x[5,0]

        tau = -(1/2)*self.rho*self.cd*(self.Ay/2)*(self.l/2)*(abs(v_R)*v_R - abs(v_L)*v_L)
        I = self.mTotal*(self.l/2)**2


        A = np.array([
            [0,0,0,1,0,0],
            [0,0,0,0,1,0],
            [0,0,0,0,0,1],
            [0,0,0,-k/self.mTotal,0,0],
            [0,0,0,0,-k/self.mTotal,0],
            [0,0,0,0,0,0]
            ])

        B = np.array([
            [0,0],
            [0,0],
            [0,0],
            [-s_phi/self.mTotal,-s_phi/self.mTotal],
            [c_phi/self.mTotal,c_phi/self.mTotal],
            [2/(self.mTotal*self.l),-2/(self.mTotal*self.l)]
            ])

        E = np.array([
            [0],
            [0],
            [0],
            [0],
            [-self.g],
            [tau/I]
            ])

        return A@x + B@u + E
        
    def __printAttributes(self) -> str:
        outputStr :str = ""
        for key,value in self.__dict__.items():
            outputStr += f"\n\t,{key} = {ResultString(value)}"
        return outputStr


    def __repr__(self):
        return super().__repr__().replace(")","") + self.__printAttributes() + "\n)"