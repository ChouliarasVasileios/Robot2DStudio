from dataclasses import dataclass
import matplotlib.pyplot as plt
from matplotlib.pyplot import Axes

#TODO: INFO: Default arguments go at the end of dataclass
def axes():
    fig = plt.figure()
    return fig.add_subplot(111)

# Data Transfer Object for visualization
@dataclass
class VisulationParams:
    title :str # Title of matplot windown
    xlabel :str # Label of x ax
    ylabel :str # Label of y ax
    grid_on : bool # True to add grid on
    xlim :list[float] # List of 2 element, [min,max]
    ylim :list[float] # List of 2 element, [min,max]
    step :float # Simulation Step in sec e.g 0.05 sec
    _axes :Axes = axes()
