import matplotlib.pyplot as plt
from Visualization.Base.VisulationParams import VisulationParams
from typing import Callable

# {IdOrder:(function,kwargs)}
Functions :dict = {}

def VisualFunction(IdOrder):
    if(IdOrder <= 0): raise Exception("Invalid IdOrder must be positive int")
    def Function(func):
        def addFunc(**kwargs):
            return Functions.update({IdOrder:(func,kwargs)})
        return addFunc
    return Function


class Visualization:

    __functions = Functions

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
        
        # Turn on interactive mode
        plt.ion()
        
    def update(self):
        # Calling all the functions that need to re-draw in simulation
        for idOrder in range(1,len(Visualization.__functions.keys() + 1)):
            func, Kwargs = Visualization.__functions.get(idOrder)
            func(**Kwargs)
            plt.draw()
        plt.pause(self.step)

    # TODO: Need Implementation
    def _on_close(self,event):
        exit(1)