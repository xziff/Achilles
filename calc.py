import numpy as np
from scipy.integrate import odeint

import matplotlib.pyplot as plt

data_type = np.float64

def get_main_list(list_nodes, list_models):
    main_list = []
    for i in range(len(list_models)):
        use_k = []
        for j in range(len(list_nodes)):
            if (list_nodes[j] != "Deleted"):
                mass_iteraion = list_nodes[j].list_connection[i][0:]
                for m in range(len(mass_iteraion)):
                    for n in use_k:
                        if (n == m):
                            mass_iteraion[m] = "none"
                for k in range(len(mass_iteraion)):
                    if (mass_iteraion[k] != "none"):
                        main_list.append([i, k])
                        use_k.append(k)
    return main_list

def initial_conditions(list_models, main_list):
    y0 = []
    for type_model, number_moder in main_list:
        for i in list_models[type_model][number_moder].get_first():
            y0.append(i)
    return y0

def communacation_matrix(list_nodes, list_models, main_list):
    all_voltage_matrix = []    
    all_current_matrix = []

    for i in range(len(list_nodes)):
        help_voltage_matrix = []    
        help_current_matrix = [[], [], []] 
        wait_index = 0
        if (list_nodes[i] != "Deleted"):
            for j in range(len(main_list)):
                if ((list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]] != "none") and (list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]].split(":")[1] == "ON_SWITCH")):
                    for o in range(len(list_models[main_list[j][0]][main_list[j][1]].get_voltage_matrix(list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]].split(":")[0]))):
                        help_voltage_matrix.append([])
                        for p in range(len(list_models[main_list[j][0]][main_list[j][1]].get_voltage_matrix(list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]].split(":")[0])[o])):
                            help_voltage_matrix[o + wait_index].append(list_models[main_list[j][0]][main_list[j][1]].get_voltage_matrix(list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]].split(":")[0])[o][p])
                    wait_index += len(list_models[main_list[j][0]][main_list[j][1]].get_voltage_matrix(list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]].split(":")[0]))
                else:
                    for o in range(len(list_models[main_list[j][0]][main_list[j][1]].height_matrix)):
                        help_voltage_matrix.append([])
                        for p in range(3):
                            help_voltage_matrix[o + wait_index].append(0)
                    wait_index += len(list_models[main_list[j][0]][main_list[j][1]].height_matrix)
                
                if ((list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]] != "none") and (list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]].split(":")[1] == "ON_SWITCH")):
                    for o in range(len(list_models[main_list[j][0]][main_list[j][1]].get_current_matrix(list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]].split(":")[0]))):
                        for p in range(len(list_models[main_list[j][0]][main_list[j][1]].get_current_matrix(list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]].split(":")[0])[o])):
                            help_current_matrix[o].append(list_models[main_list[j][0]][main_list[j][1]].get_current_matrix(list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]].split(":")[0])[o][p])
                else:
                    for o in range(3):
                        for p in range(len(list_models[main_list[j][0]][main_list[j][1]].width_matrix)):
                            help_current_matrix[o].append(0)


            width_matrix_buff = 0
            for n in range(len(help_voltage_matrix)):
                if (len(help_voltage_matrix[n]) > width_matrix_buff):
                    width_matrix_buff = len(help_voltage_matrix[n])
            for n in range(len(help_voltage_matrix)):
                while (len(help_voltage_matrix[n]) != width_matrix_buff):
                    help_voltage_matrix[n].append(0)

            mass_repeat = []
            for ii in range(len(help_voltage_matrix[0])):
                repeat_num = 0
                for jj in range(len(help_voltage_matrix)):
                    if ((help_voltage_matrix[jj][ii] == 1) or (help_voltage_matrix[jj][ii] == -1)):
                        repeat_num = 1
                if (repeat_num == 0):
                    mass_repeat.append(ii)

            for ii in mass_repeat:
                for jj in range(len(help_voltage_matrix)):
                    del help_voltage_matrix[jj][ii]

            if (len(help_voltage_matrix[0]) == 2):
                del help_current_matrix[-1]

            if (len(all_voltage_matrix) == 0):
                for ii in range(len(help_voltage_matrix)):
                    all_voltage_matrix.append([])

            for ii in range(len(help_voltage_matrix)):
                for jj in range(len(help_voltage_matrix[ii])):
                    all_voltage_matrix[ii].append(help_voltage_matrix[ii][jj])

            for ii in help_current_matrix:
                all_current_matrix.append(ii[0:])
    
    for ii in range(len(all_current_matrix)):
        for j in range(len(all_voltage_matrix[0])):
            all_current_matrix[ii].append(0)

    return np.array(all_voltage_matrix, dtype = data_type), np.array(all_current_matrix, dtype = data_type)

