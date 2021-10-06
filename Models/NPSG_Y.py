import math
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as mb
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from scipy. integrate import odeint
import numpy as np

from Models.base_model import Base_model

def line_func(list_points, t):
    for i in range(len(list_points[0]) - 1):
        if ((t >= list_points[0][i]) and (t <= list_points[0][i+1])):
            return list_points[1][i] + (list_points[1][i+1]-list_points[1][i])/(list_points[0][i+1]-list_points[0][i])*(t - list_points[0][i])

def get_wc(Xc, delta, S):
    mu0 = 4 * math.pi * (10 ** (-7))
    return math.sqrt(Xc*math.pi*delta*math.pi/(100*math.pi*2*mu0*2*S*1.5))

def get_wr(wc, delta, S, Pn, cosfi, Un, Ifn, Xc):
    mu0 = 4 * math.pi * (10 ** (-7))
    return ((math.sqrt((Pn/math.sqrt(3)/cosfi/Un*1000*math.sqrt(2)*Xc)**2 + (Un*1000/math.sqrt(3)*math.sqrt(2))**2 + 2*Pn/math.sqrt(3)/cosfi/Un*1000*math.sqrt(2)*Xc*Un*1000/math.sqrt(3)*math.sqrt(2)*math.sin(math.fabs(math.acos(cosfi)))))*(math.pi*delta*math.pi)/(100*math.pi*wc*Ifn*mu0*4*S))


coord = [
    [[587, 177]],
    [[179, 702]],
    [[10, 173]],
    [[178, 13]]]

list_nodes = ["Q:ON_SWITCH"]

list_graph = [0, 1, 2, 3]

list_text_control_actions = {"Механический момент": ["t, с", "M(t), кН*м"], "Напряжение возбуждения": ["t, с", "Uв(t), В"]}

list_text_initial_conditions = ["Ток фазы 'А', А", 
                                    "Ток фазы 'B', А",
                                    "Ток возбуждения, А",
                                    "Частота вращения ротора, рад/с",
                                    "Угол поворота ротора, рад", ]

coords_text = [
    [304, -40, "s"],
    [400, 338, 'w'],
    [304, -40, "s"],
    [400, 338, 'w']
]

