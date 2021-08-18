import math
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from scipy. integrate import odeint
import numpy as np

from base_model import Base_model

def get_wZ(w1, UnZ, UnT):
    return (w1*UnZ/UnT/math.sqrt(3))
def get_R_Z_T_11(Pkz, UnZ, Sn):
    return (Pkz/1000*(UnZ*UnZ)/(Sn*Sn))
def get_Z_Z_T_11(Uk, UnZ, Sn):
    return (Uk/100*(UnZ**2)/Sn)


def ksi_dif(H):
    return 70

coord = [
    [[1075, 172], [7, 173]],
    [[474, 1073], [474, 8]],
    [[12, 174], [1071, 173]],
    [[470, 5], [474, 1084]]
]

list_nodes = ["Z:ON_SWITCH", "T:ON_SWITCH"]

list_graph = [0, 2, 3]

list_text_secondary_parameters = ["Номинальная мощность, МВА:",
    "Номинальное напряжение обмотки звезды, кВ:",
    "Номинальное напряжение обмотки треугольника, кВ:",
    "Активная мощность потерь короткого замыкания, кВт:",
    "Активная мощность потерь холостого хода, кВт:",
    "Напряжение короткого замыкания, %:",
    "Ток холостого хода, %:"]

list_text_example_models = [
        "Пользовательский",
        "ТДЦ-80000/121/6,3",
        "ТДЦ-80000/121/15",
        "ТДЦ-1250000/121/10,5",
        "ТДЦ-200000/121/15,75",
        "ТДЦ-250000/121/15,75",
        "ТДЦ-400000/121/20",
        "ТМН-2500/110/6,6",
        "ТМН-2500/110/11",
        "ТМН-6300/115/6,6",
        "ТМН-6300/115/11",
        "ТДН-10000/115/6,6",
        "ТДН-10000/115/11",
        "ТДН-16000/115/6,6",
        "ТДН-16000/115/11",
        "ТДН-16000/115/22",
        "ТДН-16000/115/34,5",
        "ТДН-25000/115/38,5",
        "ТДН-40000/115/38,5",
        "ТДН-63000/115/38,5",
        "ТДН-80000/115/38,5",
        "ТД-80000/242/6,3",
        "ТД-80000/242/10,5",
        "ТДЦ-125000/242/10,5",
        "ТДЦ-200000/242/15,75",
        "ТДЦ-250000/242/15,75",
        "ТДЦ-400000/242/15,75",
        "ТДЦ-400000/242/20",
        "ТНЦ-630000/242/15,75",
        "ТНЦ-630000/242/20",
        "ТНЦ-630000/242/24",
        "ТНЦ-1000000/242/24",
        "ТДЦ-125000/347/10,5",
        "ТДЦ-200000/347/15,75",
        "ТДЦ-250000/347/10,5",
        "ТДЦ-400000/347/20",
        "ТНЦ-630000/347/15,75",
        "ТНЦ-630000/347/20",
        "ТНЦ-630000/347/24",
        "ТНЦ-1000000/347/24",
        "ТНЦ-1250000/347/24",
        "ТДЦ-250000/525/15,75",
        "ТДЦ-250000/525/20",
        "ТДЦ-400000/525/15,75",
        "ТДЦ-400000/525/20",
        "ТЦ-630000/525/15,75",
        "ТЦ-630000/525/20",
        "ТЦ-630000/525/24",
        "ТНЦ-1000000/525/24"
        ]

