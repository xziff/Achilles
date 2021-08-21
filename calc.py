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
                    for o in range(len(list_models[main_list[j][0]][main_list[j][1]].get_current_matrix(list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]].split(":")[0]))):
                        for p in range(len(list_models[main_list[j][0]][main_list[j][1]].get_current_matrix(list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]].split(":")[0])[o])):
                            help_current_matrix[o].append(list_models[main_list[j][0]][main_list[j][1]].get_current_matrix(list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]].split(":")[0])[o][p])

                else:
                    for o in range(list_models[main_list[j][0]][main_list[j][1]].height_matrix):
                        help_voltage_matrix.append([])
                        for p in range(3):
                            help_voltage_matrix[o + wait_index].append(0)
                    wait_index += list_models[main_list[j][0]][main_list[j][1]].height_matrix
                    for o in range(3):
                        for p in range(list_models[main_list[j][0]][main_list[j][1]].width_matrix):
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

    for i in range(len(list_nodes)):
        help_voltage_matrix = []    
        help_current_matrix = [[], [], []] 
        wait_index = 0
        if (list_nodes[i] != "Deleted"):
            for j in range(len(main_list)):
                if ((list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]] != "none") and (list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]].split(":")[1] == "OFF_SWITCH")):
                    for o in range(len(list_models[main_list[j][0]][main_list[j][1]].get_voltage_matrix(list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]].split(":")[0]))):
                        help_voltage_matrix.append([])
                        for p in range(len(list_models[main_list[j][0]][main_list[j][1]].get_voltage_matrix(list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]].split(":")[0])[o])):
                            help_voltage_matrix[o + wait_index].append(list_models[main_list[j][0]][main_list[j][1]].get_voltage_matrix(list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]].split(":")[0])[o][p])
                    wait_index += len(list_models[main_list[j][0]][main_list[j][1]].get_voltage_matrix(list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]].split(":")[0]))
                    for o in range(len(list_models[main_list[j][0]][main_list[j][1]].get_current_matrix(list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]].split(":")[0]))):
                        for p in range(len(list_models[main_list[j][0]][main_list[j][1]].get_current_matrix(list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]].split(":")[0])[o])):
                            help_current_matrix[o].append(list_models[main_list[j][0]][main_list[j][1]].get_current_matrix(list_nodes[i].list_connection[main_list[j][0]][main_list[j][1]].split(":")[0])[o][p])

                else:
                    for o in range(list_models[main_list[j][0]][main_list[j][1]].height_matrix):
                        help_voltage_matrix.append([])
                        for p in range(3):
                            help_voltage_matrix[o + wait_index].append(0)
                    wait_index += list_models[main_list[j][0]][main_list[j][1]].height_matrix
                    for o in range(3):
                        for p in range(list_models[main_list[j][0]][main_list[j][1]].width_matrix):
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
            
            buff_mass_repeat = []
            buf_width = len(mass_repeat)
            for i in range(len(mass_repeat)):
                buff_mass_repeat.append(mass_repeat[buf_width-1 - i])

            for ii in buff_mass_repeat:
                for jj in range(len(help_voltage_matrix)):
                    del help_voltage_matrix[jj][ii]

            if (len(help_voltage_matrix[0]) == 2):
                del help_current_matrix[-1]
            if (len(help_voltage_matrix[0]) == 1):
                del help_current_matrix[-2]
                del help_current_matrix[-1]
            if (len(help_voltage_matrix[0]) == 0):
                del help_current_matrix[-2]
                del help_current_matrix[-1]
                del help_current_matrix[0]

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
    t_max = 8
    t_del = 1000000
    t = np.linspace(0, t_max, t_del)

    main_list = get_main_list(list_nodes, list_models)

    y0 = initial_conditions(list_models, main_list)

    all_voltage_matrix, all_current_matrix = communacation_matrix(list_nodes, list_models, main_list)

    time_interrupt = []
    for i in list_models[4]:
        for j in i.get_interrupt_time():
            time_interrupt.append(j)
    time_interrupt = list(set(time_interrupt))
    time_interrupt.sort()
    flag_time_interrupt = [False] * len(time_interrupt)

    def f(y, t):
        global all_voltage_matrix, all_current_matrix
        wait_index = 0
        current_index = [0, 0]
        ouput_matrix = []

        bool_start = False

        for i in list_models[4]:
            i.check_switch(t)

        ###
        for i in range(len(time_interrupt)):
            if (t >= time_interrupt[i]):
                current_interrupt_time_index = i
            else:
                break
        if not flag_time_interrupt[current_interrupt_time_index]:
            for i in range(len(time_interrupt)):
                flag_time_interrupt[i] = False
            flag_time_interrupt[current_interrupt_time_index] = True

            for i in list_nodes:
                i.control_connection(list_models)

            all_voltage_matrix, all_current_matrix = communacation_matrix(list_nodes, list_models, main_list)
        ###

        for type_model, number_moder in main_list:
            width_matrix = list_models[type_model][number_moder].width_matrix
            height_matrix = list_models[type_model][number_moder].height_matrix
            width_input = list_models[type_model][number_moder].width_input

            if (bool_start == False):
                main_det = np.zeros((height_matrix, width_matrix), dtype = data_type)
                own_matrix = list_models[type_model][number_moder].get_own_matrix(y[wait_index:(wait_index+width_input)], t)
                bool_start = True
            else:   
                main_det = np.hstack((main_det, np.zeros((main_det.shape[0], width_matrix), dtype = data_type)))  
                main_det = np.vstack((main_det, np.zeros((height_matrix, main_det.shape[1]), dtype = data_type)))
                own_matrix = np.hstack((own_matrix, list_models[type_model][number_moder].get_own_matrix(y[wait_index:(wait_index+width_input)], t)))

            buffer_det = list_models[type_model][number_moder].get_main_determinant(y[wait_index:(wait_index+width_input)], t)

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
        print(t)
        return ouput_matrix

    results = odeint(f, y0, t)

    return_graphs(main_list, list_models, results, t)