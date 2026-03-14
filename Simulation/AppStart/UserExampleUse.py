from Simulation.AppStart.main import Robot2DStudioStart,RobotStudio,VisualStudio
import numpy as np
import keyboard

from Simulation.utils.integrators import Integrator

from Robot.Models.DifferentialDriveRobot import DiffDriveParams
from Robot.Models.DifferentialDriveRobot import Differential_Drive

from Visualization.Base.VisulationParams import VisulationParams
from Visualization.Models.DifferentialDriveRobot import DiffrentialDriveRobotVisual

def SimulationInit():
    x_target = np.array([[1.5,1.5,np.pi/4]]).T
    x = np.array([[0.,0.,0.]]).T
    u = np.array([[0.,0.]]).T
    error = np.ones_like(x)
    return {"x":x,"u":u,"x_target":x_target,"error":error}


def SimulationStep(robot,x,u,x_target,error,stop) -> bool:

    if keyboard.is_pressed("up"):
        u = u + np.array([[1.5,1.5]]).T

    if keyboard.is_pressed("left"):
        u = u + np.array([[-1.3,+1.3]]).T

    if keyboard.is_pressed("right"):
        u = u + np.array([[1.3,-1.3]]).T
        
    if keyboard.is_pressed("down"):
        u = u + np.array([[-1.5,-1.5]]).T

    if np.linalg.norm(error) < 17e-2:
        stop = True

    # TODO: INFO - Maybe Euler state is ahead of simulation state
    # x = Integrator.ForwardEuler(x,u,robot.DifferentialKinematics,0.05)
    x = Integrator.RK4(x,u,robot.DifferentialKinematics,0.05)
    u = np.zeros_like(u)

    error = x - x_target

    print(np.linalg.norm(error))
    # print(repr(robot))
    # print(x[0,0])
    # print(u)

    return {"x":x,"u":u,"x_target":x_target,"error":error,"stop":stop}



Robot2DStudioStart(Robot = RobotStudio(DiffDriveParams,Differential_Drive),
                    Visual = VisualStudio(VisulationParams,DiffrentialDriveRobotVisual),
                    SimulationInit = SimulationInit,
                    SimulationStep = SimulationStep)