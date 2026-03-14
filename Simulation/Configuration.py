import json
# import copy for deepcopy but propably will not needed ! 
from typing import Generic,Type, TypeVar
from Services.PrintMessage.Warning import Warning
# from Robot.RobotParams import DiffDriveParams

T = TypeVar("T")

def read() -> dict:
    with open("Simulation\\Configuration\\appsetting.json","r") as f:
        data = json.load(f)
        return data
    
class Configure(Generic[T]):

    __data :dict = read()
    
    #TODO: Make it dynamic not for just the level0
    # Now it works for Vis.Patches (jsonPath)
    @classmethod
    def Get(cls :"Configure",section_type: Type[T]) -> Generic[T]:

        params :dict = cls.__data.get(section_type.__name__,None) # Json -> Dictionary

        paramsKeys = params.keys() # All the Properties of Json file - appsettings.json
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


# def main():
#     obj = Configure.Get(DiffDriveParams)
#     print(obj.s)

# main()