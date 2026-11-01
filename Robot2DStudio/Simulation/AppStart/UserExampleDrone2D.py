from Robot2DStudio.Simulation.AppStart.SimulationMain import Robot2DStudioStart,RobotStudio,VisualStudio
import numpy as np
import matplotlib.pyplot as plt

from Robot2DStudio.Simulation.utils.integrators import Integrator

from Robot2DStudio.Robot.Models.Drone2DParams import Drone2DParams
from Robot2DStudio.Robot.Models.Drone2D import Drone2D

from Robot2DStudio.Visualization.Base.VisualationParams import VisualationParams
from Robot2DStudio.Visualization.Models.Drone2D import Drone2DVisual

# Each rotor carries half of the weight, m*g/2 with the values of the .json file
HOVER = np.array([[1.962,1.962]]).T

# Forces added to [F1,F2].T -> Forces of the rotors (right and left)
ARROWS = {
    "up": np.array([[1.0,1.0]]).T, # Both rotors push harder so the drone climbs
    "down": np.array([[-1.0,-1.0]]).T, # Both rotors push less so the drone descends
    "left": np.array([[0.2,-0.2]]).T, # Right rotor pushes harder so the drone tilts to the left
    "right": np.array([[-0.2,0.2]]).T # Left rotor pushes harder so the drone tilts to the right
}

# The arrows that are held down right now
pressedKeys :set = set()

def OnKeyPress(event):
    pressedKeys.add(event.key)

def OnKeyRelease(event):
    pressedKeys.discard(event.key)

def SimulationInit():
    # Free the left and right arrows from the default shortcuts of matplotlib
    for keymap in ("keymap.back","keymap.forward"):
        plt.rcParams[keymap] = [key for key in plt.rcParams[keymap] if key not in ("left","right")]

    canvas = VisualationParams._axes.figure.canvas
    canvas.mpl_connect("key_press_event",OnKeyPress)
    canvas.mpl_connect("key_release_event",OnKeyRelease)

    x_target = np.array([[0.,0.,0.,0.,0.,0.]]).T
    x = np.array([[0.,0.,0.,0.,0.,0.]]).T
    u = HOVER
    error = np.ones_like(x)
    return {"x":x,"u":u,"x_target":x_target,"error":error}


def SimulationStep(robot,step,x,u,x_target,error,stop) -> bool:

    u = HOVER
    for key,force in ARROWS.items():
        if key in pressedKeys:
            u = u + force

    x = Integrator.RK4(x,u,robot.Dynamics,step)

    error = x - x_target

    return {"x":x,"u":u,"x_target":x_target,"error":error,"stop":stop}


Robot2DStudioStart(Robot = RobotStudio(Drone2DParams,Drone2D),
                    Visual = VisualStudio(VisualationParams,Drone2DVisual),
                    SimulationInit = SimulationInit,
                    SimulationStep = SimulationStep)
