from typing import Callable
from numpy import ndarray

class Integrator:

    #TODO : Implementation
    @staticmethod
    def InterionPoint():
        pass
    
    #TODO : validate results
    @staticmethod
    def RK4(x :ndarray,u:ndarray,f :Callable[[ndarray,ndarray],ndarray],dt :float):
        k1 = dt*f(x,u)
        k2 = dt*f(x+k1/2,u+dt/2)
        k3 = dt*f(x+k2/2,u+dt/2)
        k4 = dt*f(x+k3,u+dt)
        return x + (1/6)*(k1+2*k2+2*k3+k4)

    #TODO : validate results
    @staticmethod
    def ForwardEuler(x :ndarray,u:ndarray,f :Callable[[ndarray,ndarray],ndarray],dt :float):
        return x + f(x,u)*dt # Returns the next state
