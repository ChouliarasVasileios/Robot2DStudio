import sys
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
    robotParams = Configure.Get(Robot.robotParams)
    robot = Robot.robot(robotParams)

    # TODO: Need Revision if you want a user to use the robotParams in init
    # cause now you create a new obj and the add the new attribute
    visual = Visual.visual(Configure.Get(Visual.visualParams))
    
    # Maybe all this is not worth it cause you can use the robotParams annotation like self.robotParams :RobotParams = robotParams
    setattr(visual,"robotParams",robotParams)
    Visual.visual.__annotations__["robotParams"] = Robot.robotParams

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

    StepWithRobot = partial(Step,Robot,Visual.step)

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
