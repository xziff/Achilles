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

class SM(Base_model):

    def __init__(self, init_x, init_y, canv, root):
        Base_model.__init__(self, init_x, init_y, canv, root, "Image/SM/", coord, 0, list_nodes)

        ###
        self.mu0 = 4 * math.pi * (10 ** (-7))
        self.wc = 8.46
        self.wr = 79.26
        self.Rs = 0.002
        self.Rr = 0.095
        self.Ls = 0.0001
        self.Lrs = 0.0002
        self.delta = 0.043
        self.tau = 1.689
        self.l = 3.1
        self.J = 2615

        ###
        self.M_max = 200000
        self.t0 = 1
        self.t2 = 1
        self.Ur = 140
        self.Urxx = 62

        self.width_input = len(self.get_first())
        self.width_matrix = len(self.get_main_determinant(self.get_first(), 0)[0])
        self.height_matrix = len(self.get_main_determinant(self.get_first(), 0))

    def get_first(self):
        return ([0, 0, 648, 100*math.pi, 0])

    def get_main_determinant(self, input_variable, t):
        main_determinant = [[-(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(1 + (-1)*math.sin(math.pi/2 - 2*math.pi/3) - (-1)*math.sin(math.pi/6) - (-1)*(-1)*math.sin(math.pi/6 + 2*math.pi/3)) - self.Ls, -(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(math.sin(math.pi/2 + 2*math.pi/3) + (-1)*math.sin(math.pi/2 - 2*math.pi/3) - (-1)*math.sin(math.pi/6 - 2*math.pi/3) - (-1)*(-1)*math.sin(math.pi/6 + 2*math.pi/3)) + self.Ls, -(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(math.sin(math.pi/2+input_variable[4]) - (-1)*math.sin(math.pi/6-input_variable[4]))],
    	                   [-(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*((-1)*math.sin(math.pi/6) + (-1)*(-1)*math.sin(math.pi/6 + 2*math.pi/3) - math.sin(-math.pi/6) - (-1)*math.sin(-math.pi/6 + 2*math.pi/3))  - self.Ls, -(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*((-1)*math.sin(math.pi/6 - 2*math.pi/3) + (-1)*(-1)*math.sin(math.pi/6 + 2*math.pi/3) - math.sin(-math.pi/6 - 2*math.pi/3) - (-1)*math.sin(-math.pi/6 + 2*math.pi/3)) - self.Ls - self.Ls, -(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*((-1)*math.sin(math.pi/6-input_variable[4]) - math.sin(-math.pi/6-input_variable[4]))],
    	                   [-(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(math.sin(math.pi/2 - input_variable[4]) + (-1)*math.sin(math.pi/2 - input_variable[4] - 2*math.pi/3)), -(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(math.sin(math.pi/2 - input_variable[4] + 2*math.pi/3) + (-1)*math.sin(math.pi/2 - input_variable[4] - 2*math.pi/3)), -(2*self.wr*self.wr*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(math.sin(math.pi/2)) - self.Lrs]
    	                  ]                      
        return main_determinant

    def get_own_matrix(self, input_variable, t):
        own_matrix = [input_variable[0]*self.Rs - input_variable[1]*self.Rs + input_variable[3]*(2*self.wc*self.wr*input_variable[2]*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(math.cos(math.pi/2 + input_variable[4]) + (-1)*math.cos(math.pi/6 - input_variable[4])),
                    input_variable[1]*self.Rs - (-input_variable[0]-input_variable[1])*self.Rs + input_variable[3]*(2*self.wc*self.wr*input_variable[2]*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(-(-1)*math.cos(math.pi/6 - input_variable[4]) + math.cos(-math.pi/6 - input_variable[4])),
                   input_variable[2]*self.Rr - self.Urxx - moment_pd(t, self.t0, self.t2, self.Ur - self.Urxx) - input_variable[3]*(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(input_variable[0]*math.cos(math.pi/2 - input_variable[4]) + input_variable[1]*math.cos(math.pi/2 - input_variable[4] + 2*math.pi/3) + (-input_variable[0]-input_variable[1])*math.cos(math.pi/2 - input_variable[4] - 2*math.pi/3))]        
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
        Melmag = 2*self.tau/math.pi*self.wr*(2*self.wc*input_variable[2]*self.l*self.mu0)/(math.pi*self.delta)*(input_variable[0]*math.cos(math.pi/2 - input_variable[4]) + input_variable[1]*math.cos(math.pi/2 - input_variable[4] + 2*math.pi/3) + (-input_variable[0]-input_variable[1])*math.cos(math.pi/2 - input_variable[4] - 2*math.pi/3))
        additional_variable = [
                            (moment_pd(t, self.t0, self.t2, self.M_max) - Melmag)/self.J,
                            input_variable[3]
                            ]
        return additional_variable