list_example_parameters = [[80, 121, 6.3, 310, 85, 11, 0.6],
    [80, 121, 15, 310, 85, 11, 0.6],
    [125, 121, 10.5, 400, 120, 10.5, 0.55],
    [200, 121, 15.75, 550, 170, 10.5, 0.5],
    [250, 121, 15.75, 640, 200, 10.5, 0.5],
    [400, 121, 20, 900, 320, 10.5, 0.45],
    [2.5, 110, 6.6, 22, 5.5, 10.5, 1.55],
    [2.5, 110, 11, 22, 5.5, 10.5, 1.55],
    [6.3, 115, 6.6, 44, 10, 10.5, 1],
    [6.3, 115, 11, 44, 10, 10.5, 1],
    [10, 115, 6.6, 58, 14, 10.5, 0.9],
    [10, 115, 11, 58, 14, 10.5, 0.9],
    [16, 115, 6.6, 85, 18, 10.5, 0.7],
    [16, 115, 11, 85, 18, 10.5, 0.7],
    [16, 115, 22, 85, 18, 10.5, 0.7],
    [16, 115, 34.5, 85, 18, 10.5, 0.7],
    [25, 115, 38.5, 120, 25, 10.5, 0.65],
    [40, 115, 38.5, 170, 34, 10.5, 0.55],
    [63, 115, 38.5, 245, 50, 10.5, 0.5],
    [80, 115, 38.5, 310, 58, 10.5, 0.45],
    [80, 242, 6.3, 315, 79, 11, 0.45],
    [80, 242, 10.5, 315, 79, 11, 0.45],
    [125, 242, 10.5, 380, 120, 11, 0.55],
    [200, 242, 15.75, 660, 130, 11, 0.4],
    [250, 242, 15.75, 600, 207, 11, 0.5],
    [400, 242, 15.75, 880, 330, 11, 0.4],
    [400, 242, 20, 880, 330, 11, 0.4],
    [630, 242, 15.75, 1200, 400, 12.5, 0.35],
    [630, 242, 20, 1200, 400, 12.5, 0.35],
    [630, 242, 24, 1200, 400, 12.5, 0.35],
    [1000, 242, 24, 2200, 480, 11.5, 0.4],
    [125, 347, 10.5, 380, 125, 11, 0.55],
    [200, 347, 15.75, 520, 180, 11, 0.5],
    [250, 347, 15.75, 605, 214, 11, 0.5],
    [400, 347, 20, 790, 300, 11.5, 0.45],
    [630, 347, 15.75, 1300, 345, 11.5, 0.35],
    [630, 347, 20, 1300, 345, 11.5, 0.35],
    [630, 347, 24, 1300, 345, 11.5, 0.35],
    [1000, 347, 24, 2200, 480, 11.5, 0.4],
    [1250, 347, 24, 2200, 715, 14.5, 0.55],
    [250, 525, 15.75, 590, 205, 13, 0.45],
    [250, 525, 20, 590, 205, 13, 0.45],
    [400, 525, 15.75, 790, 315, 13, 0.45],
    [400, 525, 20, 790, 315, 13, 0.45],
    [630, 525, 15.75, 1210, 420, 14, 0.4],
    [630, 525, 20, 1210, 420, 14, 0.4],
    [630, 525, 24, 1210, 420, 14, 0.4],
    [1000, 525, 24, 1800, 570, 14.5, 0.45],
    ]

list_text_control_actions = {}

list_text_initial_conditions = ["Ток фазы 'A' на стороне треугольника, А",
    "Ток фазы 'B' на стороне треугольника, А",
    "Ток фазы 'C' на стороне треугольника, А",
    "Ток фазы 'A' на стороне звезды, А",
    "Ток фазы 'B' на стороне звезды, А",
    "Ток фазы 'C' на стороне звезды, А"]

