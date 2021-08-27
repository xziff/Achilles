from tkinter import *
from tkinter import ttk
import os
import tkinter.font as font

from Models.Electrical_Bus import Electrical_Bus
from Models.DWT_YD_11 import DWT_YD_11
from Models.NPSG_Y import NPSG_Y
from Models.WRIM import WRIM
from Models.ES import ES
from Models.SS import SS

from tree_window import get_tree_window, add_model
from calc import calculations
from save_and_load import save_models_nodes, load_models_nodes

selection_outline_active = False
scheme_replace = False

#Массив узлов
list_nodes = []

#Массив всех моделей
list_models = []
list_models.append([]) #Трансформатор
list_models.append([]) #Синхронная машина
list_models.append([]) #Асинхронная машина
list_models.append([]) #Система
list_models.append([]) #Выключатель

#Команды кнопок на экране
def b1_command():
    tree, tree_window = get_tree_window(root)
    def OnDoubleClick(event):
        item = tree.identify('item',event.x,event.y)
        add_model(list_models, list_nodes, tree.item(item)['text'], WIDTH, HEIGHT, canv, root)
        tree_window.destroy()
    tree.bind("<Double-1>", OnDoubleClick)

def start():
    calculations(list_nodes, list_models)

def save_scheme():
    def bc():
        save_models_nodes(SV.get(), list_models, list_nodes)
        save_window.destroy()
    save_window = Toplevel(root, bg = "white")
    save_window.title("Сохранить файл")
    label = Label(master= save_window, text="Имя файла в папке '/saves_schemes'", font=('GOST Type A', 16), bg= "white")
    SV = StringVar()
    entry = Entry(save_window, width=15, font=('GOST Type A', 14), textvariable = SV)          
    b4 = Button(master = save_window, text="Сохранить", command= bc, bg = "white", font = font.Font(family = "GOST Type A"))
    label.pack(padx = 10, pady = 10)
    entry.pack(padx = 10, pady = 10)
    b4.pack(padx = 10, pady = 10)


def load_scheme():
    for i, k, files in os.walk("./saves_schemes"):
        file_names = files

    def bc():
        global list_models, list_nodes
        for i in list_models:
            for j in i:
                j.delete_model()
        for i in list_nodes:
            i.delete_node(list_models)

        list_nodes = []
        list_models = []
        list_models.append([]) #Трансформатор
        list_models.append([]) #Синхронная машина
        list_models.append([]) #Асинхронная машина
        list_models.append([]) #Система
        list_models.append([]) #Выключатель
        
        load_models_nodes(list_files.get(), list_models, list_nodes, canv, root)
        load_window.destroy()

    load_window = Toplevel(root, bg = "white")
    load_window.title("Выбор файла для загрузки")
    if (len(file_names) == 0):
        label = Label(master= load_window, text="Нет файлов для загрузки", font=('GOST Type A', 16), bg= "white")
        label.pack()
    else:
        label = Label(master= load_window, text="Файлы в папке '/saves_schemes'", font=('GOST Type A', 16), bg= "white")
        label.pack(padx = 10, pady = 10)
        list_files = ttk.Combobox(load_window, values = file_names ,state="readonly", font=('GOST Type A', 16), width= 16)
        list_files.current(0)
        list_files.pack(padx = 10, pady = 10)
        b4 = Button(master = load_window, text="Загрузить схему", command= bc, bg = "white", font = font.Font(family = "GOST Type A"))
        b4.pack(padx = 10, pady = 10)

