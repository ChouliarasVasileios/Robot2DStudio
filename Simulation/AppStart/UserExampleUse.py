from Simulation.AppStart.main import Robot2DStudioStart,RobotStudio,VisualStudio
import numpy as np
import keyboard

from Simulation.utils.integrators import Integrator

from Robot.Models.DifferentialDriveRobot import DiffDriveParams
from Robot.Models.DifferentialDriveRobot import Differential_Drive

from Visualization.Base.VisulationParams import VisulationParams
from Visualization.Models.DifferentialDriveRobot import DiffrentialDriveRobotVisual

def SimulationInit():

    x = np.array([[0.,0.,0.]]).T
    u = np.array([[0.,0.]]).T
    return {"x":x,"u":u}


def SimulationStep(robot,x,u) -> bool:

    if keyboard.is_pressed("up"):
        u = u + np.array([[1.5,1.5]]).T

    if keyboard.is_pressed("left"):
        u = u + np.array([[-1.3,+1.3]]).T

    if keyboard.is_pressed("right"):
        u = u + np.array([[1.3,-1.3]]).T
        
    if keyboard.is_pressed("down"):
        u = u + np.array([[-1.5,-1.5]]).T

    x = Integrator.ForwardEuler(x,u,robot.DifferentialKinematics,0.05)
    u = np.zeros_like(u)

    # print(repr(robot))
    # print(x)
    # print(u)

    return {"x":x,"u":u}



Robot2DStudioStart(Robot = RobotStudio(DiffDriveParams,Differential_Drive),
                    Visual = VisualStudio(VisulationParams,DiffrentialDriveRobotVisual),
                    SimulationInit = SimulationInit,
                    SimulationStep = SimulationStep)