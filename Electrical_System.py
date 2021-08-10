import math
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from scipy. integrate import odeint
import numpy as np

from base_model import Base_model

coord = [
    [[16, 275]],
    [[174, 17]],
    [[948, 276]],
    [[171, 981]]
]

list_nodes = ["Q"]

class Electrical_System(Base_model):

    def __init__(self, init_x, init_y, canv, root):

        Base_model.__init__(self, init_x, init_y, canv, root, "Image/Electrical System/", coord, 0, list_nodes)

