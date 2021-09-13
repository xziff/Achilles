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
    return 4*np.pi*10**(-7)*8000

coord = [
    [[1053, 171], [1053, 441], [9, 310]],
    [[658, 1053], [389, 1053], [521, 9]],
    [[10, 441], [10, 171], [1053, 309]],
    [[184, 9], [455, 9], [316, 1058]]
]

list_nodes = ["T_SN:ON_SWITCH", "T_NN:ON_SWITCH", "Z_VN:ON_SWITCH"]

list_graph = [0, 2, 3]

list_text_control_actions = {}

list_text_initial_conditions = [
    "Ток фазы 'A' на стороне звезды ВН, А",
    "Ток фазы 'B' на стороне звезды ВН, А",
    "Ток фазы 'C' на стороне звезды ВН, А",
    "Ток фазы 'A' на стороне треугольника СН, А",
    "Ток фазы 'B' на стороне треугольника СН, А",
    "Ток фазы 'C' на стороне треугольника СН, А",
    "Ток фазы 'A' на стороне треугольника НН, А",
    "Ток фазы 'B' на стороне треугольника НН, А",
    "Ток фазы 'C' на стороне треугольника НН, А",
    ]

coords_text = [
    [527, -40, "s"],
    [895, 513, 'w'],
    [527, -40, "s"],
    [895, 513, 'w']
]

