import math
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from scipy. integrate import odeint
import numpy as np

from Models.base_model import Base_model

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

list_text_control_actions = {}

list_text_initial_conditions = ["Ток фазы 'A' на стороне треугольника, А",
    "Ток фазы 'B' на стороне треугольника, А",
    "Ток фазы 'C' на стороне треугольника, А",
    "Ток фазы 'A' на стороне звезды, А",
    "Ток фазы 'B' на стороне звезды, А",
    "Ток фазы 'C' на стороне звезды, А"]

class DWT_YD_11(Base_model):

    def __init__(self, init_x, init_y, position, canv, root, initial_list_wires, initial_control_actions, initial_initial_conditions, initial_secondary_parameters):

        Base_model.__init__(self, init_x, init_y, canv, root, "Image/DWT_YD_11/", coord, position, list_nodes, list_graph, initial_secondary_parameters, "DWT_YD_11", list_text_control_actions, list_text_initial_conditions, initial_control_actions, initial_initial_conditions, initial_list_wires)

        self.width_input = 6
        self.width_matrix = 6
        self.height_matrix = 6

    def get_main_determinant(self, input_variable, t):
        Ha = (self.Wvn*input_variable[0]-self.Wvn*input_variable[0])/self.l
        main_determinant = np.array([
        [self.Wvn*self.Wvn*self.k*ksi_dif()+self.Lvn, -self.Wvn*self.Wvn*self.k*ksi_dif()-self.Lvn, 0, -self.Wvn*self.Wsn*self.k*ksi_dif(), self.Wvn*self.Wsn*self.k*ksi_dif(), 0, -self.Wvn*self.Wnn*self.k*ksi_dif(), self.Wvn*self.Wnn*self.k*ksi_dif(), 0],
        [0, self.Wvn*self.Wvn*self.k*ksi_dif()+self.Lvn, -self.Wvn*self.Wvn*self.k*ksi_dif()-self.Lvn, 0, -self.Wvn*self.Wsn*self.k*ksi_dif(), self.Wvn*self.Wsn*self.k*ksi_dif(), 0, -self.Wvn*self.Wnn*self.k*ksi_dif(), self.Wvn*self.Wnn*self.k*ksi_dif()],
        [0, 0, self.Wvn*self.Wvn*self.k*ksi_dif()+self.Lvn, 0, 0, -self.Wvn*self.Wsn*self.k*ksi_dif(), 0, 0, -self.Wvn*self.Wnn*self.k*ksi_dif()],
        [0, -self.Wsn*self.Wvn*self.k*ksi_dif(), 0, 0, self.Wsn*self.Wsn*self.k*ksi_dif()+self.Lsn, 0, 0, self.Wsn*self.Wnn*self.k*ksi_dif(), 0],
        [0, 0, -self.Wsn*self.Wvn*self.k*ksi_dif(), 0, 0, self.Wsn*self.Wsn*self.k*ksi_dif()+self.Lsn, 0, 0, self.Wsn*self.Wnn*self.k*ksi_dif()],
        [-self.Wsn*self.Wvn*self.k*ksi_dif(), 0, 0, self.Wsn*self.Wsn*self.k*ksi_dif()+self.Lsn, 0, 0, self.Wsn*self.Wnn*self.k*ksi_dif(), 0, 0],
        [0, -self.Wnn*self.Wvn*self.k*ksi_dif(), 0, 0, self.Wnn*self.Wsn*self.k*ksi_dif(), 0, 0, self.Wnn*self.Wnn*self.k*ksi_dif()+self.Lnn, 0],
        [0, 0, -self.Wnn*self.Wvn*self.k*ksi_dif(), 0, 0, self.Wnn*self.Wsn*self.k*ksi_dif(), 0, 0, self.Wnn*self.Wnn*self.k*ksi_dif()+self.Lnn],
        [-self.Wnn*self.Wvn*self.k*ksi_dif(), 0, 0, self.Wnn*self.Wsn*self.k*ksi_dif(), 0, 0, self.Wnn*self.Wnn*self.k*ksi_dif()+self.Lnn, 0, 0]
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