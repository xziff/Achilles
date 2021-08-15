import math
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from scipy. integrate import odeint
import numpy as np

from base_model import Base_model

coord = [
    [[16, 275]],
    [[174, 17]],
    [[948, 276]],
    [[171, 981]]
]

list_nodes = ["Q:ON_SWITCH"]

list_graph = [0, 1]

list_text_secondary_parameters = ["Действующее значение напряженя, кВ:",
    "Частота, Гц:",
    "Начальная фаза напряжения, градус:",
    "Индуктивное сопротивление сети, Ом:",
 ]

list_text_example_models = [
    "Пользовательский",
    "Сеть 10 кВ"
]

list_example_parameters = [[10.5, 50, 0, 0.02],
    ]

list_text_control_actions = []

list_text_initial_conditions = ["Ток фазы 'А', А",
    "Ток фазы 'B', А",
    "Ток фазы 'C', А",]

class Electrical_System(Base_model):

    def __init__(self, init_x, init_y, canv, root):

        Base_model.__init__(self, init_x, init_y, canv, root, "Image/Electrical System/", coord, 0, list_nodes, list_graph, list_text_secondary_parameters, None, list_text_example_models, list_example_parameters, list_text_control_actions, list_text_initial_conditions, None, None)

        ###
        self.Uc = np.float64(6060)
        self.fc = np.float64(50)
        self.phic = np.float64(0)
        self.Lc = np.float64(0.02/(314.15))

        self.width_input = 3
        self.width_matrix = 3
        self.height_matrix = 3

    def get_first(self):
        return ([0, 0, 0])

    def get_main_determinant(self, input_variable, t):
        main_determinant = np.array([[-self.Lc, self.Lc, 0],
                            [0, -self.Lc, self.Lc],
                            [0, 0, -self.Lc]
                            ], dtype = self.data_type)                              
        return main_determinant

    def get_own_matrix(self, input_variable, t):
        own_matrix = np.array([self.Uc*np.sqrt(2)*np.sin(2*np.pi*self.fc*t + 0 + self.phic) - self.Uc*np.sqrt(2)*np.sin(2*np.pi*self.fc*t - 2*np.pi/3 + self.phic),
                    self.Uc*np.sqrt(2)*np.sin(2*np.pi*self.fc*t - 2*np.pi/3 + self.phic) - self.Uc*np.sqrt(2)*np.sin(2*np.pi*self.fc*t + 2*np.pi/3 + self.phic),
                    self.Uc*np.sqrt(2)*np.sin(2*np.pi*self.fc*t + 2*np.pi/3 + self.phic)
                    ], dtype = self.data_type)     
        return own_matrix
    
    def get_voltage_matrix(self, parameter):
        if (parameter == "Q"):
            voltage_matrix = [[1, 0, 0],
                        [0, 1, 0],
                        [0, 0, 1],
                        ] 
            return voltage_matrix

    def get_current_matrix(self, parameter):
        if (parameter == "Q"):
            current_matrix = [[-1, 0, 0],
                        [0, -1, 0],
                        [0, 0, -1],
                        ] 
            return current_matrix

    def set_primary_parameters(self):
        if (self.secondary_parameters != ["Нет данных"] * len(self.list_text_secondary_parameters)):
            self.Uc = np.float64(self.secondary_parameters[0] * 1000/ np.sqrt(3))
            self.fc = np.float64(self.secondary_parameters[1])
            self.phic = np.float64(self.secondary_parameters[2] * np.pi / 180)
            self.Lc = np.float64(self.secondary_parameters[3]/(2*np.pi*self.fc))
