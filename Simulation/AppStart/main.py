import matplotlib.patches as patches
from typing import Callable,Any
from dataclasses import dataclass
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


def SetUp(Robot :RobotStudio):#,Visual :VisualStudio) -> dict[Robot,Visualization]:
    robot = Robot.robot(Configure.Get(Robot.robotParams))
    # visual = Visual.visual( Configure.Get(Visual.visualParams))
    
    #TODO: Add functionality of patches for a given robot

    return {
        "robot" : robot,
        # "visual" : visual,
    }

def Loop(robot :Robot,
        #  visual:Visualization,
         Init :Callable[[None],Any],
         Step :Callable[[Any],None]):
    
    params = Init()

    while True:

        Step(robot,**params)

        # visual.render()


def Robot2DStudioStart(Robot :RobotStudio,
                       Visual :VisualStudio,
                       SimulationInit :Callable[[None],Any],
                       SimulationStep :Callable[[Any],None]):
    
    Loop(**SetUp(Robot),Init=SimulationInit,Step=SimulationStep)#,Visual))
    print("here")




# def main():
#     Loop(**SetUp())
    

# if __name__ == "__main__":
#     main()