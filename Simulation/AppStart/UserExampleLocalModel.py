from Simulation.AppStart.SimulationMain import Robot2DStudioLocalModelStart
import numpy as np
from Simulation.utils.integrators import Integrator

def SimulationInit():
    x_target = np.array([[0.0,0.0]]).T
    x = np.array([[0.,0.]]).T
    u = np.array([[190.]])
    error = np.ones_like(x)
    return {"x":x,"u":u,"x_target":x_target,"error":error}


def SimulationStep(robot,step,x,u,x_target,error,stop) -> bool:

    x = Integrator.RK4(x,u,robot.Dynamics,step)

    u = np.zeros_like(u)
    error = x - x_target

    # if np.linalg.norm(error) < 10e-1:
    #     stop = True

    return {"x":x,"u":u,"x_target":x_target,"error":error,"stop":stop}




Robot2DStudioLocalModelStart(ModelName="Pendulum",
                             Overrride=False,
                             SimulationInit = SimulationInit,
                             SimulationStep = SimulationStep)