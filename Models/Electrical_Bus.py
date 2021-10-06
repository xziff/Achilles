import math
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from scipy. integrate import odeint
import numpy as np

k_size = 7
state_menu = 0
def create_image_for_model(pass_obj):
    buff_image = ImageTk.PhotoImage(Image.open(pass_obj))
    width_image = buff_image.width()/k_size
    image = ImageTk.PhotoImage(Image.open(pass_obj).resize((int(width_image), int((width_image)*buff_image.height()/buff_image.width())), Image.ANTIALIAS))
    #imagesprite2 = canv.create_image(WIDTH/2,HEIGHT/2,image=image2)
    return image

n_fig = 1
    
class Electrical_Bus:
    state_click = 0
    k_expand = 7
    number_of_connection = 0

    def __init__(self, init_x, init_y, position, canv, root):
        self.canv = canv
        self.root = root
        self.position = position
        self.image_model_data = create_image_for_model("Image/Electrical Bus/" + str(self.position) + ".png")
        self.image_width = self.image_model_data.width()
        self.image_height = self.image_model_data.height()
        self.x = init_x
        self.y = init_y
        self.image_model = self.canv.create_image(self.x,self.y,image = self.image_model_data, anchor = 'nw')
        self.model_text = self.canv.create_text(self.x, self.y, text = str(self.number_of_connection), fill = "black", font = ("GOST Type A", "14"), anchor="sw")   
  
        self.list_indications = []
        self.create_rect_indication_outline_selection = False #
        self.replace_state = False

    def __del__(self):
        try:
            self.canv.delete(self.model_text)
        except TclError:
            pass
        
    def control_connection(self, models):
        if (self.state_click  == 0):
            self.list_connection = []
            self.number_of_connection = 0
            for i in range(len(models)):
                self.list_connection.append([])
                for j in models[i]:
                    if (j != "Deleted"):
                        buff_tag = "none"
                        for k in j.list_wires:
                            if ((k != "not exist") and (k.set_connection(self.x, self.y, self.image_width, self.image_height) != "none")):
                                buff_tag = k.set_connection(self.x, self.y, self.image_width, self.image_height)
                        self.list_connection[i].append(buff_tag)
                    else:
                        self.list_connection[i].append("none")

            for i in self.list_connection:
                for j in i:
                    if (j != "none"):
                        self.number_of_connection += 1

            #print(self.list_connection)
            self.canv.delete(self.model_text)
            self.model_text = self.canv.create_text(self.x, self.y, text = str(self.number_of_connection), fill = "black", font = ("GOST Type A", "14"), anchor="sw")

    def set_state_click(self, m_x, m_y, list_models):
        bool_activity = False
        for i in list_models:
            for j in i:
                for k in j.list_wires:
                    if (k != "not exist"):
                        if (k.block_click_bus(self.x, self.y, self.image_width, self.image_height) != False):
                            bool_activity = k.block_click_bus(self.x, self.y, self.image_width, self.image_height)

        if ((m_x > self.x) and (m_x < self.x + self.image_width) and (m_y > self.y) and (m_y < self.y + self.image_height) and (bool_activity == False)):
            if (self.state_click  == 0):
                self.state_click = 1
                self.delta_x = m_x - self.x
                self.delta_y = m_y - self.y
            else:
                self.state_click = 0

    def rotation(self, m_x, m_y):
        if (self.state_click == 1):
            self.position += 1
            if (self.position > 1):
                self.position = 0
            self.image_model_data = create_image_for_model("Image/Electrical Bus/" + str(self.position) + ".png")
            self.image_width = self.image_model_data.width()
            self.image_height = self.image_model_data.height()
            self.canv.delete(self.image_model)
            self.delta_x = self.image_width/2
            self.delta_y = self.image_height/2 
            self.image_model = self.canv.create_image(m_x - self.delta_x, m_y - self.delta_y,image = self.image_model_data, anchor = 'nw')


    def expand_image_model(self, m_x, m_y):
        if (self.state_click == 1):
            if (self.position == 0):
                buff_image = ImageTk.PhotoImage(Image.open("Image/Electrical Bus/0.png"))
                width_image = buff_image.width()/k_size
                height_image = self.image_model_data.height() + self.k_expand
                self.image_model_data = ImageTk.PhotoImage(Image.open("Image/Electrical Bus/0.png").resize((int(width_image), int(height_image)), Image.ANTIALIAS))
                self.x = m_x - self.delta_x
                self.y = m_y - self.delta_y
                self.image_width = self.image_model_data.width()
                self.image_height = self.image_model_data.height()
                self.canv.delete(self.image_model)
                self.image_model = self.canv.create_image(self.x, self.y ,image = self.image_model_data, anchor = 'nw')
            if (self.position == 1):
                buff_image = ImageTk.PhotoImage(Image.open("Image/Electrical Bus/1.png"))
                height_image = (buff_image.width()/k_size)*buff_image.height()/buff_image.width()
                width_image = self.image_model_data.width() + self.k_expand
                self.image_model_data = ImageTk.PhotoImage(Image.open("Image/Electrical Bus/1.png").resize((int(width_image), int(height_image)), Image.ANTIALIAS))
                self.x = m_x - self.delta_x
                self.y = m_y - self.delta_y
                self.image_width = self.image_model_data.width()
                self.image_height = self.image_model_data.height()
                self.canv.delete(self.image_model)
                self.image_model = self.canv.create_image(self.x, self.y ,image = self.image_model_data, anchor = 'nw')
        
    def move_model(self, m_x, m_y):
        if (self.state_click  == 1):
            self.canv.coords(self.image_model, m_x - self.delta_x, m_y - self.delta_y)
            self.canv.coords(self.model_text, m_x - self.delta_x, m_y - self.delta_y)
            self.x = m_x - self.delta_x           
            self.y = m_y - self.delta_y
            if self.replace_state:
                self.canv.coords(self.rect_indication_outline_selection, self.x, self.y, self.x + self.image_width, self.y + self.image_height)
            else:
                pass

    def indication_for_wire_on(self, WIDTH, HEIGTH):
        color = "blue"
        if (self.position == 0):
            if (len(self.list_indications) == 0):
                self.list_indications = []
                self.list_indications.append(self.canv.create_line(0, self.y, WIDTH, self.y, dash = (5, 5), width = 1, fill = color))
                #self.list_indications.append(self.canv.create_line(0, self.y + self.image_height/2, WIDTH, self.y + self.image_height/2, dash = (5, 5), width = 1, fill = color))
                self.list_indications.append(self.canv.create_line(0, self.y + self.image_height, WIDTH, self.y + self.image_height, dash = (5, 5), width = 1, fill = color))
        
        if (self.position == 1):
            if (len(self.list_indications) == 0):
                self.list_indications = []
                self.list_indications.append(self.canv.create_line(self.x, 0, self.x, HEIGTH, dash = (5, 5), width = 1, fill = color))
                #self.list_indications.append(self.canv.create_line(self.x + self.image_width/2, 0, self.x + self.image_width/2, HEIGTH, dash = (5, 5), width = 1, fill = color))
                self.list_indications.append(self.canv.create_line(self.x + self.image_width, 0, self.x + self.image_width, HEIGTH, dash = (5, 5), width = 1, fill = color))

    def delete_node(self, list_models):
        self.canv.delete(self.image_model)
        for i in range(len(self.list_connection)):
            for j in range(len(self.list_connection[i])):
                if (self.list_connection[i][j] != "none"):
                    for k in range(len(list_models[i][j].list_wires)):
                        if (list_models[i][j].list_wires[k] != "not exist"):
                            if (list_models[i][j].list_wires[k].text_tag == self.list_connection[i][j]):
                                list_models[i][j].list_wires[k].delete_wire()
                                list_models[i][j].list_wires[k] = "not exist"

    def indication_for_wire_off(self):
        for i in self.list_indications:
            self.canv.delete(i)
        self.list_indications = []

    def context_menu(self, m_x, m_y):
        if ((m_x >= self.x) and (m_x <= self.x + self.image_width) and (m_y >= self.y) and (m_y <= self.y + self.image_height)):
            return True

    def node_in_area(self, x1, y1, x2, y2):
        if (((self.x >= x1) and (self.y >= y1) and (self.x + self.image_width < x2) and (self.y + self.image_height < y2)) or
            ((self.x >= x2) and (self.y >= y2) and (self.x + self.image_width < x1) and (self.y + self.image_height < y1)) or
            ((self.x >= x1) and (self.y + self.image_height <= y1) and (self.x + self.image_width < x2) and (self.y > y2)) or
            ((self.x >= x2) and (self.y + self.image_height <= y2) and (self.x + self.image_width < x1) and (self.y > y1))):
            if (self.create_rect_indication_outline_selection == False):
                self.create_rect_indication_outline_selection = True
                self.rect_indication_outline_selection = self.canv.create_rectangle(self.x, self.y, self.x + self.image_width, self.y + self.image_height, width = 2, outline = "red")
        else:
            if (self.create_rect_indication_outline_selection == True):
                self.create_rect_indication_outline_selection = False
                self.canv.delete(self.rect_indication_outline_selection)

    def delete_outline_node(self):
        self.create_rect_indication_outline_selection = False
        self.canv.delete(self.rect_indication_outline_selection)

    def view_voltage(self):
        fig, axs = plt.subplots(len(self.list_voltages))
        plt.subplots_adjust(left=0.04, right=0.96, top = 0.96, bottom= 0.04, hspace=0)
        fig.suptitle('Vertically stacked subplots')
        counter_g = 0
        for i in self.list_voltages:
            axs[counter_g].plot(self.t, i, linewidth=1, color='red')
            axs[counter_g].grid(True)
            counter_g += 1
        plt.show()

