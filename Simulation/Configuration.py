import json
from typing import Generic,Type, TypeVar
# from Robot.RobotParams import DiffDriveParams

T = TypeVar("T")

def read() -> dict:
    with open("Simulation\\Configuration\\appsetting.json","r") as f:
        data = json.load(f)
        return data
    
class Configure(Generic[T]):

    __data :dict = read()

    #TODO: Revisit - This works for Zero Depth
    @classmethod
    def Get(cls :"Configure",section_type: Type[T]) -> Generic[T]:
        params :dict = cls.__data.get(section_type.__name__,None)
        for par in params.keys():
            if "__" in str(par):
                params.popitem(par)

        return section_type(**params)

# def main():
#     obj = Configure.Get(DiffDriveParams)
#     print(obj.s)

# main()