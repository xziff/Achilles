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

def B_delta(N, Ica, Icb, Icc, If, Id, x, phi, mu0, delta, wc, wr, wd, tau, p):
    result = 0
    for n in range(N + 1)[1:]:
        result = result + (np.sin(np.pi/2*n)*2*mu0/(np.pi*delta*n)*(wc*Ica*np.cos(np.pi/tau*x*n)+wc*Icb*np.cos(np.pi/tau*x*n-2*np.pi/3*n)+wc*Icc*np.cos(np.pi/tau*x*n+2*np.pi/3*n)+wr*If*np.cos(np.pi/tau*x*n-phi*p*n)+wd*Id*np.cos(np.pi/tau*x*n-phi*p*n)))
    return result

coord = [
    [[587, 177]],
    [[179, 702]],
    [[10, 173]],
    [[178, 13]]]

list_nodes = ["Q:ON_SWITCH"]

list_graph = [0, 4]

list_text_control_actions = {"Механический момент": ["t, с", "M(t), кН*м"], "Напряжение возбуждения": ["t, с", "Uв(t), В"]}

list_text_initial_conditions = ["Ток фазы 'А', А", 
                                    "Ток фазы 'B', А",
                                    "Ток возбуждения, А",
                                    "Ток демпферного контура, А",
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

        self.width_input = 6
        self.width_matrix = 4
        self.height_matrix = 4
        self.N = 1

    def f_A(self, angle):
        result = np.float64(0)
        for n in range(self.N + 1)[1:]:
            result = result + np.sin(np.pi/2*n)*np.sin(np.pi/2*n)*np.sin(np.pi/2*n + angle*n)/n**2
        return self.Eps*result

    def f_B(self, angle):
        result = np.float64(0)
        for n in range(self.N + 1)[1:]:
            result = result - np.sin(np.pi/2*n)*np.sin(np.pi/6*n + angle*n)/n**2
        return self.Eps*result
    
    def f_C(self, angle):
        result = np.float64(0)
        for n in range(self.N + 1)[1:]:
            result = result + np.sin(np.pi/2*n)*np.sin(-np.pi/6*n + angle*n)/n**2
        return self.Eps*result

    def f_Ad(self, angle):
        result = np.float64(0)
        for n in range(self.N + 1)[1:]:
            result = result + np.sin(np.pi/2*n)*np.sin(np.pi/2*n)*np.cos(np.pi/2*n + angle*n)/n
        return self.Eps*result

    def f_Bd(self, angle):
        result = np.float64(0)
        for n in range(self.N + 1)[1:]:
            result = result - np.sin(np.pi/2*n)*np.cos(np.pi/6*n + angle*n)/n
        return self.Eps*result
    
    def f_Cd(self, angle):
        result = np.float64(0)
        for n in range(self.N + 1)[1:]:
            result = result + np.sin(np.pi/2*n)*np.cos(-np.pi/6*n + angle*n)/n
        return self.Eps*result

    def get_main_determinant(self, input_variable, t):

        al = 2*np.pi/3
        phi = input_variable[5]

        main_determinant = np.array([[-self.Wa*self.Wa*(self.f_A(0)-self.f_B(0)-self.f_A(0-al)+self.f_B(0+al)) - self.Las, -self.Wa*self.Wa*(self.f_A(0+al)-self.f_B(0-al)-self.f_A(0-al)+self.f_B(0+al)) + self.Las, -self.Wa*self.Wf*(self.f_A(self.p*phi)-self.f_B(-self.p*phi)), -self.Wa*self.Wd*(self.f_A(self.p*phi)-self.f_B(-self.p*phi))],
                                     [-self.Wa*self.Wa*(self.f_B(0)-self.f_C(0)-self.f_B(0+al)+self.f_C(0+al)) - self.Las, -self.Wa*self.Wa*(self.f_B(0-al)-self.f_C(0-al)-self.f_B(0+al)+self.f_C(0+al)) - self.Las - self.Las, -self.Wa*self.Wf*(self.f_B(-self.p*phi)-self.f_C(-self.p*phi)), -self.Wa*self.Wd*(self.f_B(-self.p*phi)-self.f_C(-self.p*phi))],
                                     [-self.Wf*self.Wa*(self.f_A(-self.p*phi)-self.f_A(-self.p*phi-al)), -self.Wf*self.Wa*(self.f_A(-self.p*phi+al)-self.f_A(-self.p*phi-al)), -self.Wf*self.Wf*self.f_A(0) - self.Lfs, -self.Wf*self.Wd*self.f_A(0)],
                                     [-self.Wd*self.Wa*(self.f_A(-self.p*phi)-self.f_A(-self.p*phi-al)), -self.Wd*self.Wa*(self.f_A(-self.p*phi+al)-self.f_A(-self.p*phi-al)), -self.Wd*self.Wf*self.f_A(0), -self.Wd*self.Wd*self.f_A(0) - self.Lds]], dtype = self.data_type)            
        
        if (t == 0):
            print(main_determinant)

        return main_determinant

    def get_own_matrix(self, input_variable, t):
        IaA = input_variable[0]
        IaB = input_variable[1]
        IaC = - input_variable[0] - input_variable[1]
        If = input_variable[2]
        Id = input_variable[3]
        w = input_variable[4]
        phi = input_variable[5]
        al = 2*np.pi/3

        own_matrix = np.array([self.Ra*(IaA - IaB) + w*self.p*If*self.Wa*self.Wf*(self.f_Ad(self.p*phi)+self.f_Bd(-self.p*phi)) + w*self.p*Id*self.Wa*self.Wd*(self.f_Ad(self.p*phi)+self.f_Bd(-self.p*phi)),
                                self.Ra*(IaB - IaC) - w*self.p*If*self.Wa*self.Wf*(self.f_Bd(-self.p*phi)-self.f_Cd(-self.p*phi)) - w*self.p*Id*self.Wa*self.Wd*(self.f_Bd(-self.p*phi)-self.f_Cd(-self.p*phi)),
                                self.Rf*If - line_func(self.list_params[1], t) - w*self.p*self.Wf*self.Wa*(IaA*self.f_Ad(-self.p*phi)+IaB*self.f_Ad(-self.p*phi+al)+IaC*self.f_Ad(-self.p*phi-al)),
                                self.Rd*Id - w*self.p*self.Wd*self.Wa*(IaA*self.f_Ad(-self.p*phi)+IaB*self.f_Ad(-self.p*phi+al)+IaC*self.f_Ad(-self.p*phi-al))], dtype = self.data_type)          
        
        if (t == 0):
            print(own_matrix)

        return own_matrix

    def get_voltage_matrix(self, parameter):
        if (parameter == "Q"):
            voltage_matrix = [[-1, 0],
                        [0, -1],
                        [0, 0],
                        [0, 0]
                        ] 
            return voltage_matrix

    def get_current_matrix(self, parameter):
        if (parameter == "Q"):
            current_matrix = [[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [-1, -1, 0, 0]
                        ] 
            return current_matrix

    def get_additional_variable(self, input_variable, t):
        Melmag = self.p*2*self.p*self.tau/np.pi*self.l*(self.Wf*input_variable[2]+self.Wd*input_variable[3])*B_delta(self.N, input_variable[0], input_variable[1], -input_variable[0]-input_variable[1], input_variable[2], input_variable[3], self.tau/np.pi*input_variable[5]*self.p-self.tau/2, input_variable[5], self.mu0, self.delta, self.Wa, self.Wf, self.Wd, self.tau, self.p)
        #Melmag = 2*self.tau/np.pi*self.Wf*(2*self.Wa*input_variable[2]*self.l*self.mu0)/(np.pi*self.delta)*(input_variable[0]*np.cos(np.pi/2 - input_variable[5]) + input_variable[1]*np.cos(np.pi/2 - input_variable[5] + 2*np.pi/3) + (-input_variable[0]-input_variable[1])*np.cos(np.pi/2 - input_variable[5] - 2*np.pi/3))
        additional_variable = np.array([
                            (1000 * line_func(self.list_params[0], t) - 1*Melmag)/self.J, #!!!!!!!!!!!!!!!!!!!!!
                            input_variable[4]
                            ], dtype = self.data_type)  
        return additional_variable

    def set_primary_parameters(self):
        if (self.secondary_parameters != ["Нет данных"] * len(self.list_text_secondary_parameters)):
            k = (self.secondary_parameters[0]**2)*self.secondary_parameters[2]/self.secondary_parameters[1]
            self.tau = np.float64(np.pi*self.secondary_parameters[9]/2)
            self.Wa = np.float64(get_wc(Xc = self.secondary_parameters[4]*k, delta = self.secondary_parameters[10], S = self.secondary_parameters[8]*self.tau))
            self.Wf = np.float64(get_wr(wc = self.Wa, delta = self.secondary_parameters[10], S = self.secondary_parameters[8]*self.tau, Pn = self.secondary_parameters[1], cosfi= self.secondary_parameters[2], Un= self.secondary_parameters[0], Ifn = self.secondary_parameters[3], Xc = self.secondary_parameters[4]*k))
            self.Wd = np.float64(0)
            self.Ra = np.float64(self.secondary_parameters[5])
            self.Rf = np.float64(self.secondary_parameters[6])
            self.Rd = np.float64(0.01)
            self.Las = np.float64(self.secondary_parameters[7]*k/100/np.pi)
            self.Lfs = np.float64(0.000001)
            self.Lds = np.float64(0.000001)
            self.delta = np.float64(self.secondary_parameters[10])
            self.l = np.float64(self.secondary_parameters[8])
            self.J = np.float64(self.secondary_parameters[11])
            self.p = np.float64(1)

            print(self.tau, self.l, self.delta, self.Wa, self.Wf, self.secondary_parameters[4]*k, self.Ra)

            self.Eps = np.float64((2*self.mu0*2*self.tau*self.l*self.p)/(np.pi*self.delta*np.pi))

            self.Urxx = self.secondary_parameters[0]/np.sqrt(3)*1000*self.Rf*math.pi*self.delta*math.pi/(100*math.pi*math.sqrt(2)*self.Wa*self.Wf*self.mu0*2*self.tau*self.l)
            self.Mnom = self.secondary_parameters[1]/(100*np.pi)

    def set_control_actions_help(self):
        mb.showinfo("Информация", "Напряжение возбуждения холостого хода = " + str(self.Urxx))
