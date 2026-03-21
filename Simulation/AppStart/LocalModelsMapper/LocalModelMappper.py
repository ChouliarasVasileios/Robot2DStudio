from Services.PrintMessage.Result import Result
# --------------------------------------------------------------------------------------------------
from Robot.Base.Robot import Robot
from Robot.Base.RobotParams import RobotParams
# --------------------------------------------------------------------------------------------------
from Robot.Models.DifferentialDriveRobotParams import DifferentialDriveRobotParams
from Robot.Models.DifferentialDriveRobot import DifferentialDriveRobot
from Visualization.Models.DifferentialDriveRobot import DiffrentialDriveRobotVisual
from Robot.Models.PendulumParams import PendulumParams
from Robot.Models.Pendulum import Pendulum
from Visualization.Models.Pendulum import PendulumVisual

def Mapper()->dict[RobotParams,Robot]:
    """Contains the Model associate with the DTO and implementaion"""
    return{
        "DifferentialDriveRobot":(DifferentialDriveRobotParams,DifferentialDriveRobot,DiffrentialDriveRobotVisual),
        "Pendulum": (PendulumParams,Pendulum,PendulumVisual)
    }

def Dispose(MapperVar:dict):
    """Clear Memory of a Mapper Variable that created from Mapper Property"""
    Result(f"Start Deleting Mapper {MapperVar} size of: {MapperVar.__sizeof__()}")
    MapperVar.clear()
    Result("Dipose the Mapper after initialization")