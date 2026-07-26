from Robot2DStudio.Simulation.AppStart.LocalModelsMapper.LocalModelMappper import Mapper
from Robot2DStudio.Services.Helpers.Helper import StringHelper
from enum import Enum
from dataclasses import dataclass
import sys
import os
import shutil
from importlib.resources import files

class ProjectType(Enum):
    Custom = 1,
    LocalModel = 2,
    OverrideLocalModel = 3

@dataclass
class ProjectInfos:
    Directory :str
    FileName :str

    ConfigurationDirectory :str
    ConfigurationFileName :str

@dataclass
class Project:
    ProjectName :str
    LocalModelName :str|None
    ProjectType :"ProjectType"
    Source : "ProjectInfos"
    Destination : "ProjectInfos"

def Read(path:str) -> str:
    strFile :str = ""
    with open(path,"r",encoding="utf-8") as file:
        strFile = file.read()
    return strFile

def ACCEPTED_COMMANDS() -> dict:
    return{
            "PROJECTNAME":"--newProject",
            "USEMODEL":"--useModel",
            "OVERRIDEMODEL":"--overrideModel"
        }

def _GetWorkingProjectDirectory(project: Project) -> str:
    return  os.path.join( os.getcwd(),project.ProjectName)

def _GetCustomTemplateDirectory() -> str:
    return str(files("Robot2DStudio").joinpath("Template/ProjectTemplates/Custom"))

def _GetLocalModelTemplateDirectory() -> str:
    return str(files("Robot2DStudio").joinpath("Template/ProjectTemplates/LocalModel"))

def _GetOverrideLocalModelTemplateDirectory() -> str:
    return str(files("Robot2DStudio").joinpath("Template/ProjectTemplates/OverrideLocalModel"))

def _GetConfigurationDirectory() -> str:
    return str(files("Robot2DStudio").joinpath("Template/ProjectTemplates/Models"))

def _GetOverrideModelImplementations(robotParamsFilename:str,robotFileName:str) -> tuple[str,str,str]:
    
    robotFileName = f"{robotFileName}.py"
    robotParamsFilename = f"{robotParamsFilename}.py"

    robotModelsDirectory = str(files("Robot2DStudio").joinpath("Robot/Models"))
    RobotVisualModelsDirectory = str(files("Robot2DStudio").joinpath("Visualization/Models"))

    try:
        robot = os.path.join(robotModelsDirectory,robotFileName)
        robotParams = os.path.join(robotModelsDirectory,robotParamsFilename)
        visualRobot = os.path.join(RobotVisualModelsDirectory,robotFileName)

        robotImplementation = Read(robot)



        robotParamsImplementation = Read(robotParams)
        visualRobotImplementation = Read(visualRobot)

        return (robotParamsImplementation,robotImplementation,visualRobotImplementation)

    except Exception as e:
        raise Exception(e)

def ParseArgs(*args):
    
    commands :dict = {}

    for i,arg in enumerate(args):
        if "--" not in arg:
            continue
        try:
            command = arg
            if(command not in ACCEPTED_COMMANDS().values()):
                print(f"Invalid command {command}")
                sys.exit(1)

            commandValue = args[i+1]

            if command == ACCEPTED_COMMANDS()["OVERRIDEMODEL"] and commandValue != None:
                print(f"Command {command} does not need value specification")
                sys.exit(1)

            commands.update({command:commandValue})
        except IndexError:
            if command == ACCEPTED_COMMANDS()["OVERRIDEMODEL"]:
                commands.update({command:True})
                continue

            print(f"Missing arg :{arg} value specification")
            sys.exit(1)

    return commands

