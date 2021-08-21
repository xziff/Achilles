import pickle

import sys
sys.path.insert(1, '/Models')

from Models.Electrical_Bus import Electrical_Bus
from Models.Transformator_Z_T_11 import Transformator_Z_T_11
from Models.SM import SM
from Models.AM import AM
from Models.Electrical_System import Electrical_System
from Models.Switch import Switch

def save_models_nodes(path_str, list_models, list_nodes):
    with open('saves_schemes/' + path_str + '.pickle', 'wb') as f:
        list_save_parameters = []
        for i in list_models:
            list_save_parameters.append([])
            for j in i:
                initial_list_wires = []
                for k in j.list_wires:
                    if (k == "not exist"):
                        initial_list_wires.append("not exist")
                    else:
                        initial_list_wires.append(k.coords_wire)

                list_save_parameters[-1].append([j.x, j.y, j.position, initial_list_wires, j.list_params, j.list_initial_conditions, j.secondary_parameters
                ])
        pickle.dump(list_save_parameters, f)

        list_save_parameters = []
        for i in list_nodes:
            list_save_parameters.append([i.x, i.y, i.position,
                ])
        pickle.dump(list_save_parameters, f)

def load_models_nodes(path_str, list_models, list_nodes, canv, root):
    with open('saves_schemes/' + path_str, 'rb') as f:
        data = pickle.load(f)

        for i in data[0]:
            list_models[0].append(Transformator_Z_T_11(i[0], i[1], i[2], canv, root, i[3], i[4], i[5], i[6]))
        for i in data[1]:
            list_models[1].append(SM(i[0], i[1], i[2], canv, root, i[3], i[4], i[5], i[6]))
        for i in data[2]:
            list_models[2].append(AM(i[0], i[1], i[2], canv, root, i[3], i[4], i[5], i[6]))
        for i in data[3]:
            list_models[3].append(Electrical_System(i[0], i[1], i[2], canv, root, i[3], i[4], i[5], i[6]))
        for i in data[4]:
            list_models[4].append(Switch(i[0], i[1], i[2], canv, root, i[3], i[4], i[5], i[6]))

        data = pickle.load(f)
        for i in data:
            list_nodes.append(Electrical_Bus(i[0], i[1], i[2], canv, root))

        for i in list_nodes:
            i.control_connection(list_models)

