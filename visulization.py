import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import Callable

class Visualization:

    def __init__(self,axes,title :str,xlabel :str, ylabel :str, xlim :list, ylim :list, grid_on :bool):
        
        # Set the axes
        self.axes = axes

        # Adding a title at plot
        self.axes.set_title(title)
        
        # Adding x label at plot
        self.axes.set_xlabel(xlabel)
        
        # Adding y label at plot
        self.axes.set_ylabel(ylabel)
        
        # Adding grid at plot
        self.axes.grid(grid_on)
        
        # Adding x axes limits
        self.axes.set_xlim(xlim)
        
        # Adding y axes limit
        self.axes.set_ylim(ylim)
        
        # Turn on interactive mode
        plt.ion()
        
        
    def update(self, functions :list[tuple[Callable[...,None]]], step :float = 0.05):
        
        # Calling all the functions that need to re-draw in simulation
        for func,args in functions:
            func(*args)
            # plt.draw()
        plt.pause(step)
        
    
    def move_rectangle(self,rectangle :patches.Rectangle, x :float, y :float,radians :float):
        
        # x,y input is for the center,
        # so we need to calculate the left bottom coordinates
        
        width :float = rectangle.get_width()
        height :float = rectangle.get_height()
        
        # The x left bottom coordinate of the rectangle
        x_left_bottom :float = x - (width/2)
        
        # The y left bottom coordinate of the rectangle
        y_left_bottom :float = y - (height/2)
        
        # Setting the new position of rectangle
        rectangle.set_xy((x_left_bottom,y_left_bottom))
        
        # Transforming rand to degrees
        degrees = radians*(180/np.pi)

        # Setting the angle of rectangle
        rectangle.set_angle(degrees)

    def body_frame2D(self,lineXbody,lineYbody,x_body :float,y_body :float,theta :float,lenght :float):

        # x-body axes
        lineXbody.set_data([x_body,x_body+lenght*np.cos(theta)],[y_body,y_body+lenght*np.sin(theta)])

        # y-body axes
        lineYbody.set_data([x_body,x_body+lenght*np.cos(theta + np.pi/2)],[y_body,y_body+lenght*np.sin(theta + np.pi/2)])


    def PlotData(self,N,M,axes_list,
                 pre_state,
                 state,
                 pre_state_dot,
                 state_dot,
                 pre_control,
                 control,
                 pre_error,
                 error,
                 pre_time,
                 time):
        
        state_axes,state_dot_axes,control_axes,error_axes = axes_list

        state_axes.plot([pre_time,time],[pre_state[0,0],state[0,0]],color = "red",label = "x")
        state_axes.plot([pre_time,time],[pre_state[1,0],state[1,0]],color = "green",label = "y")
        state_axes.plot([pre_time,time],[pre_state[2,0],state[2,0]],color = "blue",label = "θ")

        state_dot_axes.plot([pre_time,time],[pre_state_dot[0,0],state_dot[0,0]],color = "salmon",label = "xdot")
        state_dot_axes.plot([pre_time,time],[pre_state_dot[1,0],state_dot[1,0]],color = "lightgreen",label = "ydot")
        state_dot_axes.plot([pre_time,time],[pre_state_dot[2,0],state_dot[2,0]],color = "lightblue",label = "θdot")

        error_axes.plot([pre_time,time],[pre_error[0,0],error[0,0]],color = "orange",label = "e_x")
        error_axes.plot([pre_time,time],[pre_error[1,0],error[1,0]],color = "darkblue",label = "e_y")
        error_axes.plot([pre_time,time],[pre_error[2,0],error[2,0]],color = "pink",label = "e_θ")

        control_axes.plot([pre_time,time],[pre_control[0,0],control[0,0]],color = "cyan",label = "Left")
        control_axes.plot([pre_time,time],[pre_control[1,0],control[1,0]],color = "gray",label = "Right")

           
    def _on_close(self,event):
        exit(1)