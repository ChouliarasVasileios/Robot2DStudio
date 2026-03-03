import dataclasses

@dataclasses
class DiffDriveParams:
    Name : str = "Differential Drive Robot"
    N : int # State Dimension
    M : int # Action Dimension
    s : float # Distance between the center of L wheel to the center of R wheel
    r : float # Radius of the wheels 
