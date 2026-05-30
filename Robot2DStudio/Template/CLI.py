from Robot2DStudio.Simulation.AppStart.LocalModelsMapper.LocalModelMappper import Mapper
from enum import Enum
from dataclasses import dataclass
import sys
import os
import shutil
from importlib.resources import files

CustomTemplateDirectory:str = str(files("Robot2DStudio").joinpath("Template/ProjectTemplates/Custom"))
LocalModelTemplateDirectory:str = str(files("Robot2DStudio").joinpath("Template/ProjectTemplates/LocalModel"))

# OverrideLocalModelTemplateDirectory

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

    if(commands == None):
        return None

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

def ValidateCommandsValues(commands:dict) -> dict|None:

    for command in commands:
        value :str = commands[command]

        if((value == None) or (value.strip() == "")):
            print(f"Should provide a non empty value | {command}:{value}")
            return None

    return commands


def __CreateCustomProject(project: Project) -> str:
    
    currentWorkingDirectory :str = os.getcwd()
    workingProjectDirectory :str = os.path.join(currentWorkingDirectory,project.ProjectName)
    try:
        shutil.copytree(CustomTemplateDirectory,workingProjectDirectory,dirs_exist_ok=True)
        os.rename(os.path.join(workingProjectDirectory,"Custom.py"),os.path.join(workingProjectDirectory,"".join([project.ProjectName,".py"])))
    except:
        # TODO: RollBack
        return "Failed to Create Custom Project"
    
    return "Created Custom Project"

def __CreateLocalModelProject(project: Project) -> str:
    
    currentWorkingDirectory :str = os.getcwd()
    workingProjectDirectory :str = os.path.join(currentWorkingDirectory,project.ProjectName)

    try:
     
        shutil.copytree(LocalModelTemplateDirectory,workingProjectDirectory,dirs_exist_ok=True)
     
        localModelPythonFile :str = os.path.join(workingProjectDirectory,"".join([project.LocalModelName,".py"]))

        print(localModelPythonFile)
        os.rename(os.path.join(workingProjectDirectory,str("LocalModel.py")),localModelPythonFile)

        strFile :str = ""
        with open(localModelPythonFile,"r",encoding="utf-8") as file:
            strFile = file.read(-1)


        print(strFile.find("{{modelName}}"))
        
        for index in range(len(strFile)):
            if(index >= 728 and index < len("ModelName")):
                strFile[index] = "|"

        print(project.LocalModelName)

        with open(os.path.join(workingProjectDirectory,"".join(["replaced",".py"])),"w",encoding="utf-8") as f:
            f.write("here")

    except Exception as e:
        print(e)
        # TODO: RollBack
        return "Failed to Create LocalModel Project"


    return "Created Local Model Project"

#TODO Need Implementation
def __CreateOverrideLocalModeProject():return "Created Override Local Model Project"


def CreateProject(project :Project) -> str:

    if project == None:
        return f"Could Not Create the Project {project}"
    
    if project.ProjectType == ProjectType.Custom:
        return __CreateCustomProject(project=project)
    
    elif project.ProjectType == ProjectType.LocalModel:
        return __CreateLocalModelProject(project=project)
    
    elif project.ProjectType == ProjectType.OverrideLocalModel:
        return __CreateOverrideLocalModeProject()

    else:
        return f"Could Not Create the Project {project}"


def LogMsg(msg :str):
    print(msg)

def CLI():
    LogMsg(
        CreateProject(
            ValidateCommands(
                ValidateCommandsValues(
                    ParseArgs(*sys.argv[1:])
                    )
                )
            )
        )
    
# if __name__ == "__main__":
#     LogMsg(
#         CreateProject(
#             ValidateCommands(
#                 ParseArgs(*sys.argv[1:])
#                 )
#             )
#         )