from tkinter import * 
from tkinter import ttk

from Electrical_Bus import Electrical_Bus
from Transformator_Z_T_11 import Transformator_Z_T_11
from SM import SM
from AM import AM
from Electrical_System import Electrical_System

def add_model(mass_model, list_nodes, return_text, WIDTH, HEIGHT, canv, root):
    if (return_text == "Обычный узел"):
        list_nodes.append(Electrical_Bus(WIDTH/2, HEIGHT/2, canv, root))
    elif (return_text == "Звезда-треугольник-11"):
        mass_model[0].append(Transformator_Z_T_11(WIDTH/2, HEIGHT/2, canv, root))
    elif (return_text == "Синхронная машина"):
        mass_model[1].append(SM(WIDTH/2, HEIGHT/2, canv, root))
    elif (return_text == "Асинхронная машина"):
        mass_model[2].append(AM(WIDTH/2, HEIGHT/2, canv, root))
    elif (return_text == "Система"):
        mass_model[3].append(Electrical_System(WIDTH/2, HEIGHT/2, canv, root))
    else:
        print("Error")



def get_tree_window(root):

    tree_window = Toplevel(root)
    tree_window.title("Выбор моделей")

    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('GOST Type A', 14))
    style.configure("mystyle.Treeview.Heading", highlightthickness=0, bd=0, font=('GOST Type A', 20))

    tree = ttk.Treeview(tree_window, height= 20, style="mystyle.Treeview")
    tree.column('#0', width=600, stretch=NO)

    tree.heading('#0', text='Список моделей', anchor='w')

    tree.insert('', END, text='Элеткрические узлы', iid=0, open=False, tags= ('H',))
    tree.insert('', END, text='Обычный узел', iid=1, open=False)
    tree.move(1, 0, 0)

    tree.insert('', END, text='Трансформаторы', iid=2, open=False, tags= ('H',))
    tree.insert('', END, text='Звезда-треугольник-11', iid=3, open=False)
    tree.move(3, 2, 0)
    
    tree.insert('', END, text='Вращающиеся электрические машины', iid=4, open=False, tags= ('H',))
    tree.insert('', END, text='Синхронная машина', iid=5, open=False)
    tree.move(5, 4, 0)
    tree.insert('', END, text='Асинхронная машина', iid=6, open=False)
    tree.move(6, 4, 0)

    tree.insert('', END, text='Другое', iid=7, open=False, tags= ('H',))
    tree.insert('', END, text='Система', iid=8, open=False)
    tree.move(8, 7, 0)

    tree.grid(row=0, column=0, sticky='nsew')

    return tree, tree_window