import numpy as np
from RobotParams import DiffDriveParams

class Differential_Drive:
    
    def __init__(self,params :DiffDriveParams):
        # Robot Name
        self.name = params.Name
        # State dimensions
        self.N = params.N
        # Action dimensions
        self.M = params.M
        # Distance between the center of L wheel to the center of R wheel
        self.s = params.s
        # The Radius of the wheels
        self.r = params.r 

    def jacobian(self,x):
        return self.r*np.array([[np.cos(x[2,0])/2,np.cos(x[2,0])/2],[np.sin(x[2,0])/2,np.sin(x[2,0])/2],[-1/self.s,1/self.s]])

    def diff_kinematics(self,x,u):        
        return self.jacobian(x)@u
