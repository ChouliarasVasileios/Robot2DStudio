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
import matplotlib
import matplotlib.pyplot as plt

@dataclass
class RobotStudio:
    robotParams :RobotParams
    robot : Robot

@dataclass
class VisualStudio:
    visualParams : VisualationParams
    visual :Visualization


def __addAttribute(ClassType :object,AttributeType:object,InstanceObject :object, AttributeName :str, AttributeValue:Any):
        """ Initialize a new attribute for a class at run time"""

        # Create and set value to the new attribute
        setattr(InstanceObject,AttributeName,AttributeValue)

        # Set the type of the attribute
        ClassType.__annotations__[AttributeName] = AttributeType

def __GetLocalModelTypes(ModelName:str)->dict:
    
    # Return the Mapped Models to a Disposable variable to Free up memory
    mapper = Mapper()

    # Get the Types associated with the ModelName
    RobotParams,Robot,RobotVisual = mapper[ModelName]

    # Dispose the local Mapped Variable
    Dispose(mapper)

    return {
        "RobotParams": RobotParams,
        "Robot": Robot,
        "RobotVisual": RobotVisual
    }


def SetUp(Robot :RobotStudio,Visual:VisualStudio):
    """ Load the Robot and Visualization objects and add the robotParams attribute to Visualization.
        Used for custom Implementaion"""
    robotParams = Configure.Get(Robot.robotParams)
    robot = Robot.robot(robotParams)

    visual = Visual.visual(Configure.Get(Visual.visualParams))

    # Create an attribute self.robotParams = robotParamsDTOInstance
    __addAttribute(ClassType=Visual.visual,
                   AttributeType=Robot.robotParams,
                   InstanceObject=visual,
                   AttributeName="robotParams",
                   AttributeValue= robotParams
                   )
    

    return {
        "Robot" : robot,
        "Visual" : visual,
    }

def SetUpLocalMode(ModelName :str,Override:bool):
    """ Load the Robot and Visualization objects add the robotParms attribute to Visualization
        Used for existing Implementation """

    RobotParams,Robot,RobotVisual = __GetLocalModelTypes(ModelName).values()

    # Load from <<modelName>>.json the params of Robot 
    # and return the associate DTO
    robotParams = Configure.Get(section_type=RobotParams,
                                modelName=ModelName,
                                overrideModel=Override)

    # Create instance of the Robot associated with the provides ModelName
    robot = Robot(robotParams)
    
    # Load form <<modelName>>.json the params of Visualization
    # and return the associated DTO
    visual = RobotVisual(Configure.Get(section_type=VisualationParams,
                                modelName=ModelName,
                                overrideModel=Override))

    # Create an attribute self.robotParams = robotParamsDTOInstance
    __addAttribute(ClassType=Visualization,
                   AttributeType=RobotParams,
                   InstanceObject=visual,
                   AttributeName="robotParams",
                   AttributeValue= robotParams
                   )

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

    print("Simulation End")
    plt.ioff()
    plt.show()
    print("Exiting Robot2DStudio Bye! :)")
    sys.exit(0)
    

def Robot2DStudioStart(Robot :RobotStudio,
                       Visual :VisualStudio,
                       SimulationInit :Callable[[None],Any],
                       SimulationStep :Callable[[Any],Any]):
    
    matplotlib.use(backend="TkAgg")
    Loop(**SetUp(Robot,Visual),Init=SimulationInit,Step=SimulationStep)


def Robot2DStudioLocalModelStart(ModelName :str,
                                 Overrride :bool,
                                 SimulationInit :Callable[[None],Any],
                                 SimulationStep :Callable[[Any],Any]):
    matplotlib.use(backend="TkAgg")
    Loop(**SetUpLocalMode(ModelName=ModelName,Override=Overrride),Init=SimulationInit,Step=SimulationStep)
