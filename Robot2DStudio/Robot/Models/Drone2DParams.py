from dataclasses import dataclass
from Robot2DStudio.Robot.Base.RobotParams import RobotParams

@dataclass
class Drone2DParams(RobotParams):
    l :float # Lenght of the Drone
    m1 :float # right mass
    m2 :float # left mass
    g :float # Gravity acceleration
    rho :float # Air density
    cd :float # Drag coefficient
    Ay :float # Top area space
    Ax :float # Side area space
    