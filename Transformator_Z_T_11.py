import math
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from scipy. integrate import odeint
import numpy as np

from base_model import Base_model

coord = [
    [[1075, 172], [7, 173]],
    [[474, 1073], [474, 8]],
    [[12, 174], [1071, 173]],
    [[470, 5], [474, 1084]]
]

list_nodes = ["Z", "T"]

class Transformator_Z_T_11(Base_model):

    def __init__(self, init_x, init_y, canv, root):

        Base_model.__init__(self, init_x, init_y, canv, root, "Image/Transformator/", coord, 0, list_nodes)

