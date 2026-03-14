import sys
import matplotlib.pyplot as plt
from numpy import ndarray
from Visualization.Base.VisulationParams import VisulationParams,PatchParams
from matplotlib.patches import Patch
from Services.PrintMessage.Warning import Warning
from typing import Callable

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
        self.__PatchesParams :list[PatchParams] = visulationParams.Patches

        self.__Patches :list[tuple[str,Patch]] = self.__SetPatches()
        
        # Turn on interactive mode
        plt.ion()
        
    def render(self,x :ndarray):
        self.update(x)
        plt.draw()
        plt.pause(self.step)
    
    def InitRender(self):
        # Add close event to stop the Studio
        self.axes.figure.canvas.mpl_connect("close_event",self._on_close)
        self.addPatchesToVisualization()

    def addPatchesToVisualization(self):
        for name,patch in self.__Patches:
            self.axes.add_patch(patch)
            print(f"Patch: {patch} with name: {name} added to visualization")

    
    def __SetPatches(self) -> list[tuple[str,Patch]]:
        PatchSettings :list[tuple[str,dict]] = [(patchParams.patch,patchParams.arguments) for patchParams in self.__PatchesParams]
        return self.__ConfigurePatch(PatchSettings)

    def __ConfigurePatch(self,PatchSettings:list[tuple[str,dict]]) -> list[tuple[str,Patch]]:
        patchesToUse :list[tuple[str,Patch]] = []
        patchesClasses :dict[str,Patch]= {cls.__name__ : cls for cls in Patch.__subclasses__()}

        for patchName,args in PatchSettings:
            if not patchName in patchesClasses.keys():
                Warning(msg = f"Could not found patch {patchName}")
            else:
                patchesToUse.append((patchName,patchesClasses[patchName](**args)))
        return patchesToUse
    
    def GetPatch(self, patchName :str) -> Patch:
        for PatchName,PatchClass in self.__Patches:
            if(PatchName == patchName):
                return PatchClass
            Warning(msg = f"Could Not Find patch with PatchName {patchName}")

    def GetPatches(self, appliedFunction : Callable) -> list[Patch]:
        pass # TODO: make it return a list of patches that applied to a specific function

    def _on_close(self,event):
        print("Exiting Robot2DStudio Bye! :)")
        sys.exit(0)

    def update(self,x :ndarray):
        # Calling all the functions that need to re-draw in simulation
        raise Exception("Need Implementation")