import math
import pickle
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from scipy. integrate import odeint
import numpy as np

from Models.base_model import Base_model

def line_func(list_points, t):
    for i in range(len(list_points[0]) - 1):
        if ((t >= list_points[0][i]) and (t <= list_points[0][i+1])):
            return np.float64(list_points[1][i] + (list_points[1][i+1]-list_points[1][i])/(list_points[0][i+1]-list_points[0][i])*(t - list_points[0][i]))

def B_delta(N, Ica, Icb, Icc, Ira, Irb, Irc, x, phi, mu0, delta, wc, wr, tau, p):
    result = 0
    for n in range(N + 1)[1:]:
        result = result + (np.sin(np.pi/2*n)*2*mu0/(np.pi*delta*n)*(wc*Ica*np.cos(np.pi/tau*x*n)+wc*Icb*np.cos(np.pi/tau*x*n-2*np.pi/3*n)+wc*Icc*np.cos(np.pi/tau*x*n+2*np.pi/3*n)+wr*Ira*np.cos(np.pi/tau*x*n-phi*p*n)+wr*Irb*np.cos(np.pi/tau*x*n-phi*p*n-2*np.pi/3*n)+wr*Irc*np.cos(np.pi/tau*x*n-phi*p*n+2*np.pi/3*n)))
    return result

coord = [
    [[8, 171]],
    [[189, 10]],
    [[595, 175]],
    [[193, 745]]]

list_nodes = ["Q:ON_SWITCH"]

list_graph = [0, 6]

list_text_control_actions = {"Нагрузочный момент": ["s, %", "M(s), кН*м"], "Сопротивление реостата, доли Rr": ["s, %", "N(s), о.е."]}

list_text_initial_conditions = ["Ток фазы 'А' статора, А",
    "Ток фазы 'B' статора, А",
    "Ток фазы 'C' статора, А",
    "Ток фазы 'А' ротора, А",
    "Ток фазы 'B' ротора, А",
    "Ток фазы 'C' ротора, А",
    "Частота вращения ротора, рад/с",
    "Угол поворота ротора, рад"]

coords_text = [
    [286, -40, "s"],
    [410, 378, 'w'],
    [286, -40, "s"],
    [410, 378, 'w']
]

