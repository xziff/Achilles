import psycopg2
import pickle
import numpy as np



#list_tables = {"WRIM": ["Uном", "p", "xm", "Кт", "r1", "r2", "x1", "x2", "Lст.", "Dст.внутр.", "d", "Jрот."]}
def update_dictionary():
    def test(name, list_col):
        req = 'SELECT'
        for i in range(len(list_col)):
            req = req + ' ' + '"' + list_col[i] + '"'
            if (i != len(list_col) - 1):
                req = req + ','
        req = req + ' FROM "' + name + '" WHERE'
        for i in range(len(list_col)):
            req = req + ' ' + '"' + list_col[i] + '"' + " != 'Null'"
            if (i != len(list_col) - 1):
                req = req + ' AND'
        return req

    conn = psycopg2.connect(dbname='d39g2mm61t1cun', user='wsnpeflzildnko', 
                        password='fd2d47650c4a665bcd1082279ecd743c82714f204d51304617d477d83c8205f8', host='ec2-18-211-41-246.compute-1.amazonaws.com')
    cursor = conn.cursor()

    try:
        file = open('Dictionary/List_update.pickle', 'rb')
    except IOError:
        with open('Dictionary/List_update.pickle', 'wb') as f:
            req = 'SELECT * FROM "List_update"'
            cursor.execute(req)
            item = cursor.fetchall()
            current_update_list = {}
            for i in item:
                current_update_list[i[0]] = i[3]
            pickle.dump(item, f)
    else:
        current_update_list = {}
        with file:
            old_list = pickle.load(file)
            req = 'SELECT * FROM "List_update"'
            cursor.execute(req)
            new_list = cursor.fetchall()
            for i in new_list:
                state_found = False
                for j in old_list:
                    if (j[0] == i[0]):
                        state_found = True
                        if (j[1] < i[1]):
                            current_update_list[i[0]] = i[3]
                if not state_found:
                    current_update_list[i[0]] = i[3]
                    

    for key, item in current_update_list.items():
        req = test(key, item)
        cursor.execute(req)
        item = cursor.fetchall()
        d_item = {}
        for i in item:
            d_item[i[0]] = np.array(i[1:]).astype(np.float64)
        with open('Dictionary/' + key + '.pickle', 'wb') as f:
            pickle.dump(d_item, f)

    cursor.close()
    conn.close()

update_dictionary()