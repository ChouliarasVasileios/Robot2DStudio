from dataclasses import dataclass
from Robot.Base.RobotParams import RobotParams

# Data Transfer Object for robot modeling
@dataclass
class PendulumParams(RobotParams):
    l : float  # The Length of pendulum
    m : float  # Mass of pendulum
    g : float  # Gravity acceleration 
    b : float  # Air resistant coefficient 
