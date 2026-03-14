import matplotlib.patches as patches
from typing import Callable,Any
from dataclasses import dataclass
from functools import partial
from Simulation.Configuration import Configure
from Robot.Base.Robot import Robot
from Robot.Base.RobotParams import RobotParams
from Visualization.Base.Visulization import Visualization
from Visualization.Base.VisulationParams import VisulationParams,PatchParams


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
    temp :VisulationParams = Configure.Get(Visual.visualParams)
    print(type(temp.Patches[0]))
    visualTEST = Visual.visual(Configure.Get(Visual.visualParams))

    return {
        "Robot" : robot,
        "Visual" : visualTEST,
    }

def Loop(Robot :Robot,
         Visual:Visualization,
         Init :Callable[[None],Any],
         Step :Callable[[Any],Any]):

    Visual.InitRender()    
    params = Init()

    StepWithRobot = partial(Step,Robot)

    while True:

        params = StepWithRobot(**params)

        Visual.render(params["x"])


def Robot2DStudioStart(Robot :RobotStudio,
                       Visual :VisualStudio,
                       SimulationInit :Callable[[None],Any],
                       SimulationStep :Callable[[Any],Any]):
    
    Loop(**SetUp(Robot,Visual),Init=SimulationInit,Step=SimulationStep)



# def main():
#     Loop(**SetUp())
    

# if __name__ == "__main__":
#     main()