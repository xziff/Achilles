import math
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from scipy. integrate import odeint
import numpy as np

from base_model import Base_model

def moment_pd(t, t0, t2, M_max):
    t1 = t0 + t2
    if ((t >= t0) and (t <= t1)):
        return ((M_max)/(t1-t0)*t - (M_max)/(t1-t0)*t0)
    if (t < t0):
        return 0
    if (t > t1):
        return M_max

coord = [
    [[587, 177]],
    [[179, 702]],
    [[10, 173]],
    [[178, 13]]
]

list_nodes = ["Q:ON_SWITCH"]

list_graph = [0, 2, 3]

list_text_secondary_parameters = ["Номинальное напряжение, кВ:",
    "Номинальная активная мощность, МВт:",
    "Коэффициент мощности:",
    "Номинальное напряжение возбуждения, В:",
    "Сихнронное индуктиновное сопротивление, Ом:",
    "Активное сопротивление обмотки статора, мОм:",
    "Активное сопротивление обмотки возбуждения, Ом:",
    "Индуктивность поля рассеяния обмотки статора, мГн:",
    "Индуктивность поля рассеяния обмотки ротора, мГн:",
    "Длина машины, м:",
    "Полюсное деление машины, м:",
    "Длина воздушного зазора, м:",
    "Момент инерции ротора, кг*м2:"
 ]

list_text_example_models = [
    "Пользовательский",
    "ТВФ-63-2УЗ",
    "ТВФ-110-2ЕУЗ",
    "ТВФ-120-2УЗ",
    "ТВВ-160-2ЕУЗ",
    "ТГВ-200-2УЗ",
    "ТВВ-320-2ЕУЗ",
    "ТГВ-500-4УЗ",
    "390H"
]

list_example_parameters = [[10.5, 63, 0.8, 139.61, 2.118, 0.002, 0.0953, 0.0001, 0.0002, 3.1, 1.075*math.pi/2, 0.0425, 2615],
    [10.5, 110, 0.8,  219.24, 1.636, 0.00104, 0.126, 0.0001, 0.0002, 3.1, 1.128*math.pi/2, 0.064, 3750],
    [10.5, 120, 0.8, 205.8, 1.402, 0.00104, 0.12, 0.0001, 0.0002, 3.1, 1.128*math.pi/2, 0.064, 3750],
    [15.75, 160, 0.85, 274.72, 2.257, 0.0024, 0.136, 0.0001, 0.0002, 3.85, 1.17*math.pi/2, 0.085, 4375],
    [15.75, 200, 0.85, 327.12, 1.99, 0.00115, 0.174, 0.0001, 0.0002, 4.3, 1.235*math.pi/2, 0.080, 6070],
    [20, 320, 0.85, 332.05, 1.804, 0.001335, 0.1145, 0.0001, 0.0002, 6, 1.265*math.pi/2, 0.095, 7950],
    [20, 500, 0.85, 299.154, 1.467, 0.0011, 0.0683, 0.0001, 0.0002, 6.3, 1.315*math.pi/2, 0.095, 10280],
    [18, 400, 0.95, 439.9616, 1.62, 0.00084, 0.2644, 0.0001, 0.0002, 5.3, 1.29*math.pi/2, 0.0824, 8670]
    ]