class TwSSW_YD_11(Base_model):

    def __init__(self, init_x, init_y, position, canv, root, initial_list_wires, initial_control_actions, initial_initial_conditions, initial_secondary_parameters, Comdobox_index):

        Base_model.__init__(self, init_x, init_y, canv, root, "Image/TwSSW_YD_11/", coord, position, list_nodes, list_graph, initial_secondary_parameters, "TwSSW_YD_11", list_text_control_actions, list_text_initial_conditions, initial_control_actions, initial_initial_conditions, initial_list_wires, coords_text, Comdobox_index)

        self.width_input = 9
        self.width_matrix = 9
        self.height_matrix = 9

    def get_main_determinant(self, input_variable, t):
        Ha = (self.Wvn*input_variable[0]-self.Wsn*input_variable[3]-self.Wnn*input_variable[6])/self.l
        Hb = (self.Wvn*input_variable[1]-self.Wsn*input_variable[4]-self.Wnn*input_variable[7])/self.l
        Hc = (self.Wvn*input_variable[2]-self.Wsn*input_variable[5]-self.Wnn*input_variable[8])/self.l
        main_determinant = np.array([
        [self.Wvn*self.Wvn*self.k*ksi_dif(Ha)+self.Lvn, -self.Wvn*self.Wvn*self.k*ksi_dif(Hb)-self.Lvn, 0, -self.Wvn*self.Wsn*self.k*ksi_dif(Ha), self.Wvn*self.Wsn*self.k*ksi_dif(Hb), 0, -self.Wvn*self.Wnn*self.k*ksi_dif(Ha), self.Wvn*self.Wnn*self.k*ksi_dif(Hb), 0],
        [0, self.Wvn*self.Wvn*self.k*ksi_dif(Hb)+self.Lvn, -self.Wvn*self.Wvn*self.k*ksi_dif(Hc)-self.Lvn, 0, -self.Wvn*self.Wsn*self.k*ksi_dif(Hb), self.Wvn*self.Wsn*self.k*ksi_dif(Hc), 0, -self.Wvn*self.Wnn*self.k*ksi_dif(Hb), self.Wvn*self.Wnn*self.k*ksi_dif(Hc)],
        [0, 0, self.Wvn*self.Wvn*self.k*ksi_dif(Hc)+self.Lvn, 0, 0, -self.Wvn*self.Wsn*self.k*ksi_dif(Hc), 0, 0, -self.Wvn*self.Wnn*self.k*ksi_dif(Hc)],
        [0, -self.Wsn*self.Wvn*self.k*ksi_dif(Hb), 0, 0, self.Wsn*self.Wsn*self.k*ksi_dif(Hb)+self.Lsn, 0, 0, self.Wsn*self.Wnn*self.k*ksi_dif(Hb), 0],
        [0, 0, -self.Wsn*self.Wvn*self.k*ksi_dif(Hc), 0, 0, self.Wsn*self.Wsn*self.k*ksi_dif(Hc)+self.Lsn, 0, 0, self.Wsn*self.Wnn*self.k*ksi_dif(Hc)],
        [-self.Wsn*self.Wvn*self.k*ksi_dif(Ha), 0, 0, self.Wsn*self.Wsn*self.k*ksi_dif(Ha)+self.Lsn, 0, 0, self.Wsn*self.Wnn*self.k*ksi_dif(Ha), 0, 0],
        [0, -self.Wnn*self.Wvn*self.k*ksi_dif(Hb), 0, 0, self.Wnn*self.Wsn*self.k*ksi_dif(Hb), 0, 0, self.Wnn*self.Wnn*self.k*ksi_dif(Hb)+self.Lnn, 0],
        [0, 0, -self.Wnn*self.Wvn*self.k*ksi_dif(Hc), 0, 0, self.Wnn*self.Wsn*self.k*ksi_dif(Hc), 0, 0, self.Wnn*self.Wnn*self.k*ksi_dif(Hc)+self.Lnn],
        [-self.Wnn*self.Wvn*self.k*ksi_dif(Ha), 0, 0, self.Wnn*self.Wsn*self.k*ksi_dif(Ha), 0, 0, self.Wnn*self.Wnn*self.k*ksi_dif(Ha)+self.Lnn, 0, 0]
        ], dtype = self.data_type) 

        return main_determinant
    
    def get_own_matrix(self, input_variable, t):
        own_matrix = np.array([
        self.Rvn*(input_variable[1]-input_variable[0]),
        self.Rvn*(input_variable[2]-input_variable[1]),
        -self.Rvn*input_variable[2],
        -self.Rsn*input_variable[4],
        -self.Rsn*input_variable[5],
        -self.Rsn*input_variable[3],
        -self.Rnn*input_variable[7],
        -self.Rnn*input_variable[8],
        -self.Rnn*input_variable[6],
        ],dtype = self.data_type) 

        return own_matrix

    def get_voltage_matrix(self, parameter):
        if (parameter == "T_SN"):
            voltage_matrix = [
                        [0, 0],
                        [0, 0],
                        [0, 0], 
                        [-1, 0],
                        [0, -1],
                        [1, 1], 
                        [0, 0], 
                        [0, 0],
                        [0, 0]
                        ] 
            return voltage_matrix

        if (parameter == "T_NN"):
            voltage_matrix = [
                        [0, 0],
                        [0, 0],
                        [0, 0], 
                        [0, 0],
                        [0, 0],
                        [0, 0],
                        [-1, 0],
                        [0, -1],
                        [1, 1]
                        ] 
            return voltage_matrix

        if (parameter == "Z_VN"):
            voltage_matrix = [[-1, 0, 0],
                        [0, -1, 0],
                        [0, 0, -1],
                        [0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]
                        ] 
            return voltage_matrix

    def get_current_matrix(self, parameter):
        if (parameter == "T_SN"):
            current_matrix = [
                        [0, 0, 0, 1, -1, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, -1, 0, 0, 0],
                        [0, 0, 0, -1, 0, 1, 0, 0, 0]
                        ] 
            return current_matrix

        if (parameter == "T_NN"):
            current_matrix = [
                        [0, 0, 0, 0, 0, 0, 1, -1, 0],
                        [0, 0, 0, 0, 0, 0, 0, 1, -1],
                        [0, 0, 0, 0, 0, 0, -1, 0, 1]
                        ] 
            return current_matrix

        if (parameter == "Z_VN"):
            current_matrix = [
                        [-1, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, -1, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, -1, 0, 0, 0, 0, 0, 0]
                        ]  
            return current_matrix

    def set_primary_parameters(self):
        self.l = np.float64(1)
        self.S = np.float64(0.01) 
        self.k = self.S/self.l

        if (self.secondary_parameters != ["Нет данных"] * len(self.list_text_secondary_parameters)):
            Sn = self.secondary_parameters[0]
            Uvn = self.secondary_parameters[1]
            Usn = self.secondary_parameters[2]
            Unn = self.secondary_parameters[3]
            Pxx = self.secondary_parameters[4]
            Pkz = self.secondary_parameters[5]
            Ukvn = self.secondary_parameters[6]
            Uknn = self.secondary_parameters[7]
            Ixx = self.secondary_parameters[8]
            mu = 8000
            
            k = np.float64(Uvn/np.sqrt(3)/Usn)
            self.Wvn = np.float64(np.sqrt(100*self.l*Uvn**2/(100*np.pi*self.S*mu*self.mu0*Sn*Ixx)))
            self.Wsn = self.Wvn/k
            self.Wnn = self.Wsn

            Kr = np.float64(Uknn/Ukvn)

            self.Rvn = np.float64(1/1000*Pkz/2*(Uvn/Sn)**2)
            self.Rsn = np.float64(self.Rvn/2/k/k)
            self.Rnn = self.Rsn

            self.Lvn = np.float64(Ukvn/100*Uvn*Uvn/Sn*(1-Kr/4)/100/np.pi)
            self.Lsn = np.float64(1/2*Uknn/100*Uvn*Uvn/Sn/k**2/100/np.pi)
            self.Lnn = self.Lsn




