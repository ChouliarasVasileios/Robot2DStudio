from Robot2DStudio.Services.PrintMessage.Result import Result,ResultString
# --------------------------------------------------------------------------------------------------
from Robot2DStudio.Robot.Base.Robot import Robot
from Robot2DStudio.Robot.Base.RobotParams import RobotParams
from Robot2DStudio.Visualization.Base.Visualization import Visualization
# --------------------------------------------------------------------------------------------------
from Robot2DStudio.Robot.Models.DifferentialDriveRobotParams import DifferentialDriveRobotParams
from Robot2DStudio.Robot.Models.DifferentialDriveRobot import DifferentialDriveRobot
from Robot2DStudio.Visualization.Models.DifferentialDriveRobot import DiffrentialDriveRobotVisual
from Robot2DStudio.Robot.Models.PendulumParams import PendulumParams
from Robot2DStudio.Robot.Models.Pendulum import Pendulum
from Robot2DStudio.Visualization.Models.Pendulum import PendulumVisual
from Robot2DStudio.Robot.Models.DoublePendulumParams import DoublePendulumParams
from Robot2DStudio.Robot.Models.DoublePendulum import DoublePendulum
from Robot2DStudio.Visualization.Models.DoublePendulum import DoublePendulumVisual

def Mapper()->dict[RobotParams,Robot,Visualization]:
    """Contains the Model associate with the DTO and implementation"""
    return{
        "DifferentialDriveRobot":(DifferentialDriveRobotParams,DifferentialDriveRobot,DiffrentialDriveRobotVisual),
        "Pendulum": (PendulumParams,Pendulum,PendulumVisual),
        "DoublePendulum": (DoublePendulumParams,DoublePendulum,DoublePendulumVisual)
    }

def Dispose(MapperVar:dict):
    """Clear Memory of a Mapper Variable that created from Mapper Property"""

    print(ResultString("="*150))
    _ = 0
    for modelName, modelTypes in MapperVar.items():
        _+=1
        modelstr:str = ResultString(f"{_} - {modelName} :\n\t\t")
        print(modelstr + f"{modelTypes}\n")
    Result(f"Start Deleting Mapper size of: {MapperVar.__sizeof__()} bytes")
    MapperVar.clear()
    Result("Dipose the Mapper after initialization")
    print(ResultString("="*150))
