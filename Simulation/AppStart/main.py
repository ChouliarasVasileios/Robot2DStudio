import sys
from typing import Callable,Any
from dataclasses import dataclass
from functools import partial
from Simulation.AppStart.LocalModelsMapper.LocalModelMappper import Mapper,Dispose
from Simulation.Configuration import Configure
from Robot.Base.Robot import Robot
from Robot.Base.RobotParams import RobotParams
from Visualization.Base.Visualization import Visualization
from Visualization.Base.VisualationParams import VisualationParams

@dataclass
class RobotStudio:
    robotParams :RobotParams
    robot : Robot

@dataclass
class VisualStudio:
    visualParams : VisualationParams
    visual :Visualization


def SetUp(Robot :RobotStudio,Visual:VisualStudio):
    robotParams = Configure.Get(Robot.robotParams)
    robot = Robot.robot(robotParams)

    visual = Visual.visual(Configure.Get(Visual.visualParams))
    
    setattr(visual,"robotParams",robotParams)
    Visual.visual.__annotations__["robotParams"] = Robot.robotParams

    return {
        "Robot" : robot,
        "Visual" : visual,
    }

def SetUpLocalMode(ModelName :str,Override:bool):

    mapper = Mapper()

    RobotParams,Robot,RobotVisual = mapper[ModelName]
    Dispose(mapper)

    robotParams = Configure.Get(section_type=RobotParams,
                                modelName=ModelName,
                                overrideModel=Override)

    robot = Robot(robotParams)
    
    visual = RobotVisual(Configure.Get(section_type=VisualationParams,
                                modelName=ModelName,
                                overrideModel=Override))

    setattr(visual,"robotParams",robotParams)
    Visualization.__annotations__["robotParams"] = RobotParams

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


def Robot2DStudioLocalModelStart(ModelName :str,
                                 Overrride :bool,
                                 SimulationInit :Callable[[None],Any],
                                 SimulationStep :Callable[[Any],Any]):


     Loop(**SetUpLocalMode(ModelName=ModelName,Override=Overrride),Init=SimulationInit,Step=SimulationStep)
    