class WRIM(Base_model):

    def __init__(self, init_x, init_y, position, canv, root, initial_list_wires, initial_control_actions, initial_initial_conditions, initial_secondary_parameters, Comdobox_index):

        Base_model.__init__(self, init_x, init_y, canv, root, "Image/WRIM/", coord, position, list_nodes, list_graph, initial_secondary_parameters, "WRIM", list_text_control_actions, list_text_initial_conditions, initial_control_actions, initial_initial_conditions, initial_list_wires, coords_text, Comdobox_index)

        self.width_input = 8
        self.width_matrix = 6
        self.height_matrix = 6

        self.N = 1

    def f_A(self, angle):
        result = 0
        for n in range(self.N + 1)[1:]:
            result = result + np.sin(np.pi/2*n)*np.sin(np.pi/2*n)*np.sin(np.pi/2*n + angle*n)/n**2
        return result

    def f_B(self, angle):
        result = 0
        for n in range(self.N + 1)[1:]:
            result = result - np.sin(np.pi/2*n)*np.sin(np.pi/6*n + angle*n)/n**2
        return result
    
    def f_C(self, angle):
        result = 0
        for n in range(self.N + 1)[1:]:
            result = result + np.sin(np.pi/2*n)*np.sin(-np.pi/6*n + angle*n)/n**2
        return result

    def f_Ad(self, angle):
        result = 0
        for n in range(self.N + 1)[1:]:
            result = result + np.sin(np.pi/2*n)*np.sin(np.pi/2*n)*np.cos(np.pi/2*n + angle*n)/n
        return result

    def f_Bd(self, angle):
        result = 0
        for n in range(self.N + 1)[1:]:
            result = result - np.sin(np.pi/2*n)*np.cos(np.pi/6*n + angle*n)/n
        return result
    
    def f_Cd(self, angle):
        result = 0
        for n in range(self.N + 1)[1:]:
            result = result + np.sin(np.pi/2*n)*np.cos(-np.pi/6*n + angle*n)/n
        return result
    
    def get_main_determinant(self, input_variable, t):
        main_determinant = np.array([[-self.Kcc*(self.f_A(0) - self.f_B(0)) - self.Lcs, -self.Kcc*(self.f_A(2*np.pi/3) - self.f_B(-2*np.pi/3)) + self.Lcs, -self.Kcc*(self.f_A(-2*np.pi/3) - self.f_B(2*np.pi/3)), -self.Krc*(self.f_A(input_variable[7]*self.p) - self.f_B(-input_variable[7]*self.p)), -self.Krc*(self.f_A(input_variable[7]*self.p + 2*np.pi/3) - self.f_B(-input_variable[7]*self.p - 2*np.pi/3)), -self.Krc*(self.f_A(input_variable[7]*self.p - 2*np.pi/3) - self.f_B(-input_variable[7]*self.p + 2*np.pi/3))],
                    [-self.Kcc*(self.f_B(0) - self.f_C(0)), -self.Kcc*(self.f_B(0 - 2*np.pi/3) - self.f_C(0 - 2*np.pi/3)) - self.Lcs, -self.Kcc*(self.f_B(0 + 2*np.pi/3) - self.f_C(0 + 2*np.pi/3)) + self.Lcs, -self.Krc*(self.f_B(0 - input_variable[7]*self.p) - self.f_C(0 - input_variable[7]*self.p)), -self.Krc*(self.f_B(0 - input_variable[7]*self.p - 2*np.pi/3) - self.f_C(0 - input_variable[7]*self.p - 2*np.pi/3)), -self.Krc*(self.f_B(0 - input_variable[7]*self.p + 2*np.pi/3) - self.f_C(0 - input_variable[7]*self.p + 2*np.pi/3))],
                    [-self.Kcc*self.f_C(0), -self.Kcc*self.f_C(0 - 2*np.pi/3), -self.Kcc*self.f_C(0 + 2*np.pi/3) - self.Lcs, -self.Krc*self.f_C(0 - input_variable[7]*self.p), -self.Krc*self.f_C(0 - input_variable[7]*self.p - 2*np.pi/3), -self.Krc*self.f_C(0 - input_variable[7]*self.p + 2*np.pi/3)],
                    [-self.Krc*self.f_A(0-input_variable[7]*self.p-0), -self.Krc*self.f_A(0-input_variable[7]*self.p+2*np.pi/3), -self.Krc*self.f_A(0-input_variable[7]*self.p-2*np.pi/3), -self.Krr*self.f_A(0-0) - self.Lrs, -self.Krr*self.f_A(0+2*np.pi/3), -self.Krr*self.f_A(0-2*np.pi/3)],
                    [-self.Krc*self.f_B(0+input_variable[7]*self.p-0), -self.Krc*self.f_B(0+input_variable[7]*self.p-2*np.pi/3), -self.Krc*self.f_B(0+input_variable[7]*self.p+2*np.pi/3), -self.Krr*self.f_B(0+0), -self.Krr*self.f_B(0-2*np.pi/3) - self.Lrs, -self.Krr*self.f_B(0+2*np.pi/3)],
                    [-self.Krc*self.f_C(0+input_variable[7]*self.p-0), -self.Krc*self.f_C(0+input_variable[7]*self.p-2*np.pi/3), -self.Krc*self.f_C(0+input_variable[7]*self.p+2*np.pi/3), -self.Krr*self.f_C(0+0), -self.Krr*self.f_C(0-2*np.pi/3), -self.Krr*self.f_C(0+2*np.pi/3) - self.Lrs]
                   ], dtype = self.data_type)                    
        return main_determinant

    def get_own_matrix(self, input_variable, t):
        own_matrix = np.array([input_variable[0]*self.Rc - input_variable[1]*self.Rc + self.Krc*input_variable[6]*self.p*(input_variable[3]*self.f_Ad(0 + input_variable[7]*self.p) + input_variable[4]*self.f_Ad(0 + input_variable[7]*self.p + 2*np.pi/3) + input_variable[5]*self.f_Ad(0 + input_variable[7]*self.p - 2*np.pi/3) + input_variable[3]*self.f_Bd(0 - input_variable[7]*self.p) + input_variable[4]*self.f_Bd(0 - input_variable[7]*self.p - 2*np.pi/3) + input_variable[5]*self.f_Bd(0 - input_variable[7]*self.p + 2*np.pi/3)),
                    input_variable[1]*self.Rc - input_variable[2]*self.Rc + self.Krc*input_variable[6]*self.p*(-input_variable[3]*self.f_Bd(0 - input_variable[7]*self.p) - input_variable[4]*self.f_Bd(0 - input_variable[7]*self.p - 2*np.pi/3) - input_variable[5]*self.f_Bd(0 - input_variable[7]*self.p + 2*np.pi/3) + input_variable[3]*self.f_Cd(0 - input_variable[7]*self.p) + input_variable[4]*self.f_Cd(0 - input_variable[7]*self.p - 2*np.pi/3) + input_variable[5]*self.f_Cd(0 - input_variable[7]*self.p + 2*np.pi/3)),
                    input_variable[2]*self.Rc - self.Krc*input_variable[6]*self.p*(input_variable[3]*self.f_Cd(0 - input_variable[7]*self.p) + input_variable[4]*self.f_Cd(0 - input_variable[7]*self.p - 2*np.pi/3) + input_variable[5]*self.f_Cd(0 - input_variable[7]*self.p + 2*np.pi/3)),
                    input_variable[3]*self.Rr*(1+line_func(self.list_params[1], (100*np.pi/self.p - input_variable[6])/(100*np.pi/self.p)*100))-input_variable[6]*self.p*self.Krc*(input_variable[0]*self.f_Ad(0-input_variable[7]*self.p)+input_variable[1]*self.f_Ad(0-input_variable[7]*self.p+2*np.pi/3)+input_variable[2]*self.f_Ad(0-input_variable[7]*self.p-2*np.pi/3)),
                    input_variable[4]*self.Rr*(1+line_func(self.list_params[1], (100*np.pi/self.p - input_variable[6])/(100*np.pi/self.p)*100))+input_variable[6]*self.p*self.Krc*(input_variable[0]*self.f_Bd(0+input_variable[7]*self.p)+input_variable[1]*self.f_Bd(0+input_variable[7]*self.p-2*np.pi/3)+input_variable[2]*self.f_Bd(0+input_variable[7]*self.p+2*np.pi/3)),
                    input_variable[5]*self.Rr*(1+line_func(self.list_params[1], (100*np.pi/self.p - input_variable[6])/(100*np.pi/self.p)*100))+input_variable[6]*self.p*self.Krc*(input_variable[0]*self.f_Cd(0+input_variable[7]*self.p)+input_variable[1]*self.f_Cd(0+input_variable[7]*self.p-2*np.pi/3)+input_variable[2]*self.f_Cd(0+input_variable[7]*self.p+2*np.pi/3))
                    ], dtype = self.data_type) 
        return own_matrix

    def get_voltage_matrix(self, parameter):
        if (parameter == "Q"):
            voltage_matrix = [[-1, 0, 0],
                        [0, -1, 0],
                        [0, 0, -1],
                        [0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]
                        ] 
            return voltage_matrix

    def get_current_matrix(self, parameter):
        if (parameter == "Q"):
            current_matrix = [[1, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0]
                        ] 
            return current_matrix

    def get_additional_variable(self, input_variable, t):
        Melmag = self.p*self.D*self.l*self.wr*(input_variable[3]*B_delta(self.N, input_variable[0], input_variable[1], input_variable[2], input_variable[3], input_variable[4], input_variable[5], self.tau/np.pi*input_variable[7]*self.p-self.tau/2, input_variable[7], self.mu0, self.delta, self.wc, self.wr, self.tau, self.p)+input_variable[4]*B_delta(self.N, input_variable[0], input_variable[1], input_variable[2], input_variable[3], input_variable[4], input_variable[5], self.tau/np.pi*input_variable[7]*self.p+self.tau/6, input_variable[7], self.mu0, self.delta, self.wc, self.wr, self.tau, self.p)+input_variable[5]*B_delta(self.N, input_variable[0], input_variable[1], input_variable[2], input_variable[3], input_variable[4], input_variable[5], self.tau/np.pi*input_variable[7]*self.p-7*self.tau/6, input_variable[7], self.mu0, self.delta, self.wc, self.wr, self.tau, self.p))
        additional_variable = np.array([
                            (-1*1000*line_func(self.list_params[0], (100*np.pi/self.p - input_variable[6])/(100*np.pi/self.p)*100) - Melmag)/self.J,
                            input_variable[6]
                            ], dtype = self.data_type) 
        
        return additional_variable

    def set_primary_parameters(self):
        if (self.secondary_parameters != ["Нет данных"] * len(self.list_text_secondary_parameters)):
            self.Un = np.float64(self.secondary_parameters[0]*1000)
            self.p = np.float64(self.secondary_parameters[1])

            C = (self.secondary_parameters[2] + np.sqrt(self.secondary_parameters[2]**2 + 4*self.secondary_parameters[2]*self.secondary_parameters[6]))/(2*self.secondary_parameters[2])
            self.Rc = self.secondary_parameters[4]/C
            self.Rr = self.secondary_parameters[5]/C/self.secondary_parameters[3]**2

            self.Lcs = self.secondary_parameters[6]/C/(100*np.pi)
            self.Lrs = self.secondary_parameters[7]/C/self.secondary_parameters[3]**2/(100*np.pi)

            self.l = np.float64(self.secondary_parameters[8])
            self.D = np.float64(self.secondary_parameters[9])
            self.delta = np.float64(self.secondary_parameters[10])
            self.tau = np.pi*self.D/(2*self.p)

            self.wc = np.sqrt(self.secondary_parameters[2]*self.delta*np.pi/(4*1*3*50*self.mu0*self.tau*self.l*self.p))
            self.wr = self.wc / self.secondary_parameters[3]

            self.J = np.float64(self.secondary_parameters[11])

            self.Kcc = (4*self.wc*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)
            self.Krc = (4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)
            self.Krr = (4*self.wr*self.wr*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)


            print(self.J)
    def set_control_actions_help(self):
        s = np.linspace(-0.5, 1, 1000)
        M = []
        Mn = []
        for i in s:
            Mn.append(1000*line_func(self.list_params[0], 100*i))
            M.append(self.p*self.Un**2*self.Rr*(1+line_func(self.list_params[1],i*100))*(self.wc/self.wr)**2/i/100/np.pi/((self.Rc+self.Rr*(1+line_func(self.list_params[1],i*100))*(self.wc/self.wr)**2/i)**2+(100*np.pi*(self.Lcs + (self.wc/self.wr)**2*self.Lrs))**2))
        #fig, axs = plt.subplots(2)
        #plt.subplots_adjust(left=0.04, right=0.96, top = 0.96, bottom= 0.04, hspace=0)
        #fig.suptitle('Vertically stacked subplots')
        #axs[0].plot(s, M, linewidth=1, color='red')
        #axs[0].plot(s, Mn, linewidth=1, color='red')
        #axs[0].grid(True)

        plt.plot(s, M, linewidth=1, color='red')
        plt.plot(s, Mn, linewidth=1, color='blue')
        plt.grid()

        plt.show()