class SM(Base_model):

    def __init__(self, init_x, init_y, canv, root):
        Base_model.__init__(self, init_x, init_y, canv, root, "Image/SM/", coord, 0, list_nodes, list_graph, list_text_secondary_parameters, None, list_text_example_models, list_example_parameters)

        ###
        self.mu0 = np.float64(4 * np.pi * (10 ** (-7)))
        self.wc = np.float64(8.46)
        self.wr = np.float64(79.26)
        self.Rs = np.float64(0.002)
        self.Rr = np.float64(0.095)
        self.Ls = np.float64(0.0001)
        self.Lrs = np.float64(0.0002)
        self.delta = np.float64(0.043)
        self.tau = np.float64(1.689)
        self.l = np.float64(3.1)
        self.J = np.float64(2615)

        ###
        self.M_max = np.float64(200000)
        self.t0 = np.float64(1)
        self.t2 = np.float64(1)
        self.Ur = np.float64(140)
        self.Urxx = np.float64(62)

        self.width_input = len(self.get_first())
        self.width_matrix = len(self.get_main_determinant(self.get_first(), 0)[0])
        self.height_matrix = len(self.get_main_determinant(self.get_first(), 0))
        

    def get_first(self):
        return ([0, 0, 648, 100*np.pi, 0])

    def get_main_determinant(self, input_variable, t):
        main_determinant = np.array([[-(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*(1 + (-1)*np.sin(np.pi/2 - 2*np.pi/3) - (-1)*np.sin(np.pi/6) - (-1)*(-1)*np.sin(np.pi/6 + 2*np.pi/3)) - self.Ls, -(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*(np.sin(np.pi/2 + 2*np.pi/3) + (-1)*np.sin(np.pi/2 - 2*np.pi/3) - (-1)*np.sin(np.pi/6 - 2*np.pi/3) - (-1)*(-1)*np.sin(np.pi/6 + 2*np.pi/3)) + self.Ls, -(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*(np.sin(np.pi/2+input_variable[4]) - (-1)*np.sin(np.pi/6-input_variable[4]))],
    	                   [-(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*((-1)*np.sin(np.pi/6) + (-1)*(-1)*np.sin(np.pi/6 + 2*np.pi/3) - np.sin(-np.pi/6) - (-1)*np.sin(-np.pi/6 + 2*np.pi/3))  - self.Ls, -(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*((-1)*np.sin(np.pi/6 - 2*np.pi/3) + (-1)*(-1)*np.sin(np.pi/6 + 2*np.pi/3) - np.sin(-np.pi/6 - 2*np.pi/3) - (-1)*np.sin(-np.pi/6 + 2*np.pi/3)) - self.Ls - self.Ls, -(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*((-1)*np.sin(np.pi/6-input_variable[4]) - np.sin(-np.pi/6-input_variable[4]))],
    	                   [-(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*(np.sin(np.pi/2 - input_variable[4]) + (-1)*np.sin(np.pi/2 - input_variable[4] - 2*np.pi/3)), -(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*(np.sin(np.pi/2 - input_variable[4] + 2*np.pi/3) + (-1)*np.sin(np.pi/2 - input_variable[4] - 2*np.pi/3)), -(2*self.wr*self.wr*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*(np.sin(np.pi/2)) - self.Lrs]
    	                  ], dtype = self.data_type)            
        return main_determinant

    def get_own_matrix(self, input_variable, t):
        own_matrix = np.array([input_variable[0]*self.Rs - input_variable[1]*self.Rs + input_variable[3]*(2*self.wc*self.wr*input_variable[2]*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*(np.cos(np.pi/2 + input_variable[4]) + (-1)*np.cos(np.pi/6 - input_variable[4])),
                    input_variable[1]*self.Rs - (-input_variable[0]-input_variable[1])*self.Rs + input_variable[3]*(2*self.wc*self.wr*input_variable[2]*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*(-(-1)*np.cos(np.pi/6 - input_variable[4]) + np.cos(-np.pi/6 - input_variable[4])),
                   input_variable[2]*self.Rr - self.Urxx - moment_pd(t, self.t0, self.t2, self.Ur - self.Urxx) - input_variable[3]*(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*(input_variable[0]*np.cos(np.pi/2 - input_variable[4]) + input_variable[1]*np.cos(np.pi/2 - input_variable[4] + 2*np.pi/3) + (-input_variable[0]-input_variable[1])*np.cos(np.pi/2 - input_variable[4] - 2*np.pi/3))], dtype = self.data_type)          
        return own_matrix

    def get_voltage_matrix(self, parameter):
        if (parameter == "Q"):
            voltage_matrix = [[-1, 0],
                        [0, -1],
                        [0, 0]
                        ] 
            return voltage_matrix

    def get_current_matrix(self, parameter):
        if (parameter == "Q"):
            current_matrix = [[1, 0, 0],
                        [0, 1, 0],
                        [-1, -1, 0]
                        ] 
            return current_matrix

    def get_additional_variable(self, input_variable, t):
        Melmag = 2*self.tau/np.pi*self.wr*(2*self.wc*input_variable[2]*self.l*self.mu0)/(np.pi*self.delta)*(input_variable[0]*np.cos(np.pi/2 - input_variable[4]) + input_variable[1]*np.cos(np.pi/2 - input_variable[4] + 2*np.pi/3) + (-input_variable[0]-input_variable[1])*np.cos(np.pi/2 - input_variable[4] - 2*np.pi/3))
        additional_variable = np.array([
                            (moment_pd(t, self.t0, self.t2, self.M_max) - Melmag)/self.J,
                            input_variable[3]
                            ], dtype = self.data_type)  
        return additional_variable

