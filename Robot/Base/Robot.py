from numpy import ndarray
from typing import Generic, TypeVar
from Services.PrintMessage.Warning import Warning
from Services.PrintMessage.Result import ResultString


T = TypeVar("T")

class Robot:
    
    def __init__(self,params: Generic[T]):
        # Robot Name
        self.name :str = params.Name
        # State dimensions
        self.N :int = params.N
        # Action dimensions
        self.M :int = params.M

    @property
    def JointsConstraints(self) -> ndarray:
        Warning("Need Implementation Joints Constraints")

    def Jacobian(self,x :ndarray) -> ndarray:
        Warning("Need Implementation Jacobian")

    def InverseJacobian(self,x :ndarray) -> ndarray:
        Warning("Need Implementaion InverseJacobian")

    def DifferentialKinematics(self,x :ndarray, u :ndarray) -> ndarray:        
        Warning("Need Implementation Differential Kinematics")

    def Dynamics(self,x :ndarray, u :ndarray) -> ndarray:
        Warning("Need Implementation Dynamics")


    def __repr__(self):
        return f"{self.__class__.__name__}(\n\tname='{ResultString(self.name)}'\n\t,N={ResultString(self.N)}\n\t,M={ResultString(self.M)}\n\t,JointConstaints={ResultString(self.JointsConstraints)})"