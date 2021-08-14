import math
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

def create_image_for_model(pass_obj, k_size):
    buff_image = ImageTk.PhotoImage(Image.open(pass_obj))
    width_image = buff_image.width()/k_size
    image = ImageTk.PhotoImage(Image.open(pass_obj).resize((int(width_image), int((width_image)*buff_image.height()/buff_image.width())), Image.ANTIALIAS))
    #imagesprite2 = canv.create_image(WIDTH/2,HEIGHT/2,image=image2)
    return image

class Wire:
    def __init__(self, canv, x0, y0, text_tag):
        self.text_tag = text_tag
        self.canv = canv
        self.activity = True
        self.coords_wire = [[x0, y0], [x0, y0]]
        self.canvas_object_wire = [canv.create_line(x0, y0, x0, y0, dash = (5, 5), width = 1, fill = "red")]

    def move_end_wire(self, m_x, m_y, list_nodes, WIDTH, HEIGHT):
        if self.activity:
            try:
                if (math.fabs((m_x - self.coords_wire[-2][0])/(m_y - self.coords_wire[-2][1])) <= 1):
                    may_nodes = []
                    for i in list_nodes:
                        if ((i.position == 1) and (self.coords_wire[-2][0] > i.x) and (self.coords_wire[-2][0] < i.x + i.image_width)):
                            may_nodes.append(i)
                    find_own_bus = False
                    if (m_y < self.coords_wire[-2][1]):
                        max_y = -1
                        for i in may_nodes:
                            if ((i.y < self.coords_wire[-2][1]) and (i.y > max_y)):
                                max_y = i.y
                                self.coords_wire[-1][0] = self.coords_wire[-2][0]
                                self.coords_wire[-1][1] = i.y + i.image_height/2
                                find_own_bus = True

                    if (m_y > self.coords_wire[-2][1]):
                        min_y = HEIGHT + 1
                        for i in may_nodes:
                            if ((i.y > self.coords_wire[-2][1]) and (i.y < min_y)):
                                min_y = i.y
                                self.coords_wire[-1][0] = self.coords_wire[-2][0]
                                self.coords_wire[-1][1] = i.y + i.image_height/2
                                find_own_bus = True
                    if not find_own_bus:
                        self.coords_wire[-1][0] = self.coords_wire[-2][0]
                        self.coords_wire[-1][1] = m_y
                if (math.fabs((m_x - self.coords_wire[-2][0])/(m_y - self.coords_wire[-2][1])) > 1):
                    may_nodes = []
                    for i in list_nodes:
                        if ((i.position == 0) and (self.coords_wire[-2][1] > i.y) and (self.coords_wire[-2][1] < i.y + i.image_height)):
                            may_nodes.append(i)
                    find_own_bus = False
                    if (m_x < self.coords_wire[-2][0]):
                        max_x = -1
                        for i in may_nodes:
                            if ((i.x < self.coords_wire[-2][0]) and (i.x > max_x)):
                                max_x = i.x
                                self.coords_wire[-1][0] = i.x + i.image_width/2
                                self.coords_wire[-1][1] = self.coords_wire[-2][1]
                                find_own_bus = True

                    if (m_x > self.coords_wire[-2][0]):
                        min_x = WIDTH + 1
                        for i in may_nodes:
                            if ((i.x > self.coords_wire[-2][0]) and (i.x < min_x)):
                                min_x = i.x
                                self.coords_wire[-1][0] = i.x + i.image_width/2
                                self.coords_wire[-1][1] = self.coords_wire[-2][1]
                                find_own_bus = True

                    if not find_own_bus:
                        self.coords_wire[-1][0] = m_x
                        self.coords_wire[-1][1] = self.coords_wire[-2][1]

            except ZeroDivisionError:
                pass

            self.canv.coords(self.canvas_object_wire[-1], self.coords_wire[-2][0], self.coords_wire[-2][1],  self.coords_wire[-1][0], self.coords_wire[-1][1])

    def add_wire_node(self, m_x, m_y):
        if self.activity:
            self.coords_wire.append([m_x, m_y])
            self.canvas_object_wire.append(self.canv.create_line(self.coords_wire[-2][0], self.coords_wire[-2][1], m_x, m_y, dash = (5, 5), width = 1, fill = "red"))

    def set_connection(self, bus_x, bus_y, bus_width, bus_height):
        if ((self.coords_wire[-1][0] > bus_x) and (self.coords_wire[-1][1] > bus_y) and (self.coords_wire[-1][0] < bus_x + bus_width) and (self.coords_wire[-1][1] < bus_y + bus_height)):
            if self.activity:
                self.activity = False
                for i in self.canvas_object_wire:
                    self.canv.delete(i)
                self.canvas_object_wire = []
                for i in range(len(self.coords_wire) - 1):
                    w_x, w_y = self.coords_wire[i]
                    w_x_new, w_y_new = self.coords_wire[i + 1]
                    self.canvas_object_wire.append(self.canv.create_line(w_x, w_y, w_x_new, w_y_new, width = 3.5))

            return self.text_tag
        else:
            return "none"

    def block_click_bus(self, bus_x, bus_y, bus_width, bus_height):
        if ((self.coords_wire[-1][0] > bus_x) and (self.coords_wire[-1][1] > bus_y) and (self.coords_wire[-1][0] < bus_x + bus_width) and (self.coords_wire[-1][1] < bus_y + bus_height)):
            return self.activity
        else:
            return False

    def delete_wire(self):
        for i in self.canvas_object_wire:
            self.canv.delete(i)
        self.coords_wire = []

