import math
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from scipy. integrate import odeint
import numpy as np

from Models.base_model import Base_model

coord = [
    [[87, 9]],
    [[87, 9]],
    [[87, 9]],
    [[87, 9]]
]

list_nodes = ["Q1:ON_SWITCH"]

list_graph = [0, 1]

list_text_control_actions = {"Позиции КЗ": ["Время, с", "Позиция"]}

list_text_initial_conditions = ["Ток фазы 'А' статора, А",
    "Ток фазы 'B' статора, А",]

coords_text = [
    [152, 234, "w"],
    [152, 234, 'w'],
    [152, 234, "w"],
    [152, 234, 'w']
]

class KZ_3(Base_model):

    def __init__(self, init_x, init_y, position, canv, root, initial_list_wires, initial_control_actions, initial_initial_conditions, initial_secondary_parameters, Comdobox_index):

        Base_model.__init__(self, init_x, init_y, canv, root, "Image/KZ_3/", coord, position, list_nodes, list_graph, initial_secondary_parameters, "KZ", list_text_control_actions, list_text_initial_conditions, initial_control_actions, initial_initial_conditions, initial_list_wires, coords_text, Comdobox_index)

        self.width_input = 2
        self.width_matrix = 2
        self.height_matrix = 2
        self.type_switch = True

        ###
        #self.L = 0.0000001
        self.Loff = 0
        #self.R = 0.0002
        self.Roff = 0
        #self.dt = 0.2

        #self.inital_position_switch = True # T - замкнут, F разомкнут
        #self.position_switch = self.inital_position_switch
        #self.switch_time = [0, 2.5, 5]
    
    def get_main_determinant(self, input_variable, t):
        main_determinant = np.array([[self.L + self.Loff, -self.L - self.Loff],
                                    [self.L + self.Loff, 2*(self.L + self.Loff),]], dtype = self.data_type)
        return main_determinant

    def get_own_matrix(self, input_variable, t):
        self.help_ss(t)

        own_matrix = np.array([(self.R + self.Roff)*(input_variable[1] - input_variable[0]),  
                                (self.R + self.Roff)*(-2*input_variable[1] - input_variable[0])], dtype = self.data_type)
        return own_matrix

    def get_voltage_matrix(self, parameter):
        if (parameter == "Q1"):
            voltage_matrix = [[-1, 0],
                            [0, -1]
                        ] 
        return voltage_matrix

    def get_current_matrix(self, parameter):
        if (parameter == "Q1"):
            current_matrix = [[-1, 0],
                            [0, -1],
                            [1, 1]
                            ] 
        return current_matrix

    def set_primary_parameters(self):
        if (self.secondary_parameters != ["Нет данных"] * len(self.list_text_secondary_parameters)):
            self.L = np.float64(self.secondary_parameters[1])
            self.R = np.float64(self.secondary_parameters[0])
            self.dt = np.float64(self.secondary_parameters[2])


    def corrent_list_params(self):
        if (self.list_params != [[[],[]]]):
            if (self.list_params[0][1][0] == 0):
                self.inital_position_switch = False
            else:
                self.inital_position_switch = True
            self.position_switch = self.inital_position_switch
            self.switch_time = self.list_params[0][0]
