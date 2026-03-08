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

    if keyboard.is_pressed("w"):
        u = u + np.array([[0.5,0.5]]).T

    if keyboard.is_pressed("a"):
        u = u + np.array([[-0.3,+0.3]]).T

    if keyboard.is_pressed("d"):
        u = u + np.array([[0.3,-0.3]]).T
        
    if keyboard.is_pressed("s"):
        u = u + np.array([[-0.5,-0.5]]).T

    x = Integrator.ForwardEuler(x,u,robot.DifferentialKinematics,0.05)
    u = np.zeros_like(u)

    # print(repr(robot))
    print(x)
    # print(u)

    return {"x":x,"u":u}



# if __name__ == "main":
Robot2DStudioStart(Robot = RobotStudio(DiffDriveParams,Differential_Drive),
                    Visual = VisualStudio(VisulationParams,DiffrentialDriveRobotVisual),
                    SimulationInit = SimulationInit,
                    SimulationStep = SimulationStep)