from dataclasses import dataclass
from Robot.Base.RobotParams import RobotParams


@dataclass
class DoublePendulumParams(RobotParams):
    m1 :float # Mass of the first joint
    l1 :float # Length of the first link
    m2 :float # Mass of the second joint
    l2 :float # Lenght of the seconf link
    g  :float  # Gravity acceleration
