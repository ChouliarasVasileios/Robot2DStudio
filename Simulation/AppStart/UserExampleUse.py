from Simulation.AppStart.SimulationMain import Robot2DStudioStart,RobotStudio,VisualStudio
import numpy as np
import keyboard

from Simulation.utils.integrators import Integrator

from Robot.Models.DifferentialDriveRobot import DifferentialDriveRobotParams
from Robot.Models.DifferentialDriveRobot import DifferentialDriveRobot


from Visualization.Base.VisualationParams import VisualationParams
from Visualization.Models.DifferentialDriveRobot import DiffrentialDriveRobotVisual

# TODO: May i need to expose the x_target from appsetting 

def SimulationInit():
    x_target = np.array([[1.5,1.5,np.pi/4]]).T# Wrong position
    x = np.array([[0.,0.,0.]]).T
    u = np.array([[0.,0.]]).T
    error = np.ones_like(x)
    return {"x":x,"u":u,"x_target":x_target,"error":error}


def SimulationStep(robot,step,x,u,x_target,error,stop) -> bool:

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
    # x = Integrator.RK4(x,u,robot.DifferentialKinematics,step)
    x = Integrator.RK4(x,u,robot.DifferentialKinematics,step)

    u = np.zeros_like(u)

    error = x - x_target

    print(np.linalg.norm(error))
    # print(repr(robot))
    print(x)
    print(u)

    return {"x":x,"u":u,"x_target":x_target,"error":error,"stop":stop}


# TODO: Use this if the user want to write it's own robot so the program will automatically 
# read from yourRobot.json
Robot2DStudioStart(Robot = RobotStudio(DifferentialDriveRobotParams,DifferentialDriveRobot),
                    Visual = VisualStudio(VisualationParams,DiffrentialDriveRobotVisual),
                    SimulationInit = SimulationInit,
                    SimulationStep = SimulationStep)

# TODO: Implement a new interface that user can use when he want to use local models
# you propable will need to add a mapper so in runtime to read from correct file