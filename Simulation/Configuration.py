import json
from pathlib import Path
# import copy for deepcopy but propably will not needed ! 
from typing import Generic,Type, TypeVar
from Services.PrintMessage.Warning import Warning

T = TypeVar("T")
    
class Configure(Generic[T]):


    __localModelsDirectory :Path = Path("Robot\\Models")
    
    #TODO: Make it dynamic not for just the level1
    # Now it works for Vis.Patches (jsonPath)
    @classmethod
    def Get(cls :"Configure",section_type: Type[T]) -> Generic[T]:

        filename = Configure.__IsLocalModel(section_type.__name__)

        data :dict = Configure.__read(filename,filename == None)

        params :dict = data.get(section_type.__name__,None)

        paramsKeys = params.keys() # All the Properties of Json file - filename.json
        if(Configure.__IsFlatObject(params)):
            return section_type(**params)

        # Used for not-flat json formating - Works for one level of encapsulatio 
        # propName : [ {parametersOfCustomObject}, {parametersOfCustomObject}, {parametersOfCustomObject}]
        for param in paramsKeys:
            
            # Json Attributes
            paramName = param # Property Name
            paramValue = params[param] # Property Value

            # Checks if a value is list and contains dictionary
            if isinstance(paramValue,list) and Configure.__IsNameLessObject(paramValue):

                # Matching the jsonProperty that contains a list of dictionaries
                # to the associated property of DTO - Data Transfer Object
                ListNameLessObject = section_type.__annotations__[paramName]

                # Get the DTOs that encapsulate the list
                NameLessObjects = ListNameLessObject.__args__
                
                # Just one DTOs
                if len(NameLessObjects) != 1: Warning(f"Could not parse multiple namelessObjects e.g\nDO : list[MyObj]\nDO_NOT : list[MyObj1,MyObj2] Total NameLessObjects = {len(NameLessObjects)}")
                NameLessObject = NameLessObjects[0]

                # Generate the DTOs and replace the old json property value with the generated DTOs
                # each dictionary inside the list is a mapped DTO now
                GeneratedDtos = [NameLessObject(**NameLessObjectParams) for NameLessObjectParams in paramValue]
                # print(f"DTO Type{type(GeneratedDtos[0])}")
                # IDEA: Replace the old Patches with the new one!!!
                params.update({paramName:GeneratedDtos})

        return section_type(**params)

    @staticmethod
    def __IsNameLessObject(lst :list) -> bool:
        isTrueCount :int = 0
        for item in lst:
            if isinstance(item,dict):
                isTrueCount+=1
        return isTrueCount == len(lst)
    
    @staticmethod
    def __IsFlatObject(dictionary :dict) -> bool:
        for item in dictionary.keys():
            if isinstance(dictionary[item],list) and Configure.__IsNameLessObject(dictionary[item]):
                return False
        return True
    @staticmethod
    def __read(filename :str,default: bool) -> dict:
        if default:
            with open("Simulation\\Configuration\\appsetting.json","r") as f:
                data = json.load(f)
            return data
            
        with open(f"Simulation\\Configuration\\Models\\{filename}","r") as f:
            data = json.load(f)
        return data
    
    @classmethod
    def __IsLocalModel(self,sectionTypeName :str) -> str|None:
        for file in Configure.__localModelsDirectory.iterdir():
            if(file.is_file() and ".py" in file.name and file.name.replace(".py","") == sectionTypeName):
                return self.toCamelCase(sectionTypeName.replace("Params","")) + ".json"
        return None
    
    def toCamelCase(string :str) -> str:
        string = string[0].lower() + string[1:]
        return string
