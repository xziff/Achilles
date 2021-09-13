from tkinter import * 
from tkinter import ttk

from Models.Electrical_Bus import Electrical_Bus
from Models.DWT_YD_11 import DWT_YD_11
from Models.NPSG_Y import NPSG_Y
from Models.WRIM import WRIM
from Models.ES import ES
from Models.SS import SS
from Models.SL_Y import SL_Y
from Models.TwSSW_YD_11 import TwSSW_YD_11

def add_model(mass_model, list_nodes, return_text, WIDTH, HEIGHT, canv, root):
    if (return_text == "Обычный узел"):
        list_nodes.append(Electrical_Bus(WIDTH, HEIGHT, 0, canv, root))
        list_nodes[-1].state_click = 1
        list_nodes[-1].delta_x = list_nodes[-1].image_width/2
        list_nodes[-1].delta_y = list_nodes[-1].image_height/2
    else:
        if (return_text == "Звезда-треугольник-11"):
            m_i = 0
            mass_model[0].append(DWT_YD_11(WIDTH, HEIGHT, 0, canv, root, None, None, None, None))
        elif (return_text == "Синхронная машина"):
            m_i = 1
            mass_model[1].append(NPSG_Y(WIDTH, HEIGHT, 0, canv, root, None, None, None, None))
        elif (return_text == "Асинхронная машина"):
            m_i = 2
            mass_model[2].append(WRIM(WIDTH, HEIGHT, 0, canv, root, None, None, None, None))
        elif (return_text == "Система"):
            m_i = 3
            mass_model[3].append(ES(WIDTH, HEIGHT, 0, canv, root, None, None, None, None))
        elif (return_text == "Вылючатель"):
            m_i = 4
            mass_model[4].append(SS(WIDTH, HEIGHT, 0, canv, root, None, None, None, None))
        elif (return_text == "Статическаая нагрузка"):
            m_i = 5
            mass_model[5].append(SL_Y(WIDTH, HEIGHT, 0, canv, root, None, None, None, None))
        elif (return_text == "Трансформатор с расщепленной обмоткой"):
            m_i = 6
            mass_model[6].append(TwSSW_YD_11(WIDTH, HEIGHT, 0, canv, root, None, None, None, None))
        else:
            print("Error")
        mass_model[m_i][-1].state_click = 1
        mass_model[m_i][-1].delta_x = mass_model[m_i][-1].image_width/2
        mass_model[m_i][-1].delta_y = mass_model[m_i][-1].image_height/2
        mass_model[m_i][-1].click_indication = canv.create_rectangle(mass_model[m_i][-1].x, mass_model[m_i][-1].y, mass_model[m_i][-1].x + mass_model[m_i][-1].image_width, mass_model[m_i][-1].y + mass_model[m_i][-1].image_height, width = 2, outline = "red")



def get_tree_window(root):

    tree_window = Toplevel(root, bg = "white")
    tree_window.title("Выбор моделей")

    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('GOST Type A', 14))
    style.configure("mystyle.Treeview.Heading", highlightthickness=0, bd=0, font=('GOST Type A', 20))

    tree = ttk.Treeview(tree_window, height= 20, style="mystyle.Treeview")
    tree.column('#0', width=600, stretch=NO)

    tree.heading('#0', text='Список моделей', anchor='w')

    nodes = tree.insert("", 1, text="Элеткрические узлы")
    tree.insert(nodes, "end", text="Обычный узел", tags= ('node',))

    Trans = tree.insert("", 2, text="Трансформаторы")
    tree.insert(Trans, "end", text="Звезда-треугольник-11", tags= ('0',))
    tree.insert(Trans, "end", text='Трансформатор с расщепленной обмоткой', tags= ('6',))

    rotM = tree.insert("", 3, text="Вращающиеся электрические машины")
    tree.insert(rotM, "end", text="Синхронная машина", tags= ('1',))
    tree.insert(rotM, "end", text="Асинхронная машина", tags= ('2',))

    anoter = tree.insert("", 4, text="Другое")
    tree.insert(anoter, "end", text="Система", tags= ('3',))
    tree.insert(anoter, "end", text="Вылючатель", tags= ('4',))
    tree.insert(anoter, "end", text="Статическаая нагрузкаа", tags= ('5',))

    tree.grid(row=0, column=0, sticky='nsew')

    return tree, tree_window