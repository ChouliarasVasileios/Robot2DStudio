from dataclasses import dataclass
from Robot.Base.RobotParams import RobotParams

# Data Transfer Object for robot modeling
@dataclass
class DiffDriveParams(RobotParams):
    # Name : str # Robot Name
    # N : int  # State Dimension
    # M : int  # Action Dimension
    s : float # Distance between the center of L wheel to the center of R wheel
    r : float  # Radius of the wheels 
