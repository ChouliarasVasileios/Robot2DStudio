from Robot2DStudio.Simulation.AppStart.SimulationMain import Robot2DStudioStart,RobotStudio,VisualStudio,RobotParams,Robot,VisualationParams,Visualization
from Services.PrintMessage.Result import ResultString
from Robot2DStudio.Simulation.utils.integrators import Integrator # You can use one of the existing integrator
from dataclasses import dataclass
from numpy import ndarray
import numpy as np

class YourVisualRobot(Visualization):
    def __init__(self, visualationParams):
        super().__init__(visualationParams)
        
        #README : In RunTime the Robot2DStudio will add the robotParams that you specified in .json file
        # So feel free to access your robotParams and use them to visualize your robot

    def Init(self):pass
        # Run Once before the simulation loop

    def Update(self, x :ndarray):
        # Run for each simulation step
        self.YourRobotVisualFunction(x)

    def YourRobotVisualFunction(self,x :ndarray):pass
        # Add you visualization logic for your robot here


# Data Transfer Object for robot modeling
@dataclass
class YourRobotParams(RobotParams):pass
# Your Robot parameter Here
# Name, State Dim: N, Control Dim: N are inherit from RobotParams


class YourRobot(Robot):

    def __init__(self,params :YourRobotParams):
        super().__init__(params)


    def __printAttributes(self) -> str:
        outputStr :str = ""
        for key,value in self.__dict__.items():
            outputStr += f"\n\t,{key} = {ResultString(value)}"
        return outputStr


    def __repr__(self):
        return super().__repr__().replace(")","") + self.__printAttributes() + "\n)"


def SimulationInit():
    # Add your Variable that initialize before the simulation Loop
    x_target :ndarray = None # Add your target state here shape : (x,y) [Invalid (,y) or (x,)] 
    x :ndarray = None # Add your initial state here shape : (x,y) [Invalid (,y) or (x,)]
    u :ndarray = None # Add your initial contol signal here shape : (x,y) [Invalid (,y) or (x,)]
    error = np.ones_like(x) 
    return {"x":x,"u":u,"x_target":x_target,"error":error} # Add more variable if need them at Simulation Step like "varName" : var


def SimulationStep(robot :Robot,step :float,x :ndarray,u:ndarray,x_target :ndarray,error :ndarray,stop :bool) -> dict:

    # Add you Implementation of simulation loop

    error = x - x_target # Calculates the error 
    return {"x":x,"u":u,"x_target":x_target,"error":error,"stop":stop}



Robot2DStudioStart(Robot = RobotStudio(YourRobotParams,YourRobot),
                    Visual = VisualStudio(VisualationParams,YourVisualRobot),
                    SimulationInit = SimulationInit,
                    SimulationStep = SimulationStep)