def ValidateCommands(commands:dict) -> Project|None:

    if(commands == None):
        return None

    if len(commands.keys()) > len(ACCEPTED_COMMANDS()):
        return None
    
    PROJECTNAME = ACCEPTED_COMMANDS()["PROJECTNAME"]
    USEMODEL = ACCEPTED_COMMANDS()["USEMODEL"]
    OVERRIDEMODEL = ACCEPTED_COMMANDS()["OVERRIDEMODEL"]

    if (PROJECTNAME not in commands.keys()):
        return None
    
    if (PROJECTNAME in commands.keys()) and (USEMODEL not in commands.keys()) and (OVERRIDEMODEL in commands.keys()):
        print("Please specify the Model to override")
        return None

    if (PROJECTNAME in commands.keys()) and (USEMODEL not in commands.keys()) and (OVERRIDEMODEL not in commands.keys()):
        # Generate Only the Project
        # And Custom classes
        return Project(commands[PROJECTNAME],None,ProjectType.Custom,None,None)

    if (PROJECTNAME in commands.keys()) and (USEMODEL in commands.keys()) and (OVERRIDEMODEL not in commands.keys()):
        # Generate Only the Project for the local models
        # And copy the appsettings to override the default values
        return Project(commands[PROJECTNAME],commands[USEMODEL],ProjectType.LocalModel,None,None)
    
    if (PROJECTNAME in commands.keys()) and (USEMODEL in commands.keys()) and (OVERRIDEMODEL in commands.keys()):
        # Generate the Project for the local models
        # And copy the appsettings to override the default values or Add new Ones
        return Project(commands[PROJECTNAME],commands[USEMODEL],ProjectType.OverrideLocalModel,None,None)
     
    return None

def ValidateCommandsValues(commands:dict) -> dict|None:

    for command in commands:
        value :str = commands[command]

        if(isinstance(value,bool)):
            continue

        if((value == None) or (value.strip() == "")):
            print(f"Should provide a non empty value | {command}:{value}")
            return None

    return commands


def CopyProject(project:Project):
    # Create the Project Folder
    os.mkdir(os.path.join(project.Source.Directory,project.Destination.Directory))

    # Copy inside the Project Folder the .py file
    shutil.copy(os.path.join(project.Source.Directory,project.Source.FileName),
                os.path.join(project.Destination.Directory,project.Destination.FileName))

    # Create the Configuration Folder
    os.mkdir(os.path.join(project.Source.ConfigurationDirectory,project.Destination.ConfigurationDirectory))

    # Copy inside the ConfigurationFolder the .json file
    shutil.copy(os.path.join(project.Source.ConfigurationDirectory,project.Source.ConfigurationFileName),
                os.path.join(project.Destination.ConfigurationDirectory,project.Destination.ConfigurationFileName))
    
    return

def CreateCustomProject(project: Project) -> str:
    # TODO: Add Validations
    try:
       CopyProject(project)
    except Exception as e:
        # TODO: RollBack
        print(e)
        return "Failed to Create Custom Project"
    
    return "Created Custom Project"

def CreateLocalModelProject(project: Project) -> str:

    # TODO: Add Validations
    try:
        if(project.LocalModelName not in Mapper().keys()):
            raise Exception("Failed to map to a LocalModel")
        
        CopyProject(project)

        localModelPythonFile = os.path.join(project.Destination.Directory,project.Destination.FileName)

        strFile :str = ""
        with open(localModelPythonFile,"r",encoding="utf-8") as file:
            strFile = file.read(-1)

        strFile = strFile.replace("{{modelName}}",project.LocalModelName)

        with open(localModelPythonFile,"w",encoding="utf-8") as f:
            f.write(strFile)

    except Exception as e:
        print(e)
        # TODO: RollBack
        return "Failed to Create LocalModel Project"


    return "Created Local Model Project"

