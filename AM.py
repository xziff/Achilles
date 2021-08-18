import math
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from scipy. integrate import odeint
import numpy as np

from base_model import Base_model

def line_func(list_points, t):
    for i in range(len(list_points[0]) - 1):
        if ((t >= list_points[0][i]) and (t <= list_points[0][i+1])):
            return np.float64(list_points[1][i] + (list_points[1][i+1]-list_points[1][i])/(list_points[0][i+1]-list_points[0][i])*(t - list_points[0][i]))

def B_delta(Ica, Icb, Icc, Ira, Irb, Irc, x, phi, mu0, delta, wc, wr, tau, p):
    return (2*mu0/(np.pi*delta)*(wc*Ica*np.cos(np.pi/tau*x)+wc*Icb*np.cos(np.pi/tau*x-2*np.pi/3)+wc*Icc*np.cos(np.pi/tau*x+2*np.pi/3)+wr*Ira*np.cos(np.pi/tau*x-phi*p)+wr*Irb*np.cos(np.pi/tau*x-phi*p-2*np.pi/3)+wr*Irc*np.cos(np.pi/tau*x-phi*p+2*np.pi/3)))

coord = [
    [[8, 171]],
    [[189, 10]],
    [[595, 175]],
    [[193, 745]]]

list_nodes = ["Q:ON_SWITCH"]

list_graph = [0, 3, 6]

list_text_secondary_parameters = ["Номинальное напряжение, кВ:",
    "Число пар полюсов, шт:",
    "Главное индуктивное сопротивление обмотки статора, Ом:",
    "Коэффициент трансформации:",
    "Активное сопротивление обмотки статора, Ом:",
    "Активное сопротивление обмотки ротора, Ом:",
    "Индуктивность поля рассеяния обмотки статора, Гн:",
    "Индуктивность поля рассеяния обмотки ротора, Гн:",
    "Длина машины, м:",
    "Полюсное деление машины, м:",
    "Длина воздушного зазора, м:",
    "Момент инерции ротора, кг*м2:"]

list_text_example_models = [
    "Пользовательский",
    "АК-2000-6"]

list_example_parameters = [[6, 3, 50.8, 4.05, 0.133, 0.00954,  0.0004776, 0.0003096, 0.57, np.pi*0.795/6, 0.0018, 200]]

list_text_control_actions = {"Нагрузочный момент": ["s, %", "M(s), кН*м"], "Сопротивление реостата, доли Rr": ["s, %", "N(s), о.е."]}

list_text_initial_conditions = ["Ток фазы 'А' статора, А",
    "Ток фазы 'B' статора, А",
    "Ток фазы 'C' статора, А",
    "Ток фазы 'А' ротора, А",
    "Ток фазы 'B' ротора, А",
    "Ток фазы 'C' ротора, А",
    "Частота вращения ротора, рад/с",
    "Угол поворота ротора, рад"]