class Base_model:

    def __init__(self, init_x, init_y, canv, root, path_to_image_model, dxdy, position, list_nodes, 
    list_graph, list_text_secondary_parameters, initial_secondary_parameters, list_text_example_models, list_example_parameters):

        self.list_example_parameters = list_example_parameters
        self.list_text_example_models = list_text_example_models
        self.list_text_secondary_parameters = list_text_secondary_parameters
        if (initial_secondary_parameters == None):
            self.secondary_parameters = ["Нет данных"] * len(self.list_text_secondary_parameters)
        else:
            self.secondary_parameters = initial_secondary_parameters
            self.set_primary_parameters()
        self.list_graph = list_graph
        self.list_nodes = list_nodes
        self.canv = canv
        self.root = root
        self.k_size = 6
        self.dxdy = []
        for i in range(len(dxdy)):
            self.dxdy.append([])
            for j in range(len(dxdy[i])):
                self.dxdy[-1].append([])
                for n in dxdy[i][j]:
                    self.dxdy[-1][-1].append(int(n / self.k_size))

        self.position = position
        self.connection_coords = self.dxdy[self.position]
        self.path_to_image_model = path_to_image_model
        self.image_model_data = create_image_for_model(path_to_image_model + str(self.position) + ".png", self.k_size)
        self.image_width = self.image_model_data.width()
        self.image_height = self.image_model_data.height()
        self.x = init_x
        self.y = init_y
        self.image_model = self.canv.create_image(self.x,self.y,image = self.image_model_data, anchor = 'nw')

        self.list_wires = ["not exist"] * len(self.list_nodes)
        self.state_click = 0 #
        self.k_click = 0.0 #
        self.quad_indication_create = False #
        self.data_type = np.float64

    #def __del__(self):
    #    print("111111")

    def set_state_click(self, m_x, m_y):
        if ((m_x >= self.x + self.k_click*self.image_width) and (m_x <= self.x + self.image_width - self.k_click*self.image_width) and (m_y >= self.y + self.k_click*self.image_height) and (m_y <= self.y + self.image_height - self.k_click*self.image_height) and (self.bool_mouse_in_area == False)):
            if (self.state_click  == 0):
                self.click_indication = self.canv.create_rectangle(self.x, self.y, self.x + self.image_width, self.y + self.image_height, width = 2, outline = "red")
                self.state_click = 1
                self.delta_x = m_x - self.x
                self.delta_y = m_y - self.y
            else:
                self.canv.delete(self.click_indication)
                self.state_click = 0 

    def delete_all_wires(self):
        for i in self.list_wires:
            if (i != "not exist"):
                i.delete_wire()
        self.list_wires = ["not exist"] * len(self.list_nodes)
            
    def move_model(self, m_x, m_y):
        if (self.state_click  == 1):
            self.canv.coords(self.image_model, m_x - self.delta_x, m_y - self.delta_y)
            self.x = m_x - self.delta_x
            self.y = m_y - self.delta_y
            self.canv.coords(self.click_indication, self.x, self.y, self.x + self.image_width, self.y + self.image_height) 
            self.delete_all_wires()
    
    def indication_wire_connection(self, m_x, m_y):
        size_area_indication = 10
        self.bool_mouse_in_area = False
        for dx, dy in self.connection_coords:
            if ((m_x > self.x + dx - size_area_indication) and (m_y > self.y + dy - size_area_indication)
            and (m_x < self.x + dx + size_area_indication) and (m_y < self.y + dy + size_area_indication)):
                self.bool_mouse_in_area = True
                if (self.quad_indication_create == False):
                    self.quad_indication = self.canv.create_rectangle(self.x + dx - size_area_indication, self.y + dy - size_area_indication, 
                    self.x + dx + size_area_indication, self.y + dy + size_area_indication, width = 2, outline = "red")
                    self.quad_indication_create = True
        if (self.bool_mouse_in_area == False):
            if (self.quad_indication_create == True):
                self.canv.delete(self.quad_indication)
                self.quad_indication_create = False

    def wire_connection(self, m_x, m_y):
        size_area_indication = 10
        for i in range(len(self.connection_coords)):
            dx, dy = self.connection_coords[i]
            if ((m_x > self.x + dx - size_area_indication) and (m_y > self.y + dy - size_area_indication)
            and (m_x < self.x + dx + size_area_indication) and (m_y < self.y + dy + size_area_indication)):
                if (self.list_wires[i] == "not exist"):
                    self.list_wires[i] = Wire(self.canv, self.x + dx, self.y + dy, self.list_nodes[i])
                else:
                    self.list_wires[i].delete_wire()
                    self.list_wires[i] = Wire(self.canv, self.x + dx, self.y + dy, self.list_nodes[i])

    def rotation(self, m_x, m_y):
        if (self.state_click == 1):
            self.position += 1
            if (self.position > 3):
                self.position = 0
            self.image_model_data = create_image_for_model(self.path_to_image_model + str(self.position) + ".png", self.k_size)
            self.image_width = self.image_model_data.width()
            self.image_height = self.image_model_data.height()
            self.canv.delete(self.image_model)
            self.delta_x = self.image_width/2
            self.delta_y = self.image_height/2
            self.image_model = self.canv.create_image(m_x - self.k_click*self.image_width, m_y - self.k_click*self.image_height,image = self.image_model_data, anchor = 'nw')
            self.canv.coords(self.click_indication, m_x - self.k_click*self.image_width, m_y - self.k_click*self.image_height, m_x - self.k_click*self.image_width + self.image_width, m_y - self.k_click*self.image_height + self.image_height) 

            self.connection_coords = self.dxdy[self.position]
            for i in self.list_wires:
                    if (i != "not exist"):
                        i.delete_wire()
            self.list_wires = ["not exist"] * len(self.list_nodes)

    def view_results(self):
        fig, axs = plt.subplots(len(self.list_graph))
        plt.subplots_adjust(left=0.04, right=0.96, top = 0.96, bottom= 0.04, hspace=0)
        fig.suptitle('Vertically stacked subplots')
        counter_g = 0
        for i in self.list_graph:
            axs[counter_g].plot(self.t, self.list_results[i], linewidth=1, color='red')
            axs[counter_g].grid(True)
            counter_g += 1

        plt.show()


        #for i in range(math.ceil(len(self.list_results)/4)):
        #    root_graph = Toplevel(self.root)
        #    root_graph.title("Выбор моделей")

        #    if (i == (math.ceil(len(self.list_results)/4) - 1)):
        #        number_of_gr = len(self.list_results) - 4 * i
        #    else:
        #        number_of_gr = 4

        #    fig = Figure(figsize=(15, 10), dpi=100)

        #    for j in range(number_of_gr):
        #        fig.add_subplot(221 + j).plot(self.t, self.list_results[4*i + j], linewidth=1, color='red')

        #    canvas = FigureCanvasTkAgg(fig, master=root_graph)  # A tk.DrawingArea.
        #    canvas.draw()
        #    canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand=1)

    def context_menu(self, m_x, m_y):
        if ((m_x >= self.x + self.k_click*self.image_width) and (m_x <= self.x + self.image_width - self.k_click*self.image_width) and (m_y >= self.y + self.k_click*self.image_height) and (m_y <= self.y + self.image_height - self.k_click*self.image_height) and (self.bool_mouse_in_area == False)):
            return True

    def set_secondary_parameters(self):
        def on_closing():
            if (list_example.current() == 0):
                for i in range(len(self.list_text_secondary_parameters)):
                    try:
                        self.secondary_parameters[i] = float(list_string_variable[i].get())
                    except ValueError:
                        self.secondary_parameters[i] = list_string_variable[i].get()
            else:
                for i in range(len(self.list_text_secondary_parameters)):
                    self.secondary_parameters[i] = self.list_example_parameters[list_example.current()-1][i]
            self.set_primary_parameters()
            secondary_parameters_window.destroy()

        secondary_parameters_window = Toplevel(self.root, bg = "white")
        secondary_parameters_window.title("Выбор параметров модели")
        secondary_parameters_window.protocol("WM_DELETE_WINDOW", on_closing)

        def ComboboxSelected(event):
            if (list_example.current() != 0):
                for i in range(len(list_string_variable)):
                    list_string_variable[i].set(str(round(self.list_example_parameters[list_example.current()-1][i], 5)))
            
        list_example = ttk.Combobox(secondary_parameters_window, values = self.list_text_example_models,state="readonly", font=('GOST Type A', 16), width= 16)
        list_example.bind("<<ComboboxSelected>>", ComboboxSelected)
        list_example.current(0)
        list_string_variable = []

        ttk.Separator(secondary_parameters_window, orient=VERTICAL).grid(column=1, row=0, rowspan=len(self.list_text_secondary_parameters)*2 + 2, sticky='ns') 

        for i in range(len(self.list_text_secondary_parameters)):
            ttk.Separator(secondary_parameters_window, orient=HORIZONTAL).grid(column=0, row=2*i, columnspan=3, sticky='ew')
            for j in [0, 2]:
                if (j == 0):
                    label = Label(master= secondary_parameters_window, text=self.list_text_secondary_parameters[i], font=('GOST Type A', 16), bg= "white")
                    label.grid(row=i*2 + 1, column=j)
                else:
                    try:
                        list_string_variable.append(StringVar(value=str(round(self.secondary_parameters[i], 5))))
                    except TypeError:
                        list_string_variable.append(StringVar(value=self.secondary_parameters[i]))
                    entry = Entry(secondary_parameters_window, textvariable = list_string_variable[-1], width=10,
                        font=('GOST Type A', 14), relief = FLAT, justify = CENTER)
                    entry.grid(row=i*2 + 1, column=j)
        ttk.Separator(secondary_parameters_window, orient=HORIZONTAL).grid(column=0, row=len(self.list_text_secondary_parameters)*2, columnspan=3, sticky='ew')
        label = Label(master= secondary_parameters_window, text="Выбрать из справочника", font=('GOST Type A', 16), bg= "white")
        label.grid(row=len(self.list_text_secondary_parameters)*2 + 1, column=0)
        list_example.grid(row=len(self.list_text_secondary_parameters)*2 + 1, column=2)

    def set_control_actions(self):
        control_actions_window = Toplevel(self.root, bg = "white")
        control_actions_window.title("Выбор управляющих воздействий")

        label = Label(master= control_actions_window, text="Время, с", font=('GOST Type A', 16), bg= "white")
        label.grid(row=0, column=0)
        label = Label(master= control_actions_window, text="Параметр", font=('GOST Type A', 16), bg= "white")
        label.grid(row=2, column=0)

        for j in range(5):
            ttk.Separator(control_actions_window, orient=VERTICAL).grid(column=1 + 2*j, row=0, rowspan=3, sticky='ns')

        for i in [0, 2]:
            for j in range(5):
                entry = Entry(control_actions_window, width=5,
                            font=('GOST Type A', 14), relief = FLAT, justify = CENTER)
                entry.grid(row=i, column=2*j + 1 + 1, padx = 15)

        ttk.Separator(control_actions_window, orient=HORIZONTAL).grid(column=0, row=1, columnspan=11, sticky='ew')       
        

    def delete_model(self):
        self.canv.delete(self.image_model)
        self.delete_all_wires()