def CreateOverrideLocalModeProject(project:Project):
    
    # TODO: Add Validations
    try:
        if(project.LocalModelName not in Mapper().keys()):
            raise Exception("Failed to map to a LocalModel")
        
        CopyProject(project)
        localModelPythonFile = os.path.join(project.Destination.Directory,project.Destination.FileName)

        ImplementationDirectory = os.path.join(_GetWorkingProjectDirectory(project),"Implementations")
        TypesDirectory = os.path.join(_GetWorkingProjectDirectory(project),"Types")
        os.mkdir(ImplementationDirectory)
        os.mkdir(TypesDirectory)

        strFile :str = ""
        with open(localModelPythonFile,"r",encoding="utf-8") as file:
            strFile = file.read(-1)

        (RobotParams,Robot,VisualRobot) = Mapper()[project.LocalModelName]
        strFile = strFile.replace("{{localModelRobotParams}}",str(RobotParams.__name__))
        strFile = strFile.replace("{{localModelRobot}}",str(Robot.__name__))
        strFile = strFile.replace("{{localModelVisualRobot}}",str(VisualRobot.__name__))

        (robotParamsImplementation,RobotImplementation,VisualRobotImplementation) = _GetOverrideModelImplementations(str(RobotParams.__name__),str(Robot.__name__))
        
        with open(os.path.join(TypesDirectory,f"{str(RobotParams.__name__)}.py"),"w",encoding="utf-8") as f:
            f.write(robotParamsImplementation)

        with open(os.path.join(ImplementationDirectory,f"{str(Robot.__name__)}.py"),"w",encoding="utf-8") as f:
            f.write(RobotImplementation)

        with open(os.path.join(ImplementationDirectory,f"{str(VisualRobot.__name__)}.py"),"w",encoding="utf-8") as f:
            f.write(VisualRobotImplementation)

        with open(localModelPythonFile,"w",encoding="utf-8") as f:
            f.write(strFile)

    except Exception as e:
        print(e)
        # TODO: RollBack
        return "Failed to Override Local Model Project"
    return "Created Override Local Model Project"


def CreateProject(project :Project) -> str:

    if project == None:
        return f"Could Not Create the Project {project}"
    
    if project.ProjectType == ProjectType.Custom:

        project.Source = ProjectInfos(
            Directory = _GetCustomTemplateDirectory(),
            FileName = "YourRobot.py",

            ConfigurationDirectory = _GetConfigurationDirectory(),
            ConfigurationFileName = "YourRobot.json"
        )

        project.Destination = ProjectInfos(
            Directory = _GetWorkingProjectDirectory(project),
            FileName = "YourRobot.py",

            ConfigurationDirectory = os.path.join(_GetWorkingProjectDirectory(project),"Configuration"),
            ConfigurationFileName = "YourRobot.json"
        )

        return CreateCustomProject(project)
    
    elif project.ProjectType == ProjectType.LocalModel:

        project.Source = ProjectInfos(
            Directory = _GetLocalModelTemplateDirectory(),
            FileName = "LocalModel.py",

            ConfigurationDirectory = _GetConfigurationDirectory(),
            ConfigurationFileName = f"{project.LocalModelName.strip()}.json"
        )

        project.Destination = ProjectInfos(
            Directory = _GetWorkingProjectDirectory(project),
            FileName = f"{project.LocalModelName.strip()}.py",

            ConfigurationDirectory = os.path.join(_GetWorkingProjectDirectory(project),"Configuration"),
            ConfigurationFileName = f"{project.LocalModelName.strip()}.json"
        )

        return CreateLocalModelProject(project)
    
    elif project.ProjectType == ProjectType.OverrideLocalModel:
        project.Source = ProjectInfos(
            Directory = _GetOverrideLocalModelTemplateDirectory(),
            FileName = "OverrideLocalModel.txt",

            ConfigurationDirectory = _GetConfigurationDirectory(),
            ConfigurationFileName = f"{project.LocalModelName.strip()}.json"
        )

        project.Destination = ProjectInfos(
            Directory = _GetWorkingProjectDirectory(project),
            FileName = f"{project.LocalModelName.strip()}.py",

            ConfigurationDirectory = os.path.join(_GetWorkingProjectDirectory(project),"Configuration"),
            ConfigurationFileName = f"{project.LocalModelName.strip()}.json"
        )
        return CreateOverrideLocalModeProject(project)

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
#     CLI()