import numpy as np
from numpy import ndarray
from Services.PrintMessage.Result import ResultString
from Robot.Base.Robot import Robot
from Robot.Models.DoublePendulumParams import DoublePendulumParams

#TODO : add dump term b
class DoublePendulum(Robot):

    def __init__(self, params:DoublePendulumParams):
        super().__init__(params)
        
        self.m1 :float = params.m1 # Mass of the first joint
        self.l1 :float = params.l1 # Lenght of the first link
        self.m2 :float = params.m2 # Mass of the second joint
        self.l2 :float = params.l2 # Lenght of the  joint
        self.g :float = params.g # Gravity acceleration


    def _mass_matrix(self,x :ndarray):
        
        # The joint position of the 2nd pendulum
        q2 = x[1,0]
        
        l1 = self.l1
        m1 = self.m1
        
        l2 = self.l2
        m2 = self.m2
        
        A0 = (l1**2)*m1 + (l2**2)*m2 + (l1**2)*m2 + 2*l1*m2*l2*np.cos(q2)
        A1 = (l2**2)*m2 + l1*m2*l2*np.cos(q2)
        A2 = (l2**2)*m2 + l1*m2*l2*np.cos(q2)
        A3 = (l2**2)*m2
        
        M = np.array([[A0,A1],[A2,A3]])
        
        return M # 2x2 Mass Matrix of the double Pendulum
    
    def _coriolis_matrix(self,x :ndarray):
        
        # Unpacking the state of the system
        q2 = x[1,0] # The joint position of the 2nd pendulum
        q1_dot = x[2,0] # The joint velocity of the 1st pendulum
        q2_dot = x[3,0] # The joint velocity of the 2nd pendulum
        
        l1 = self.l1
        
        l2 = self.l2
        m2 = self.m2
        
        B0 = -2*q2_dot*l1*m2*l2*np.sin(q2)
        B1 = -q2_dot*l1*m2*l2*np.sin(q2)
        B2 = q1_dot*l1*m2*l2*np.sin(q2)
        B3 = 0.0
        
        C = np.array([[B0,B1],[B2,B3]])
        
        return C # 2x2 Coriolis of the double pendulum
    
    def _gravity_matrix(self,x :ndarray):
        
        q1 = x[0,0] # The joint position of the 1st pendulum
        q2 = x[1,0] # The joint position of the 2nd pendulum
        
        l1 = self.l1
        m1 = self.m1
        
        l2 = self.l2
        m2 = self.m2
        
        D0 = -self.g*m1*l1*np.sin(q1) - self.g*m2*(l1*np.sin(q1) + l2*np.sin(q1 + q2))
        D1 = -self.g*m2*l2*np.sin(q1 + q2)
        
        G = np.array([[D0,D1]]).T
        
        return G
        
    # The dynamics of the Double Pendulum
    def Dynamics(self,x :ndarray,u :ndarray):
        
        q_dot = np.array([[x[2,0],x[3,0]]]).T
        
        M_inv = np.linalg.inv(self._mass_matrix(x))
        
        q_ddot = M_inv @ (u - self._coriolis_matrix(x) @ q_dot + self._gravity_matrix(x))
        
        x_dot = np.vstack((q_dot,q_ddot))
        return x_dot
    

    def __printAttributes(self) -> str:
        outputStr :str = ""
        for key,value in self.__dict__.items():
            outputStr += f"\n\t,{key} = {ResultString(value)}"
        return outputStr


    def __repr__(self):
        return super().__repr__().replace(")","") + self.__printAttributes() + "\n)"