#Команды кнопок на клавиатуре и мыши
def click_1(event):
    global scheme_replace
    if not scheme_replace:
        #Проверяем, были ли активны wire для выделения
        Press_model = False
        for i in list_models:
            for j in i:
                for k in j.list_wires:
                    if (k != "not exist"):
                        if (k.activity != False):
                            Press_model = True

        for i in list_nodes:
            i.set_state_click(event.x, event.y, list_models)
            i.control_connection(list_models)

        activity_wire = False

        for i in list_models:
            for j in i:
                if (j != "Deleted"):
                    j.set_state_click(event.x, event.y)
                    j.wire_connection(event.x, event.y)
                    for k in j.list_wires:
                        if (k != "not exist"):
                            k.add_wire_node(event.x, event.y)
                            if (k.activity != False):
                                activity_wire = True

        if not activity_wire:
            for i in list_nodes:
                i.indication_for_wire_off() 

        if activity_wire:
            for i in list_nodes:
                i.indication_for_wire_on(WIDTH, HEIGHT)

        #Выделение моделей
        global list_copy_help
        list_copy_help = []
            # Удаляем предыдущее выделение
        for i in list_models:
            for j in i:
                for k in j.list_wires:
                    if (k != "not exist"):
                        k.bool_wire_in_area = False
                        try:
                            for i in k.canvas_object_wire_indication_outline:
                                canv.delete(i)
                        except AttributeError:
                            pass
                j.create_rect_indication_outline_selection = False
                try:
                    canv.delete(j.rect_indication_outline_selection)
                except AttributeError:
                    pass
        for i in list_nodes:
            i.create_rect_indication_outline_selection = False
            try:
                canv.delete(i.rect_indication_outline_selection)
            except AttributeError:
                pass
            #Проверям не нажали ли на моделькуs
        for i in list_nodes:
            if (i.context_menu(event.x, event.y) == True):
                Press_model = True
        for i in list_models:
            for j in i:
                if ((j.mouse_in_model(event.x, event.y) == True)) or (j.bool_mouse_in_area == True):
                    Press_model = True
        if activity_wire:
            Press_model = True
        if not Press_model:
            global selection_outline, selection_outline_active, x_o, y_o
            x_o = event.x
            y_o = event.y
            selection_outline_active = True
            selection_outline = canv.create_rectangle(event.x, event.y, event.x, event.y, outline="red", width=2)
    if scheme_replace:
        scheme_replace = False
        for i in list_models:
            for j in i:
                if j.create_rect_indication_outline_selection:
                    for k in j.list_wires:
                        if (k != "not exist"):
                            k.bool_wire_in_area = False
                            for m in k.canvas_object_wire_indication_outline:
                                    canv.delete(m)
                    j.replace_state = False
                    j.state_click = 0
                    j.create_rect_indication_outline_selection = False
                    canv.delete(j.rect_indication_outline_selection)
        for i in list_nodes:
            i.replace_state = False
            i.state_click = 0
            i.create_rect_indication_outline_selection = False
            canv.delete(i.rect_indication_outline_selection)

        for i in list_nodes:
            i.control_connection(list_models)


def click_1_release(event):
    global selection_outline, selection_outline_active
    if (selection_outline_active == True):
        canv.delete(selection_outline)
        selection_outline_active = False


def mouse_motion(event):
    for i in list_models:
        for j in i:
            if (j != "Deleted"):
                j.move_model(event.x, event.y)
                j.indication_wire_connection(event.x, event.y)
                for k in j.list_wires:
                    if (k != "not exist"):
                        k.move_end_wire(event.x, event.y, list_nodes, WIDTH, HEIGHT)
 
    for i in list_nodes:
        i.move_model(event.x, event.y)

    global selection_outline, selection_outline_active, x_o, y_o
    if selection_outline_active:
        canv.coords(selection_outline, x_o, y_o, event.x, event.y)
        for i in list_models:
            for j in i:
                for k in j.list_wires:
                    if (k != "not exist"):
                        k.wire_in_area(x_o, y_o, event.x, event.y)
                j.model_in_area(x_o, y_o, event.x, event.y)
        for i in list_nodes:
            i.node_in_area(x_o, y_o, event.x, event.y)

def rotation(event):
    for i in list_nodes:
        i.rotation(event.x, event.y)
    for i in list_models:
        for j in i:
            if (j != "Deleted"):
                j.rotation(event.x, event.y)

def get_list_nodes(event):
    print("#####################################################")
    for i in list_nodes:
        print(i.list_connection)
    print("#####################################################")

def view(event):
    for i in list_models:
        for j in i:
            if (j != "Deleted"):
                j.view_results()

