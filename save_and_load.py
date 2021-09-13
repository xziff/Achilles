import pickle

#from main import add_model
from Models.Electrical_Bus import Electrical_Bus

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

                if (j.list_params == [[[],[]]] * len(j.list_text_secondary_parameters)):
                    P1 = None
                else:
                    P1 = j.list_params 
                if (j.secondary_parameters == []):
                    P2 = None
                else:
                    P2 = j.secondary_parameters

                list_save_parameters[-1].append([j.x, j.y, j.position, initial_list_wires, P1, j.list_initial_conditions, P2, j.Comdobox_index
                ])
        pickle.dump(list_save_parameters, f)

        list_save_parameters = []
        for i in list_nodes:
            list_save_parameters.append([i.x, i.y, i.position,
                ])
        pickle.dump(list_save_parameters, f)

def load_models_nodes(path_str, list_models, list_nodes, canv, root, add_model):
    with open('saves_schemes/' + path_str, 'rb') as f:
        data = pickle.load(f)

        for i in range(len(data)):
            for j in data[i]:
                add_model(i, j[0], j[1], j[2], canv, root, j[3], j[4], j[5], j[6], j[7])

        data = pickle.load(f)
        for i in data:
            list_nodes.append(Electrical_Bus(i[0], i[1], i[2], canv, root))

        for i in list_nodes:
            i.control_connection(list_models)

