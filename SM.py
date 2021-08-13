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

class SM(Base_model):

    def __init__(self, init_x, init_y, canv, root):
        Base_model.__init__(self, init_x, init_y, canv, root, "Image/SM/", coord, 0, list_nodes, list_graph)

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