def return_graphs(main_list, list_models, results, t):
    wain_index = 0
    for type_model, number_moder in main_list:
        width_input = list_models[type_model][number_moder].width_input
        list_models[type_model][number_moder].list_results = []
        list_models[type_model][number_moder].t = t
        for i in range(width_input):
            list_models[type_model][number_moder].list_results.append(results[:, wain_index + i])
        wain_index += width_input
        


def calculations(list_nodes, list_models):
    t_max = 5
    t_del = 500000
    t = np.linspace(0, t_max, t_del)

    main_list = get_main_list(list_nodes, list_models)

    y0 = initial_conditions(list_models, main_list)

    all_voltage_matrix, all_current_matrix = communacation_matrix(list_nodes, list_models, main_list)

    print(all_voltage_matrix)

    print(all_current_matrix)

    def f(y, t):
        wait_index = 0
        current_index = [0, 0]
        ouput_matrix = []

        bool_start = False

        for type_model, number_moder in main_list:
            width_matrix = list_models[type_model][number_moder].width_matrix
            height_matrix = list_models[type_model][number_moder].height_matrix
            width_input = list_models[type_model][number_moder].width_input

            if (bool_start == False):
                main_det = np.zeros((height_matrix, width_matrix), dtype = data_type)
                own_matrix = np.array(list_models[type_model][number_moder].get_own_matrix(y[wait_index:(wait_index+width_input)], t), dtype = data_type)
                bool_start = True
            else:   
                main_det = np.hstack((main_det, np.zeros((main_det.shape[0], width_matrix), dtype = data_type)))  
                main_det = np.vstack((main_det, np.zeros((height_matrix, main_det.shape[1]), dtype = data_type)))
                own_matrix = np.hstack((own_matrix, np.array(list_models[type_model][number_moder].get_own_matrix(y[wait_index:(wait_index+width_input)], t), dtype = data_type)))

            buffer_det = np.array(list_models[type_model][number_moder].get_main_determinant(y[wait_index:(wait_index+width_input)], t), dtype = data_type)

            for i in range(height_matrix):
                for j in range(width_matrix):
                    main_det[current_index[0] + i][current_index[1] + j] = buffer_det[i][j]

            current_index[0] += height_matrix
            current_index[1] += width_matrix
            wait_index += width_input

        main_det = np.hstack((main_det, all_voltage_matrix))
        main_det = np.vstack((main_det, all_current_matrix))
        own_matrix = np.hstack((own_matrix, np.zeros((all_current_matrix.shape[0]), dtype = data_type)))

        solve_matrix = np.linalg.solve(main_det, own_matrix)

        wait_index = 0
        qwe_i = 0
        for type_model, number_moder in main_list:
            for m in range(list_models[type_model][number_moder].width_matrix):
                ouput_matrix.append(solve_matrix[qwe_i])
                qwe_i += 1
            for m in range(list_models[type_model][number_moder].width_input - list_models[type_model][number_moder].width_matrix):
                ouput_matrix.append(list_models[type_model][number_moder].get_additional_variable(y[wait_index:(wait_index+list_models[type_model][number_moder].width_input)], t)[m])
            wait_index += list_models[type_model][number_moder].width_input

        #print(str(round(t/t_max*100, 3)), end = "\r")
    
        return ouput_matrix

    results = odeint(f, y0, t)

    return_graphs(main_list, list_models, results, t)