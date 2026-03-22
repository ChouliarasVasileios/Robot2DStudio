from dataclasses import dataclass

# Data Transfer Object for robot modeling
@dataclass
class RobotParams:
    Name : str # Robot Name
    N : int  # State Dimension
    M : int  # Action Dimension

