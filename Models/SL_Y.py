import math
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from scipy. integrate import odeint
import numpy as np

from Models.base_model import Base_model

coord = [
    [[13, 124]],
    [[227, 9]],
    [[486, 126]],
    [[232, 480]]
]

list_nodes = ["Q:ON_SWITCH"]

list_graph = [0, 1]

list_text_control_actions = {}

list_text_initial_conditions = ["Ток фазы 'А', А",
    "Ток фазы 'B', А"]

class SL_Y(Base_model):

    def __init__(self, init_x, init_y, position, canv, root, initial_list_wires, initial_control_actions, initial_initial_conditions, initial_secondary_parameters):

        Base_model.__init__(self, init_x, init_y, canv, root, "Image/SL_Y/", coord, position, list_nodes, list_graph, initial_secondary_parameters, "SL_Y", list_text_control_actions, list_text_initial_conditions, initial_control_actions, initial_initial_conditions, initial_list_wires)
        ###

        self.width_input = 2
        self.width_matrix = 2
        self.height_matrix = 2

    def get_main_determinant(self, input_variable, t):
        main_determinant = np.array([[self.L, -self.L],
                            [self.L, 2*self.L]
                            ], dtype = self.data_type)                              
        return main_determinant

    def get_own_matrix(self, input_variable, t):
        own_matrix = np.array([self.R*(input_variable[1] - input_variable[0]),
                    self.R*(-input_variable[0] - 2*input_variable[1])
                    ], dtype = self.data_type)     
        return own_matrix
    
    def get_voltage_matrix(self, parameter):
        if (parameter == "Q"):
            voltage_matrix = [[-1, 0],
                        [0, -1]] 
            return voltage_matrix

    def get_current_matrix(self, parameter):
        if (parameter == "Q"):
            current_matrix = [[-1, 0],
                        [0, -1],
                        [1, 1],
                        ] 
            return current_matrix

    def set_primary_parameters(self):
        if (self.secondary_parameters != ["Нет данных"] * len(self.list_text_secondary_parameters)):
            self.R = self.secondary_parameters[0]**2/self.secondary_parameters[1]
            self.L = self.secondary_parameters[0]**2/self.secondary_parameters[2]/(100*np.pi)
            print(self.R, self.L)