class Transformator_Z_T_11(Base_model):

    def __init__(self, init_x, init_y, position, canv, root, initial_list_wires, initial_control_actions, initial_initial_conditions, initial_secondary_parameters):

        Base_model.__init__(self, init_x, init_y, canv, root, "Image/Transformator/", coord, position, list_nodes, list_graph, list_text_secondary_parameters, initial_secondary_parameters, list_text_example_models, list_example_parameters, list_text_control_actions, list_text_initial_conditions, initial_control_actions, initial_initial_conditions, initial_list_wires)

        self.width_input = 6
        self.width_matrix = 6
        self.height_matrix = 6

    def get_main_determinant(self, input_variable, t):
        main_determinant = np.array([[self.Ls1 - self.w1*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[0]+self.w2/self.lm*input_variable[4]), 0, 0, 0, self.w1*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[0]+self.w2/self.lm*input_variable[4]), 0],
                            [0, self.Ls1 - self.w1*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[1]+self.w2/self.lm*input_variable[5]), 0, 0, 0, self.w1*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[1]+self.w2/self.lm*input_variable[5])],
                            [0, 0, self.Ls1 - self.w1*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[2]+self.w2/self.lm*input_variable[3]), self.w1*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[2]+self.w2/self.lm*input_variable[3]), 0, 0],
                            [self.w2*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[0]+self.w2/self.lm*input_variable[4]), 0, -self.w2*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[2]+self.w2/self.lm*input_variable[3]), -self.Ls2 + self.w2*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[2]+self.w2/self.lm*input_variable[3]), self.Ls2 - self.w2*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[0]+self.w2/self.lm*input_variable[4]), 0],
                            [-self.w2*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[0]+self.w2/self.lm*input_variable[4]), self.w2*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[1]+self.w2/self.lm*input_variable[5]), 0, 0, -self.Ls2 + self.w2*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[0]+self.w2/self.lm*input_variable[4]), self.Ls2 - self.w2*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[1]+self.w2/self.lm*input_variable[5])],
                            [0, -self.w2*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[1]+self.w2/self.lm*input_variable[5]), 0, 0, 0, -self.Ls2 + self.w2*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[1]+self.w2/self.lm*input_variable[5])]
                            ], dtype = self.data_type) 

        return main_determinant
    
    def get_own_matrix(self, input_variable, t):
        own_matrix = np.array([-input_variable[0]*self.R1,
                    -input_variable[1]*self.R1,
                    -input_variable[2]*self.R1,
                    input_variable[3]*self.R2 - input_variable[4]*self.R2,
                    input_variable[4]*self.R2 - input_variable[5]*self.R2,
                    input_variable[5]*self.R2
                    ],dtype = self.data_type) 

        return own_matrix

    def get_voltage_matrix(self, parameter):
        if (parameter == "T"):
            voltage_matrix = [[1, 0],
                        [0, 1],
                        [-1, -1], 
                        [0, 0], 
                        [0, 0],
                        [0, 0]
                        ] 
            return voltage_matrix

        if (parameter == "Z"):
            voltage_matrix = [[0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0],
                        [-1, 0, 0],
                        [0, -1, 0],
                        [0, 0, -1]
                        ] 
            return voltage_matrix

    def get_current_matrix(self, parameter):
        if (parameter == "T"):
            current_matrix = [[1, 0, -1, 0, 0, 0],
                        [-1, 1, 0, 0, 0, 0],
                        [0, -1, 1, 0, 0, 0]
                        ] 
            return current_matrix

        if (parameter == "Z"):
            current_matrix = [[0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 0, 1]
                        ] 
            return current_matrix

    def set_primary_parameters(self):
        self.L = np.float64(1)
        self.ra = np.float64(0.4)
        self.R_t = np.float64(0.1)
        self.lm = np.float64(2*(self.L + self.ra))
        self.S = np.float64(np.pi*self.R_t**2)
        self.Ls1 = np.float64(0.000087)
        self.Ls2 = np.float64(0.032)
        if (self.secondary_parameters != ["Нет данных"] * len(self.list_text_secondary_parameters)):
            self.w1 = 100
            self.w2 = get_wZ(w1 = self.w1, UnZ = self.secondary_parameters[1], UnT = self.secondary_parameters[2])
            self.R2 = get_R_Z_T_11(Pkz = self.secondary_parameters[3], UnZ = self.secondary_parameters[1], Sn = self.secondary_parameters[0])/2
            self.R1 = 2*self.R2/2*3*self.secondary_parameters[2]*self.secondary_parameters[2]/self.secondary_parameters[1]/self.secondary_parameters[1]