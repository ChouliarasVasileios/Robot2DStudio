import keyboard
from Simulation.Configuration import Configure
from Robot.RobotParams import DiffDriveParams
from Visualization.VisulationParams import VisulationParams
from Robot.modeling import Differential_Drive
from Visualization.visulization import Visualization
from Simulation.utils.integrators import Integrator
import numpy as np
import matplotlib.patches as patches

# diffDriveParams  :DiffDriveParams
# visulationParams :VisulationParams

DDR : Differential_Drive
visual : Visualization

def Init():
    # global diffDriveParams 
    # global visulationParams

    # Loading the parameters to Data transfer objects
    diffDriveParams = Configure.Get(DiffDriveParams)
    visulationParams = Configure.Get(VisulationParams)

    global DDR
    global visual

    DDR = Differential_Drive(diffDriveParams)
    visual = Visualization(VisulationParams)



def Loop():

    x_start = np.array([[0.,0.,0.]]).T
    u_start = np.array([[0.,0.]]).T

    rect = patches.Rectangle((0.0,0.0),0.6,0.3,linewidth = 0.5,edgecolor = 'blue',facecolor ='blue')

    # print(np.shape(x_start))
    # print(np.shape(u_start))
    # print(np.shape(DDR.jacobian(x_start)@u_start))

    # exit(1)

    x = np.copy(x_start)
    u = np.copy(u_start)
    while True:

        if keyboard.is_pressed("w"):
            u = u + np.array([[0.5,0.5]]).T

        if keyboard.is_pressed("a"):
            u = u + np.array([[-0.3,+0.3]]).T

        if keyboard.is_pressed("d"):
            u = u + np.array([[0.3,-0.3]]).T
            
        if keyboard.is_pressed("s"):
            u = u + np.array([[-0.5,-0.5]]).T

        x = Integrator.ForwardEuler(x,u,DDR.diff_kinematics,0.05)
        u = np.zeros_like(u)
        print(x)

        functions = [
            (visual.move_rectangle,(rect,x[0,0],x[1,0]))
        ]

        visual.update(functions)


def main():
    Init()
    Loop()

    # print(diffDriveParams)
    # print(visulationParams)
    

if __name__ == "__main__":
    main()