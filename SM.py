import math
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from scipy. integrate import odeint
import numpy as np

from base_model import Base_model

coord = [
    [[587, 177]],
    [[179, 702]],
    [[10, 173]],
    [[178, 13]]
]

list_nodes = ["Q"]

class SM(Base_model):

    def __init__(self, init_x, init_y, canv, root):

        Base_model.__init__(self, init_x, init_y, canv, root, "Image/SM/", coord, 0, list_nodes)

