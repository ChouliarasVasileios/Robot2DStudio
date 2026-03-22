# Robot2DStudio/CLI.py
from Robot2DStudio.Simulation.AppStart.LocalModelsMapper.LocalModelMappper import Mapper
from enum import Enum
from dataclasses import dataclass
import sys

class ProjectType(Enum):
    Custom = 1,
    LocalModel = 2,
    OverrideLocalModel = 3

@dataclass
class Project:
    ProjectName :str
    LocalModelName :str|None
    ProjectType :"ProjectType"


TOTAL_COMMANDS :int = 3
PROJECTNAME :str = "--newProject"
USEMODEL :str = "--useModel"
OVERRIDEMODEL :str = "--overrideModel"

ACCEPTED_COMMANDS :list[str] = [PROJECTNAME,USEMODEL,OVERRIDEMODEL]

def ParseArgs(*args):
    
    commands :dict = {}

    for i,arg in enumerate(args):
        if "--" not in arg:
            continue
        try:
            command = arg
            if(command not in ACCEPTED_COMMANDS):
                print(f"Invalid command {command}")
                sys.exit(1)

            commandValue = args[i+1]

            if command == OVERRIDEMODEL and commandValue != None:
                print(f"Command {command} does not need value specification")
                sys.exit(1)

            commands.update({command:commandValue})
        except IndexError:
            if command == OVERRIDEMODEL:
                commands.update({command:True})
                continue

            print(f"Missing arg :{arg} value specification")
            sys.exit(1)

    return commands

def ValidateCommands(commands:dict) -> Project|None:
    if len(commands.keys()) > TOTAL_COMMANDS:
        return None
    
    if (PROJECTNAME not in commands.keys()):
        return None
    
    if (PROJECTNAME in commands.keys()) and (USEMODEL not in commands.keys()) and (OVERRIDEMODEL in commands.keys()):
        print("Please specify the Model to override")
        return None

    if (PROJECTNAME in commands.keys()) and (USEMODEL not in commands.keys()) and (OVERRIDEMODEL not in commands.keys()):
        # Generate Only the Project
        # And Custom classes
        return Project(commands[PROJECTNAME],None,ProjectType.Custom)

    if (PROJECTNAME in commands.keys()) and (USEMODEL in commands.keys()) and (OVERRIDEMODEL not in commands.keys()):
        # Generate Only the Project for the local models
        return Project(commands[PROJECTNAME],commands[USEMODEL],ProjectType.LocalModel)

    
    if (PROJECTNAME in commands.keys()) and (USEMODEL in commands.keys()) and (OVERRIDEMODEL in commands.keys()):
        # Generate the Project for the local models
        # And copy the appsettings to override the default values
        return Project(commands[PROJECTNAME],commands[USEMODEL],ProjectType.OverrideLocalModel)
     
    return None

def __CreateCustomProject():return "Create Custom Project"

def __CreateLocalModelProject():return "Create Local Model Project"

#TODO Need Implementation
def __CreateOverrideLocalModeProject():return "Create Override Local Model Project"


def CreateProject(project :Project) -> str:
    
    if project.ProjectType == ProjectType.Custom:
        return __CreateCustomProject()
    
    elif project.ProjectType == ProjectType.LocalModel:
        return __CreateLocalModelProject()
    
    elif project.ProjectType == ProjectType.OverrideLocalModel:
        return __CreateOverrideLocalModeProject()

    else:
        return f"Could Not Create the Project {project}"


def LogMsg(msg :str):
    print(msg)

if __name__ == "__main__":
    LogMsg(
        CreateProject(
            ValidateCommands(
                ParseArgs(*sys.argv[1:])
                )
            )
        )