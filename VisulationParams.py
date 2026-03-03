import dataclasses
import matplotlib.pyplot as plt
from matplotlib.pyplot import Axes

@dataclasses
class VisulationParams:
    axes :Axes = lambda fig = plt.figure() : fig.add_subplot(111)
    title :str # Title of matplot windown
    xlabel :str # Label of x ax
    ylabel :str # Label of y ax
    grid_on : bool # True to add grid on
    xlim :list[float] # List of 2 element, [min,max]
    ylim :list[float] # List of 2 element, [min,max]