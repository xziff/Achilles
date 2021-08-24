import math
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from scipy. integrate import odeint
import numpy as np

from Models.base_model import Base_model

coord = [
    [[430, 66], [8, 66]],
    [[58, 428], [58, 9]],
    [[430, 66], [8, 66]],
    [[58, 428], [58, 9]]]

list_nodes = ["Q1:ON_SWITCH", "Q2:ON_SWITCH"]

list_graph = [0, 1]

list_text_secondary_parameters = ["Фиктивная индуктивность, Гн:",
"Активное сопротивление, Ом:",
"Время отключения, с"]

list_text_example_models = [
    "Пользовательский",
    "Тест"]

list_example_parameters = [[0.00001, 0.002, 0.02]]

list_text_control_actions = {"Позиции выключателя": ["Время, с", "Позиция"]}

list_text_initial_conditions = ["Ток фазы 'А' статора, А",
    "Ток фазы 'B' статора, А"]

class SS(Base_model):

    def __init__(self, init_x, init_y, position, canv, root, initial_list_wires, initial_control_actions, initial_initial_conditions, initial_secondary_parameters):

        Base_model.__init__(self, init_x, init_y, canv, root, "Image/SS/", coord, position, list_nodes, list_graph, list_text_secondary_parameters, initial_secondary_parameters, "SS", list_text_control_actions, list_text_initial_conditions, initial_control_actions, initial_initial_conditions, initial_list_wires)

        self.width_input = 2
        self.width_matrix = 2
        self.height_matrix = 2

        ###
        #self.L = 0.0000001
        self.Loff = 0
        #self.R = 0.0002
        self.Roff = 0
        #self.dt = 0.02

        #self.inital_position_switch = True # T - замкнут, F разомкнут
        #self.position_switch = self.inital_position_switch
        #self.switch_time = [0, 2.5, 5]

    def get_interrupt_time(self):
        list_interrupt = []
        for i in range(len(self.switch_time)):
            if self.inital_position_switch:
                if (i%2 == 0):
                    list_interrupt.append(self.switch_time[i])
                else:
                    list_interrupt.append(self.switch_time[i] + self.dt)
            else:
                if (i%2 == 0):
                    if (self.switch_time[i] == 0):
                        list_interrupt.append(self.switch_time[i] + 0)
                    else:
                        list_interrupt.append(self.switch_time[i] + self.dt)
                else:
                    list_interrupt.append(self.switch_time[i])
        return list_interrupt

    def check_switch(self, t):
        for i in self.switch_time:
            if (t >= i):
                current_switch_time = i
            else:
                break
        if (current_switch_time == 0):
            self.start_position = True
        else:
            self.start_position = False
        self.index_current_switch_time = self.switch_time.index(current_switch_time)
        if self.inital_position_switch:
            if (self.index_current_switch_time%2 == 0):
                self.position_switch = True
                self.list_wires[0].text_tag = "Q1:ON_SWITCH"
                #self.list_wires[1].text_tag = "Q2:ON_SWITCH"
            else:
                self.position_switch = False
                self.list_wires[0].text_tag = "Q1:OFF_SWITCH"
                #self.list_wires[1].text_tag = "Q2:OFF_SWITCH"
        else:
            if (self.index_current_switch_time%2 == 0):
                self.position_switch = False
                self.list_wires[0].text_tag = "Q1:OFF_SWITCH"
                #self.list_wires[1].text_tag = "Q2:OFF_SWITCH"
            else:
                self.position_switch = True
                self.list_wires[0].text_tag = "Q1:ON_SWITCH"
                #self.list_wires[1].text_tag = "Q2:ON_SWITCH"
    
    def get_main_determinant(self, input_variable, t):
        main_determinant = np.array([[self.L + self.Loff, -self.L - self.Loff],
                                    [self.L + self.Loff, 2*(self.L + self.Loff),]], dtype = self.data_type)
        return main_determinant

    def get_own_matrix(self, input_variable, t):
        if not self.start_position:
            if (self.position_switch == False):
                if (t - self.switch_time[self.index_current_switch_time] < self.dt):
                    self.Roff = 1000000/self.dt*(t - self.switch_time[self.index_current_switch_time]) 
                else:
                    self.Roff = 0
                self.Loff = 0
            else:
                if (t - self.switch_time[self.index_current_switch_time] < self.dt):
                    self.Loff = 0.002*(1-1/self.dt*(t - self.switch_time[self.index_current_switch_time])) 
                else:
                    self.Loff = 0
                self.Roff = 0

        own_matrix = np.array([(self.R + self.Roff)*(input_variable[1] - input_variable[0]),  
                                (self.R + self.Roff)*(-2*input_variable[1] - input_variable[0])], dtype = self.data_type)
        return own_matrix

    def get_voltage_matrix(self, parameter):
        if (parameter == "Q1"):
            voltage_matrix = [[-1, 0],
                            [0, -1]
                        ] 
        if (parameter == "Q2"):
            voltage_matrix = [[1, 0],
                            [0, 1]
                            ] 
        return voltage_matrix

    def get_current_matrix(self, parameter):
        if (parameter == "Q1"):
            current_matrix = [[-1, 0],
                            [0, -1],
                            [1, 1]
                            ] 
        if (parameter == "Q2"):
            current_matrix = [[1, 0],
                            [0, 1],
                            [-1, -1]
                            ] 
        return current_matrix

    def set_primary_parameters(self):
        if (self.secondary_parameters != ["Нет данных"] * len(self.list_text_secondary_parameters)):
            self.L = np.float64(self.secondary_parameters[0])
            self.R = np.float64(self.secondary_parameters[1])
            self.dt = np.float64(self.secondary_parameters[2])


    def corrent_list_params(self):
        if (self.list_params[0][1][0] == 0):
            self.inital_position_switch = False
        else:
            self.inital_position_switch = True
        self.position_switch = self.inital_position_switch
        self.switch_time = self.list_params[0][0]