class AM(Base_model):

    def __init__(self, init_x, init_y, position, canv, root, initial_list_wires, initial_control_actions, initial_initial_conditions, initial_secondary_parameters):

        Base_model.__init__(self, init_x, init_y, canv, root, "Image/AM/", coord, position, list_nodes, list_graph, list_text_secondary_parameters, initial_secondary_parameters, list_text_example_models, list_example_parameters, list_text_control_actions, list_text_initial_conditions, initial_control_actions, initial_initial_conditions, initial_list_wires)

        self.width_input = 8
        self.width_matrix = 6
        self.height_matrix = 6

    def get_main_determinant(self, input_variable, t):
        main_determinant = np.array([[-(4*self.wc*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*(np.sin(np.pi/2) - (-1)*np.sin(np.pi/6)) - self.Lcs, -(4*self.wc*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*(np.sin(np.pi/2 + 2*np.pi/3) - (-1)*np.sin(np.pi/6 - 2*np.pi/3)) + self.Lcs, -(4*self.wc*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*(np.sin(np.pi/2 - 2*np.pi/3) - (-1)*np.sin(np.pi/6 + 2*np.pi/3)), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*(np.sin(np.pi/2 + input_variable[7]*self.p) - (-1)*np.sin(np.pi/6 - input_variable[7]*self.p)), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*(np.sin(np.pi/2 + input_variable[7]*self.p + 2*np.pi/3) - (-1)*np.sin(np.pi/6 - input_variable[7]*self.p - 2*np.pi/3)), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*(np.sin(np.pi/2 + input_variable[7]*self.p - 2*np.pi/3) - (-1)*np.sin(np.pi/6 - input_variable[7]*self.p + 2*np.pi/3))],
                    [-(4*self.wc*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*((-1)*np.sin(np.pi/6) - np.sin(-np.pi/6)), -(4*self.wc*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*((-1)*np.sin(np.pi/6 - 2*np.pi/3) - np.sin(-np.pi/6 - 2*np.pi/3)) - self.Lcs, -(4*self.wc*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*((-1)*np.sin(np.pi/6 + 2*np.pi/3) - np.sin(-np.pi/6 + 2*np.pi/3)) + self.Lcs, -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*((-1)*np.sin(np.pi/6 - input_variable[7]*self.p) - np.sin(-np.pi/6 - input_variable[7]*self.p)), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*((-1)*np.sin(np.pi/6 - input_variable[7]*self.p - 2*np.pi/3) - np.sin(-np.pi/6 - input_variable[7]*self.p - 2*np.pi/3)), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*((-1)*np.sin(np.pi/6 - input_variable[7]*self.p + 2*np.pi/3) - np.sin(-np.pi/6 - input_variable[7]*self.p + 2*np.pi/3))],
                    [-(4*self.wc*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*np.sin(-np.pi/6), -(4*self.wc*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*np.sin(-np.pi/6 - 2*np.pi/3), -(4*self.wc*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*np.sin(-np.pi/6 + 2*np.pi/3) - self.Lcs, -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*np.sin(-np.pi/6 - input_variable[7]*self.p), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*np.sin(-np.pi/6 - input_variable[7]*self.p - 2*np.pi/3), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*np.sin(-np.pi/6 - input_variable[7]*self.p + 2*np.pi/3)],
                    [-(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*np.sin(np.pi/2-input_variable[7]*self.p-0), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*np.sin(np.pi/2-input_variable[7]*self.p+2*np.pi/3), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*np.sin(np.pi/2-input_variable[7]*self.p-2*np.pi/3), -(4*self.wr*self.wr*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*np.sin(np.pi/2-0) - self.Lrs, -(4*self.wr*self.wr*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*np.sin(np.pi/2+2*np.pi/3), -(4*self.wr*self.wr*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*np.sin(np.pi/2-2*np.pi/3)],
                    [-(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*(-1)*np.sin(np.pi/6+input_variable[7]*self.p-0), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*(-1)*np.sin(np.pi/6+input_variable[7]*self.p-2*np.pi/3), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*(-1)*np.sin(np.pi/6+input_variable[7]*self.p+2*np.pi/3), -(4*self.wr*self.wr*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*(-1)*np.sin(np.pi/6+0), -(4*self.wr*self.wr*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*(-1)*np.sin(np.pi/6-2*np.pi/3) - self.Lrs, -(4*self.wr*self.wr*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*(-1)*np.sin(np.pi/6+2*np.pi/3)],
                    [-(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*np.sin(-np.pi/6+input_variable[7]*self.p-0), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*np.sin(-np.pi/6+input_variable[7]*self.p-2*np.pi/3), -(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*np.sin(-np.pi/6+input_variable[7]*self.p+2*np.pi/3), -(4*self.wr*self.wr*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*np.sin(-np.pi/6+0), -(4*self.wr*self.wr*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*np.sin(-np.pi/6-2*np.pi/3), -(4*self.wr*self.wr*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*np.sin(-np.pi/6+2*np.pi/3) - self.Lrs]
                   ], dtype = self.data_type)                    
        return main_determinant

    def get_own_matrix(self, input_variable, t):
        own_matrix = np.array([input_variable[0]*self.Rc - input_variable[1]*self.Rc + (4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*input_variable[6]*self.p*(input_variable[3]*np.cos(np.pi/2 + input_variable[7]*self.p) + input_variable[4]*np.cos(np.pi/2 + input_variable[7]*self.p + 2*np.pi/3) + input_variable[5]*np.cos(np.pi/2 + input_variable[7]*self.p - 2*np.pi/3) + (-1)*input_variable[3]*np.cos(np.pi/6 - input_variable[7]*self.p) + (-1)*input_variable[4]*np.cos(np.pi/6 - input_variable[7]*self.p - 2*np.pi/3) + (-1)*input_variable[5]*np.cos(np.pi/6 - input_variable[7]*self.p + 2*np.pi/3)),
                    input_variable[1]*self.Rc - input_variable[2]*self.Rc + (4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*input_variable[6]*self.p*(input_variable[3]*np.cos(np.pi/6 - input_variable[7]*self.p) + input_variable[4]*np.cos(np.pi/6 - input_variable[7]*self.p - 2*np.pi/3) + input_variable[5]*np.cos(np.pi/6 - input_variable[7]*self.p + 2*np.pi/3) + input_variable[3]*np.cos(-np.pi/6 - input_variable[7]*self.p) + input_variable[4]*np.cos(-np.pi/6 - input_variable[7]*self.p - 2*np.pi/3) + input_variable[5]*np.cos(-np.pi/6 - input_variable[7]*self.p + 2*np.pi/3)),
                    input_variable[2]*self.Rc - (4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*input_variable[6]*self.p*(input_variable[3]*np.cos(-np.pi/6 - input_variable[7]*self.p) + input_variable[4]*np.cos(-np.pi/6 - input_variable[7]*self.p - 2*np.pi/3) + input_variable[5]*np.cos(-np.pi/6 - input_variable[7]*self.p + 2*np.pi/3)),
                    input_variable[3]*self.Rr*(1+line_func(self.list_params[1], (100*np.pi/self.p - input_variable[6])/(100*np.pi/self.p)*100))-input_variable[6]*self.p*(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*(input_variable[0]*np.cos(np.pi/2-input_variable[7]*self.p)+input_variable[1]*np.cos(np.pi/2-input_variable[7]*self.p+2*np.pi/3)+input_variable[2]*np.cos(np.pi/2-input_variable[7]*self.p-2*np.pi/3)),
                    input_variable[4]*self.Rr*(1+line_func(self.list_params[1], (100*np.pi/self.p - input_variable[6])/(100*np.pi/self.p)*100))+input_variable[6]*self.p*(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*(-1)*(input_variable[0]*np.cos(np.pi/6+input_variable[7]*self.p)+input_variable[1]*np.cos(np.pi/6+input_variable[7]*self.p-2*np.pi/3)+input_variable[2]*np.cos(np.pi/6+input_variable[7]*self.p+2*np.pi/3)),
                    input_variable[5]*self.Rr*(1+line_func(self.list_params[1], (100*np.pi/self.p - input_variable[6])/(100*np.pi/self.p)*100))+input_variable[6]*self.p*(4*self.wr*self.wc*self.tau*self.l*self.mu0*self.p)/(np.pi*self.delta*np.pi)*(input_variable[0]*np.cos(-np.pi/6+input_variable[7]*self.p)+input_variable[1]*np.cos(-np.pi/6+input_variable[7]*self.p-2*np.pi/3)+input_variable[2]*np.cos(-np.pi/6+input_variable[7]*self.p+2*np.pi/3))
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
        Melmag = self.p*2*self.p*self.tau/np.pi*self.l*self.wr*(input_variable[3]*B_delta(input_variable[0], input_variable[1], input_variable[2], input_variable[3], input_variable[4], input_variable[5], self.tau/np.pi*input_variable[7]*self.p-self.tau/2, input_variable[7], self.mu0, self.delta, self.wc, self.wr, self.tau, self.p)+input_variable[4]*B_delta(input_variable[0], input_variable[1], input_variable[2], input_variable[3], input_variable[4], input_variable[5], self.tau/np.pi*input_variable[7]*self.p+self.tau/6, input_variable[7], self.mu0, self.delta, self.wc, self.wr, self.tau, self.p)+input_variable[5]*B_delta(input_variable[0], input_variable[1], input_variable[2], input_variable[3], input_variable[4], input_variable[5], self.tau/np.pi*input_variable[7]*self.p-7*self.tau/6, input_variable[7], self.mu0, self.delta, self.wc, self.wr, self.tau, self.p))
        additional_variable = np.array([
                            (-1*1000*line_func(self.list_params[0], (100*np.pi/self.p - input_variable[6])/(100*np.pi/self.p)*100) - Melmag)/self.J,
                            input_variable[6]
                            ], dtype = self.data_type) 
        return additional_variable

    def set_primary_parameters(self):
        if (self.secondary_parameters != ["Нет данных"] * len(self.list_text_secondary_parameters)):
            self.Un = np.float64(self.secondary_parameters[0]*1000)
            self.p = np.float64(self.secondary_parameters[1])
            self.Rc = np.float64(self.secondary_parameters[4])
            self.Rr = np.float64(self.secondary_parameters[5])
            self.Lcs = np.float64(self.secondary_parameters[6])
            self.Lrs = np.float64(self.secondary_parameters[7])
            self.l = np.float64(self.secondary_parameters[8])
            self.tau = np.float64(self.secondary_parameters[9])
            self.delta = np.float64(self.secondary_parameters[10])
            self.J = np.float64(self.secondary_parameters[11])
            self.wc = np.float64(23.14)
            self.wr = np.float64(5.71)

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
