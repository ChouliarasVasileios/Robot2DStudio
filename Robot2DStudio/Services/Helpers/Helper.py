import numpy as np
from numpy import ndarray

class StringHelper:
    @staticmethod
    def ToCamelCase(string :str) -> str:
        string = string[0].lower() + string[1:]
        return string
    
class RotationMatrix3:

    @staticmethod
    def Rx(theta : float) -> ndarray:
        return np.array(
            [[1.0, 0.0, 0.0],
             [0.0, np.cos(theta), -np.sin(theta)],
             [0.0, np.sin(theta),  np.cos(theta)]])

    @staticmethod
    def Ry(theta : float) -> ndarray:
        return np.array(
            [[np.cos(theta), 0.0, np.sin(theta)],
             [0.0, 1.0, 0.0],
             [-np.sin(theta), 0.0, np.cos(theta)]])

    @staticmethod
    def Rz(theta : float) -> ndarray:
        return np.array(
            [[np.cos(theta), -np.sin(theta), 0.0],
             [np.sin(theta), np.cos(theta), 0.0],
             [0.0, 0.0, 1.0]])

class RotationMatrix2:

    @staticmethod
    def Rx(theta : float) -> ndarray:
        return RotationMatrix3.Rx(theta)[0:2,0:2]

    @staticmethod
    def Ry(theta : float) -> ndarray:
        return RotationMatrix3.Ry(theta)[0:2,0:2]

    @staticmethod
    def Rz(theta : float) -> ndarray:
        return RotationMatrix3.Rz(theta)[0:2,0:2]
