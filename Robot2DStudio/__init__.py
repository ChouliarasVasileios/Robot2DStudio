# --- Robot2DStudio Function when built in model is used --- 
from Robot2DStudio.Simulation.AppStart.SimulationMain import Robot2DStudioLocalModelStart
# --------------------------------------------------------------------------

# -- Robot2DStudio built in class to use built in integrators ---
from Robot2DStudio.Simulation.utils.integrators import Integrator
# --------------------------------------------------------------------------

# --- Robot2DStudio Functions|DTOs when custom implementation is needed ---
from Robot2DStudio.Simulation.AppStart.SimulationMain import Robot2DStudioStart,RobotStudio,VisualStudio
from Robot2DStudio.Robot.Base.Robot import Robot
from Robot2DStudio.Robot.Base.RobotParams import RobotParams
from Robot2DStudio.Visualization.Base.Visualization import Visualization
from Robot2DStudio.Visualization.Base.VisualationParams import VisualationParams
# --------------------------------------------------------------------------

# --- Robot2DStudio built in models|DTOs ---
# --- Robot2DStudio built in visualization Models | DTOS ---
from Robot2DStudio.Simulation.AppStart.LocalModelsMapper.LocalModelsImport import *
# --------------------------------------------------------------------------


# Here the user can do the following
# import Robot2DStudio 
# Robot2DStudio.hello() and call it
def hello():
    print("Hello message from Robot2DStudio.\n Your installation seems to be succesful :D")