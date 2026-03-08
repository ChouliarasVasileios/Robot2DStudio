import matplotlib.pyplot as plt
from Visualization.Base.VisulationParams import VisulationParams

class Visualization:

    def __init__(self,visulationParams:VisulationParams):
        
        # Set the axes
        self.axes = visulationParams._axes

        # Adding a title at plot
        self.axes.set_title(visulationParams.title)
        
        # Adding x label at plot
        self.axes.set_xlabel(visulationParams.xlabel)
        
        # Adding y label at plot
        self.axes.set_ylabel(visulationParams.ylabel)
        
        # Adding grid at plot
        self.axes.grid(visulationParams.grid_on)
        
        # Adding x axes limits
        self.axes.set_xlim(visulationParams.xlim)
        
        # Adding y axes limit
        self.axes.set_ylim(visulationParams.ylim)

        self.step = visulationParams.step

        # Internal Variables
        self.Patches :dict = {} #Key : functionName - Value : patch if have 
        
        # Turn on interactive mode
        plt.ion()
        
    def render(self):
        self.update()
        plt.draw()
        plt.pause(self.step)

    # TODO: Need Implementation
    def _on_close(self,event):
        exit(1)

    def update(self):
        # Calling all the functions that need to re-draw in simulation
        raise Exception("Need Implementation")