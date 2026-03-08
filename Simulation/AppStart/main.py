import keyboard
from Simulation.Configuration import Configure
from Robot.Base.Robot import Robot
from Robot.Base.RobotParams import DiffDriveParams
from Visualization.Base.VisulationParams import VisulationParams
from Robot.Models.DifferentialDriveRobot import Differential_Drive
from Visualization.Base.VisulizationBase import Visualization
from Simulation.utils.integrators import Integrator
from dataclasses import dataclass
from numpy import ndarray
import numpy as np
import matplotlib.patches as patches

from Services.PrintMessage.Result import Result
from Services.PrintMessage.Warning import Warning


@dataclass
class States:
    x_start :ndarray
    x_target :ndarray

@dataclass
class Controls:
    u_start :ndarray
    u_target :ndarray


def LoadParams():
    return {
        "diffDriveParams" : Configure.Get(DiffDriveParams),
        "visulationParams" : Configure.Get(VisulationParams)
    }


def InitSimulation(diffDriveParams : DiffDriveParams,
                    visulationParams :VisulationParams):

    DDR = Differential_Drive(diffDriveParams)

    print(repr(DDR))
    exit(1)
    visual = Visualization(visulationParams)

    # Add robot Graphics
    rect = patches.Rectangle((0.0,0.0),0.6,0.3,linewidth = 0.5,edgecolor = 'blue',facecolor ='blue')
    visual.axes.add_patch(rect)
    

    # Add States - Controls
    states = States(x_start = np.array([[0.,0.,0.]]).T
                    ,x_target = None)
    
    controls = Controls(u_start = np.array([[0.,0.]]).T,
                        u_target = None)
    
    return {
        "robot" : DDR,
        "visual" : visual,
        "states" : states,
        "controls" : controls,
        "rect" : rect 
    }

def SetUp():
    params = LoadParams()
    return InitSimulation(**params)


def Loop(robot :Robot
         ,visual:Visualization
         ,states :States
         ,controls :Controls
         ,rect):

    x = np.copy(states.x_start)
    u = np.copy(controls.u_start)
    while True:

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
        print(x)

        functions = [
            (visual.move_rectangle,(rect,x[0,0],x[1,0],x[2,0]))
        ]

        visual.update(functions,0.05)


def main():
    Loop(**SetUp())
    

if __name__ == "__main__":
    main()