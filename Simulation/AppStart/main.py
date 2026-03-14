import sys
import matplotlib.patches as patches
from typing import Callable,Any
from dataclasses import dataclass
from functools import partial
from Simulation.Configuration import Configure
from Robot.Base.Robot import Robot
from Robot.Base.RobotParams import RobotParams
from Visualization.Base.Visulization import Visualization
from Visualization.Base.VisulationParams import VisulationParams


@dataclass
class RobotStudio:
    robotParams :RobotParams
    robot : Robot

@dataclass
class VisualStudio:
    visualParams : VisulationParams
    visual :Visualization


def SetUp(Robot :RobotStudio,Visual:VisualStudio):
    robot = Robot.robot(Configure.Get(Robot.robotParams))
    visual = Visual.visual(Configure.Get(Visual.visualParams))

    return {
        "Robot" : robot,
        "Visual" : visual,
    }

def Loop(Robot :Robot,
         Visual:Visualization,
         Init :Callable[[None],Any],
         Step :Callable[[Any],Any]):

    Visual.InitRender()
        
    params :dict = Init()
    params.update({"stop":False})

    StepWithRobot = partial(Step,Robot)

    while True:

        params = StepWithRobot(**params)

        if(params["stop"]):
            break

        Visual.Render(params["x"])

    print("Exiting Robot2DStudio Bye! :)")
    sys.exit(0)
    

def Robot2DStudioStart(Robot :RobotStudio,
                       Visual :VisualStudio,
                       SimulationInit :Callable[[None],Any],
                       SimulationStep :Callable[[Any],Any]):
    
    Loop(**SetUp(Robot,Visual),Init=SimulationInit,Step=SimulationStep)



# def main():
#     Loop(**SetUp())
    

# if __name__ == "__main__":
#     main()