from typing import Generic,TypeVar,Callable
from Robot2DStudio.Services.PrintMessage.Warning import WarningString
from enum import Enum

# TODO : Revisit for capturing variables and plotting after or for saving variables in a file and re-open them

T = TypeVar("T")

class ActionCode(Enum):
    NO_ACTION = 0,
    CLEAN_AFTER_SET = 1,
    SAVE_AFTER_GET = 2,
    LOAD_DATATABLE = 3

class DataTableUtils:
    
    def __Clear(self):
        print("hello from clear method!!!")

    def __Save(self):
        pass

    def __Load(self):
        pass


class DataTable:

    Table :dict = {}
    UtilAction : ActionCode = ActionCode.CLEAN_AFTER_SET

    def Get(self,var :Generic[T]) -> Generic[T]:
        pass
    
    def Set(self):
        pass

    def Dispose(self):
        pass



