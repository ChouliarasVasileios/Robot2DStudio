import numpy as np
from numpy import ndarray
import matplotlib.patches as patches
from Visualization.Base.Visulization import Visualization

class DiffrentialDriveRobotVisual(Visualization):
    
    def __init__(self, visulationParams):
        super().__init__(visulationParams)

        # ''' This space can be use to add more attributes or to used as init function for graphics '''

        # Init BodyFrame
        self.LineXBody, = self.axes.plot([],[],"o-",markersize = 0.5,lw = 1.5,color = "red")
        self.LineXBody.set_data([],[])
        
        self.LineYBody, = self.axes.plot([],[],"o-",markersize = 0.5,lw = 1.5,color = "green")
        self.LineYBody.set_data([],[])


    def Init(self):
        self.SetTargetRectagleCenterPoint()

    def Update(self,x :ndarray):
        self.MoveRectangle(x)
        self.BodyFrame2D(x)

    def MoveRectangle(self, x :ndarray):
    
        # x,y input is for the center,
        # so we need to calculate the left bottom coordinates
        
        rectangle :patches.Rectangle = self.GetPatch("DifferentialDriveRobot") 

        width :float = rectangle.get_width()
        height :float = rectangle.get_height()
        
        # The x left bottom coordinate of the rectangle
        x_left_bottom :float = x[0,0] - (width/2)
        
        # The y left bottom coordinate of the rectangle
        y_left_bottom :float = x[1,0] - (height/2)
        
        # Setting the new position of rectangle
        rectangle.set_xy((x_left_bottom,y_left_bottom))
        
        # Transforming rand to degrees
        degrees = x[2,0]*(180/np.pi)

        # Setting the angle of rectangle
        rectangle.set_angle(degrees)

    def BodyFrame2D(self,x :ndarray):

        lenght :float = 0.5
        # x-body axes
        self.LineXBody.set_data([x[0,0],x[0,0]+lenght*np.cos(x[2,0])],[x[1,0],x[1,0]+lenght*np.sin(x[2,0])])

        # y-body axes
        self.LineYBody.set_data([x[0,0],x[0,0]+lenght*np.cos(x[2,0] + np.pi/2)],[x[1,0],x[1,0]+lenght*np.sin(x[2,0] + np.pi/2)])

    def SetTargetRectagleCenterPoint(self):
        rectangle :patches.Rectangle = self.GetPatch("TargetRectangle") 
        # The x left bottom coordinate of the rectangle
        x_left_bottom :float = rectangle.get_x() - (rectangle.get_width()/2)
        
        # The y left bottom coordinate of the rectangle
        y_left_bottom :float = rectangle.get_y() - (rectangle.get_width()/2)
        rectangle.set_xy((x_left_bottom,y_left_bottom))


    # def PlotData(self,N,M,axes_list,
    #                 pre_state,
    #                 state,
    #                 pre_state_dot,
    #                 state_dot,
    #                 pre_control,
    #                 control,
    #                 pre_error,
    #                 error,
    #                 pre_time,
    #                 time):
        
    #     state_axes,state_dot_axes,control_axes,error_axes = axes_list

    #     state_axes.plot([pre_time,time],[pre_state[0,0],state[0,0]],color = "red",label = "x")
    #     state_axes.plot([pre_time,time],[pre_state[1,0],state[1,0]],color = "green",label = "y")
    #     state_axes.plot([pre_time,time],[pre_state[2,0],state[2,0]],color = "blue",label = "θ")

    #     state_dot_axes.plot([pre_time,time],[pre_state_dot[0,0],state_dot[0,0]],color = "salmon",label = "xdot")
    #     state_dot_axes.plot([pre_time,time],[pre_state_dot[1,0],state_dot[1,0]],color = "lightgreen",label = "ydot")
    #     state_dot_axes.plot([pre_time,time],[pre_state_dot[2,0],state_dot[2,0]],color = "lightblue",label = "θdot")

    #     error_axes.plot([pre_time,time],[pre_error[0,0],error[0,0]],color = "orange",label = "e_x")
    #     error_axes.plot([pre_time,time],[pre_error[1,0],error[1,0]],color = "darkblue",label = "e_y")
    #     error_axes.plot([pre_time,time],[pre_error[2,0],error[2,0]],color = "pink",label = "e_θ")

    #     control_axes.plot([pre_time,time],[pre_control[0,0],control[0,0]],color = "cyan",label = "Left")
    #     control_axes.plot([pre_time,time],[pre_control[1,0],control[1,0]],color = "gray",label = "Right")