def get_menu(event):

    # Меню модели
    delete_index = []
    def delete_models():
        list_models[delete_index[0]][delete_index[1]].delete_model()
        del list_models[delete_index[0]][delete_index[1]]
        for i in list_nodes:
            i.control_connection(list_models)
    for i in range(len(list_models)):
        for j in range(len(list_models[i])):
            if (list_models[i][j] != "Deleted"):
                if (list_models[i][j].context_menu(event.x, event.y) == True):
                    if list_models[i][j].create_rect_indication_outline_selection:
                        menu = Menu(tearoff=0, font = ('GOST Type A', 14))
                        menu.add_command(label="Копировать",
                        command = copy)
                        menu.add_command(label="Переместить",
                        command = replace)
                        menu.add_separator() 
                        menu.add_command(label="Отменить выделенеи", 
                        command= list_models[i][j].delete_outline_model)
                        menu.post(event.x, event.y)
                    else:
                        delete_index = [i, j]
                        menu = Menu(tearoff=0, font = ('GOST Type A', 14))
                        menu.add_command(label="Осциллограммы", 
                        command= list_models[i][j].view_results)
                        menu.add_separator()    
                        menu.add_command(label="Параметры модели", 
                        command= list_models[i][j].set_secondary_parameters)
                        menu.add_command(label="Управляющие воздействия", 
                        command= list_models[i][j].set_control_actions)
                        menu.add_separator()                      
                        menu.add_command(label="Удалить модель", 
                        command= delete_models)
                        menu.post(event.x, event.y)

    def delete_nodes():
        list_nodes[delete_index].delete_node(list_models)        
        del list_nodes[delete_index]
    for i in range(len(list_nodes)):
        if (list_nodes[i].context_menu(event.x, event.y) == True):
            if list_nodes[i].create_rect_indication_outline_selection:
                menu = Menu(tearoff=0, font = ('GOST Type A', 14)) 
                menu.add_command(label="Копировать",
                command = copy)
                menu.add_command(label="Переместить",
                command = replace)
                menu.add_separator() 
                menu.add_command(label="Отменить выделение", 
                command= list_nodes[i].delete_outline_node) 
                menu.post(event.x, event.y)
            else:
                delete_index = i
                menu = Menu(tearoff=0, font = ('GOST Type A', 14))         
                menu.add_command(label="Удалить узел", 
                command= delete_nodes)
                menu.post(event.x, event.y)

def replace():
    global scheme_replace
    scheme_replace = True
    list_x = []
    list_y = []
    for i in list_models:
        for j in i:
            if j.create_rect_indication_outline_selection:
                j.replace_state = True
                j.state_click = 1
                list_x.append(j.x)
                list_y.append(j.y)
    for i in list_nodes:
        if i.create_rect_indication_outline_selection:
            i.replace_state = True
            i.state_click = 1
            list_x.append(i.x)
            list_y.append(i.y)

    cent_x = (max(list_x) + min(list_x))/2
    cent_y = (max(list_y) + min(list_y))/2

    for i in list_models:
        for j in i:
            for k in j.list_wires:
                if (k != "not exist"):
                    if (k.bool_wire_in_area == True):
                        k.delta_for_points_wire = []
                        for m in k.coords_wire:
                            k.delta_for_points_wire.append([cent_x - m[0], cent_y - m[1]])
            if j.create_rect_indication_outline_selection:
                j.delta_x = cent_x - j.x
                j.delta_y = cent_y - j.y
    for i in list_nodes:
        i.delta_x = cent_x - i.x
        i.delta_y = cent_y - i.y    


def paste(event):
    global copy_list_model, copy_list_node

    #Определение геометрического центра вставки


    for i in copy_list_model[0]:
        list_models[0].append(DWT_YD_11(i[0], i[1], i[2], canv, root, i[3], i[4], i[5], i[6]))
    for i in copy_list_model[1]:
        list_models[1].append(NPSG_Y(i[0], i[1], i[2], canv, root, i[3], i[4], i[5], i[6]))
    for i in copy_list_model[2]:
        list_models[2].append(WRIM(i[0], i[1], i[2], canv, root, i[3], i[4], i[5], i[6]))
    for i in copy_list_model[3]:
        list_models[3].append(ES(i[0], i[1], i[2], canv, root, i[3], i[4], i[5], i[6]))
    for i in copy_list_model[4]:
        list_models[4].append(SS(i[0], i[1], i[2], canv, root, i[3], i[4], i[5], i[6]))

    for i in copy_list_node:
        list_nodes.append(Electrical_Bus(i[0], i[1], i[2], canv, root))

    for i in list_nodes:
        i.control_connection(list_models)


