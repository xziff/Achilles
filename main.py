from tkinter import *
from tkinter import ttk
import os
import tkinter.font as font

from tree_window import get_tree_window, add_model
from calc import calculations
from save_and_load import save_models_nodes, load_models_nodes


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
            delete_index = i
            menu = Menu(tearoff=0, font = ('GOST Type A', 14))           
            menu.add_command(label="Удалить узел", 
            command= delete_nodes)
            menu.post(event.x, event.y)


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

#Бинды кнопок
canv.bind('<Button-1>', click_1)
canv.bind('<Button-3>', get_menu)
canv.bind('<Motion>', mouse_motion)

root.bind('v', view)
root.bind('r', rotation)
root.bind('n', get_list_nodes)


canv.pack()
root.mainloop()