class NPSG_Y(Base_model):

    def __init__(self, init_x, init_y, position, canv, root, initial_list_wires, initial_control_actions, initial_initial_conditions, initial_secondary_parameters, Comdobox_index):
        Base_model.__init__(self, init_x, init_y, canv, root, "Image/NPSG_Y/", coord, position, list_nodes, list_graph, initial_secondary_parameters, "NPSG_Y", list_text_control_actions, list_text_initial_conditions, initial_control_actions, initial_initial_conditions, initial_list_wires, coords_text, Comdobox_index)

        self.width_input = 5
        self.width_matrix = 3
        self.height_matrix = 3

    def get_main_determinant(self, input_variable, t):
        main_determinant = np.array([[-(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*(1 + (-1)*np.sin(np.pi/2 - 2*np.pi/3) - (-1)*np.sin(np.pi/6) - (-1)*(-1)*np.sin(np.pi/6 + 2*np.pi/3)) - self.Ls, -(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*(np.sin(np.pi/2 + 2*np.pi/3) + (-1)*np.sin(np.pi/2 - 2*np.pi/3) - (-1)*np.sin(np.pi/6 - 2*np.pi/3) - (-1)*(-1)*np.sin(np.pi/6 + 2*np.pi/3)) + self.Ls, -(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*(np.sin(np.pi/2+input_variable[4]) - (-1)*np.sin(np.pi/6-input_variable[4]))],
    	                   [-(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*((-1)*np.sin(np.pi/6) + (-1)*(-1)*np.sin(np.pi/6 + 2*np.pi/3) - np.sin(-np.pi/6) - (-1)*np.sin(-np.pi/6 + 2*np.pi/3))  - self.Ls, -(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*((-1)*np.sin(np.pi/6 - 2*np.pi/3) + (-1)*(-1)*np.sin(np.pi/6 + 2*np.pi/3) - np.sin(-np.pi/6 - 2*np.pi/3) - (-1)*np.sin(-np.pi/6 + 2*np.pi/3)) - self.Ls - self.Ls, -(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*((-1)*np.sin(np.pi/6-input_variable[4]) - np.sin(-np.pi/6-input_variable[4]))],
    	                   [-(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*(np.sin(np.pi/2  - input_variable[4]) + (-1)*np.sin(np.pi/2 - input_variable[4] - 2*np.pi/3)), -(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*(np.sin(np.pi/2 - input_variable[4] + 2*np.pi/3) + (-1)*np.sin(np.pi/2 - input_variable[4] - 2*np.pi/3)), -(2*self.wr*self.wr*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*(np.sin(np.pi/2)) - self.Lrs]
    	                  ], dtype = self.data_type) 
        if (t == 0):
            print(main_determinant)           
        return main_determinant

    def get_own_matrix(self, input_variable, t):
        own_matrix = np.array([input_variable[0]*self.Rs - input_variable[1]*self.Rs + input_variable[3]*(2*self.wc*self.wr*input_variable[2]*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*(np.cos(np.pi/2 + input_variable[4]) + (-1)*np.cos(np.pi/6 - input_variable[4])),
                    input_variable[1]*self.Rs - (-input_variable[0]-input_variable[1])*self.Rs + input_variable[3]*(2*self.wc*self.wr*input_variable[2]*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*(-(-1)*np.cos(np.pi/6 - input_variable[4]) + np.cos(-np.pi/6 - input_variable[4])),
                   input_variable[2]*self.Rr - line_func(self.list_params[1], t) - input_variable[3]*(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(np.pi*self.delta*np.pi)*(input_variable[0]*np.cos(np.pi/2 - input_variable[4]) + input_variable[1]*np.cos(np.pi/2 - input_variable[4] + 2*np.pi/3) + (-input_variable[0]-input_variable[1])*np.cos(np.pi/2 - input_variable[4] - 2*np.pi/3))], dtype = self.data_type)          
        if (t == 0):
            print(own_matrix)  
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
                            (1000 * line_func(self.list_params[0], t) - 1*Melmag)/self.J,
                            input_variable[3]
                            ], dtype = self.data_type)  
        return additional_variable

    def set_primary_parameters(self):
        if (self.secondary_parameters != ["Нет данных"] * len(self.list_text_secondary_parameters)):
            k = (self.secondary_parameters[0]**2)*self.secondary_parameters[2]/self.secondary_parameters[1]
            self.tau = np.float64(np.pi*self.secondary_parameters[9]/2)
            self.wc = np.float64(get_wc(Xc = self.secondary_parameters[4]*k, delta = self.secondary_parameters[10], S = self.secondary_parameters[8]*self.tau))
            self.wr = np.float64(get_wr(wc = self.wc, delta = self.secondary_parameters[10], S = self.secondary_parameters[8]*self.tau, Pn = self.secondary_parameters[1], cosfi= self.secondary_parameters[2], Un= self.secondary_parameters[0], Ifn = self.secondary_parameters[3], Xc = self.secondary_parameters[4]*k))
            self.Rs = np.float64(self.secondary_parameters[5])
            self.Rr = np.float64(self.secondary_parameters[6])
            self.Ls = np.float64(self.secondary_parameters[7]*k/100/np.pi)
            self.Lrs = np.float64(0.00001)
            self.delta = self.secondary_parameters[10]
            self.l = self.secondary_parameters[8]
            self.J = self.secondary_parameters[11]

            self.Urxx = self.secondary_parameters[0]/np.sqrt(3)*1000*self.Rr*math.pi*self.delta*math.pi/(100*math.pi*math.sqrt(2)*self.wc*self.wr*self.mu0*2*self.tau*self.l)
            self.Mnom = self.secondary_parameters[1]/(100*np.pi)

    def set_control_actions_help(self):
        mb.showinfo("Информация", "Напряжение возбуждения холостого хода = " + str(self.Urxx))
