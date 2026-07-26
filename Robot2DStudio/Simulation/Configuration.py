import json
from typing import Generic,Type, TypeVar
from Robot2DStudio.Services.PrintMessage.Warning import Warning

T = TypeVar("T")
    
class Configure(Generic[T]):

    #TODO: Make it dynamic not for just the level1
    # Now it works for Vis.Patches (jsonPath)
    @classmethod
    def Get(cls :"Configure",section_type: Type[T],filePath :str) -> Generic[T]:

        #TODO: Implement The Load a Local Model that user Need to override its Parameters
        data :dict = Configure.__read(filePath)

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
    def __read(filePath :str | None) -> dict:
        data = None
        try :
            with open(filePath,"r",encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception as e:
                raise Exception(e) #TODO: Check logic
        finally:
            return data