def copy():
    global copy_list_model
    copy_list_model = []
    for i in list_models:
        copy_list_model.append([])
        for j in i:
            if j.create_rect_indication_outline_selection:
                initial_list_wires = []
                for k in j.list_wires:
                    if (k != "not exist"):
                        if (k.bool_wire_in_area == True):
                            initial_list_wires.append(k.coords_wire)
                        else:
                            initial_list_wires.append("not exist")
                    else:
                        initial_list_wires.append("not exist")      
                copy_list_model[-1].append([j.x, j.y, j.position, initial_list_wires, j.list_params, j.list_initial_conditions, j.secondary_parameters])
    
    global copy_list_node
    copy_list_node = []
    for i in list_nodes:
        copy_list_node.append([i.x, i.y, i.position])


# Создание главного окна
root = Tk()
root.title("Achilles")
root.geometry("1920x1080")
root.state('zoomed')
#root.resizable(width=False, height=False)
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()

HEIGHT_MENU = int(HEIGHT/15)

#Создание главной рамки
frame=Frame(master = root, bg = "white", width=WIDTH,height=HEIGHT)
frame.grid_propagate(0)
frame.grid(row = 0, column = 0)

#Окно для рисовки
canv = Canvas(frame, width = WIDTH, height = HEIGHT, bg = "white", cursor = "pencil")

for i in range(150):
    AQ = 35
    canv.create_line(i*AQ, HEIGHT_MENU, i*AQ, HEIGHT, fill = "#dbdbdb")
    canv.create_line(0, i*AQ, WIDTH, i*AQ, fill = "#dbdbdb")

#Создание рамки главного меню
frame_menu=Frame(master = frame,  bg = "white", highlightbackground="black", highlightthickness=1, width=WIDTH, height=HEIGHT_MENU)
frame_menu.pack_propagate(0)
frame_menu.grid(row = 0, column = 0)

#Кнопка вызова дерева моделей
b1 = Button(master = frame_menu, text="Дерево моделей", command= b1_command, height=HEIGHT_MENU, bg = "white", font = font.Font(family = "GOST Type A"))
b1.pack(side = LEFT, padx = 10, pady = 10)

#Кнопка для расчета
b2 = Button(master = frame_menu, text="Начать расчет", command= start, height=HEIGHT_MENU, bg = "white", font = font.Font(family = "GOST Type A"))
b2.pack(side = LEFT, padx = 10, pady = 10)

#Кнопка для сохранения схемы
b3 = Button(master = frame_menu, text="Сохранить схему", command= save_scheme, height=HEIGHT_MENU, bg = "white", font = font.Font(family = "GOST Type A"))
b3.pack(side = RIGHT, padx = 10, pady = 10)

#Кнопка для загрузки схемы
b4 = Button(master = frame_menu, text="Загрузить схему", command= load_scheme, height=HEIGHT_MENU, bg = "white", font = font.Font(family = "GOST Type A"))
b4.pack(side = RIGHT, padx = 10, pady = 10)

#Кнопка для загрузки схемы
frame_help_menu = Frame(master = frame_menu,  bg = "white", highlightbackground="black", highlightthickness=1)
frame_help_menu.pack(side = LEFT, padx = 10, pady = 10)

#Бинды кнопок
canv.bind('<Button-1>', click_1)
canv.bind('<Button-3>', get_menu)
canv.bind('<Motion>', mouse_motion)
canv.bind('<ButtonRelease-1>', click_1_release)

root.bind('r', rotation)
root.bind('n', get_list_nodes)
root.bind('v', paste)

canv.pack()
root.mainloop()
